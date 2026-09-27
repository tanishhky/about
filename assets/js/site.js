// Progressive enhancement only: every page works without this file.
(function () {
  var root = document.documentElement;

  function stored() {
    try { return localStorage.getItem("theme"); } catch (e) { return null; }
  }
  function store(v) {
    try { localStorage.setItem("theme", v); } catch (e) { /* private mode: ignore */ }
  }
  function current() {
    var t = root.getAttribute("data-theme");
    if (t === "light" || t === "dark") return t;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  var toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    var sync = function () {
      toggle.setAttribute("aria-label", current() === "dark" ? "Switch to light theme" : "Switch to dark theme");
    };
    sync();
    toggle.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store(next);
      sync();
    });
  }
  if (!stored()) root.removeAttribute("data-theme");

  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.hidden = false;
    btn.addEventListener("click", function () {
      var src = document.getElementById(btn.getAttribute("data-copy"));
      if (!src) return;
      var text = src.textContent;
      var done = function () {
        var old = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = old; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () {});
      } else {
        var ta = document.createElement("textarea");
        ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
  });
})();
