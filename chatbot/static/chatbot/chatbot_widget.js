document.getElementById('chatbot-circle').addEventListener('click', function () {
  document.getElementById('chatbot-circle').style.display = 'none';
  document.getElementById('chatbot-box').style.display = 'flex';
});

document.getElementById('chatbot-close').addEventListener('click', function () {
  document.getElementById('chatbot-circle').style.display = 'flex';
  document.getElementById('chatbot-box').style.display = 'none';
});

document.getElementById('chatbot-send').addEventListener('click', sendMessage);
document.getElementById('chatbot-input').addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    sendMessage();
  }
});

function sendMessage() {
  const inputElement = document.getElementById('chatbot-input');
  const message = inputElement.value.trim();

  if (message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('user-message');
    messageElement.innerText = message;
    document.getElementById('chatbot-box-content').appendChild(messageElement);
    inputElement.value = '';

    // Send the message to the chatbot backend
    fetch('/chatbot/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': '{{ csrf_token }}',
      },
      body: 'message=' + encodeURIComponent(message),
    })
      .then((response) => response.json())
      .then((data) => {
        const chatbotResponseElement = document.createElement('div');
        chatbotResponseElement.classList.add('chatbot-message');
        chatbotResponseElement.innerText = data.message;
        document.getElementById('chatbot-box-content').appendChild(chatbotResponseElement);
        scrollToBottom();
      });
  }
}

function scrollToBottom() {
  const chatContent = document.getElementById('chatbot-box-content');
  chatContent.scrollTop = chatContent.scrollHeight;
}
