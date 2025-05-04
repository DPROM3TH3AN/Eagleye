// frontend/static/scripts.js
document.addEventListener("DOMContentLoaded", () => {
    // Chatbot functionality
    const sendChatBtn = document.getElementById("send-btn");
    const chatInput = document.getElementById("chat-input");
    const chatOutput = document.getElementById("chat-output");

    sendChatBtn.addEventListener("click", async () => {
        const message = chatInput.value.trim();
        if (!message) {
            alert("Please enter a message.");
            return;
        }
        try {
            const response = await fetch('/chat/message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            chatOutput.textContent = data.reply;
        } catch (error) {
            console.error("Error sending chat message:", error);
            chatOutput.textContent = "Error: Unable to get a reply.";
        }
    });

    // WebSocket for realtime tracking updates
    const ws = new WebSocket(`ws://${window.location.host}/tracking/ws/tracking`);
    ws.onmessage = function(event) {
        const message = JSON.parse(event.data);
        console.log("Realtime tracking update:", message);
    };

    ws.onopen = function() {
        // Send a default device identifier
        ws.send(JSON.stringify({ device_id: "device123", imei: "IMEI123456789" }));
    };

    // Fetch Folium map endpoint for tracking
    const getMapBtn = document.getElementById("get-map-btn");
    const mapContainer = document.getElementById("map-container");
    getMapBtn.addEventListener("click", async () => {
        try {
            const response = await fetch('/tracking/map?device_id=device123');
            const data = await response.json();
            mapContainer.innerHTML = data.map;
        } catch (error) {
            console.error("Error fetching the map:", error);
            mapContainer.textContent = "Error: Unable to load the map.";
        }
    });
});
