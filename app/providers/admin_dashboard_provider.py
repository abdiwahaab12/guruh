"""Admin dashboard data provider — placeholder metrics until live DB queries."""

from __future__ import annotations

from app.constants.admin_nav import build_quick_actions
from app.schemas.admin import (
    ActivityItemDTO,
    AdminDashboardDTO,
    ChartConfigDTO,
    ChartDatasetDTO,
    DashboardStatDTO,
    NotificationDTO,
)


class AdminDashboardProvider:
    """Placeholder dashboard metrics — replaced with live queries in future steps."""

    @staticmethod
    def get_stats() -> list[DashboardStatDTO]:
        return [
            DashboardStatDTO("pages", "Total Pages", 12, "bi-file-earmark-text", "primary", "+2", "up", "content", "stats.pages"),
            DashboardStatDTO("services", "Services", 6, "bi-grid", "accent", "", "neutral", "content", "stats.services"),
            DashboardStatDTO("projects", "Projects", 12, "bi-building", "success", "+1", "up", "projects", "stats.projects"),
            DashboardStatDTO("equipment", "Equipment", 24, "bi-truck", "info", "", "neutral", "equipment", "stats.equipment"),
            DashboardStatDTO("team", "Team Members", 8, "bi-people", "primary", "", "neutral", "team", "stats.team"),
            DashboardStatDTO("gallery", "Gallery Images", 156, "bi-images", "accent", "+12", "up", "gallery", "stats.gallery"),
            DashboardStatDTO("careers", "Careers", 5, "bi-briefcase", "warning", "", "neutral", "careers", "stats.careers"),
            DashboardStatDTO("contacts", "Contact Messages", 23, "bi-envelope", "danger", "5 new", "up", "forms", "stats.contacts"),
            DashboardStatDTO("quotes", "Quote Requests", 17, "bi-chat-quote", "info", "3 new", "up", "forms", "stats.quotes"),
        ]

    @staticmethod
    def get_charts() -> list[ChartConfigDTO]:
        return [
            ChartConfigDTO(
                chart_id="chartTrafficOverview",
                chart_type="line",
                title="Site Traffic Overview",
                labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                datasets=[
                    ChartDatasetDTO(
                        label="Page Views",
                        data=[1200, 1900, 1500, 2200, 2400, 2100, 2800],
                        borderColor="#33A8FF",
                        backgroundColor="rgba(51, 168, 255, 0.12)",
                    ),
                    ChartDatasetDTO(
                        label="Unique Visitors",
                        data=[800, 1100, 950, 1300, 1400, 1250, 1600],
                        borderColor="#E91E63",
                        backgroundColor="rgba(233, 30, 99, 0.08)",
                    ),
                ],
                i18n_key="charts.traffic",
            ),
            ChartConfigDTO(
                chart_id="chartContentMix",
                chart_type="doughnut",
                title="Content Distribution",
                labels=["Pages", "Projects", "Services", "Media", "Careers"],
                datasets=[
                    ChartDatasetDTO(
                        label="Items",
                        data=[12, 12, 6, 156, 5],
                        backgroundColor=[
                            "#33A8FF",
                            "#1A94EB",
                            "#E91E63",
                            "#6B7280",
                            "#F59E0B",
                        ],
                    ),
                ],
                i18n_key="charts.content_mix",
            ),
            ChartConfigDTO(
                chart_id="chartFormSubmissions",
                chart_type="bar",
                title="Form Submissions",
                labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                datasets=[
                    ChartDatasetDTO(
                        label="Contact",
                        data=[4, 6, 3, 8, 5, 2, 1],
                        backgroundColor="rgba(51, 168, 255, 0.85)",
                    ),
                    ChartDatasetDTO(
                        label="Quotes",
                        data=[2, 3, 4, 3, 5, 1, 0],
                        backgroundColor="rgba(233, 30, 99, 0.75)",
                    ),
                ],
                i18n_key="charts.forms",
            ),
        ]

    @staticmethod
    def get_activities() -> list[ActivityItemDTO]:
        return [
            ActivityItemDTO(
                1,
                "New quote request received",
                "Commercial building project in Mogadishu — pending review.",
                "bi-chat-quote-fill",
                "info",
                "12 minutes ago",
                "System",
                "quote_request",
            ),
            ActivityItemDTO(
                2,
                "Contact message flagged",
                "Partnership inquiry from private sector client.",
                "bi-envelope-fill",
                "primary",
                "45 minutes ago",
                "System",
                "contact_submission",
            ),
            ActivityItemDTO(
                3,
                "Content block updated",
                "Company history section revised for Somalia operations.",
                "bi-pencil-square",
                "accent",
                "2 hours ago",
                "Super Admin",
                "content_block",
            ),
            ActivityItemDTO(
                4,
                "User signed in",
                "Successful login from Mogadishu office IP.",
                "bi-person-check-fill",
                "success",
                "3 hours ago",
                "Super Admin",
                "auth",
            ),
            ActivityItemDTO(
                5,
                "Gallery media prepared",
                "12 new project images queued for review.",
                "bi-images",
                "warning",
                "Yesterday",
                "Media Manager",
                "gallery",
            ),
        ]

    @staticmethod
    def get_notifications() -> list[NotificationDTO]:
        return [
            NotificationDTO(
                1,
                "5 unread contact messages",
                "Review inbox before end of business day.",
                "bi-envelope",
                "primary",
                "10m ago",
                False,
                "#",
            ),
            NotificationDTO(
                2,
                "3 new quote requests",
                "High-priority commercial inquiries awaiting response.",
                "bi-chat-quote",
                "accent",
                "25m ago",
                False,
                "#",
            ),
            NotificationDTO(
                3,
                "System update ready",
                "Admin modules will roll out in upcoming steps.",
                "bi-info-circle",
                "info",
                "1h ago",
                True,
                "#",
            ),
            NotificationDTO(
                4,
                "Session security",
                "Your last login was from a recognized device.",
                "bi-shield-check",
                "success",
                "3h ago",
                True,
                "#",
            ),
        ]

    @staticmethod
    def get_dashboard() -> AdminDashboardDTO:
        notifications = AdminDashboardProvider.get_notifications()
        unread = sum(1 for n in notifications if not n.is_read)
        return AdminDashboardDTO(
            stats=AdminDashboardProvider.get_stats(),
            charts=AdminDashboardProvider.get_charts(),
            activities=AdminDashboardProvider.get_activities(),
            notifications=notifications,
            unread_notification_count=unread,
        )

    @staticmethod
    def get_quick_actions() -> list[dict]:
        return build_quick_actions()
