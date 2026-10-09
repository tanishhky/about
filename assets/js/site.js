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
  // Analytics: GA runs on every page, but it cannot see inside a PDF or follow a
  // visitor off the site, so record which papers get opened and which repos,
  // SSRN pages and profiles get clicked. Custom names avoid double counting with
  // GA's own enhanced-measurement events.
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest ? ev.target.closest("a[href]") : null;
    if (!a || typeof window.gtag !== "function") return;
    var url = a.href;
    var name = null;
    if (/\.pdf($|[?#])/i.test(url)) name = "pdf_open";
    else if (/github\.com/i.test(url)) name = "github_click";
    else if (/ssrn\.com/i.test(url)) name = "ssrn_click";
    else if (/linkedin\.com/i.test(url)) name = "linkedin_click";
    else if (/^mailto:/i.test(url)) name = "email_click";
    if (!name) return;
    window.gtag("event", name, {
      link_url: url,
      link_text: (a.textContent || "").trim().slice(0, 100),
      page_path: location.pathname
    });
  });
  // Owner opt-out: ?notrack=1 turns Google Analytics off in this browser (the flag is
  // read in <head> before GA loads), ?notrack=0 turns it back on. Say which, briefly.
  var nt = /[?&]notrack=([01])(&|$)/.exec(location.search);
  if (nt) {
    var note = document.createElement("div");
    note.setAttribute("role", "status");
    note.textContent = nt[1] === "1" ? "Analytics is now off in this browser." : "Analytics is back on in this browser.";
    note.style.cssText = "position:fixed;left:50%;bottom:20px;transform:translateX(-50%);z-index:50;" +
      "padding:10px 16px;border-radius:8px;background:var(--ink);color:var(--bg);font:500 14px/1.3 Inter,system-ui,sans-serif;";
    document.body.appendChild(note);
    setTimeout(function () { note.remove(); }, 4000);
  }
})();
