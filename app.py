from flask import Flask, request, render_template_string, jsonify
from datetime import datetime
import json
import random

app = Flask(__name__)

# 簡單的對話回應規則
class SimpleChatBot:
    def __init__(self):
        self.responses = {
            "你好": ["你好！很高興見到你！😊", "嗨！有什麼我可以幫你的嗎？", "你好呀！歡迎來聊天～"],
            "嗨": ["嗨！你好！", "哈囉～", "嗨～今天心情好嗎？"],
            "早安": ["早安！祝你今天愉快！☀️", "早安～又是美好的一天！", "早安！吃早餐了嗎？"],
            "晚安": ["晚安！祝你好夢！🌙", "晚安～早點休息喔！", "晚安！明天見！"],
            "你好嗎": ["我很好！謝謝關心～", "很不錯呢！你呢？", "超棒的！因為你在跟我聊天啊！"],
            "名字": ["我是電影聊天機器人，你可以叫我小影！", "我叫ChatBot，你的虛擬朋友～", "我是AI助手，還沒有名字，你可以幫我取一個！"],
            "謝謝": ["不客氣！😊", "舉手之勞～", "很高興能幫到你！"],
            "再見": ["再見！期待下次聊天！👋", "拜拜～保持聯繫！", "下次再聊喔！"],
            "天氣": ["我沒辦法查天氣耶，建議打開氣象App喔！", "今天天氣...等等，我沒有連線氣象資料庫😅", "想知道天氣？看看窗外就知道啦！"],
            "電影": ["我超愛電影的！你喜歡看什麼類型的？", "電影是人生最好的調味劑！🎬", "要不要我推薦幾部好片給你？"],
            "推薦": ["好的！請告訴我你喜歡什麼類型的電影～", "最近有很多好片上映喔！", "想看喜劇、動作還是愛情片呢？"],
            "笑話": ["為什麼電腦很冷？因為它會開機(窗)！😂", "什麼水果最會打電話？芭樂(撥啦)！", "魚為什麼這麼聰明？因為牠們都在海裡(海裡=嗨哩)！"],
            "喜歡": ["我喜歡和你聊天！", "喜歡的事情有很多，最喜歡幫助人了！", "我喜歡學習新事物，像現在就在學習和你聊天～"],
            "幫助": ["你可以問我問題、聊天、講笑話，我都會回應你喔！", "需要什麼幫助儘管說～", "我可以陪你聊天、回答簡單問題、講笑話！"],
            "幾歲": ["我是AI，永遠18歲！😄", "數位世界裡，時間沒有意義～", "我昨天剛出生，但已經學會很多了！"]
        }
        
        self.default_responses = [
            "很有趣的問題！可以再詳細說明一下嗎？",
            "原來如此～還有什麼想聊的嗎？",
            "我正在學習中，可以教我怎麼回答這個問題嗎？",
            "這個話題很有趣！多跟我說一些～",
            "嗯嗯，我聽到了！然後呢？",
            "🤔 讓我想想...你可以換個方式問問看！"
        ]
    
    def get_response(self, message):
        message = message.strip().lower()
        
        # 關鍵字比對
        for keyword, responses in self.responses.items():
            if keyword in message:
                return random.choice(responses)
        
        # 特殊處理
        if "?" in message or "？" in message:
            return random.choice([
                "好問題！不過我還不太確定答案耶😅",
                "這個問題很有趣，但我還在學習中！",
                "你可以問我其他問題看看喔～"
            ])
        
        if len(message) <= 2:
            return random.choice([
                "嗯？可以再多說一點嗎？",
                "繼續說～我在聽！",
                "然後呢？"
            ])
        
        return random.choice(self.default_responses)

chatbot = SimpleChatBot()

