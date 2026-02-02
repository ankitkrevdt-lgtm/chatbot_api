from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

app = FastAPI(title="🤖 EVD Technology AI Assistant")

# Load EVD knowledge
with open("knowledge.json") as f:
    evd_knowledge = json.load(f)

client = None  

def get_evd_response(query: str):
    responses = {
        "price": "EVD offers competitive pricing. Contact for custom quotes: Mon-Sat 10am-7pm",
        "web": "We build custom websites, e-commerce stores, and enterprise web apps. Fully responsive!",
        "app": "Android & iOS apps - native or hybrid. Let's discuss your mobile app needs!",
        "erp": "Complete LMS/ERP solutions. Our clients love our custom business automation!",
        "mobile": "We develop native Android/iOS apps and hybrid solutions. Let's build your app!",
        "contact": "Korba, Chhattisgarh. Mon-Sat: 10am-7pm. 24/7 support available!",
        "service": "We offer Web Development, Mobile Apps, ERP/CRM, Digital Marketing, UI/UX, SaaS"
    }
    
    query_lower = query.lower()
    for key, response in responses.items():
        if key in query_lower:
            return response
    
    return "Hi! I'm EVD Technology's AI assistant! What can I help you with today?"

@app.get("/", response_class=HTMLResponse)  
async def chat_home(request: Request):
    return """
<!DOCTYPE html>
<html>
<head>
    <title>EVD Technology AI Assistant</title>
    <meta name="viewport" content="width=device-width">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            height: 100vh; display: flex; flex-direction: column;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        }
        .header { background: rgba(255,255,255,0.1); padding: 20px; text-align: center; backdrop-filter: blur(10px); color: white; }
        .chat-container { flex: 1; max-width: 800px; margin: 0 auto; width: 100%; padding: 20px; }
        .messages { height: 70vh; overflow-y: auto; background: rgba(255,255,255,0.05); border-radius: 20px; padding: 20px; margin-bottom: 20px; }
        .message { margin-bottom: 15px; padding: 12px 18px; border-radius: 20px; max-width: 80%; word-wrap: break-word; }
        .user { background: #007bff; color: white; margin-left: auto; text-align: right; }
        .bot { background: rgba(255,255,255,0.2); color: white; backdrop-filter: blur(10px); }
        .input-area { display: flex; gap: 10px; background: rgba(255,255,255,0.1); padding: 20px; border-radius: 25px; backdrop-filter: blur(10px); }
        input[type=text] { flex: 1; padding: 15px 20px; border: none; border-radius: 25px; background: rgba(255,255,255,0.3); color: white; font-size: 16px; }
        input::placeholder { color: rgba(255,255,255,0.7); }
        button { background: linear-gradient(45deg, #ff6b6b, #feca57); color: white; border: none; padding: 15px 30px; border-radius: 25px; cursor: pointer; font-weight: bold; transition: transform 0.2s; }
        button:hover { transform: scale(1.05); }
        .typing { opacity: 0.7; font-style: italic; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 EVD Technology AI Assistant</h1>
        <p>Your 24/7 Korba-based tech partner | Web, Mobile, ERP/CRM experts</p>
    </div>
    
    <div class="chat-container">
        <div class="messages" id="messages">
            <div class="message bot">
                Hey there! 👋 I'm EVD Technology's AI assistant from Korba, Chhattisgarh. 
                I can help with Web Development, Mobile Apps, ERP/CRM, Digital Marketing. What would you like to know?
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Ask about services, pricing, timeline..." autocomplete="off">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const messagesEl = document.getElementById('messages');
        const inputEl = document.getElementById('messageInput');
        
        inputEl.focus();
        
        async function sendMessage() {
            const message = inputEl.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            inputEl.value = '';
            
            const typingMsg = addMessage('Typing...', 'bot typing');
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                const data = await response.json();
                
                messagesEl.removeChild(typingMsg);
                addMessage(data.response, 'bot');
            } catch (error) {
                messagesEl.removeChild(typingMsg);
                addMessage('Sorry, something went wrong. Please try again!', 'bot');
            }
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }
        
        function addMessage(text, type) {
            const div = document.createElement('div');
            div.className = `message ${type}`;
            div.textContent = text;
            messagesEl.appendChild(div);
            return div;
        }
        
        inputEl.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
    """

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("message", "").strip()
    
    if len(query) < 2:
        return {"response": "Tell me more! What service interests you?"}
    
    response = get_evd_response(query)
    return {"response": response}

@app.get("/api/health")
async def health():
    return {"status": " EVD Technology AI Chatbot LIVE!", "services": list(evd_knowledge["services"].keys())}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting EVD Technology Chatbot...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
