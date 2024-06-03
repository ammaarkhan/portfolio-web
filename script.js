document.addEventListener("DOMContentLoaded", function () {
  const audio = document.getElementById("background-music");
  const descriptionSection = document.querySelector(".description-section");
  const playButton = document.getElementById("play-button");

  let isPlaying = false;

  audio.volume = 0.15;

  const observerOptions = {
    root: null,
    rootMargin: "0px",
    threshold: 0.5,
  };

  const observerCallback = (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && isPlaying) {
        audio.play();
      } else {
        audio.pause();
      }
    });
  };

  const observer = new IntersectionObserver(observerCallback, observerOptions);
  observer.observe(descriptionSection);

  playButton.addEventListener("click", function () {
    if (isPlaying) {
      audio.pause();
      playButton.innerText = "play elevator music 🎵";
    } else {
      audio
        .play()
        .then(() => {
          playButton.innerText = "click here to reach the floor :)";
        })
        .catch((error) => {
          console.error("Error playing audio:", error);
        });
    }
    isPlaying = !isPlaying;
  });
});
