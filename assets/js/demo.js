// Section 5 : lance la boucle de démonstration quand elle est visible, sauf si le visiteur préfère un mouvement réduit.
// Sans ce script (ou avec mouvement réduit) : l'affiche reste visible et le lecteur garde ses commandes (lecture, pause).
(function () {
  var video = document.querySelector(".demo__video");
  if (!video) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!("IntersectionObserver" in window)) return;
  var arreteParVisiteur = false;
  video.addEventListener("pause", function () { if (!video.dataset.auto) arreteParVisiteur = true; delete video.dataset.auto; });
  new IntersectionObserver(function (entrees) {
    entrees.forEach(function (e) {
      if (e.isIntersecting && !arreteParVisiteur) {
        video.preload = "auto";
        var lecture = video.play();
        if (lecture && lecture.catch) lecture.catch(function () {});
      } else if (!e.isIntersecting && !video.paused) {
        video.dataset.auto = "1";
        video.pause();
      }
    });
  }, { threshold: 0.25 }).observe(video);
})();
