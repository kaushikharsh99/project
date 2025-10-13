let activeChat = "Chat 1";
let chats = {"Chat 1": []};

// Function to switch chat
function switchChat(chatName) {
    activeChat = chatName;
    const chatBox = document.querySelector("#chatbot");
    chatBox.innerHTML = ""; // clear chat

    const messages = chats[chatName] || [];
    messages.forEach(msg => {
        addMessageToUI(msg.user, msg.bot);
    });

    document.querySelectorAll(".chat-item").forEach(item => {
        item.classList.remove("active");
        if (item.innerText === chatName) item.classList.add("active");
    });
}

// Add message to UI
function addMessageToUI(user, bot) {
    const chatBox = document.querySelector("#chatbot");
    if (user) {
        const userMsg = document.createElement("div");
        userMsg.className = "message user";
        userMsg.innerText = user;
        chatBox.appendChild(userMsg);
    }
    if (bot) {
        const botMsg = document.createElement("div");
        botMsg.className = "message bot";
        botMsg.innerText = bot;
        chatBox.appendChild(botMsg);
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Create initial chat list
function initSidebar() {
    const sidebar = document.querySelector(".chat-list");
    sidebar.innerHTML = "";
    Object.keys(chats).forEach(chatName => {
        const div = document.createElement("div");
        div.className = "chat-item" + (chatName === activeChat ? " active" : "");
        div.innerText = chatName;
        div.onclick = () => switchChat(chatName);
        sidebar.appendChild(div);
    });
}

document.addEventListener("DOMContentLoaded", initSidebar);
