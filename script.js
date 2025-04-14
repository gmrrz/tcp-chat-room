let ws; // WebSocket connection
let currentRoomCode = null;

// Function to create a chat room
function createChatRoom() {
    currentRoomCode = generateRoomCode();
    document.getElementById("room-code").style.display = "block";
    document.getElementById("generated-code").textContent = currentRoomCode;

    connectToWebSocket(currentRoomCode);
    document.getElementById("chat-room").style.display = "block"; // Show chat room
    alert(`Chat room created! Share this code: ${currentRoomCode}`);
}

// Function to join a chat room
function joinChatRoom() {
    const roomCodeInput = document.getElementById("room-code-input").value.trim();
    if (!roomCodeInput) {
        alert("Please enter a valid room code.");
        return;
    }

    currentRoomCode = roomCodeInput;
    connectToWebSocket(currentRoomCode);
    document.getElementById("chat-room").style.display = "block"; // Show chat room
    alert(`Joined chat room: ${currentRoomCode}`);
}

// Function to connect to the WebSocket server
function connectToWebSocket(roomCode) {
    if (ws) {
        ws.close(); // Close any existing connection
    }

    ws = new WebSocket(`ws://localhost:8080/${roomCode}`);

    ws.onopen = function () {
        console.log(`Connected to room: ${roomCode}`);
    };

    ws.onmessage = function (event) {
        const message = event.data;
        const chatBox = document.getElementById("chat");
        const div = document.createElement("div");
        div.textContent = message;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    ws.onclose = function () {
        console.log("Disconnected from the server.");
    };

    ws.onerror = function (error) {
        console.error("WebSocket error:", error);
    };
}

// Function to send a message
function sendMessage() {
    const messageInput = document.getElementById("message");
    const message = messageInput.value.trim();
    if (message && ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ room: currentRoomCode, message }));
        messageInput.value = "";
    } else {
        alert("Unable to send message. Make sure you're connected to a chat room.");
    }
}

// Utility function to generate a random room code
function generateRoomCode() {
    return Math.random().toString(36).substring(2, 8).toUpperCase();
}