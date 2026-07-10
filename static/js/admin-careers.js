/**
 * GURUH Admin — Careers module
 */

(function () {
    'use strict';

    var selectAll = document.getElementById('selectAllJobs');
    if (selectAll) {
        selectAll.addEventListener('change', function () {
            document.querySelectorAll('.job-row-check').forEach(function (cb) {
                cb.checked = selectAll.checked;
            });
        });
    }
})();
