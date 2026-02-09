/**
 * Books Page Widgets
 * - Currently Reading carousel: rotates every 10 seconds with a swipe animation
 * - Recommendations list: auto-scrolls via CSS, with manual arrow controls
 */

(function () {
  "use strict";

  // ── Currently Reading Carousel ──────────────────────────
  var track = document.querySelector(".carousel-track");
  if (!track) return;

  var slides = track.querySelectorAll(".carousel-slide");
  var dots = document.querySelectorAll(".carousel-dot");
  var prevBtn = document.querySelector(".carousel-prev");
  var nextBtn = document.querySelector(".carousel-next");
  var current = 0;
  var total = slides.length;
  var intervalMs = 10000; // 10 seconds
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

    function onExitEnd() {
      outgoing.classList.remove("exiting");
      outgoing.removeEventListener("animationend", onExitEnd);
    }
    outgoing.addEventListener("animationend", onExitEnd);

    // Show incoming slide
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

  function prev() {
    goTo((current - 1 + total) % total);
  }

  // Arrow click handlers
  if (prevBtn) {
    prevBtn.addEventListener("click", function () {
      prev();
      resetTimer();
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener("click", function () {
      next();
      resetTimer();
    });
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

  // ── Recommendations Arrow Controls ──────────────────────
  var recViewport = document.querySelector(".recommendations-viewport");
  var recList = document.querySelector(".recommendations-list");
  var recPrev = document.querySelector(".rec-prev");
  var recNext = document.querySelector(".rec-next");

  if (recViewport && recList && recPrev && recNext) {
    var scrollStep = 40; // pixels to jump per click

    recPrev.addEventListener("click", function () {
      // Pause auto-scroll, manually shift up
      recList.style.animationPlayState = "paused";
      recViewport.scrollTop = Math.max(0, recViewport.scrollTop - scrollStep);
    });

    recNext.addEventListener("click", function () {
      recList.style.animationPlayState = "paused";
      recViewport.scrollTop += scrollStep;
    });
  }
})();
