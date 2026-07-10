/**
 * GURUH Admin — Team module
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

    var selectAll = document.getElementById('selectAllTeam');
    if (selectAll) {
        selectAll.addEventListener('change', function () {
            document.querySelectorAll('.team-row-check').forEach(function (cb) {
                cb.checked = selectAll.checked;
            });
        });
    }
})();