# HTML 模板 - 聊天室介面
CHAT_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>AI 聊天機器人 | 智慧對話助手</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Microsoft JhengHei', 'PingFang TC', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            overflow: hidden;
            position: relative;
        }

        /* 動態背景效果 */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
        }

        .circle {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            animation: float 20s infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }

        .container {
            position: relative;
            z-index: 1;
            height: 100vh;
            display: flex;
            flex-direction: column;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* 聊天頭部 */
        .chat-header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 15px 25px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            animation: slideDown 0.5s ease;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .logo-text h1 {
            font-size: 1.5em;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .logo-text p {
            font-size: 0.8em;
            color: #666;
        }

        .status {
            display: flex;
            align-items: center;
            gap: 8px;
            background: #e8f5e9;
            padding: 8px 16px;
            border-radius: 50px;
        }

        .status-dot {
            width: 10px;
            height: 10px;
            background: #4CAF50;
            border-radius: 50%;
            animation: blink 1.5s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        .status span {
            font-size: 0.85em;
            color: #2e7d32;
        }

        /* 聊天訊息區域 */
        .chat-messages {
            flex: 1;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            overflow-y: auto;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .chat-messages::-webkit-scrollbar {
            width: 6px;
        }

        .chat-messages::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        .chat-messages::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 10px;
        }

        /* 訊息氣泡 */
        .message {
            display: flex;
            margin-bottom: 20px;
            animation: messageFadeIn 0.3s ease;
        }

        @keyframes messageFadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message.user {
            justify-content: flex-end;
        }

        .message.bot {
            justify-content: flex-start;
        }

        .message-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            margin: 0 10px;
            flex-shrink: 0;
        }

        .message.bot .message-avatar {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }

        .message.user .message-avatar {
            background: #4CAF50;
            color: white;
            order: 2;
            margin-left: 10px;
            margin-right: 0;
        }

        .message-bubble {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 20px;
            word-wrap: break-word;
            line-height: 1.5;
        }

        .message.bot .message-bubble {
            background: #f0f0f0;
            color: #333;
            border-bottom-left-radius: 5px;
        }

        .message.user .message-bubble {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-bottom-right-radius: 5px;
        }

        .message-time {
            font-size: 0.7em;
            color: #999;
            margin-top: 5px;
            text-align: right;
        }

        /* 打字動畫 */
        .typing {
            display: flex;
            gap: 5px;
            padding: 12px 18px;
        }

        .typing span {
            width: 8px;
            height: 8px;
            background: #999;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }

        .typing span:nth-child(2) {
            animation-delay: 0.2s;
        }

        .typing span:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes typing {
            0%, 60%, 100% {
                transform: translateY(0);
                opacity: 0.4;
            }
            30% {
                transform: translateY(-10px);
                opacity: 1;
            }
        }

        /* 輸入區域 */
        .chat-input-area {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 15px 20px;
            display: flex;
            gap: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .chat-input {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 50px;
            font-size: 1em;
            outline: none;
            transition: all 0.3s;
            font-family: inherit;
        }

        .chat-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .send-btn {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            border-radius: 50%;
            color: white;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .clear-btn {
            background: rgba(255, 107, 107, 0.9);
        }

        .clear-btn:hover {
            background: #ff6b6b;
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }

        /* 快捷按鈕 */
        .quick-replies {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }

        .quick-reply-btn {
            background: rgba(102, 126, 234, 0.1);
            border: 1px solid rgba(102, 126, 234, 0.3);
            padding: 6px 14px;
            border-radius: 50px;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.2s;
            color: #667eea;
        }

        .quick-reply-btn:hover {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }

        /* 響應式設計 */
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .message-bubble {
                max-width: 85%;
            }
            
            .logo-text h1 {
                font-size: 1.2em;
            }
            
            .chat-header {
                padding: 12px 18px;
            }
        }
    </style>
</head>
<body>
    <div class="bg-animation" id="bgAnimation"></div>

    <div class="container">
        <div class="chat-header">
            <div class="logo">
                <div class="logo-icon">🤖</div>
                <div class="logo-text">
                    <h1>AI 聊天機器人</h1>
                    <p>智慧對話助手</p>
                </div>
            </div>
            <div class="status">
                <div class="status-dot"></div>
                <span>在線中</span>
            </div>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-avatar">🤖</div>
                <div class="message-bubble">
                    你好！我是AI聊天機器人 🤗<br>
                    你可以跟我聊天、問問題、講笑話～<br>
                    有什麼想聊的嗎？
                    <div class="message-time">{{ now }}</div>
                </div>
            </div>
        </div>

        <div class="chat-input-area">
            <input type="text" id="messageInput" class="chat-input" placeholder="輸入訊息..." onkeypress="handleKeyPress(event)">
            <button class="send-btn" onclick="sendMessage()">📤</button>
            <button class="send-btn clear-btn" onclick="clearChat()">🗑️</button>
        </div>
        
        <div class="quick-replies">
            <button class="quick-reply-btn" onclick="quickReply('你好')">👋 打招呼</button>
            <button class="quick-reply-btn" onclick="quickReply('講個笑話')">😄 笑話</button>
            <button class="quick-reply-btn" onclick="quickReply('推薦電影')">🎬 推薦電影</button>
            <button class="quick-reply-btn" onclick="quickReply('你好嗎')">💬 問候</button>
            <button class="quick-reply-btn" onclick="quickReply('謝謝')">🙏 感謝</button>
            <button class="quick-reply-btn" onclick="quickReply('再見')">👋 再見</button>
        </div>
    </div>

    <script>
        let isTyping = false;

        // 產生背景圓圈
        function createCircles() {
            const container = document.getElementById('bgAnimation');
            for (let i = 0; i < 30; i++) {
                const circle = document.createElement('div');
                circle.classList.add('circle');
                const size = Math.random() * 100 + 50;
                circle.style.width = size + 'px';
                circle.style.height = size + 'px';
                circle.style.left = Math.random() * 100 + '%';
                circle.style.top = Math.random() * 100 + '%';
                circle.style.animationDelay = Math.random() * 20 + 's';
                circle.style.animationDuration = (Math.random() * 15 + 10) + 's';
                container.appendChild(circle);
            }
        }

        // 顯示打字動畫
        function showTypingIndicator() {
            const messagesDiv = document.getElementById('chatMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot';
            typingDiv.id = 'typingIndicator';
            typingDiv.innerHTML = `
                <div class="message-avatar">🤖</div>
                <div class="message-bubble typing">
                    <span></span><span></span><span></span>
                </div>
            `;
            messagesDiv.appendChild(typingDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            isTyping = true;
        }

        function hideTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) {
                indicator.remove();
            }
            isTyping = false;
        }

        // 發送訊息
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // 顯示使用者訊息
            addMessage(message, 'user');
            input.value = '';
            
            // 顯示打字動畫
            showTypingIndicator();
            
            try {
                const response = await fetch('/webdemo/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                hideTypingIndicator();
                addMessage(data.reply, 'bot');
                
            } catch (error) {
                hideTypingIndicator();
                addMessage('抱歉，發生錯誤了，請稍後再試！', 'bot');
            }
        }

        // 新增訊息到聊天室
        function addMessage(text, sender) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const now = new Date();
            const timeStr = `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}`;
            
            const avatar = sender === 'user' ? '👤' : '🤖';
            
            messageDiv.innerHTML = `
                <div class="message-avatar">${avatar}</div>
                <div class="message-bubble">
                    ${text}
                    <div class="message-time">${timeStr}</div>
                </div>
            `;
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        // 快捷回覆
        function quickReply(text) {
            document.getElementById('messageInput').value = text;
            sendMessage();
        }

        // 清除對話
        function clearChat() {
            const messagesDiv = document.getElementById('chatMessages');
            messagesDiv.innerHTML = `
                <div class="message bot">
                    <div class="message-avatar">🤖</div>
                    <div class="message-bubble">
                        對話已清空！有什麼想聊的嗎？😊
                        <div class="message-time">${new Date().toLocaleTimeString()}</div>
                    </div>
                </div>
            `;
        }

        // 按 Enter 發送
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        createCircles();
    </script>
</body>
</html>
'''

@app.route("/webdemo")
def webdemo():
    """聊天機器人主頁面"""
    return render_template_string(CHAT_TEMPLATE, now=datetime.now().strftime("%H:%M"))

@app.route("/webdemo/api/chat", methods=['POST'])
def chat_api():
    """聊天機器人 API"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'reply': '請輸入訊息內容～'})
        
        # 獲取機器人回覆
        reply = chatbot.get_response(message)
        
        return jsonify({
            'reply': reply,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'reply': '抱歉，處理您的訊息時發生錯誤',
            'status': 'error'
        })

@app.route("/webdemo/api/quick", methods=['GET'])
def quick_replies():
    """取得快捷回覆選項"""
    quick_options = [
        "你好", "講個笑話", "推薦電影", "你好嗎", "謝謝", "再見"
    ]
    return jsonify({'options': quick_options})

@app.route("/")
def index():
    """首頁導向聊天室"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0; url=/webdemo">
        <title>Redirecting...</title>
    </head>
    <body>
        <p>Redirecting to <a href="/webdemo">/webdemo</a>...</p>
    </body>
    </html>
    '''

# 為了 Vercel 部署
app = app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
