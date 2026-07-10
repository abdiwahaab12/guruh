"""Reports & Analytics admin data provider — aggregates existing models."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta

from sqlalchemy import desc, func

from app.extensions import db
from app.models.auth import AuditLog, LoginHistory, User
from app.models.catalog import (
    ContactSubmission,
    GalleryImage,
    JobListing,
    Project,
    QuoteRequest,
    Service,
    TeamMember,
)
from app.models.cms import Page
from app.models.content_blocks import ContentBlock
from app.models.equipment import Equipment
from app.models.job_application import JobApplication
from app.models.page_sections import PageSection
from app.providers.auth_provider import AuthProvider
from app.schemas.reports_admin import (
    AuditReportDTO,
    AuditReportRowDTO,
    ChartSeriesDTO,
    DateRangeDTO,
    ReportsOverviewDTO,
    StatCardDTO,
)


class ReportsAdminProvider:
    """Read-only analytics queries across CMS modules."""

    @staticmethod
    def record_audit(**kwargs) -> None:
        AuthProvider.record_audit_event(**kwargs)

    @staticmethod
    def commit() -> bool:
        return AuthProvider.commit()

    @staticmethod
    def parse_date_range(
        preset: str,
        *,
        date_from: str = "",
        date_to: str = "",
    ) -> tuple[datetime, datetime, DateRangeDTO]:
        now = datetime.utcnow()
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        if preset == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            label = "Today"
        elif preset == "week":
            start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            label = "This Week"
        elif preset == "year":
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            label = "This Year"
        elif preset == "custom" and date_from and date_to:
            start = datetime.fromisoformat(date_from)
            end = datetime.fromisoformat(date_to).replace(hour=23, minute=59, second=59)
            label = f"{date_from} – {date_to}"
        else:
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            label = "This Month"
            preset = "month"

        return start, end, DateRangeDTO(preset=preset, label=label, start=start.date().isoformat(), end=end.date().isoformat())

    @staticmethod
    def _between(model, start: datetime, end: datetime):
        return model.created_at >= start, model.created_at <= end

    @staticmethod
    def _count_in_range(model, start: datetime, end: datetime, **filters) -> int:
        query = model.query.filter(*ReportsAdminProvider._between(model, start, end))
        for key, val in filters.items():
            query = query.filter_by(**{key: val})
        return query.count()

    @staticmethod
    def get_overview(start: datetime, end: datetime) -> ReportsOverviewDTO:
        from app.providers.gallery_admin_provider import GalleryAdminProvider
        from app.providers.projects_admin_provider import ProjectsAdminProvider
        from app.providers.services_admin_provider import ServicesAdminProvider
        from app.providers.equipment_admin_provider import EquipmentAdminProvider
        from app.providers.careers_admin_provider import CareersAdminProvider
        from app.providers.messages_admin_provider import MessagesAdminProvider
        from app.providers.users_admin_provider import UsersAdminProvider

        website = {
            "pages": Page.query.count(),
            "published_pages": Page.query.filter_by(is_published=True).count(),
            "sections": PageSection.query.count(),
            "content_blocks": ContentBlock.query.filter_by(is_active=True).count(),
            "new_pages": ReportsAdminProvider._count_in_range(Page, start, end),
        }
        projects_stats = ProjectsAdminProvider.get_stats()
        services_stats = ServicesAdminProvider.get_stats()
        equipment_stats = EquipmentAdminProvider.get_stats()
        gallery_stats = GalleryAdminProvider.get_stats()
        careers_stats = CareersAdminProvider.get_stats()
        messages_stats = MessagesAdminProvider.get_stats()
        users_stats = UsersAdminProvider.get_stats()

        projects = {
            **projects_stats,
            "new": ReportsAdminProvider._count_in_range(Project, start, end),
        }
        services = {**services_stats, "new": ReportsAdminProvider._count_in_range(Service, start, end)}
        equipment = {**equipment_stats, "new": ReportsAdminProvider._count_in_range(Equipment, start, end)}
        gallery = {**gallery_stats, "new": ReportsAdminProvider._count_in_range(GalleryImage, start, end)}
        careers = {**careers_stats, "new": ReportsAdminProvider._count_in_range(JobListing, start, end)}
        messages = {
            "contacts_total": messages_stats.contacts_total,
            "contacts_unread": messages_stats.contacts_unread,
            "quotes_total": messages_stats.quotes_total,
            "quotes_unread": messages_stats.quotes_unread,
            "applications_total": messages_stats.applications_total,
            "applications_unread": messages_stats.applications_unread,
            "new_contacts": ReportsAdminProvider._count_in_range(ContactSubmission, start, end),
            "new_quotes": ReportsAdminProvider._count_in_range(QuoteRequest, start, end),
            "new_applications": ReportsAdminProvider._count_in_range(JobApplication, start, end),
        }
        users = {
            **asdict(users_stats),
            "new_users": ReportsAdminProvider._count_in_range(User, start, end),
            "team_members": TeamMember.query.filter_by(is_active=True).count(),
        }

        cards = [
            StatCardDTO("website", "Website Pages", website["pages"], f"{website['published_pages']} published", "bi-file-earmark-text", "primary"),
            StatCardDTO("projects", "Projects", projects.get("total", 0), f"{projects.get('active', 0)} active", "bi-building", "success"),
            StatCardDTO("services", "Services", services.get("total", 0), f"{services.get('active', 0)} active", "bi-grid", "info"),
            StatCardDTO("equipment", "Equipment", equipment.get("total", 0), f"{equipment.get('active', 0)} active", "bi-truck", "secondary"),
            StatCardDTO("gallery", "Gallery Items", gallery.get("total", 0), f"{gallery.get('albums', 0)} albums", "bi-images", "warning"),
            StatCardDTO("careers", "Job Listings", careers.get("total", 0), f"{careers.get('active', 0)} active", "bi-briefcase", "dark"),
            StatCardDTO("messages", "Messages", messages["contacts_total"] + messages["quotes_total"] + messages["applications_total"], f"{messages['contacts_unread'] + messages['quotes_unread'] + messages['applications_unread']} unread", "bi-envelope", "danger"),
            StatCardDTO("users", "Admin Users", users.get("total_users", 0), f"{users.get('active_users', 0)} active", "bi-people", "primary"),
        ]

        charts = [
            ReportsAdminProvider._monthly_activity_chart(start, end),
            ReportsAdminProvider._messages_trend_chart(start, end),
            ReportsAdminProvider._projects_country_chart(),
            ReportsAdminProvider._gallery_growth_chart(start, end),
            ReportsAdminProvider._users_activity_chart(start, end),
        ]

        return ReportsOverviewDTO(
            cards=cards,
            charts=charts,
            website=website,
            projects=projects,
            services=services,
            equipment=equipment,
            gallery=gallery,
            careers=careers,
            messages=messages,
            users=users,
        )

    @staticmethod
    def _monthly_labels(start: datetime, end: datetime) -> list[str]:
        labels = []
        cursor = start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        while cursor <= end:
            labels.append(cursor.strftime("%b %Y"))
            if cursor.month == 12:
                cursor = cursor.replace(year=cursor.year + 1, month=1)
            else:
                cursor = cursor.replace(month=cursor.month + 1)
        if not labels:
            labels = [start.strftime("%b %Y")]
        return labels[-12:] if len(labels) > 12 else labels

    @staticmethod
    def _monthly_activity_chart(start: datetime, end: datetime) -> ChartSeriesDTO:
        labels = ReportsAdminProvider._monthly_labels(start, end)
        audit_counts = []
        for label in labels:
            month_start = datetime.strptime(label, "%b %Y")
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1)
            audit_counts.append(
                AuditLog.query.filter(
                    AuditLog.created_at >= month_start,
                    AuditLog.created_at < month_end,
                ).count()
            )
        return ChartSeriesDTO(
            chart_id="monthlyActivity",
            title="Monthly Activity",
            chart_type="bar",
            labels=labels,
            datasets=[{"label": "Audit Events", "data": audit_counts, "backgroundColor": "rgba(13,110,253,0.7)"}],
        )

    @staticmethod
    def _messages_trend_chart(start: datetime, end: datetime) -> ChartSeriesDTO:
        labels = ReportsAdminProvider._monthly_labels(start, end)
        contacts, quotes, applications = [], [], []
        for label in labels:
            month_start = datetime.strptime(label, "%b %Y")
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1)
            contacts.append(ContactSubmission.query.filter(ContactSubmission.created_at >= month_start, ContactSubmission.created_at < month_end).count())
            quotes.append(QuoteRequest.query.filter(QuoteRequest.created_at >= month_start, QuoteRequest.created_at < month_end).count())
            applications.append(JobApplication.query.filter(JobApplication.created_at >= month_start, JobApplication.created_at < month_end).count())
        return ChartSeriesDTO(
            chart_id="messagesTrend",
            title="Messages Trend",
            chart_type="line",
            labels=labels,
            datasets=[
                {"label": "Contacts", "data": contacts, "borderColor": "#0d6efd", "fill": False},
                {"label": "Quotes", "data": quotes, "borderColor": "#198754", "fill": False},
                {"label": "Applications", "data": applications, "borderColor": "#ffc107", "fill": False},
            ],
        )

    @staticmethod
    def _projects_country_chart() -> ChartSeriesDTO:
        rows = (
            db.session.query(Project.country, func.count(Project.id))
            .filter(Project.is_active.is_(True))
            .group_by(Project.country)
            .order_by(desc(func.count(Project.id)))
            .limit(8)
            .all()
        )
        return ChartSeriesDTO(
            chart_id="projectsCountry",
            title="Projects by Country",
            chart_type="doughnut",
            labels=[r[0] or "Unknown" for r in rows],
            datasets=[{"label": "Projects", "data": [r[1] for r in rows], "backgroundColor": [
                "#0d6efd", "#6610f2", "#6f42c1", "#d63384", "#dc3545", "#fd7e14", "#ffc107", "#198754"
            ]}],
        )

    @staticmethod
    def _gallery_growth_chart(start: datetime, end: datetime) -> ChartSeriesDTO:
        labels = ReportsAdminProvider._monthly_labels(start, end)
        counts = []
        for label in labels:
            month_start = datetime.strptime(label, "%b %Y")
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1)
            counts.append(GalleryImage.query.filter(GalleryImage.created_at >= month_start, GalleryImage.created_at < month_end).count())
        return ChartSeriesDTO(
            chart_id="galleryGrowth",
            title="Gallery Growth",
            chart_type="line",
            labels=labels,
            datasets=[{"label": "New Items", "data": counts, "borderColor": "#fd7e14", "backgroundColor": "rgba(253,126,20,0.2)", "fill": True}],
        )

    @staticmethod
    def _users_activity_chart(start: datetime, end: datetime) -> ChartSeriesDTO:
        labels = ReportsAdminProvider._monthly_labels(start, end)
        logins, audits = [], []
        for label in labels:
            month_start = datetime.strptime(label, "%b %Y")
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1)
            logins.append(LoginHistory.query.filter(LoginHistory.success.is_(True), LoginHistory.created_at >= month_start, LoginHistory.created_at < month_end).count())
            audits.append(AuditLog.query.filter(AuditLog.created_at >= month_start, AuditLog.created_at < month_end).count())
        return ChartSeriesDTO(
            chart_id="usersActivity",
            title="Users Activity",
            chart_type="bar",
            labels=labels,
            datasets=[
                {"label": "Successful Logins", "data": logins, "backgroundColor": "rgba(25,135,84,0.7)"},
                {"label": "Audit Events", "data": audits, "backgroundColor": "rgba(13,110,253,0.5)"},
            ],
        )

    @staticmethod
    def get_audit_report(tab: str, start: datetime, end: datetime) -> AuditReportDTO:
        rows: list[AuditReportRowDTO] = []
        if tab == "user":
            data = (
                db.session.query(User.email, func.count(AuditLog.id))
                .join(AuditLog, AuditLog.user_id == User.id)
                .filter(AuditLog.created_at >= start, AuditLog.created_at <= end)
                .group_by(User.email)
                .order_by(desc(func.count(AuditLog.id)))
                .limit(25)
                .all()
            )
            rows = [AuditReportRowDTO(label=email, count=count, detail="audit events") for email, count in data]
            title = "User Activity"
        elif tab == "login":
            data = (
                db.session.query(LoginHistory.email_attempted, LoginHistory.success, func.count(LoginHistory.id))
                .filter(LoginHistory.created_at >= start, LoginHistory.created_at <= end)
                .group_by(LoginHistory.email_attempted, LoginHistory.success)
                .order_by(desc(func.count(LoginHistory.id)))
                .limit(25)
                .all()
            )
            rows = [
                AuditReportRowDTO(
                    label=email,
                    count=count,
                    detail="success" if success else f"failed",
                )
                for email, success, count in data
            ]
            title = "Login Activity"
        else:
            data = (
                db.session.query(AuditLog.action, func.count(AuditLog.id))
                .filter(AuditLog.created_at >= start, AuditLog.created_at <= end)
                .group_by(AuditLog.action)
                .order_by(desc(func.count(AuditLog.id)))
                .limit(30)
                .all()
            )
            rows = [AuditReportRowDTO(label=action, count=count, detail="system actions") for action, count in data]
            title = "System Activity"
            tab = "system"

        return AuditReportDTO(tab=tab, title=title, rows=rows, total=sum(r.count for r in rows))

    @staticmethod
    def overview_export_rows(overview: ReportsOverviewDTO) -> list[list[str]]:
        rows = [["Section", "Metric", "Value"]]
        for card in overview.cards:
            rows.append([card.key, card.label, str(card.value)])
        rows.append(["website", "content_blocks", str(overview.website.get("content_blocks", 0))])
        rows.append(["messages", "unread_total", str(
            overview.messages.get("contacts_unread", 0)
            + overview.messages.get("quotes_unread", 0)
            + overview.messages.get("applications_unread", 0)
        )])
        return rows

    @staticmethod
    def audit_export_rows(report: AuditReportDTO) -> list[list[str]]:
        rows = [["Label", "Count", "Detail"]]
        for row in report.rows:
            rows.append([row.label, str(row.count), row.detail])
        return rows
