/**
 * GURUH Admin — Projects module
 */

(function () {
    'use strict';

    document.querySelectorAll('.admin-media-picker-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var targetId = btn.getAttribute('data-target');
            var path = btn.getAttribute('data-path');
            var input = document.getElementById(targetId);
            if (input && path) input.value = path;
        });
    });

    var selectAll = document.getElementById('selectAllProjects');
    if (selectAll) {
        selectAll.addEventListener('change', function () {
            document.querySelectorAll('.project-row-check').forEach(function (cb) {
                cb.checked = selectAll.checked;
            });
        });
    }

    function initChart(canvasId, labels, values, label) {
        var canvas = document.getElementById(canvasId);
        if (!canvas || typeof Chart === 'undefined') return;
        new Chart(canvas.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: values,
                    backgroundColor: ['#33A8FF', '#E91E63', '#10B981', '#F59E0B', '#6B7280', '#3B82F6'],
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } },
            },
        });
    }

    function initDashboardCharts() {
        var el = document.getElementById('projectsChartData');
        if (!el) return;
        try {
            var data = JSON.parse(el.textContent || '{}');
            var country = data.country || {};
            var status = data.status || {};
            initChart('projectsCountryChart', Object.keys(country), Object.values(country), 'Country');
            initChart('projectsStatusChart', Object.keys(status), Object.values(status), 'Status');
        } catch (e) { /* ignore */ }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDashboardCharts);
    } else {
        initDashboardCharts();
    }
})();
