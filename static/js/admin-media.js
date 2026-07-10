/**
 * GURUH Admin — Enterprise Media Manager
 */

(function () {
    'use strict';

    var dropzone = document.getElementById('mediaDropzone');
    var dropInput = document.getElementById('mediaDropInput');
    var previewList = document.getElementById('mediaUploadPreview');
    var progressWrap = document.getElementById('mediaUploadProgress');
    var progressBar = document.getElementById('mediaUploadProgressBar');
    var progressStatus = document.getElementById('mediaUploadStatus');
    var uploadForm = document.getElementById('mediaUploadForm');
    var config = window.GURUH_MEDIA_UPLOAD || {};

    function bindDropzone() {
        if (!dropzone || !dropInput) return;

        dropzone.addEventListener('click', function () {
            dropInput.click();
        });

        dropzone.addEventListener('keydown', function (event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                dropInput.click();
            }
        });

        dropzone.addEventListener('dragover', function (event) {
            event.preventDefault();
            dropzone.classList.add('is-dragover');
        });

        dropzone.addEventListener('dragleave', function () {
            dropzone.classList.remove('is-dragover');
        });

        dropzone.addEventListener('drop', function (event) {
            event.preventDefault();
            dropzone.classList.remove('is-dragover');
            if (event.dataTransfer && event.dataTransfer.files.length) {
                uploadFilesAjax(event.dataTransfer.files);
            }
        });

        dropInput.addEventListener('change', function () {
            if (dropInput.files && dropInput.files.length) {
                uploadFilesAjax(dropInput.files);
            }
        });
    }

    function renderPreviewResults(results) {
        if (!previewList) return;
        previewList.innerHTML = '';
        results.forEach(function (item) {
            var li = document.createElement('li');
            li.className = 'admin-media-upload-preview-item' + (item.success ? ' is-success' : ' is-error');
            li.textContent = item.message + (item.asset ? ' — ' + item.asset.title : '');
            previewList.appendChild(li);
        });
    }

    function uploadFilesAjax(fileList) {
        if (!config.apiUrl || !config.csrfToken) return;

        var formData = new FormData();
        formData.append('csrf_token', config.csrfToken);
        var folderSelect = document.getElementById('folder');
        formData.append('folder', folderSelect ? folderSelect.value : 'general');

        Array.prototype.forEach.call(fileList, function (file) {
            formData.append('files', file);
        });

        if (progressWrap) progressWrap.hidden = false;
        if (progressBar) progressBar.style.width = '0%';
        if (progressStatus) progressStatus.textContent = 'Uploading ' + fileList.length + ' file(s)…';

        var xhr = new XMLHttpRequest();
        xhr.open('POST', config.apiUrl, true);

        xhr.upload.addEventListener('progress', function (event) {
            if (event.lengthComputable && progressBar) {
                var pct = Math.round((event.loaded / event.total) * 100);
                progressBar.style.width = pct + '%';
                progressBar.setAttribute('aria-valuenow', String(pct));
            }
        });

        xhr.onload = function () {
            var response = {};
            try {
                response = JSON.parse(xhr.responseText || '{}');
            } catch (e) { /* ignore */ }

            if (progressBar) progressBar.style.width = '100%';
            if (progressStatus) {
                progressStatus.textContent = response.success
                    ? 'Upload complete.'
                    : 'Upload finished with errors.';
            }

            if (response.results) {
                renderPreviewResults(response.results);
            }

            if (response.success) {
                setTimeout(function () {
                    var folder = folderSelect ? folderSelect.value : 'general';
                    var base = config.libraryUrl || '/admin/media/library';
                    window.location.href = base + '?folder=' + encodeURIComponent(folder);
                }, 800);
            }
        };

        xhr.onerror = function () {
            if (progressStatus) progressStatus.textContent = 'Upload failed.';
        };

        xhr.send(formData);
    }

    bindDropzone();
})();
