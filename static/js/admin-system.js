/** System Administration — minimal client helpers */
(function () {
    "use strict";
    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll("[data-confirm-restore]").forEach(function (btn) {
            btn.addEventListener("click", function () {
                if (!window.confirm("Restore this backup? Current data may be overwritten.")) {
                    btn.closest("form")?.reset();
                }
            });
        });
    });
})();
