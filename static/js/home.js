/**
 * GURUH Construction — Homepage-only interactions
 */
(function () {
    'use strict';

    if (!document.body.classList.contains('page-home')) return;

    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function restartAnimation(elements) {
        elements.forEach(function (el) {
            el.style.animation = 'none';
            void el.offsetWidth;
            el.style.animation = '';
        });
    }

    function initHeroSlideAnimation() {
        var carousel = document.getElementById('heroCarousel');
        if (!carousel || reducedMotion) return;

        function onSlideActive(item) {
            if (!item) return;
            restartAnimation(item.querySelectorAll('.hero-anim'));
            restartAnimation(item.querySelectorAll('.hero-slide-bg'));
        }

        onSlideActive(carousel.querySelector('.carousel-item.active'));

        carousel.addEventListener('slid.bs.carousel', function (e) {
            onSlideActive(e.target.querySelector('.carousel-item.active'));
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        initHeroSlideAnimation();
    });
})();
