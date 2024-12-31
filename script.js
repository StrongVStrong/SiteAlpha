const audio = document.getElementById('background-audio');
const muteButton = document.getElementById('mute-button');
const muteIcon = document.getElementById('mute-icon');
const volumeSlider = document.getElementById('volume-slider');

if (localStorage.getItem('audio-muted') === 'true') {
    audio.muted = true;
    muteIcon.src = 'assets/mute.png';
} else {
    audio.muted = false;
    muteIcon.src = 'assets/unmute.png';
}

if (localStorage.getItem('audio-volume')) {
    audio.volume = parseFloat(localStorage.getItem('audio-volume'));
    volumeSlider.value = audio.volume;
}

muteButton.addEventListener('click', () => {
    if (audio.muted) {
        audio.muted = false;
        muteIcon.src = 'assets/unmute.png';
        localStorage.setItem('audio-muted', 'false');
    }
    else {
        audio.muted = true;
        muteIcon.src = 'assets/mute.png';
        localStorage.setItem('audio-muted', 'true');
    }
});

volumeSlider.addEventListener('input', (event) => {
    audio.volume = event.target.value;
    localStorage.setItem('audio-volume', event.target.value);
})