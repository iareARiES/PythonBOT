document.addEventListener('DOMContentLoaded', function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
    document.head.appendChild(script);
});

document.getElementById('sendBtn').addEventListener('click', function() {
    var userInput = document.getElementById('userInput').value;

    if (userInput.trim() !== "") {
        document.getElementById('welcomeMessage').style.display = 'none';
        document.getElementById('optionsSection').style.display = 'none';

        var messageDisplay = document.getElementById('messageDisplay');
        var userMessageContainer = document.createElement('div');
        userMessageContainer.classList.add('message', 'user-message-container');

        var userLabel = document.createElement('div');
        userLabel.classList.add('label');
        userLabel.textContent = 'User:';

        var userMessage = document.createElement('div');
        userMessage.classList.add('text', 'user-message');
        userMessage.textContent = userInput;

        userMessageContainer.appendChild(userLabel);
        userMessageContainer.appendChild(userMessage);
        messageDisplay.appendChild(userMessageContainer);

        messageDisplay.scrollTop = messageDisplay.scrollHeight;
        document.getElementById('userInput').value = "";

        fetch('/get', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'msg': userInput
            })
        })
        .then(response => response.json())
        .then(data => {
            var aiMessageText = marked.parse(data.response);

            var aiMessageContainer = document.createElement('div');
            aiMessageContainer.classList.add('message', 'ai-message-container');

            var aiLabel = document.createElement('div');
            aiLabel.classList.add('label');
            aiLabel.textContent = 'AI Mentor:';

            var aiMessage = document.createElement('div');
            aiMessage.classList.add('text', 'ai-message');
            aiMessage.innerHTML = aiMessageText;

            aiMessageContainer.appendChild(aiLabel);
            aiMessageContainer.appendChild(aiMessage);
            messageDisplay.appendChild(aiMessageContainer);

            messageDisplay.scrollTop = messageDisplay.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('sendBtn').click();
    }
});
