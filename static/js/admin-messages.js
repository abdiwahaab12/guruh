(function () {
    "use strict";

    var selectAll = document.getElementById("selectAllMessages");
    if (selectAll) {
        selectAll.addEventListener("change", function () {
            document.querySelectorAll('input[name="message_ids"]').forEach(function (cb) {
                cb.checked = selectAll.checked;
            });
        });
    }
})();
