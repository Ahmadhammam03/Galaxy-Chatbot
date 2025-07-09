document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const chatbotIcon = document.getElementById('chatbotIcon');
    const chatbotWindow = document.getElementById('chatbotWindow');
    const closeChatbot = document.getElementById('closeChatbot');
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const speechBubble = document.getElementById('speechBubble');
    const bubbleText = document.getElementById('bubbleText');
    
    // API endpoint
    const API_URL = '/chat';
    
    // Creative messages to invite users
    const messages = [
        "Hi there, Do you want to know about Galaxy!",
        "Ask me anything about Galaxy Organisation and Alibaba Cloud!",
        "I'm here to help! Ask me about Galaxy 💬",
        "Need assistance? I'm your digital guide! ✨",
        "Curious about our programs? Just ask! 🌟",
        "Let's chat! I'm here to answer your questions 🤖",
        "Welcome! How can I assist you today?"
    ];
    
    let messageIndex = 0;
    let messageTimeout;
    
    // Function to show a new message
    function showMessage() {
        bubbleText.innerHTML = messages[messageIndex];
        speechBubble.classList.add('show');
        
        // Cycle to next message
        messageIndex = (messageIndex + 1) % messages.length;
        
        // Hide after 4 seconds
        setTimeout(() => {
            speechBubble.classList.remove('show');
            
            // Show next message after 8 seconds (only if chat is closed)
            messageTimeout = setTimeout(() => {
                if (chatbotWindow.style.display !== 'flex') {
                    showMessage();
                }
            }, 8000);
        }, 4000);
    }
    
    // Show first message after 1 second
    setTimeout(showMessage, 1000);
    
    // Toggle chatbot window
    chatbotIcon.addEventListener('click', function() {
        if (chatbotWindow.style.display === 'flex') {
            chatbotWindow.style.display = 'none';
            chatbotIcon.innerHTML = '<i class="fas fa-robot"></i>';
            
            // Resume showing messages after closing chat
            setTimeout(showMessage, 5000);
        } else {
            chatbotWindow.style.display = 'flex';
            chatbotIcon.innerHTML = '<i class="fas fa-comment"></i>';
            speechBubble.classList.remove('show');
            
            // Clear any pending message timeouts
            if (messageTimeout) {
                clearTimeout(messageTimeout);
            }
            
            // Focus on input
            userInput.focus();
        }
    });
    
    closeChatbot.addEventListener('click', function() {
        chatbotWindow.style.display = 'none';
        chatbotIcon.innerHTML = '<i class="fas fa-robot"></i>';
        
        // Resume showing messages after closing chat
        setTimeout(showMessage, 5000);
    });
    
    // Send message function - YOUR CHATBOT FUNCTIONALITY
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Disable input while processing
        userInput.disabled = true;
        sendButton.disabled = true;
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Show typing indicator
        const typingId = showTypingIndicator();
        
        try {
            // Send request to backend - YOUR API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            removeTypingIndicator(typingId);
            
            // Add bot response - YOUR TRAINED MODEL RESPONSE
            addMessage(data.response, 'bot');
            
            // Show confidence if available
            if (data.confidence) {
                console.log(`Confidence: ${(data.confidence * 100).toFixed(1)}%`);
            }
            
        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator(typingId);
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        } finally {
            // Re-enable input
            userInput.disabled = false;
            sendButton.disabled = false;
            sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
            userInput.focus();
        }
    }
    
    // Add message to chat
    function addMessage(text, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(sender + '-message');
        
        // Format message for better display
        if (sender === 'bot') {
            messageElement.innerHTML = formatMessage(text);
        } else {
            messageElement.textContent = text;
        }
        
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    // Format message (for bot responses)
    function formatMessage(message) {
        return message
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }
    
    // Show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message');
        typingDiv.id = `typing-${Date.now()}`;
        
        typingDiv.innerHTML = `
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
        
        return typingDiv.id;
    }
    
    // Remove typing indicator
    function removeTypingIndicator(id) {
        const typingDiv = document.getElementById(id);
        if (typingDiv) {
            typingDiv.remove();
        }
    }
    
    // Smooth scroll to bottom
    function scrollToBottom() {
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
    }
    
    // Event listeners for sending messages
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Example questions - YOUR CHATBOT SPECIFIC QUESTIONS
    const exampleQuestions = [
        "What is Galaxy Organisation?",
        "Tell me about ACA certification",
        "Where is Galaxy located?",
        "What services does Alibaba Cloud offer?",
        "How can I donate electronics to Galaxy?"
    ];
    
    // Add example questions as clickable hints after initial welcome
    setTimeout(() => {
        const exampleDiv = document.createElement('div');
        exampleDiv.classList.add('message', 'bot-message');
        
        exampleDiv.innerHTML = `
            <p><strong>Try asking:</strong></p>
            <div style="margin-top: 10px;">
                ${exampleQuestions.map(q => `
                    <div style="margin: 5px 0;">
                        <a href="#" onclick="askQuestion('${q}'); return false;"
                           style="color: #c0a53e; text-decoration: none; display: block; padding: 5px; border-radius: 5px; transition: background 0.2s;"
                           onmouseover="this.style.background='#f0f0f0'"
                           onmouseout="this.style.background='transparent'">
                            → ${q}
                        </a>
                    </div>
                `).join('')}
            </div>
        `;
        
        chatMessages.appendChild(exampleDiv);
        scrollToBottom();
    }, 2000);
    
    // Function to ask a question (make it global)
    window.askQuestion = function(question) {
        userInput.value = question;
        sendMessage();
    };
    
    // Focus on input when chat opens
    userInput.addEventListener('focus', () => {
        // Clear any pending message timeouts when user starts typing
        if (messageTimeout) {
            clearTimeout(messageTimeout);
        }
        speechBubble.classList.remove('show');
    });
});