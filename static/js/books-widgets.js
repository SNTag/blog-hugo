/**
 * Books Page Widgets
 * - Currently Reading carousel: rotates every 15 seconds with a swipe animation
 * - Recommendations list: auto-scrolls via CSS, pauses on hover
 */

(function () {
  "use strict";

  // ── Currently Reading Carousel ──────────────────────────
  var track = document.querySelector(".carousel-track");
  if (!track) return;

  var slides = track.querySelectorAll(".carousel-slide");
  var dots = document.querySelectorAll(".carousel-dot");
  var current = 0;
  var total = slides.length;
  var intervalMs = 15000; // 15 seconds
  var timer = null;

  if (total === 0) return;

  // Initialise: show the first slide
  slides[0].classList.add("active");

  function goTo(index) {
    if (index === current) return;

    var outgoing = slides[current];
    var incoming = slides[index];

    // Animate outgoing slide away
    outgoing.classList.remove("active");
    outgoing.classList.add("exiting");

    // After the exit animation completes, clean up and show the new slide
    function onExitEnd() {
      outgoing.classList.remove("exiting");
      outgoing.removeEventListener("animationend", onExitEnd);
    }
    outgoing.addEventListener("animationend", onExitEnd);

    // Show incoming slide (it will animate in via CSS)
    incoming.classList.add("active");

    // Update dots
    if (dots.length) {
      dots[current].classList.remove("active");
      dots[index].classList.add("active");
    }

    current = index;
  }

  function next() {
    goTo((current + 1) % total);
  }

  // Dot click handlers
  dots.forEach(function (dot) {
    dot.addEventListener("click", function () {
      var idx = parseInt(this.getAttribute("data-index"), 10);
      if (isNaN(idx)) return;
      goTo(idx);
      resetTimer();
    });
  });

  // Auto-advance timer
  function resetTimer() {
    if (timer) clearInterval(timer);
    timer = setInterval(next, intervalMs);
  }

  // Pause on hover, resume on leave
  var carouselEl = document.querySelector(".reading-carousel");
  if (carouselEl) {
    carouselEl.addEventListener("mouseenter", function () {
      if (timer) clearInterval(timer);
    });
    carouselEl.addEventListener("mouseleave", function () {
      resetTimer();
    });
  }

  // Start
  resetTimer();
})();
