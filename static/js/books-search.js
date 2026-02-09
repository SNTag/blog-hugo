(function () {
  'use strict';

  var input = document.getElementById('book-search-input');
  var clearBtn = document.getElementById('book-search-clear');
  var statusEl = document.getElementById('book-search-status');
  var catalogue = document.getElementById('books-catalogue');
  var pagination = document.getElementById('books-pagination');

  if (!input || !catalogue) return;

  var bookItems = catalogue.querySelectorAll('.book-item[data-url]');
  var fuse = null;
  var searchIndex = [];

  // Fetch the JSON index and initialise Fuse
  var basePath = document.querySelector('link[rel="canonical"]');
  var indexUrl = '/books/index.json';

  fetch(indexUrl)
    .then(function (res) { return res.json(); })
    .then(function (data) {
      searchIndex = data;
      fuse = new Fuse(data, {
        keys: [
          { name: 'title', weight: 0.35 },
          { name: 'author', weight: 0.25 },
          { name: 'tags', weight: 0.2 },
          { name: 'keywords', weight: 0.1 },
          { name: 'publisher', weight: 0.1 }
        ],
        threshold: 0.4,
        ignoreLocation: true,
        minMatchCharLength: 2
      });
    })
    .catch(function () {
      // Fallback: disable search gracefully
      input.placeholder = 'Search unavailable';
      input.disabled = true;
    });

  // Normalise URL for comparison (strip trailing slash, protocol, host)
  function normaliseUrl(url) {
    try {
      var u = new URL(url, window.location.origin);
      return u.pathname.replace(/\/+$/, '');
    } catch (e) {
      return url.replace(/\/+$/, '');
    }
  }

  // Build a lookup from normalised URL -> DOM element
  var itemsByUrl = {};
  bookItems.forEach(function (el) {
    var url = normaliseUrl(el.getAttribute('data-url'));
    itemsByUrl[url] = el;
  });

  function performSearch(query) {
    query = query.trim();

    if (!query) {
      // Show all items, restore pagination
      bookItems.forEach(function (el) {
        el.style.display = '';
      });
      if (pagination) pagination.style.display = '';
      if (statusEl) statusEl.textContent = '';
      clearBtn.style.display = 'none';
      return;
    }

    clearBtn.style.display = '';

    if (!fuse) return;

    var results = fuse.search(query);
    var matchedUrls = {};
    results.forEach(function (r) {
      matchedUrls[normaliseUrl(r.item.url)] = true;
    });

    // Show/hide book cards
    bookItems.forEach(function (el) {
      var url = normaliseUrl(el.getAttribute('data-url'));
      el.style.display = matchedUrls[url] ? '' : 'none';
    });

    // Hide pagination during search
    if (pagination) pagination.style.display = 'none';

    // Status message
    if (statusEl) {
      var count = results.length;
      statusEl.textContent = count === 0
        ? 'No books found.'
        : count + (count === 1 ? ' book found.' : ' books found.');
    }
  }

  // Debounce helper
  var timer = null;
  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      performSearch(input.value);
    }, 200);
  });

  // Clear button
  clearBtn.addEventListener('click', function () {
    input.value = '';
    performSearch('');
    input.focus();
  });

  // Allow Escape to clear
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      input.value = '';
      performSearch('');
    }
  });
})();
