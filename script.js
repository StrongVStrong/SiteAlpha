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

window.addEventListener('scroll', function() {
    const scrollPosition = window.scrollY + window.innerHeight;
    
    // Add class for fixed header when scrolling
    const container = document.querySelector('.container');
    if (window.scrollY > 0) {
        container.classList.add('header-fixed');
    } else {
        container.classList.remove('header-fixed');
    }
    
    // Reveal project items on scroll
    const projects = document.querySelectorAll('li');
    projects.forEach(function(project) {
        if (project.offsetTop < scrollPosition) {
            project.classList.add('visible');
        }
    });
});

// Function to append a message to the chatbox
function appendMessage(message, type) {
    const messagesContainer = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(type === 'user' ? 'user-message' : 'bot-message');
    messageDiv.textContent = message;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight; // Scroll to the bottom
}

async function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() === '') return; // Don't send empty messages

    appendMessage(userInput, 'user'); // Show user message
    document.getElementById('userInput').value = ''; // Clear input box

    try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.response) {
            appendMessage(data.response, 'bot');
        } else {
            appendMessage("Sorry, I couldn't get a response.", 'bot');
        }
    } catch (error) {
        console.error('Error:', error);
        appendMessage("Looks like @strongvstrong is offline go spam @ him and wake him up");
    }
}

// Function to send the first message from Vegito
function sendInitialMessage() {
    const initialMessage = "Yosha! Welcome to Megas Hub enjoy your stay!";
    appendMessage(initialMessage, 'bot');
}

// Trigger initial message when the page is loaded
window.onload = sendInitialMessage;

// Event listener for sending the message when the "Send" button is clicked
document.getElementById('sendBtn').addEventListener('click', sendMessage);

// Event listener for sending the message when "Enter" is pressed
document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

document.getElementById("hideBtn").addEventListener("click", function() {
    var chatbotContainer = document.getElementById("bot-container");
    chatbotContainer.style.display = "none";
    chatbotIcon.style.display = "block";
});

document.getElementById("showChatbotIcon").addEventListener("click", function() {
    // Show the chatbot container and hide the icon
    var chatbotContainer = document.getElementById("bot-container");
    var chatbotIcon = document.getElementById("chatbotIcon");

    chatbotContainer.style.display = "block";
    chatbotIcon.style.display = "none";
});

let ostcommand = document.getElementById("ost-commands");

function goBottom() {
    document.body.scrollTop = document.body.scrollHeight;
    document.documentElement.scrollTop = document.documentElement.scrollHeight;
}

document.getElementById("fetchThumb").addEventListener("click", function () {
    const url = document.getElementById("videoUrl").value;
    const videoId = extractYouTubeID(url);

    if (!videoId) {
        alert("Invalid YouTube URL");
        return;
    }

    const thumbnails = [
        "default.jpg",
        "mqdefault.jpg",
        "hqdefault.jpg",
        "sddefault.jpg",
        "maxresdefault.jpg"
    ];

    const container = document.createElement("div");
    container.style.marginTop = "20px";

    thumbnails.forEach(format => {
        const img = document.createElement("img");
        img.src = `https://img.youtube.com/vi/${videoId}/${format}`;
        img.alt = format;
        img.style.display = "block";
        img.style.marginBottom = "10px";
        container.appendChild(img);
    });

    const existingThumbnails = document.getElementById("thumbnailContainer");
    if (existingThumbnails) {
        existingThumbnails.innerHTML = '';
    }

    existingThumbnails.appendChild(container);
});

function extractYouTubeID(url) {
    const match = url.match(
        /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/
    );
    return match ? match[1] : null;
}
