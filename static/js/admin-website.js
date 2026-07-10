(function () {
    "use strict";

    var uploadConfig = window.GURUH_MEDIA_UPLOAD || {};

    function staticUrl(path) {
        return "/static/" + String(path || "").replace(/^\//, "");
    }

    function getFieldWrap(field) {
        return field.closest(".admin-hero-banner-field") || field.closest(".admin-dynamic-field");
    }

    function updateMediaPreview(field, path) {
        var fieldWrap = getFieldWrap(field);
        if (!fieldWrap) {
            return;
        }

        if (fieldWrap.getAttribute("data-field-type") === "document") {
            var docPreview = fieldWrap.querySelector(".admin-document-preview");
            var fileName = String(path || "").split("/").pop();
            if (docPreview) {
                var link = docPreview.querySelector("a");
                if (link) {
                    link.href = staticUrl(path);
                    link.textContent = fileName || path;
                }
            } else if (path) {
                var previewBlock = document.createElement("p");
                previewBlock.className = "small mb-2 admin-document-preview";
                previewBlock.innerHTML = '<i class="bi bi-file-earmark-pdf text-danger" aria-hidden="true"></i> Current file: '
                    + '<a href="' + staticUrl(path) + '" target="_blank" rel="noopener">' + fileName + "</a>";
                var pickerGrid = fieldWrap.querySelector(".admin-media-picker-grid");
                if (pickerGrid) {
                    fieldWrap.insertBefore(previewBlock, pickerGrid);
                } else {
                    fieldWrap.appendChild(previewBlock);
                }
            }

            fieldWrap.querySelectorAll(".admin-media-picker-btn").forEach(function (item) {
                item.classList.toggle("is-selected", item.getAttribute("data-path") === path);
            });
            return;
        }

        var preview = fieldWrap.querySelector(".admin-hero-banner-preview")
            || fieldWrap.querySelector(".admin-website-media-preview");
        var url = staticUrl(path);

        if (preview && preview.tagName === "IMG") {
            preview.src = url;
            preview.classList.remove("admin-hero-banner-preview--empty");
        } else if (preview && preview.classList.contains("admin-hero-banner-preview--empty")) {
            var img = document.createElement("img");
            img.src = url;
            img.alt = "Media preview";
            img.className = "admin-website-media-preview admin-hero-banner-preview";
            img.loading = "lazy";
            preview.replaceWith(img);
        } else if (preview) {
            preview.src = url;
        } else if (path) {
            var newImg = document.createElement("img");
            newImg.src = url;
            newImg.alt = "Media preview";
            newImg.className = "admin-website-media-preview";
            newImg.loading = "lazy";
            var pickerGrid = fieldWrap.querySelector(".admin-media-picker-grid");
            if (pickerGrid) {
                fieldWrap.insertBefore(newImg, pickerGrid);
            } else {
                fieldWrap.appendChild(newImg);
            }
        }

        fieldWrap.querySelectorAll(".admin-media-picker-btn").forEach(function (item) {
            item.classList.toggle("is-selected", item.getAttribute("data-path") === path);
        });
    }

    function setMediaFieldValue(field, path) {
        if (!field || !path) {
            return;
        }
        field.value = path;
        field.dispatchEvent(new Event("change", { bubbles: true }));
        field.dispatchEvent(new Event("input", { bubbles: true }));
        updateMediaPreview(field, path);
    }

    function getCsrfToken() {
        if (uploadConfig.csrfToken) {
            return uploadConfig.csrfToken;
        }
        var tokenInput = document.querySelector('input[name="csrf_token"]');
        return tokenInput ? tokenInput.value : "";
    }

    function uploadFileToField(file, field, folder) {
        if (!uploadConfig.apiUrl || !file || !field) {
            return;
        }

        var formData = new FormData();
        formData.append("csrf_token", getCsrfToken());
        formData.append("folder", folder || "general");
        formData.append("files", file);
        formData.append("title", file.name.replace(/\.[^.]+$/, ""));

        var uploadBtn = field.closest(".admin-dynamic-field")
            ? field.closest(".admin-dynamic-field").querySelector(".admin-media-upload-btn")
            : null;
        var originalLabel = uploadBtn ? uploadBtn.innerHTML : "";
        if (uploadBtn) {
            uploadBtn.disabled = true;
            uploadBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Uploading…';
        }

        fetch(uploadConfig.apiUrl, {
            method: "POST",
            body: formData,
            credentials: "same-origin"
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                var result = (data.results || []).find(function (item) {
                    return item.success && item.asset && item.asset.storage_path;
                });
                if (result && result.asset) {
                    setMediaFieldValue(field, result.asset.storage_path);
                } else {
                    window.alert((data.results && data.results[0] && data.results[0].message) || "Upload failed.");
                }
            })
            .catch(function () {
                window.alert("Upload failed. Please try again.");
            })
            .finally(function () {
                if (uploadBtn) {
                    uploadBtn.disabled = false;
                    uploadBtn.innerHTML = originalLabel;
                }
            });
    }

    document.addEventListener("click", function (event) {
        var btn = event.target.closest(".admin-media-picker-btn");
        if (btn) {
            var path = btn.getAttribute("data-path");
            if (!path) {
                return;
            }

            var targetId = btn.getAttribute("data-target");
            var field = targetId ? document.getElementById(targetId) : null;
            if (!field) {
                field = document.querySelector(".admin-media-target:focus")
                    || document.querySelector(".admin-media-target");
            }
            if (!field) {
                return;
            }

            setMediaFieldValue(field, path);
            return;
        }

        var uploadBtn = event.target.closest(".admin-media-upload-btn");
        if (uploadBtn) {
            var uploadTargetId = uploadBtn.getAttribute("data-target");
            var uploadFieldWrap = uploadBtn.closest(".admin-dynamic-field");
            var fileInput = uploadFieldWrap
                ? uploadFieldWrap.querySelector('.admin-media-upload-input[data-target="' + uploadTargetId + '"]')
                : null;
            if (!fileInput && uploadFieldWrap) {
                fileInput = uploadFieldWrap.querySelector(".admin-media-upload-input");
            }
            if (fileInput) {
                fileInput.click();
            }
        }
    });

    document.addEventListener("change", function (event) {
        var fileInput = event.target.closest(".admin-media-upload-input");
        if (!fileInput || !fileInput.files || !fileInput.files.length) {
            return;
        }

        var targetId = fileInput.getAttribute("data-target");
        var field = targetId ? document.getElementById(targetId) : null;
        if (!field) {
            return;
        }

        uploadFileToField(
            fileInput.files[0],
            field,
            fileInput.getAttribute("data-folder") || "general"
        );
        fileInput.value = "";
    });
})();
