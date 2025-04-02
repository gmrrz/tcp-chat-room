const chatBox = document.getElementById("chat");
const messageInput = document.getElementById("message");
const ws = new WebSocket("ws://localhost:8080")

ws.onmessage = function(event) {
    const message = event.data;
    const div = document.createElement("div");
    div.textContent = message;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
};

function sendMessage() {
    const message = messageInput.ariaValueMax;
    ws.send(message);
    messageInput.value = "";
}