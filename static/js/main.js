/**
 * GURUH Construction — Main JavaScript
 */

(function () {
    'use strict';

    var SCROLL_THRESHOLD = 60;
    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function initStickyHeader() {
        var header = document.getElementById('header');
        if (!header) return;

        function updateHeaderState() {
            header.classList.toggle('is-scrolled', window.scrollY > SCROLL_THRESHOLD);
        }

        updateHeaderState();
        window.addEventListener('scroll', updateHeaderState, { passive: true });
    }

    function initMobileNavClose() {
        var navbarCollapse = document.getElementById('mainNavbar');
        if (!navbarCollapse) return;

        navbarCollapse.querySelectorAll('.nav-link:not(.nav-link--submenu-toggle), .dropdown-item, .nav-link--sub, .btn-quote').forEach(function (link) {
            link.addEventListener('click', function () {
                if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                    var toggler = document.querySelector('.navbar-toggler');
                    if (toggler) toggler.click();
                }
            });
        });
    }

    function initServicesNav() {
        var navbar = document.getElementById('mainNavbar');
        if (!navbar) return;

        var servicesItem = navbar.querySelector('.nav-item--services');
        var trigger = servicesItem ? servicesItem.querySelector('.nav-link--services') : null;
        var menu = servicesItem ? servicesItem.querySelector('.nav-services-menu') : null;
        var closeTimer = null;
        var desktopMq = window.matchMedia('(min-width: 992px)');

        function isDesktop() {
            return desktopMq.matches;
        }

        function setExpanded(open) {
            if (!trigger) return;
            trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
            if (servicesItem) {
                servicesItem.classList.toggle('is-open', open);
            }
        }

        function openMenu() {
            if (!isDesktop()) return;
            clearTimeout(closeTimer);
            setExpanded(true);
        }

        function closeMenu() {
            if (!isDesktop()) return;
            closeTimer = setTimeout(function () {
                setExpanded(false);
            }, 150);
        }

        if (servicesItem && trigger && menu) {
            servicesItem.addEventListener('mouseenter', openMenu);
            servicesItem.addEventListener('mouseleave', closeMenu);

            servicesItem.addEventListener('focusin', openMenu);
            servicesItem.addEventListener('focusout', function (e) {
                if (!servicesItem.contains(e.relatedTarget)) {
                    closeMenu();
                }
            });

            trigger.addEventListener('click', function (e) {
                if (!isDesktop()) return;
                e.preventDefault();
            });

            trigger.addEventListener('keydown', function (e) {
                if (!isDesktop()) return;
                var items = menu.querySelectorAll('.dropdown-item');
                if (e.key === 'Escape') {
                    setExpanded(false);
                    trigger.focus();
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    openMenu();
                    if (items.length) items[0].focus();
                } else if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    var willOpen = !servicesItem.classList.contains('is-open');
                    setExpanded(willOpen);
                }
            });

            menu.querySelectorAll('.dropdown-item').forEach(function (link, index, links) {
                link.addEventListener('keydown', function (e) {
                    if (!isDesktop()) return;
                    if (e.key === 'ArrowDown') {
                        e.preventDefault();
                        links[Math.min(index + 1, links.length - 1)].focus();
                    } else if (e.key === 'ArrowUp') {
                        e.preventDefault();
                        if (index === 0) {
                            trigger.focus();
                        } else {
                            links[index - 1].focus();
                        }
                    } else if (e.key === 'Escape') {
                        setExpanded(false);
                        trigger.focus();
                    }
                });
            });
        }

        navbar.querySelectorAll('.nav-link--submenu-toggle').forEach(function (toggle) {
            toggle.addEventListener('click', function (e) {
                if (isDesktop()) return;
                e.preventDefault();
            });
        });
    }

    function initScrollAnimations() {
        var els = document.querySelectorAll('[data-animate]');
        if (!els.length) return;

        if (reducedMotion || !('IntersectionObserver' in window)) {
            els.forEach(function (el) { el.classList.add('is-visible'); });
            return;
        }

        var obs = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) {
                    e.target.classList.add('is-visible');
                    obs.unobserve(e.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -24px 0px' });

        els.forEach(function (el) { obs.observe(el); });
    }

    function initCounters() {
        var counters = document.querySelectorAll('.counter[data-target]');
        if (!counters.length) return;

        var done = new WeakSet();

        function animate(el) {
            var raw = el.getAttribute('data-target') || '';
            var target = parseInt(raw, 10);
            if (isNaN(target)) {
                el.textContent = raw;
                return;
            }
            if (reducedMotion) {
                el.textContent = target;
                return;
            }

            var duration = 1600;
            var startTime = null;
            function step(ts) {
                if (!startTime) startTime = ts;
                var p = Math.min((ts - startTime) / duration, 1);
                el.textContent = Math.floor(target * (1 - Math.pow(1 - p, 3)));
                if (p < 1) requestAnimationFrame(step);
                else el.textContent = target;
            }
            requestAnimationFrame(step);
        }

        if (!('IntersectionObserver' in window)) {
            counters.forEach(animate);
            return;
        }

        var obs = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting && !done.has(e.target)) {
                    done.add(e.target);
                    animate(e.target);
                }
            });
        }, { threshold: 0.35 });

        counters.forEach(function (c) { obs.observe(c); });
    }

    function initProjectFilters() {
        if (!document.body.classList.contains('page-services')) return;

        var toolbar = document.querySelector('.page-services .pb-project-filters');
        var grid = document.getElementById('servicesProjectsGrid');
        var empty = document.getElementById('servicesProjectsEmpty');
        var status = document.getElementById('servicesFilterStatus');
        if (!toolbar || !grid) return;

        var buttons = toolbar.querySelectorAll('.pb-project-filter-btn');
        var items = grid.querySelectorAll('.pb-project-item');

        function applyFilter(key, label) {
            var visible = 0;
            items.forEach(function (item) {
                var match = key === 'all' || item.getAttribute('data-filter') === key;
                item.classList.toggle('is-hidden', !match);
                if (match) visible += 1;
            });
            if (empty) {
                empty.classList.toggle('d-none', visible > 0);
            }
            if (status) {
                status.textContent = visible + ' project' + (visible === 1 ? '' : 's') + ' shown for ' + label + '.';
            }
        }

        buttons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                var key = btn.getAttribute('data-filter') || 'all';
                var label = btn.textContent.trim();
                buttons.forEach(function (b) {
                    var active = b === btn;
                    b.classList.toggle('is-active', active);
                    b.setAttribute('aria-pressed', active ? 'true' : 'false');
                });
                applyFilter(key, label);
            });
        });

        if (buttons.length) {
            applyFilter(
                buttons[0].getAttribute('data-filter') || 'all',
                buttons[0].textContent.trim()
            );
        }
    }

    function initProjectsPortfolio() {
        if (!document.body.classList.contains('page-projects') || document.body.classList.contains('page-project-detail')) return;

        var grid = document.getElementById('projectsPortfolioGrid');
        var search = document.getElementById('projectsSearchInput');
        var empty = document.getElementById('projectsPortfolioEmpty');
        var status = document.getElementById('projectsFilterStatus');
        if (!grid) return;

        var items = grid.querySelectorAll('.pb-portfolio-item');
        var filterButtons = document.querySelectorAll('.pb-portfolio-filter');
        var activeFilters = {
            category: 'all',
            country: 'all',
            county: 'all',
            status: 'all',
            year: 'all',
            client: 'all',
            service: 'all'
        };

        function itemMatches(item) {
            var searchTerm = search ? search.value.trim().toLowerCase() : '';
            var haystack = item.getAttribute('data-search') || '';
            if (searchTerm && haystack.indexOf(searchTerm) === -1) return false;
            if (activeFilters.category !== 'all' && item.getAttribute('data-category') !== activeFilters.category) return false;
            if (activeFilters.country !== 'all' && item.getAttribute('data-country') !== activeFilters.country) return false;
            if (activeFilters.county !== 'all' && item.getAttribute('data-county') !== activeFilters.county) return false;
            if (activeFilters.status !== 'all' && item.getAttribute('data-status') !== activeFilters.status) return false;
            if (activeFilters.year !== 'all' && item.getAttribute('data-year') !== activeFilters.year) return false;
            if (activeFilters.client !== 'all' && item.getAttribute('data-client') !== activeFilters.client) return false;
            if (activeFilters.service !== 'all' && item.getAttribute('data-service') !== activeFilters.service) return false;
            return true;
        }

        function applyPortfolioFilters() {
            var visible = 0;
            items.forEach(function (item) {
                var match = itemMatches(item);
                item.classList.toggle('is-hidden', !match);
                if (match) visible += 1;
            });
            if (empty) empty.classList.toggle('d-none', visible > 0);
            if (status) {
                status.textContent = visible + ' project' + (visible === 1 ? '' : 's') + ' matching your criteria.';
            }
        }

        filterButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                var group = btn.getAttribute('data-filter-group');
                var value = btn.getAttribute('data-filter') || 'all';
                if (!group) return;
                activeFilters[group] = value;
                document.querySelectorAll('.pb-portfolio-filter[data-filter-group=\"' + group + '\"]').forEach(function (b) {
                    var active = b === btn;
                    b.classList.toggle('is-active', active);
                    b.setAttribute('aria-pressed', active ? 'true' : 'false');
                });
                applyPortfolioFilters();
            });
        });

        if (search) {
            search.addEventListener('input', applyPortfolioFilters);
        }

        applyPortfolioFilters();
    }

    function initAreasMap() {
        if (!document.body.classList.contains('page-projects')) return;
        var buttons = document.querySelectorAll('.pb-areas-county-btn');
        if (!buttons.length) return;

        buttons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                var active = btn.getAttribute('aria-pressed') === 'true';
                buttons.forEach(function (b) {
                    b.classList.remove('is-active');
                    b.setAttribute('aria-pressed', 'false');
                });
                if (!active) {
                    btn.classList.add('is-active');
                    btn.setAttribute('aria-pressed', 'true');
                }
            });
        });
    }

    function initProjectGallery() {
        var isProjectDetail = document.body.classList.contains('page-project-detail');
        var isEquipment = document.body.classList.contains('page-equipment');
        if (!isProjectDetail && !isEquipment) return;

        var masonry = document.querySelector('.pb-gallery-masonry');
        var filters = document.querySelectorAll('.pb-gallery-filter');
        var lightbox = document.getElementById('projectLightbox');
        var lightboxImg = document.getElementById('projectLightboxImage');
        var lightboxCaption = document.getElementById('projectLightboxCaption');
        if (!masonry) return;

        var triggers = masonry.querySelectorAll('.pb-gallery-trigger');
        var currentIndex = 0;
        var visibleTriggers = [];

        function refreshVisibleTriggers() {
            visibleTriggers = Array.prototype.filter.call(triggers, function (t) {
                return !t.closest('.pb-gallery-item').classList.contains('is-hidden');
            });
        }

        function applyGalleryFilter(key) {
            masonry.querySelectorAll('.pb-gallery-item').forEach(function (item) {
                var cat = item.getAttribute('data-category') || 'all';
                var match = key === 'all' || cat === key;
                item.classList.toggle('is-hidden', !match);
            });
            refreshVisibleTriggers();
        }

        filters.forEach(function (btn) {
            btn.addEventListener('click', function () {
                var key = btn.getAttribute('data-gallery-filter') || 'all';
                filters.forEach(function (b) {
                    var active = b === btn;
                    b.classList.toggle('is-active', active);
                    b.setAttribute('aria-pressed', active ? 'true' : 'false');
                });
                applyGalleryFilter(key);
            });
        });

        function openLightbox(index) {
            if (!lightbox || !lightboxImg || !visibleTriggers.length) return;
            currentIndex = index;
            var trigger = visibleTriggers[currentIndex];
            lightboxImg.src = trigger.getAttribute('data-lightbox-src');
            lightboxImg.alt = trigger.getAttribute('data-lightbox-caption') || 'Project image';
            if (lightboxCaption) {
                lightboxCaption.textContent = trigger.getAttribute('data-lightbox-caption') || '';
            }
            lightbox.hidden = false;
            document.body.style.overflow = 'hidden';
        }

        function closeLightbox() {
            if (!lightbox) return;
            lightbox.hidden = true;
            document.body.style.overflow = '';
        }

        function stepLightbox(delta) {
            if (!visibleTriggers.length) return;
            currentIndex = (currentIndex + delta + visibleTriggers.length) % visibleTriggers.length;
            openLightbox(currentIndex);
        }

        triggers.forEach(function (trigger, index) {
            trigger.addEventListener('click', function () {
                refreshVisibleTriggers();
                var idx = visibleTriggers.indexOf(trigger);
                openLightbox(idx >= 0 ? idx : 0);
            });
        });

        if (lightbox) {
            lightbox.querySelectorAll('[data-lightbox-close]').forEach(function (el) {
                el.addEventListener('click', closeLightbox);
            });
            var prev = lightbox.querySelector('[data-lightbox-prev]');
            var next = lightbox.querySelector('[data-lightbox-next]');
            if (prev) prev.addEventListener('click', function () { stepLightbox(-1); });
            if (next) next.addEventListener('click', function () { stepLightbox(1); });

            document.addEventListener('keydown', function (e) {
                if (lightbox.hidden) return;
                if (e.key === 'Escape') closeLightbox();
                if (e.key === 'ArrowLeft') stepLightbox(-1);
                if (e.key === 'ArrowRight') stepLightbox(1);
            });
        }

        refreshVisibleTriggers();
    }

    function initGalleryVideoCenter() {
        if (!document.body.classList.contains('page-gallery')) return;

        var lightbox = document.getElementById('galleryVideoLightbox');
        var embedHost = document.getElementById('galleryVideoEmbedHost');
        var nativeVideo = document.getElementById('galleryVideoNative');
        var caption = document.getElementById('galleryVideoCaption');
        var triggers = document.querySelectorAll('.pb-video-trigger:not(.pb-video-trigger--disabled)');
        if (!lightbox || !triggers.length) return;

        function resetPlayer() {
            if (embedHost) {
                embedHost.innerHTML = '';
                embedHost.hidden = true;
            }
            if (nativeVideo) {
                nativeVideo.pause();
                nativeVideo.removeAttribute('src');
                nativeVideo.load();
                nativeVideo.hidden = true;
            }
        }

        function closeVideo() {
            resetPlayer();
            lightbox.hidden = true;
            document.body.classList.remove('pb-lightbox-open');
        }

        function openVideo(trigger) {
            var playUrl = trigger.getAttribute('data-video-play-url') || '';
            var isEmbed = trigger.getAttribute('data-video-embed') === 'true';
            var title = trigger.getAttribute('data-video-title') || 'Gallery video';
            if (!playUrl) return;

            resetPlayer();
            if (caption) caption.textContent = title;

            if (isEmbed && embedHost) {
                var iframe = document.createElement('iframe');
                iframe.src = playUrl;
                iframe.title = title;
                iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
                iframe.allowFullscreen = true;
                iframe.className = 'pb-video-lightbox-iframe';
                embedHost.appendChild(iframe);
                embedHost.hidden = false;
            } else if (nativeVideo) {
                nativeVideo.src = playUrl;
                nativeVideo.hidden = false;
                nativeVideo.play().catch(function () {});
            }

            lightbox.hidden = false;
            document.body.classList.add('pb-lightbox-open');
        }

        triggers.forEach(function (trigger) {
            trigger.addEventListener('click', function () {
                openVideo(trigger);
            });
        });

        lightbox.querySelectorAll('[data-video-close]').forEach(function (el) {
            el.addEventListener('click', closeVideo);
        });

        document.addEventListener('keydown', function (e) {
            if (lightbox.hidden) return;
            if (e.key === 'Escape') closeVideo();
        });
    }

    function initGalleryMediaCenter() {
        if (!document.body.classList.contains('page-gallery')) return;

        var grid = document.getElementById('galleryMediaGrid');
        var empty = document.getElementById('galleryEmptyState');
        var results = document.getElementById('galleryResultsCount');
        var searchInput = document.getElementById('gallerySearchInput');
        var resetBtn = document.getElementById('galleryFilterReset');
        var selects = document.querySelectorAll('.pb-gallery-select');
        var albumButtons = document.querySelectorAll('.pb-album-card-link[data-album-filter]');
        var lightbox = document.getElementById('galleryLightbox');
        var lightboxImg = document.getElementById('galleryLightboxImage');
        var lightboxCaption = document.getElementById('galleryLightboxCaption');
        if (!grid) return;

        var cards = grid.querySelectorAll('.pb-gallery-card');
        var triggers = grid.querySelectorAll('.pb-gallery-trigger');
        var activeAlbum = '';
        var visibleTriggers = [];
        var currentIndex = 0;

        function getFilterValues() {
            var values = { search: '', project: '', service: '', equipment: '', category: '', county: '', year: '' };
            if (searchInput) values.search = (searchInput.value || '').trim().toLowerCase();
            selects.forEach(function (sel) {
                var key = sel.getAttribute('data-filter-key');
                if (key && Object.prototype.hasOwnProperty.call(values, key)) {
                    values[key] = sel.value || '';
                }
            });
            return values;
        }

        function applyGalleryFilters() {
            var f = getFilterValues();
            var visible = 0;
            cards.forEach(function (card) {
                var match = true;
                if (f.project && card.getAttribute('data-project') !== f.project) match = false;
                if (f.service && card.getAttribute('data-service') !== f.service) match = false;
                if (f.equipment && card.getAttribute('data-equipment') !== f.equipment) match = false;
                if (f.category && card.getAttribute('data-category') !== f.category) match = false;
                if (f.county && card.getAttribute('data-county') !== f.county) match = false;
                if (f.year && card.getAttribute('data-year') !== f.year) match = false;
                if (activeAlbum && card.getAttribute('data-album') !== activeAlbum) match = false;
                if (f.search) {
                    var hay = card.getAttribute('data-search') || '';
                    if (hay.indexOf(f.search) === -1) match = false;
                }
                card.classList.toggle('is-hidden', !match);
                if (match) visible += 1;
            });
            if (empty) empty.classList.toggle('d-none', visible > 0);
            if (results) {
                results.textContent = visible + ' media item' + (visible === 1 ? '' : 's') + ' shown.';
            }
            refreshVisibleTriggers();
        }

        function refreshVisibleTriggers() {
            visibleTriggers = Array.prototype.filter.call(triggers, function (t) {
                return !t.closest('.pb-gallery-card').classList.contains('is-hidden');
            });
        }

        function resetFilters() {
            activeAlbum = '';
            if (searchInput) searchInput.value = '';
            selects.forEach(function (sel) { sel.value = ''; });
            applyGalleryFilters();
        }

        if (searchInput) {
            searchInput.addEventListener('input', applyGalleryFilters);
        }
        selects.forEach(function (sel) {
            sel.addEventListener('change', function () {
                activeAlbum = '';
                applyGalleryFilters();
            });
        });
        if (resetBtn) resetBtn.addEventListener('click', resetFilters);

        albumButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                activeAlbum = btn.getAttribute('data-album-filter') || '';
                selects.forEach(function (sel) { sel.value = ''; });
                if (searchInput) searchInput.value = '';
                applyGalleryFilters();
                var gridSection = document.getElementById('gallery-grid');
                if (gridSection) gridSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
        });

        function openLightbox(index) {
            if (!lightbox || !lightboxImg || !visibleTriggers.length) return;
            currentIndex = index;
            var trigger = visibleTriggers[currentIndex];
            lightboxImg.src = trigger.getAttribute('data-lightbox-src');
            lightboxImg.alt = trigger.getAttribute('data-lightbox-caption') || 'Gallery image';
            if (lightboxCaption) {
                lightboxCaption.textContent = trigger.getAttribute('data-lightbox-caption') || '';
            }
            lightbox.hidden = false;
            document.body.style.overflow = 'hidden';
        }

        function closeLightbox() {
            if (!lightbox) return;
            lightbox.hidden = true;
            document.body.style.overflow = '';
        }

        function stepLightbox(delta) {
            if (!visibleTriggers.length) return;
            currentIndex = (currentIndex + delta + visibleTriggers.length) % visibleTriggers.length;
            openLightbox(currentIndex);
        }

        triggers.forEach(function (trigger) {
            trigger.addEventListener('click', function () {
                refreshVisibleTriggers();
                var idx = visibleTriggers.indexOf(trigger);
                openLightbox(idx >= 0 ? idx : 0);
            });
        });

        if (lightbox) {
            lightbox.querySelectorAll('[data-lightbox-close]').forEach(function (el) {
                el.addEventListener('click', closeLightbox);
            });
            var prev = lightbox.querySelector('[data-lightbox-prev]');
            var next = lightbox.querySelector('[data-lightbox-next]');
            if (prev) prev.addEventListener('click', function () { stepLightbox(-1); });
            if (next) next.addEventListener('click', function () { stepLightbox(1); });

            document.addEventListener('keydown', function (e) {
                if (lightbox.hidden) return;
                if (e.key === 'Escape') closeLightbox();
                if (e.key === 'ArrowLeft') stepLightbox(-1);
                if (e.key === 'ArrowRight') stepLightbox(1);
            });
        }

        applyGalleryFilters();
    }

    function initEquipmentGrid() {
        if (!document.body.classList.contains('page-equipment') || document.body.classList.contains('page-equipment-detail')) return;

        var grid = document.getElementById('equipmentGrid');
        var empty = document.getElementById('equipmentGridEmpty');
        var status = document.getElementById('equipmentFilterStatus');
        var filters = document.querySelectorAll('.pb-equipment-filter');
        var categoryCards = document.querySelectorAll('.pb-equipment-category-card[data-category-filter]');
        if (!grid) return;

        var items = grid.querySelectorAll('.pb-equipment-item');
        var activeKey = 'all';

        function applyEquipmentFilter(key) {
            activeKey = key || 'all';
            var visible = 0;
            items.forEach(function (item) {
                var cat = item.getAttribute('data-category') || '';
                var match = activeKey === 'all' || cat === activeKey;
                item.classList.toggle('is-hidden', !match);
                if (match) visible += 1;
            });
            if (empty) empty.classList.toggle('d-none', visible > 0);
            if (status) {
                status.textContent = visible + ' equipment item' + (visible === 1 ? '' : 's') + ' shown.';
            }
        }

        filters.forEach(function (btn) {
            btn.addEventListener('click', function () {
                var key = btn.getAttribute('data-equipment-filter') || 'all';
                filters.forEach(function (b) {
                    var active = b === btn;
                    b.classList.toggle('is-active', active);
                    b.setAttribute('aria-pressed', active ? 'true' : 'false');
                });
                applyEquipmentFilter(key);
            });
        });

        categoryCards.forEach(function (card) {
            card.addEventListener('click', function (e) {
                var key = card.getAttribute('data-category-filter') || 'all';
                filters.forEach(function (b) {
                    var match = (b.getAttribute('data-equipment-filter') || 'all') === key;
                    b.classList.toggle('is-active', match);
                    b.setAttribute('aria-pressed', match ? 'true' : 'false');
                });
                applyEquipmentFilter(key);
            });
        });

        applyEquipmentFilter('all');
    }

    function initQuoteWizard() {
        if (!document.body.classList.contains('page-quote')) return;

        var form = document.querySelector('[data-multistep-form]');
        if (!form) return;

        var panels = Array.prototype.slice.call(form.querySelectorAll('[data-step-panel]'));
        var stepperItems = Array.prototype.slice.call(form.querySelectorAll('.pb-quote-stepper-item'));
        var progressBar = form.querySelector('.pb-quote-progress-bar');
        var progressWrap = form.querySelector('.pb-quote-progress');
        var backBtn = document.getElementById('quoteStepBack');
        var nextBtn = document.getElementById('quoteStepNext');
        var submitBtn = document.getElementById('quoteStepSubmit');
        var reviewList = document.getElementById('quoteReviewList');
        var autosaveStatus = document.getElementById('quoteAutosaveStatus');
        var autosaveKey = form.getAttribute('data-autosave-key') || 'guruh-quote-draft';
        var currentStep = 0;

        function getPanelFields(panel) {
            if (!panel || panel.getAttribute('data-step-type') === 'confirmation') return [];
            return Array.prototype.filter.call(
                panel.querySelectorAll('.pb-form-control, .form-control, .form-select'),
                function (input) { return !input.disabled; }
            );
        }

        function validatePanel(panel) {
            var valid = true;
            getPanelFields(panel).forEach(function (input) {
                var wrapper = input.closest('[class*="col-"]') || input.parentElement;
                var feedback = wrapper ? wrapper.querySelector('.invalid-feedback') : null;
                var isValid = input.checkValidity();
                input.classList.toggle('is-invalid', !isValid);
                input.classList.toggle('is-valid', isValid && input.value.trim() !== '');
                if (feedback && !isValid) {
                    feedback.textContent = input.validity.valueMissing
                        ? 'This field is required.'
                        : (input.validity.typeMismatch && input.type === 'email'
                            ? 'Please enter a valid email address.'
                            : input.validationMessage);
                }
                if (!isValid) valid = false;
            });
            return valid;
        }

        function getSelectLabel(input) {
            var option = input.options[input.selectedIndex];
            return option ? option.textContent : input.value;
        }

        function getFieldDisplayValue(input) {
            if (input.tagName === 'SELECT') return getSelectLabel(input);
            return input.value.trim();
        }

        function buildReviewSummary() {
            if (!reviewList) return;
            reviewList.innerHTML = '';
            form.querySelectorAll('.pb-form-control, .form-control, .form-select').forEach(function (input) {
                if (input.disabled || input.type === 'file') return;
                var value = getFieldDisplayValue(input);
                if (!value) return;
                var labelEl = form.querySelector('label[for="' + input.id + '"]');
                var label = labelEl ? labelEl.textContent.replace('*', '').trim() : input.name;
                var dt = document.createElement('dt');
                dt.textContent = label;
                var dd = document.createElement('dd');
                dd.textContent = value;
                reviewList.appendChild(dt);
                reviewList.appendChild(dd);
            });
        }

        function saveDraft() {
            try {
                var data = {};
                form.querySelectorAll('.pb-form-control, .form-control, .form-select').forEach(function (input) {
                    if (input.disabled || input.type === 'file') return;
                    data[input.name] = input.value;
                });
                data._step = currentStep;
                localStorage.setItem(autosaveKey, JSON.stringify(data));
                if (autosaveStatus) autosaveStatus.textContent = 'Draft saved locally';
            } catch (err) { /* storage unavailable */ }
        }

        function restoreDraft() {
            try {
                var raw = localStorage.getItem(autosaveKey);
                if (!raw) return;
                var data = JSON.parse(raw);
                form.querySelectorAll('.pb-form-control, .form-control, .form-select').forEach(function (input) {
                    if (data[input.name] !== undefined) input.value = data[input.name];
                });
                if (typeof data._step === 'number' && data._step >= 0 && data._step < panels.length) {
                    currentStep = data._step;
                }
                if (autosaveStatus) autosaveStatus.textContent = 'Draft restored';
            } catch (err) { /* ignore corrupt draft */ }
        }

        function updateStepUI() {
            panels.forEach(function (panel, index) {
                panel.classList.toggle('d-none', index !== currentStep);
            });
            stepperItems.forEach(function (item, index) {
                var active = index === currentStep;
                var complete = index < currentStep;
                item.classList.toggle('is-active', active);
                item.classList.toggle('is-complete', complete);
                item.setAttribute('aria-current', active ? 'step' : 'false');
            });
            if (progressBar && progressWrap) {
                var pct = ((currentStep + 1) / panels.length) * 100;
                progressBar.style.width = pct + '%';
                progressWrap.setAttribute('aria-valuenow', String(currentStep + 1));
            }
            if (backBtn) backBtn.classList.toggle('d-none', currentStep === 0);
            var isLast = currentStep === panels.length - 1;
            if (nextBtn) nextBtn.classList.toggle('d-none', isLast);
            if (submitBtn) submitBtn.classList.toggle('d-none', !isLast);
            if (isLast) buildReviewSummary();
            saveDraft();
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', function () {
                var panel = panels[currentStep];
                if (!validatePanel(panel)) {
                    form.classList.add('was-validated');
                    return;
                }
                if (currentStep < panels.length - 1) {
                    currentStep += 1;
                    updateStepUI();
                    var header = panels[currentStep].querySelector('.pb-quote-step-header');
                    if (header) header.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        }

        if (backBtn) {
            backBtn.addEventListener('click', function () {
                if (currentStep > 0) {
                    currentStep -= 1;
                    updateStepUI();
                }
            });
        }

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var valid = true;
            panels.forEach(function (panel) {
                if (panel.getAttribute('data-step-type') === 'confirmation') return;
                if (!validatePanel(panel)) valid = false;
            });
            form.classList.add('was-validated');
            if (!valid) {
                for (var i = 0; i < panels.length; i += 1) {
                    if (panels[i].getAttribute('data-step-type') !== 'confirmation' && !validatePanel(panels[i])) {
                        currentStep = i;
                        updateStepUI();
                        break;
                    }
                }
                return;
            }
            var feedbackEl = form.querySelector('.pb-form-feedback');
            var message = form.getAttribute('data-success-message') || 'Form validated successfully.';
            if (feedbackEl) {
                feedbackEl.textContent = message;
                feedbackEl.classList.remove('d-none');
            }
            try { localStorage.removeItem(autosaveKey); } catch (err) { /* ignore */ }
            if (autosaveStatus) autosaveStatus.textContent = 'Submitted — draft cleared';
            form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });

        form.querySelectorAll('.pb-form-control, .form-control, .form-select').forEach(function (input) {
            input.addEventListener('input', saveDraft);
            input.addEventListener('change', saveDraft);
        });

        restoreDraft();
        updateStepUI();
    }

    function initFormValidation() {
        var forms = document.querySelectorAll('[data-validate-form]:not([data-multistep-form])');
        if (!forms.length) return;

        forms.forEach(function (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                var valid = true;

                form.querySelectorAll('.pb-form-control, .form-control, .form-select').forEach(function (input) {
                    if (input.disabled) return;
                    var wrapper = input.closest('[class*="col-"]') || input.parentElement;
                    var feedback = wrapper ? wrapper.querySelector('.invalid-feedback') : null;
                    var isValid = input.checkValidity();

                    input.classList.toggle('is-invalid', !isValid);
                    input.classList.toggle('is-valid', isValid && input.value.trim() !== '');

                    if (feedback && !isValid) {
                        if (input.validity.valueMissing) {
                            feedback.textContent = 'This field is required.';
                        } else if (input.validity.typeMismatch && input.type === 'email') {
                            feedback.textContent = 'Please enter a valid email address.';
                        } else if (input.validity.patternMismatch) {
                            feedback.textContent = 'Please match the requested format.';
                        } else {
                            feedback.textContent = input.validationMessage;
                        }
                    }

                    if (!isValid) valid = false;
                });

                form.classList.add('was-validated');

                if (valid) {
                    var feedbackEl = form.querySelector('.pb-form-feedback');
                    var message = form.getAttribute('data-success-message') || 'Form validated successfully.';
                    if (feedbackEl) {
                        feedbackEl.textContent = message;
                        feedbackEl.classList.remove('d-none');
                    }
                }
            });

            form.querySelectorAll('.pb-form-control, .form-control, .form-select').forEach(function (input) {
                input.addEventListener('input', function () {
                    if (!form.classList.contains('was-validated')) return;
                    var wrapper = input.closest('[class*="col-"]') || input.parentElement;
                    var feedback = wrapper ? wrapper.querySelector('.invalid-feedback') : null;
                    var isValid = input.checkValidity();
                    input.classList.toggle('is-invalid', !isValid);
                    input.classList.toggle('is-valid', isValid && input.value.trim() !== '');
                    if (feedback && isValid) feedback.textContent = '';
                });
            });
        });
    }

    function initPartnersSlider() {
        document.querySelectorAll('[data-partners-slider]').forEach(function (slider) {
            var track = slider.querySelector('.partners-slider-track');
            var count = parseInt(slider.getAttribute('data-partner-count') || '0', 10);
            if (!track || count < 2) {
                return;
            }

            if (reducedMotion) {
                slider.classList.add('is-static');
                track.classList.remove('is-marquee');
                return;
            }

            var duration = Math.max(count * 4, 18);
            track.classList.add('is-marquee');
            track.style.setProperty('--partners-marquee-duration', duration + 's');

            slider.addEventListener('mouseenter', function () {
                track.style.animationPlayState = 'paused';
            });
            slider.addEventListener('mouseleave', function () {
                track.style.animationPlayState = 'running';
            });
            slider.addEventListener('focusin', function () {
                track.style.animationPlayState = 'paused';
            });
            slider.addEventListener('focusout', function () {
                track.style.animationPlayState = 'running';
            });
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        initStickyHeader();
        initMobileNavClose();
        initServicesNav();
        initScrollAnimations();
        initCounters();
        initProjectFilters();
        initProjectsPortfolio();
        initAreasMap();
        initProjectGallery();
        initGalleryMediaCenter();
        initGalleryVideoCenter();
        initQuoteWizard();
        initEquipmentGrid();
        initFormValidation();
        initPartnersSlider();
    });
})();
