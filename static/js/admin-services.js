/**
 * GURUH Admin — Services module
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

    var selectAll = document.getElementById('selectAllServices');
    if (selectAll) {
        selectAll.addEventListener('change', function () {
            document.querySelectorAll('.service-row-check').forEach(function (cb) {
                cb.checked = selectAll.checked;
            });
        });
    }
})();
