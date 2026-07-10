/**
 * GURUH Admin — Gallery module
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

    var selectAll = document.getElementById('selectAllGallery');
    if (selectAll) {
        selectAll.addEventListener('change', function () {
            document.querySelectorAll('.gallery-row-check').forEach(function (cb) {
                cb.checked = selectAll.checked;
            });
        });
    }

    var BEFORE_AFTER_CATEGORY = 'Before & After';
    var PROGRESS_CATEGORY = 'Project Progress';
    var AWARDS_CATEGORIES = ['Awards', 'Company Events'];

    function categoryHelpText(category, mediaType) {
        if (category === BEFORE_AFTER_CATEGORY) {
            return 'Shows in <strong>Before &amp; After Gallery</strong>. Set before + after images on the Media tab.';
        }
        if (category === PROGRESS_CATEGORY) {
            return 'Shows in <strong>Project Progress Gallery</strong>. Use Caption for project name and Date for the milestone date.';
        }
        if (AWARDS_CATEGORIES.indexOf(category) !== -1) {
            return 'Shows in <strong>Awards &amp; Events Gallery</strong>.';
        }
        if (mediaType === 'video') {
            return 'Shows in <strong>Video Gallery</strong>. Upload MP4/WebM in Media → Upload first.';
        }
        return 'Shows in the main <strong>Gallery Grid</strong> (photo cards with filters).';
    }

    function toggleGalleryFieldGroups() {
        var typeSelect = document.getElementById('media_type');
        var categorySelect = document.getElementById('category');
        var videoBlock = document.getElementById('galleryVideoFields');
        var beforeAfterBlock = document.getElementById('galleryBeforeAfterFields');
        var mediaHelp = document.getElementById('galleryMediaPathHelp');
        var categoryHelp = document.getElementById('galleryCategoryHelp');

        var mediaType = typeSelect ? typeSelect.value : 'image';
        var category = categorySelect ? categorySelect.value : '';
        var isVideo = mediaType === 'video';
        var isBeforeAfter = category === BEFORE_AFTER_CATEGORY;

        if (videoBlock) videoBlock.style.display = isVideo && !isBeforeAfter ? 'block' : 'none';
        if (beforeAfterBlock) beforeAfterBlock.style.display = isBeforeAfter ? 'block' : 'none';
        if (categoryHelp) categoryHelp.innerHTML = categoryHelpText(category, mediaType);
        if (mediaHelp) {
            mediaHelp.innerHTML = isBeforeAfter
                ? 'Choose the <strong>After</strong> photo below. Set the <strong>Before</strong> photo in the Before &amp; After section.'
                : isVideo
                    ? 'Video file path or thumbnail image. Upload MP4/WebM in Media → Upload first.'
                    : 'Primary image for the gallery grid.';
        }
    }

    var mediaType = document.getElementById('media_type');
    var category = document.getElementById('category');
    if (mediaType) mediaType.addEventListener('change', toggleGalleryFieldGroups);
    if (category) category.addEventListener('change', toggleGalleryFieldGroups);
    toggleGalleryFieldGroups();
})();
