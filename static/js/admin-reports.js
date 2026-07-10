/**
 * Reports & Analytics — Chart.js initialization and date filter UX.
 */
(function () {
    "use strict";

    function initDateFilter() {
        var preset = document.getElementById("reportsPreset");
        if (!preset) return;

        var customBlocks = document.querySelectorAll(".admin-reports-custom-dates");
        function toggleCustom() {
            var show = preset.value === "custom";
            customBlocks.forEach(function (el) {
                el.classList.toggle("d-none", !show);
            });
        }
        preset.addEventListener("change", toggleCustom);
        toggleCustom();
    }

    function initCharts() {
        var dataEl = document.getElementById("reportsChartData");
        if (!dataEl || typeof Chart === "undefined") return;

        var series;
        try {
            series = JSON.parse(dataEl.textContent || "[]");
        } catch (e) {
            return;
        }

        series.forEach(function (cfg) {
            var canvas = document.getElementById(cfg.chart_id);
            if (!canvas) return;

            new Chart(canvas, {
                type: cfg.chart_type,
                data: {
                    labels: cfg.labels || [],
                    datasets: cfg.datasets || [],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: cfg.chart_type === "doughnut" ? "right" : "top",
                        },
                    },
                    scales:
                        cfg.chart_type === "doughnut"
                            ? {}
                            : {
                                  y: { beginAtZero: true, ticks: { precision: 0 } },
                              },
                },
            });
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        initDateFilter();
        initCharts();
    });
})();
