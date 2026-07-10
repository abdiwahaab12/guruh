(function () {
    "use strict";
    var selectAll = document.getElementById("selectAllUsers");
    if (selectAll) {
        selectAll.addEventListener("change", function () {
            document.querySelectorAll('input[name="item_ids"]').forEach(function (cb) {
                cb.checked = selectAll.checked;
            });
        });
    }
})();
