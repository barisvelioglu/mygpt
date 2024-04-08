<template>
  <div id="app">
    <header id="top-header">
      <img src="./assets/logo.png" alt="myGPT logo" class="logo">
    </header>
    <div id="chat-container" style="max-width: 1024px; margin: 0 auto;"> <!-- Add this container -->
      <div id="chat">
        <ul id="messages">
          <li v-for="msg in messages" :key="msg.id" :class="{'user-msg': msg.user, 'bot-msg': !msg.user}">
            <i :class="{'fas fa-user': msg.user, 'fas fa-robot': !msg.user}"></i> {{ msg.text }}
          </li>
        </ul>
      </div>
        <!-- Input field with loading icon -->
      <div class="input-with-loader">
        <input v-model="newMessage" @keyup.enter="sendMessage" :disabled="isLoading" placeholder="Type a message..." class="input-field"/>
        <div v-if="isLoading" class="loader"></div>
      </div>

    </div>
  </div>
</template>

<script>
const predefinedResponses = [
  "Hello! How can I assist you today?",
  "Can you please clarify your question?",
  "That's interesting! Tell me more.",
  "I'm here to help you.",
  "Thank you for sharing that.",
  "I'm not sure I understand. Can you elaborate?",
  "Let's try to solve this together.",
  "I'm here, ready to listen.",
  "That sounds good.",
  "I'm glad we're talking today."
];

export default {
  data() {
    return {
      messages: [
        {
          id: 0,
          text: "Hello! I'm your smart assistant. Tell me what you need.",
          user: false // Indicating this message is from the bot
        }
      ],
      newMessage: '',
      isLoading: false, // Track loading state
    };
  },
  methods: {
    async sendMessage() {
      if (this.newMessage.trim() !== '') {
      this.isLoading = true; // Start loading
      try {
        const response = await fetch('http://localhost:8080/reply', {
          method: 'POST', // or 'GET' if your endpoint is designed that way
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: this.newMessage }), // If your API requires the message
        });
        const data = await response.json();
        this.addMessage(this.newMessage, true); // Your message
        this.addMessage(data.message, false); // Bot response
      } catch (error) {
        console.error('Error fetching the reply:', error);
      }
      this.isLoading = false; // End loading
      this.newMessage = '';
    }
  },
    addMessage(text, isUser) {
      this.messages.push({ id: this.messages.length + 1, text, user: isUser });
    },
    botReply() {
      const reply = predefinedResponses[Math.floor(Math.random() * predefinedResponses.length)];
      setTimeout(() => this.addMessage(reply, false), 500);
    }
  },
};
</script>

<style>
/* Existing styles */
* {
  box-sizing: border-box;
}


/* Add this to your existing styles */
#top-header {
  text-align: center;
  padding: 20px;
}

.logo {
  /* Adjust the width as needed or keep it auto to maintain the original ratio */
  width: auto;
  max-height: 150px; /* You can adjust this as needed */
}

/* Set a maximum width of 1024px for both the chat container and the textarea */
#chat-container {
  max-width: 1024px;
  margin: 0 auto; /* Center the container */
}

.input-with-loader {
  position: relative;
  display: flex;
  align-items: center;
}

/* Adjust the input field */
.input-field {
  width: 100%; /* Ensure the input field fills the container */
  padding: 10px; 
  padding-right: 40px; /* Make space for loader */

  margin-top: 10px; /* Spacing above the input field */
  border: 2px solid #007BFF;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  font-family: 'Arial', sans-serif;
  font-size: 16px;
  color: #333;
  outline: none;
  margin-bottom: 20px; /* Space below the input field */
  box-sizing: border-box; /* Include padding and border in the input field's total width and height */
}

/* Adjustments for the chat box and messages for consistency */
#chat {
  margin-bottom: 20px; /* Add space below the chat history container */
  padding: 10px; /* Padding inside the chat history container */
  border: 1px solid #ccc; /* Border style for the chat history container */
  border-radius: 5px; /* Rounded corners for the chat history container */
  padding: 10px;
  overflow-y: auto;
  height: 400px; /* Adjust the height as needed */
  background-color: #f9f9f9; /* Light background for the chat area */
}
#messages li {
  max-width: 100%; /* Ensure messages use the full width of the chat history container */
  font-size: 1.2rem; /* Increase font size */
  display: flex;
  align-items: center; /* Aligns icon and text */
  padding:10px;
  gap: 10px; /* Adds space between icon and text */
  margin: 5px 0;
}

.user-msg {
  background-color: #007bff;
  color: white;
  border-bottom-right-radius: 0;
}

.bot-msg {
  background-color: #e9ecef;
  color: #333;
  border-bottom-left-radius: 0;
}

/* Style for icons */
#messages li i {
  font-size: 1.5rem; /* Larger icons */
}

.user-msg i {
  color: white; /* Icon color for user messages */
}

.bot-msg i {
  color: #333; /* Icon color for bot messages */
}

.loader {
  position: absolute;
  top: 20px;
  right: 10px;
  border: 5px solid #f3f3f3;
  border-radius: 50%;
  border-top: 5px solid #3498db;
  width: 25px;
  height: 25px;
  -webkit-animation: spin 2s linear infinite; /* Safari */
  animation: spin 2s linear infinite;
}

/* Safari */
@-webkit-keyframes spin {
  0% { -webkit-transform: rotate(0deg); }
  100% { -webkit-transform: rotate(360deg); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}


</style>
