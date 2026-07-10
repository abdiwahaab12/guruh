/**
 * GURUH Admin — shell interactions (sidebar, theme, mobile)
 */

(function () {
    'use strict';

    var app = document.getElementById('adminApp');
    var sidebar = document.getElementById('adminSidebar');
    var backdrop = document.getElementById('adminSidebarBackdrop');
    var toggleBtn = document.getElementById('adminSidebarToggle');
    var collapseBtn = document.getElementById('adminSidebarCollapse');
    var closeBtn = document.getElementById('adminSidebarClose');
    var themeBtn = document.getElementById('adminThemeToggle');
    var root = document.documentElement;
    var THEME_KEY = 'guruh_admin_theme';

    function setSidebarOpen(open) {
        if (!app) return;
        app.classList.toggle('is-sidebar-open', open);
        if (toggleBtn) toggleBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (backdrop) {
            backdrop.hidden = !open;
            backdrop.setAttribute('aria-hidden', open ? 'false' : 'true');
        }
    }

    function setSidebarCollapsed(collapsed) {
        if (!app) return;
        app.classList.toggle('is-sidebar-collapsed', collapsed);
        if (collapseBtn) collapseBtn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
        try {
            localStorage.setItem('guruh_admin_sidebar_collapsed', collapsed ? '1' : '0');
        } catch (e) { /* ignore */ }
    }

    function applyTheme(theme) {
        root.setAttribute('data-admin-theme', theme);
        if (themeBtn) themeBtn.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
        try {
            localStorage.setItem(THEME_KEY, theme);
        } catch (e) { /* ignore */ }
    }

    function initTheme() {
        var saved = null;
        try {
            saved = localStorage.getItem(THEME_KEY);
        } catch (e) { /* ignore */ }
        if (saved === 'dark' || saved === 'light') {
            applyTheme(saved);
            return;
        }
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            applyTheme('dark');
        }
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            setSidebarOpen(!app.classList.contains('is-sidebar-open'));
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            setSidebarOpen(false);
        });
    }

    if (backdrop) {
        backdrop.addEventListener('click', function () {
            setSidebarOpen(false);
        });
    }

    if (collapseBtn) {
        collapseBtn.addEventListener('click', function () {
            setSidebarCollapsed(!app.classList.contains('is-sidebar-collapsed'));
        });
    }

    if (themeBtn) {
        themeBtn.addEventListener('click', function () {
            var current = root.getAttribute('data-admin-theme') || 'light';
            applyTheme(current === 'dark' ? 'light' : 'dark');
        });
    }

    try {
        if (localStorage.getItem('guruh_admin_sidebar_collapsed') === '1') {
            setSidebarCollapsed(true);
        }
    } catch (e) { /* ignore */ }

    initTheme();

    window.addEventListener('resize', function () {
        if (window.innerWidth >= 992) {
            setSidebarOpen(false);
        }
    });
})();
