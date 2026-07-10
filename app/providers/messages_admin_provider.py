"""Messages / Inbox admin data provider."""

from __future__ import annotations

import csv
import io
import json
from datetime import datetime

from sqlalchemy import asc, desc, or_
from sqlalchemy.exc import SQLAlchemyError

from app.constants.messages_admin import (
    EXPORT_COLUMNS,
    TAB_APPLICATIONS,
    TAB_CONTACTS,
    TAB_QUOTES,
)
from app.extensions import db
from app.models.catalog import ContactSubmission, QuoteRequest
from app.models.contact_submission_detail import ContactSubmissionDetail
from app.models.job_application import JobApplication
from app.models.quote_request_detail import QuoteRequestDetail
from app.providers.auth_provider import AuthProvider
from app.schemas.messages_admin import InboxStatsDTO, MessageDetailDTO, MessageListItemDTO


class MessagesAdminProvider:
    """Database operations for the unified messages inbox."""

    @staticmethod
    def commit() -> bool:
        return AuthProvider.commit()

    @staticmethod
    def rollback() -> None:
        AuthProvider.rollback()

    @staticmethod
    def record_audit(**kwargs) -> None:
        AuthProvider.record_audit_event(**kwargs)

    @staticmethod
    def _format_dt(value: datetime | None) -> str:
        return value.strftime("%d %b %Y, %H:%M") if value else "—"

    @staticmethod
    def _load_extra(raw: str | None) -> dict:
        if not raw:
            return {}
        try:
            data = json.loads(raw)
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def _contact_detail(row: ContactSubmission) -> ContactSubmissionDetail:
        if row.detail:
            return row.detail
        detail = ContactSubmissionDetail(contact_submission_id=row.id)
        db.session.add(detail)
        db.session.flush()
        return detail

    @staticmethod
    def _quote_detail(row: QuoteRequest) -> QuoteRequestDetail:
        if row.detail:
            return row.detail
        detail = QuoteRequestDetail(quote_request_id=row.id)
        db.session.add(detail)
        db.session.flush()
        return detail

    @staticmethod
    def _badges(is_read: bool, is_starred: bool, is_archived: bool, is_deleted: bool) -> list[str]:
        badges: list[str] = []
        if is_deleted:
            badges.append("Deleted")
        elif is_archived:
            badges.append("Archived")
        elif not is_read:
            badges.append("Unread")
        else:
            badges.append("Read")
        if is_starred:
            badges.append("Starred")
        return badges

    @staticmethod
    def get_stats() -> InboxStatsDTO:
        contacts = ContactSubmission.query.all()
        quotes = QuoteRequest.query.all()
        applications = JobApplication.query.filter(JobApplication.deleted_at.is_(None)).all()

        def unread_contacts() -> int:
            count = 0
            for row in contacts:
                detail = row.detail
                if detail and detail.deleted_at:
                    continue
                if detail and detail.is_archived:
                    continue
                if not row.is_read:
                    count += 1
            return count

        def unread_quotes() -> int:
            count = 0
            for row in quotes:
                detail = row.detail
                if detail and detail.deleted_at:
                    continue
                if detail and detail.is_archived:
                    continue
                if not row.is_read:
                    count += 1
            return count

        return InboxStatsDTO(
            contacts_total=len(contacts),
            contacts_unread=unread_contacts(),
            quotes_total=len(quotes),
            quotes_unread=unread_quotes(),
            applications_total=JobApplication.query.filter(JobApplication.deleted_at.is_(None)).count(),
            applications_unread=JobApplication.query.filter(
                JobApplication.deleted_at.is_(None),
                JobApplication.is_archived.is_(False),
                JobApplication.is_read.is_(False),
            ).count(),
        )

    @staticmethod
    def _apply_status_filters_contact(query, status: str, include_deleted: bool):
        query = query.outerjoin(ContactSubmissionDetail)
        if include_deleted:
            query = query.filter(ContactSubmissionDetail.deleted_at.isnot(None))
        else:
            query = query.filter(or_(ContactSubmissionDetail.id.is_(None), ContactSubmissionDetail.deleted_at.is_(None)))
        if status == "unread":
            query = query.filter(ContactSubmission.is_read.is_(False))
            query = query.filter(or_(ContactSubmissionDetail.id.is_(None), ContactSubmissionDetail.is_archived.is_(False)))
        elif status == "read":
            query = query.filter(ContactSubmission.is_read.is_(True))
        elif status == "starred":
            query = query.filter(ContactSubmissionDetail.is_starred.is_(True))
        elif status == "archived":
            query = query.filter(ContactSubmissionDetail.is_archived.is_(True))
        return query

    @staticmethod
    def query_contacts(
        *,
        q: str = "",
        status: str = "",
        sort: str = "newest",
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> tuple[list[MessageListItemDTO], int]:
        query = ContactSubmission.query
        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    ContactSubmission.name.ilike(like),
                    ContactSubmission.email.ilike(like),
                    ContactSubmission.subject.ilike(like),
                    ContactSubmission.message.ilike(like),
                )
            )
        query = MessagesAdminProvider._apply_status_filters_contact(query, status, include_deleted)

        if sort == "oldest":
            query = query.order_by(asc(ContactSubmission.created_at))
        elif sort == "name_asc":
            query = query.order_by(asc(ContactSubmission.name))
        elif sort == "name_desc":
            query = query.order_by(desc(ContactSubmission.name))
        else:
            query = query.order_by(desc(ContactSubmission.created_at))

        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
        items = []
        for row in rows:
            detail = row.detail
            is_starred = detail.is_starred if detail else False
            is_archived = detail.is_archived if detail else False
            is_deleted = bool(detail and detail.deleted_at)
            items.append(
                MessageListItemDTO(
                    id=row.id,
                    tab=TAB_CONTACTS,
                    name=row.name,
                    email=row.email,
                    summary=row.subject or (row.message[:80] + "…" if len(row.message) > 80 else row.message),
                    is_read=row.is_read,
                    is_starred=is_starred,
                    is_archived=is_archived,
                    is_deleted=is_deleted,
                    created_at_label=MessagesAdminProvider._format_dt(row.created_at),
                    status_badges=MessagesAdminProvider._badges(row.is_read, is_starred, is_archived, is_deleted),
                )
            )
        return items, total

    @staticmethod
    def _apply_status_filters_quote(query, status: str, include_deleted: bool):
        query = query.outerjoin(QuoteRequestDetail)
        if include_deleted:
            query = query.filter(QuoteRequestDetail.deleted_at.isnot(None))
        else:
            query = query.filter(or_(QuoteRequestDetail.id.is_(None), QuoteRequestDetail.deleted_at.is_(None)))
        if status == "unread":
            query = query.filter(QuoteRequest.is_read.is_(False))
            query = query.filter(or_(QuoteRequestDetail.id.is_(None), QuoteRequestDetail.is_archived.is_(False)))
        elif status == "read":
            query = query.filter(QuoteRequest.is_read.is_(True))
        elif status == "starred":
            query = query.filter(QuoteRequestDetail.is_starred.is_(True))
        elif status == "archived":
            query = query.filter(QuoteRequestDetail.is_archived.is_(True))
        return query

    @staticmethod
    def query_quotes(
        *,
        q: str = "",
        status: str = "",
        sort: str = "newest",
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> tuple[list[MessageListItemDTO], int]:
        query = QuoteRequest.query
        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    QuoteRequest.name.ilike(like),
                    QuoteRequest.email.ilike(like),
                    QuoteRequest.project_type.ilike(like),
                    QuoteRequest.message.ilike(like),
                )
            )
        query = MessagesAdminProvider._apply_status_filters_quote(query, status, include_deleted)

        if sort == "oldest":
            query = query.order_by(asc(QuoteRequest.created_at))
        elif sort == "name_asc":
            query = query.order_by(asc(QuoteRequest.name))
        elif sort == "name_desc":
            query = query.order_by(desc(QuoteRequest.name))
        else:
            query = query.order_by(desc(QuoteRequest.created_at))

        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
        items = []
        for row in rows:
            detail = row.detail
            is_starred = detail.is_starred if detail else False
            is_archived = detail.is_archived if detail else False
            is_deleted = bool(detail and detail.deleted_at)
            summary = row.project_type or row.budget or row.message[:80]
            items.append(
                MessageListItemDTO(
                    id=row.id,
                    tab=TAB_QUOTES,
                    name=row.name,
                    email=row.email,
                    summary=summary,
                    is_read=row.is_read,
                    is_starred=is_starred,
                    is_archived=is_archived,
                    is_deleted=is_deleted,
                    created_at_label=MessagesAdminProvider._format_dt(row.created_at),
                    status_badges=MessagesAdminProvider._badges(row.is_read, is_starred, is_archived, is_deleted),
                )
            )
        return items, total

    @staticmethod
    def query_applications(
        *,
        q: str = "",
        status: str = "",
        sort: str = "newest",
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> tuple[list[MessageListItemDTO], int]:
        query = JobApplication.query
        if include_deleted:
            query = query.filter(JobApplication.deleted_at.isnot(None))
        else:
            query = query.filter(JobApplication.deleted_at.is_(None))

        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    JobApplication.full_name.ilike(like),
                    JobApplication.email.ilike(like),
                    JobApplication.position.ilike(like),
                    JobApplication.cover_letter.ilike(like),
                )
            )
        if status == "unread":
            query = query.filter(JobApplication.is_read.is_(False), JobApplication.is_archived.is_(False))
        elif status == "read":
            query = query.filter(JobApplication.is_read.is_(True))
        elif status == "starred":
            query = query.filter(JobApplication.is_starred.is_(True))
        elif status == "archived":
            query = query.filter(JobApplication.is_archived.is_(True))

        if sort == "oldest":
            query = query.order_by(asc(JobApplication.created_at))
        elif sort == "name_asc":
            query = query.order_by(asc(JobApplication.full_name))
        elif sort == "name_desc":
            query = query.order_by(desc(JobApplication.full_name))
        else:
            query = query.order_by(desc(JobApplication.created_at))

        total = query.count()
        rows = query.offset((page - 1) * per_page).limit(per_page).all()
        items = []
        for row in rows:
            is_deleted = bool(row.deleted_at)
            items.append(
                MessageListItemDTO(
                    id=row.id,
                    tab=TAB_APPLICATIONS,
                    name=row.full_name,
                    email=row.email,
                    summary=row.position or (row.cover_letter[:80] + "…" if row.cover_letter and len(row.cover_letter) > 80 else (row.cover_letter or "")),
                    is_read=row.is_read,
                    is_starred=row.is_starred,
                    is_archived=row.is_archived,
                    is_deleted=is_deleted,
                    created_at_label=MessagesAdminProvider._format_dt(row.created_at),
                    status_badges=MessagesAdminProvider._badges(row.is_read, row.is_starred, row.is_archived, is_deleted),
                )
            )
        return items, total

    @staticmethod
    def get_contact_detail(item_id: int, *, mark_read: bool = False) -> MessageDetailDTO | None:
        row = ContactSubmission.query.get(item_id)
        if not row:
            return None
        detail = MessagesAdminProvider._contact_detail(row)
        if mark_read and not row.is_read:
            row.is_read = True
        extra = MessagesAdminProvider._load_extra(detail.extra_json)
        extra_fields = {k: str(v) for k, v in extra.items()}
        return MessageDetailDTO(
            id=row.id,
            tab=TAB_CONTACTS,
            title=row.subject or "Contact Message",
            name=row.name,
            email=row.email,
            phone=row.phone or "",
            subject=row.subject or "",
            body=row.message,
            is_read=row.is_read,
            is_starred=detail.is_starred,
            is_archived=detail.is_archived,
            is_deleted=bool(detail.deleted_at),
            admin_notes=detail.admin_notes or "",
            reply_subject=detail.reply_subject or "",
            reply_body=detail.reply_body or "",
            replied_at_label=MessagesAdminProvider._format_dt(detail.replied_at),
            created_at_label=MessagesAdminProvider._format_dt(row.created_at),
            updated_at_label=MessagesAdminProvider._format_dt(row.updated_at),
            extra_fields=extra_fields,
        )

    @staticmethod
    def get_quote_detail(item_id: int, *, mark_read: bool = False) -> MessageDetailDTO | None:
        row = QuoteRequest.query.get(item_id)
        if not row:
            return None
        detail = MessagesAdminProvider._quote_detail(row)
        if mark_read and not row.is_read:
            row.is_read = True
        extra = MessagesAdminProvider._load_extra(detail.extra_json)
        extra_fields = {
            "Project Type": row.project_type or "",
            "Budget": row.budget or "",
            **{k.replace("_", " ").title(): str(v) for k, v in extra.items()},
        }
        return MessageDetailDTO(
            id=row.id,
            tab=TAB_QUOTES,
            title=row.project_type or "Quote Request",
            name=row.name,
            email=row.email,
            phone=row.phone or "",
            subject=row.project_type or "Quote Request",
            body=row.message,
            is_read=row.is_read,
            is_starred=detail.is_starred,
            is_archived=detail.is_archived,
            is_deleted=bool(detail.deleted_at),
            admin_notes=detail.admin_notes or "",
            reply_subject=detail.reply_subject or "",
            reply_body=detail.reply_body or "",
            replied_at_label=MessagesAdminProvider._format_dt(detail.replied_at),
            created_at_label=MessagesAdminProvider._format_dt(row.created_at),
            updated_at_label=MessagesAdminProvider._format_dt(row.updated_at),
            extra_fields=extra_fields,
        )

    @staticmethod
    def get_application_detail(item_id: int, *, mark_read: bool = False) -> MessageDetailDTO | None:
        row = JobApplication.query.get(item_id)
        if not row:
            return None
        if mark_read and not row.is_read:
            row.is_read = True
        extra = MessagesAdminProvider._load_extra(row.extra_json)
        job_title = row.job_listing.title if row.job_listing else ""
        return MessageDetailDTO(
            id=row.id,
            tab=TAB_APPLICATIONS,
            title=row.position or "Job Application",
            name=row.full_name,
            email=row.email,
            phone=row.phone or "",
            subject=row.position or "",
            body=row.cover_letter or "",
            is_read=row.is_read,
            is_starred=row.is_starred,
            is_archived=row.is_archived,
            is_deleted=bool(row.deleted_at),
            admin_notes=row.admin_notes or "",
            reply_subject=row.reply_subject or "",
            reply_body=row.reply_body or "",
            replied_at_label=MessagesAdminProvider._format_dt(row.replied_at),
            created_at_label=MessagesAdminProvider._format_dt(row.created_at),
            updated_at_label=MessagesAdminProvider._format_dt(row.updated_at),
            extra_fields={
                "Years of Experience": row.years_experience or "",
                "Education": row.education or "",
                **{k.replace("_", " ").title(): str(v) for k, v in extra.items()},
            },
            job_position=row.position or "",
            job_listing_title=job_title,
        )

    @staticmethod
    def save_reply(
        tab: str,
        item_id: int,
        *,
        subject: str,
        body: str,
        admin_notes: str,
        user_id: int,
    ) -> bool:
        now = datetime.utcnow()
        if tab == TAB_CONTACTS:
            row = ContactSubmission.query.get(item_id)
            if not row:
                return False
            detail = MessagesAdminProvider._contact_detail(row)
            detail.reply_subject = subject.strip()
            detail.reply_body = body.strip()
            detail.admin_notes = admin_notes.strip()
            detail.replied_at = now
            detail.replied_by_user_id = user_id
            row.is_read = True
        elif tab == TAB_QUOTES:
            row = QuoteRequest.query.get(item_id)
            if not row:
                return False
            detail = MessagesAdminProvider._quote_detail(row)
            detail.reply_subject = subject.strip()
            detail.reply_body = body.strip()
            detail.admin_notes = admin_notes.strip()
            detail.replied_at = now
            detail.replied_by_user_id = user_id
            row.is_read = True
        elif tab == TAB_APPLICATIONS:
            row = JobApplication.query.get(item_id)
            if not row:
                return False
            row.reply_subject = subject.strip()
            row.reply_body = body.strip()
            row.admin_notes = admin_notes.strip()
            row.replied_at = now
            row.replied_by_user_id = user_id
            row.is_read = True
        else:
            return False
        return True

    @staticmethod
    def apply_bulk(tab: str, ids: list[int], action: str) -> int:
        updated = 0
        for item_id in ids:
            if MessagesAdminProvider._apply_action(tab, item_id, action):
                updated += 1
        return updated

    @staticmethod
    def _apply_action(tab: str, item_id: int, action: str) -> bool:
        if tab == TAB_CONTACTS:
            row = ContactSubmission.query.get(item_id)
            if not row:
                return False
            detail = MessagesAdminProvider._contact_detail(row)
            return MessagesAdminProvider._workflow_action(row, detail, action)
        if tab == TAB_QUOTES:
            row = QuoteRequest.query.get(item_id)
            if not row:
                return False
            detail = MessagesAdminProvider._quote_detail(row)
            return MessagesAdminProvider._workflow_action(row, detail, action)
        if tab == TAB_APPLICATIONS:
            row = JobApplication.query.get(item_id)
            if not row:
                return False
            return MessagesAdminProvider._workflow_action(row, row, action)
        return False

    @staticmethod
    def _workflow_action(core, detail, action: str) -> bool:
        if action == "mark_read":
            core.is_read = True
        elif action == "mark_unread":
            core.is_read = False
        elif action == "star":
            detail.is_starred = True
        elif action == "unstar":
            detail.is_starred = False
        elif action == "archive":
            detail.is_archived = True
        elif action == "unarchive":
            detail.is_archived = False
        elif action == "delete":
            detail.mark_deleted()
        elif action == "restore":
            detail.restore()
        else:
            return False
        return True

    @staticmethod
    def export_csv(tab: str, ids: list[int] | None = None) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        columns = EXPORT_COLUMNS.get(tab, ())
        writer.writerow(columns)

        if tab == TAB_CONTACTS:
            query = ContactSubmission.query
            if ids:
                query = query.filter(ContactSubmission.id.in_(ids))
            for row in query.order_by(desc(ContactSubmission.created_at)).all():
                writer.writerow(
                    [
                        row.id,
                        row.name,
                        row.email,
                        row.phone or "",
                        row.subject or "",
                        row.message,
                        row.is_read,
                        MessagesAdminProvider._format_dt(row.created_at),
                    ]
                )
        elif tab == TAB_QUOTES:
            query = QuoteRequest.query
            if ids:
                query = query.filter(QuoteRequest.id.in_(ids))
            for row in query.order_by(desc(QuoteRequest.created_at)).all():
                writer.writerow(
                    [
                        row.id,
                        row.name,
                        row.email,
                        row.phone,
                        row.project_type or "",
                        row.budget or "",
                        row.message,
                        row.is_read,
                        MessagesAdminProvider._format_dt(row.created_at),
                    ]
                )
        elif tab == TAB_APPLICATIONS:
            query = JobApplication.query.filter(JobApplication.deleted_at.is_(None))
            if ids:
                query = query.filter(JobApplication.id.in_(ids))
            for row in query.order_by(desc(JobApplication.created_at)).all():
                writer.writerow(
                    [
                        row.id,
                        row.full_name,
                        row.email,
                        row.phone or "",
                        row.position or "",
                        row.years_experience or "",
                        row.education or "",
                        row.cover_letter or "",
                        row.is_read,
                        MessagesAdminProvider._format_dt(row.created_at),
                    ]
                )
        return output.getvalue()

    @staticmethod
    def seed_sample_messages() -> None:
        """Insert demo inbox rows when tables are empty (dev/test)."""
        if ContactSubmission.query.count() == 0:
            row = ContactSubmission(
                name="Ahmed Hassan",
                email="ahmed@example.com",
                phone="+252 61 000 0001",
                subject="Road project inquiry",
                message="We are planning a road rehabilitation project in Mogadishu and would like to discuss capabilities.",
                is_read=False,
            )
            db.session.add(row)
            db.session.flush()
            db.session.add(ContactSubmissionDetail(contact_submission_id=row.id))

        if QuoteRequest.query.count() == 0:
            row = QuoteRequest(
                name="Somali Infrastructure Ltd",
                email="tenders@somali-infra.example",
                phone="+252 61 000 0002",
                project_type="Water Infrastructure",
                budget="$500k – $1M",
                message="Requesting a formal quotation for a borehole and pipeline package in Banadir.",
                is_read=False,
            )
            db.session.add(row)
            db.session.flush()
            db.session.add(QuoteRequestDetail(quote_request_id=row.id))

        if JobApplication.query.count() == 0:
            db.session.add(
                JobApplication(
                    full_name="Fatima Ali",
                    email="fatima@example.com",
                    phone="+252 61 000 0003",
                    position="Civil Engineer",
                    years_experience="5–10 years",
                    education="BSc Civil Engineering",
                    cover_letter="I am interested in joining GURUH Construction to contribute to infrastructure delivery across Somalia.",
                    is_read=False,
                )
            )

    @staticmethod
    def safe_commit(action: str, resource_type: str, resource_id: str, details: str, user_id: int, ip: str) -> bool:
        try:
            MessagesAdminProvider.record_audit(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                ip_address=ip,
            )
            return MessagesAdminProvider.commit()
        except SQLAlchemyError:
            MessagesAdminProvider.rollback()
            return False
