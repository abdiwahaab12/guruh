/**
 * GURUH Admin — Chart.js placeholder dashboard charts
 */

(function () {
    'use strict';

    function readChartData() {
        var el = document.getElementById('adminChartsData');
        if (!el) return [];
        try {
            return JSON.parse(el.textContent || '[]');
        } catch (e) {
            return [];
        }
    }

    function chartTextColor() {
        var theme = document.documentElement.getAttribute('data-admin-theme') || 'light';
        return theme === 'dark' ? '#E5E7EB' : '#64748B';
    }

    function gridColor() {
        var theme = document.documentElement.getAttribute('data-admin-theme') || 'light';
        return theme === 'dark' ? 'rgba(255,255,255,0.08)' : 'rgba(15,23,42,0.08)';
    }

    function buildOptions(type) {
        var common = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: chartTextColor() }
                }
            }
        };

        if (type === 'line' || type === 'bar') {
            common.scales = {
                x: {
                    ticks: { color: chartTextColor() },
                    grid: { color: gridColor() }
                },
                y: {
                    beginAtZero: true,
                    ticks: { color: chartTextColor() },
                    grid: { color: gridColor() }
                }
            };
        }

        return common;
    }

    var chartInstances = [];

    function destroyCharts() {
        chartInstances.forEach(function (instance) {
            instance.destroy();
        });
        chartInstances = [];
    }

    function initCharts() {
        if (typeof Chart === 'undefined') return;

        destroyCharts();
        var configs = readChartData();
        configs.forEach(function (cfg) {
            var canvas = document.getElementById(cfg.chart_id);
            if (!canvas) return;

            var datasets = (cfg.datasets || []).map(function (ds) {
                return {
                    label: ds.label,
                    data: ds.data,
                    backgroundColor: ds.backgroundColor,
                    borderColor: ds.borderColor || ds.backgroundColor,
                    borderWidth: cfg.chart_type === 'line' ? 2 : 1,
                    fill: cfg.chart_type === 'line',
                    tension: 0.35
                };
            });

            chartInstances.push(new Chart(canvas.getContext('2d'), {
                type: cfg.chart_type,
                data: {
                    labels: cfg.labels || [],
                    datasets: datasets
                },
                options: buildOptions(cfg.chart_type)
            }));
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCharts);
    } else {
        initCharts();
    }

    var themeBtn = document.getElementById('adminThemeToggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', function () {
            setTimeout(initCharts, 150);
        });
    }
})();
