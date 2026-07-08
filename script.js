document.addEventListener("DOMContentLoaded", function () {
  const audio = document.getElementById("background-music");
  const playButton = document.getElementById("play-button");
  const pitch = playButton.closest(".pitch");
  const dot = '<span class="pitch-dot" aria-hidden="true"></span>';

  audio.volume = 0.1;
  audio.loop = true;

  function setUI(playing) {
    pitch.classList.toggle("playing", playing);
    playButton.innerHTML = dot + (playing ? "going up&hellip; 🛗" : "elevator music 🛗");
  }

  playButton.addEventListener("click", function () {
    if (audio.paused) {
      setUI(true);
      audio.play().catch(function (error) {
        console.error("Error playing audio:", error);
        setUI(false);
      });
    } else {
      audio.pause();
      setUI(false);
    }
  });
});
