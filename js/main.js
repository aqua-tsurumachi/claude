/* =========================================================
   第一カード商会 - アドウォールLP
   ページ内の挙動をまとめたスクリプト
   ========================================================= */
(function () {
  'use strict';

  /* ---------------------------------------------------------
     設定 : 遷移先URLをここで差し替えてください
     （アドウォールのトラッキングパラメータが必要な場合も
       ここに追記します）
     --------------------------------------------------------- */
  var CONFIG = {
    ctaUrl: 'https://example.com/adwall'   // TODO: 「ポイントを獲得する」の遷移先
  };

  document.addEventListener('DOMContentLoaded', function () {
    applyLinks();
    initHeaderShadow();
    initReveal();
    initStickyCta();
    initFaqAccordion();
  });

  /* リンクの一括設定 --------------------------------------- */
  function applyLinks() {
    setHref('[data-cta]', CONFIG.ctaUrl);
  }
  function setHref(selector, url) {
    if (!url) return;
    var nodes = document.querySelectorAll(selector);
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].setAttribute('href', url);
    }
  }

  /* スクロールでヘッダーに影 ------------------------------ */
  function initHeaderShadow() {
    var header = document.getElementById('siteHeader');
    if (!header) return;
    var onScroll = function () {
      header.classList.toggle('scrolled', window.scrollY > 10);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* セクションのフェードイン ------------------------------ */
  function initReveal() {
    var targets = document.querySelectorAll('.reveal');
    if (!targets.length) return;

    // JSが有効なときだけ初期非表示にしてフェードインさせる
    document.documentElement.classList.add('js-reveal');

    if (!('IntersectionObserver' in window)) {
      for (var i = 0; i < targets.length; i++) targets[i].classList.add('in-view');
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    targets.forEach(function (el) { io.observe(el); });
  }

  /* ヒーローを過ぎたら追従CTAを表示 ---------------------- */
  function initStickyCta() {
    var sticky = document.getElementById('stickyCta');
    var hero = document.querySelector('.hero');
    if (!sticky || !hero) return;

    var update = function () {
      var passed = hero.getBoundingClientRect().bottom <= 0;
      sticky.hidden = !passed;
    };
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* よくある質問のアコーディオン ------------------------- */
  function initFaqAccordion() {
    var items = document.querySelectorAll('.faq-item');
    for (var i = 0; i < items.length; i++) {
      (function (item) {
        var q = item.querySelector('.faq-q');
        if (!q) return;
        q.addEventListener('click', function () {
          item.classList.toggle('open');
        });
      })(items[i]);
    }
  }
})();
