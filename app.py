from flask import Flask, request, jsonify
from datetime import datetime
import random
import re

app = Flask(__name__)

# 升級版聊天機器人
class SmartChatBot:
    def __init__(self):
        # 更豐富的回應庫
        self.responses = {
            "你好|嗨|哈囉|hi|hello": [
                "你好呀！今天過得怎麼樣？😊",
                "嗨～很高興見到你！有什麼想聊的嗎？",
                "哈囉！需要我幫忙什麼嗎？",
                "嗨！今天心情如何？"
            ],
            "早安|早上好": [
                "早安！今天也是充滿希望的一天！☀️",
                "早安～吃早餐了嗎？",
                "早上好！祝你今天事事順利！"
            ],
            "晚安|睡覺|睡": [
                "晚安～祝你有個好夢！🌙",
                "早點休息喔，明天見！",
                "晚安！記得要蓋好被子～"
            ],
            "你好嗎|how are you": [
                "我很好！謝謝關心～你呢？",
                "超棒的！因為在跟你聊天啊！😊",
                "很不錯呢！有什麼我可以幫你的嗎？"
            ],
            "名字|你叫什麼": [
                "我是智慧聊天機器人，你可以叫我小智！",
                "我叫ChatBot，是你的AI助手～",
                "你可以叫我小幫手，隨時為你服務！"
            ],
            "謝謝|感謝|3q": [
                "不客氣！能幫到你我很高興！😊",
                "舉手之勞～還有什麼需要嗎？",
                "很高興能為你服務！"
            ],
            "再見|掰掰|bye|88": [
                "再見～期待下次聊天！👋",
                "拜拜！保持聯繫喔！",
                "下次再聊，祝你今天開心！"
            ],
            "天氣|氣象": [
                "我雖然不能查天氣，但我可以推薦天氣相關的電影喔！☀️",
                "要不要看看窗外？比問我更準確😄",
                "建議打開氣象App查詢更準確喔～"
            ],
            "電影|影片": [
                "我超愛電影的！你喜歡看什麼類型？動作、喜劇、愛情還是科幻？🎬",
                "最近《玩命關頭X》、《蜘蛛人》都很好看！",
                "推薦你去看IMDb高分電影，都不會踩雷！"
            ],
            "推薦|介紹|好看": [
                "最近很推《奧本海默》！劇情超精彩！",
                "如果你想看喜劇，推薦《芭比》，輕鬆有趣！",
                "動作片的話，《不可能的任務7》很刺激！"
            ],
            "笑話|搞笑": [
                "為什麼電腦很冷？因為它會開機(窗)！😂",
                "什麼水果最會打電話？芭樂(撥啦)！",
                "魚為什麼那麼聰明？因為牠們都在海裡(海裡=嗨哩)！",
                "蘋果沒出門，為什麼還是黑了？因為它被咬了一口(lightning)！"
            ],
            "喜歡|愛好": [
                "我喜歡和你聊天！學習新東西也很有趣～",
                "我喜歡幫助人，還有看電影！你呢？",
                "我最喜歡跟使用者互動了！"
            ],
            "幫助|功能|能做什麼": [
                "我可以陪你聊天、講笑話、推薦電影、回答問題！",
                "有什麼需要盡管說～問問題、聊天、講笑話都可以！",
                "你可以問我問題，或者單純找我聊天喔！"
            ],
            "幾歲|年齡": [
                "我是AI，永遠18歲！😄",
                "數位世界裡，時間對我來說沒有意義～",
                "我昨天剛出生，但我學得很快！"
            ],
            "厲害|聰明|強": [
                "謝謝誇獎！我還在學習中～",
                "過獎了！有什麼問題儘管問！",
                "你也很厲害呀！"
            ],
            "無聊|好無聊": [
                "那我們來聊天吧！你喜歡什麼？",
                "要我講個笑話給你聽嗎？",
                "要不要我推薦一部好電影給你看？"
            ],
            "心情不好|難過|傷心": [
                "抱一個～希望你能開心起來！🤗",
                "難過的話可以跟我聊聊，我會聽你說～",
                "希望你趕快好起來！需要講笑話給你聽嗎？"
            ],
            "高興|開心": [
                "太棒了！快樂的心情會感染人呢！😊",
                "保持開心喔！",
                "聽到你開心，我也開心！"
            ],
            "吃什麼|美食": [
                "我雖然不用吃東西，但我可以推薦美食電影！",
                "推薦你看《飲食男女》，很經典的美食電影！",
                "《總鋪師》也很讚，看完會很想吃東西～"
            ],
            "音樂|歌曲": [
                "你喜歡聽什麼類型的音樂？",
                "推薦你聽Lofi，讀書工作很適合！",
                "電影原聲帶都很好聽，推薦《星際效應》的配樂！"
            ],
            "遊戲|玩": [
                "你喜歡玩什麼遊戲？",
                "最近《薩爾達傳說》很紅，你玩過嗎？",
                "推薦你玩獨立遊戲，很多都很有創意！"
            ],
            "學習|讀書|考試": [
                "加油！努力一定會有收穫的！💪",
                "休息一下再讀會更有效率喔～",
                "要不要設定番茄鐘？25分鐘讀書，5分鐘休息！"
            ],
            "工作|上班|加班": [
                "辛苦了！記得要適度休息喔～",
                "加油！工作之餘也要照顧自己！",
                "需要我講笑話讓你放鬆一下嗎？"
            ]
        }
        
        # 更自然的默認回應
        self.default_responses = [
            "嗯～讓我想想...你說的是什麼意思呢？",
            "原來如此！可以再多說一些嗎？",
            "這個話題很有趣，我很想聽你多說說！",
            "我還在學習中，你能教我怎麼回答會更好嗎？",
            "哇～這個問題很有意思！",
            "繼續說，我有在認真聽喔！"
        ]
        
        # 跟進問題回應
        self.follow_up_responses = [
            "然後呢？",
            "真的嗎？",
            "哇！然後呢然後呢？",
            "我也這麼覺得！",
            "說得對！"
        ]
    
    def get_response(self, message):
        message = message.strip()
        
        # 特別處理：純表情符號
        emojis_only = re.match(r'^[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+$', message)
        if emojis_only:
            return random.choice(["😊", "👍", "🤗", "😄", "❤️"])
        
        # 特別處理：很短的訊息（表示想聊天）
        if len(message) <= 3:
            return random.choice(self.follow_up_responses)
        
        # 問句處理
        is_question = "?" in message or "？" in message or "嗎" in message
        
        # 關鍵字匹配（使用正則表達式）
        for pattern, responses in self.responses.items():
            if re.search(pattern, message, re.IGNORECASE):
                return random.choice(responses)
        
        # 問句但沒匹配到關鍵字
        if is_question:
            return random.choice([
                "好問題！讓我想想...",
                "這個問題很有趣，但我還不太確定答案耶😅",
                "你能再說詳細一點嗎？",
                "我還在學習中，也許你可以問我其他問題！"
            ])
        
        # 長句子處理
        if len(message) > 20:
            return random.choice([
                "哇～你說了很多，讓我想想怎麼回你...",
                "嗯嗯，我有在聽！還有嗎？",
                f"你說的「{message[:30]}...」這個話題很有意思！"
            ])
        
        # 默認回應
        return random.choice(self.default_responses)

chatbot = SmartChatBot()

# 首頁 HTML
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 智慧聊天機器人</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Microsoft JhengHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
        }
        .bg-animation { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; }
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
            text-align: center;
            padding: 40px;
            animation: fadeInUp 0.8s ease;
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .logo {
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 30px;
            animation: pulse 2s infinite;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        .logo span { font-size: 60px; }
        h1 {
            font-size: 3em;
            color: white;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .subtitle {
            font-size: 1.2em;
            color: rgba(255,255,255,0.9);
            margin-bottom: 40px;
        }
        .features {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-bottom: 50px;
        }
        .feature-card {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 20px;
            width: 200px;
            transition: all 0.3s;
        }
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        .feature-icon { font-size: 48px; margin-bottom: 15px; }
        .feature-title {
            font-size: 1.1em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 8px;
        }
        .feature-desc { font-size: 0.85em; color: #666; }
        .btn {
            display: inline-block;
            background: white;
            color: #667eea;
            text-decoration: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 1.2em;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.3);
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        .footer {
            margin-top: 60px;
            color: rgba(255,255,255,0.7);
            font-size: 0.85em;
        }
        @media (max-width: 768px) {
            h1 { font-size: 2em; }
            .feature-card { width: 160px; padding: 20px; }
            .container { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="bg-animation" id="bgAnimation"></div>
    <div class="container">
        <div class="logo"><span>🧠</span></div>
        <h1>AI 智慧聊天機器人</h1>
        <div class="subtitle">更聰明、更自然、更懂你</div>
        <div class="features">
            <div class="feature-card"><div class="feature-icon">💬</div><div class="feature-title">自然對話</div><div class="feature-desc">更像真人的對話體驗</div></div>
            <div class="feature-card"><div class="feature-icon">🎯</div><div class="feature-title">智慧回應</div><div class="feature-desc">理解你的意圖</div></div>
            <div class="feature-card"><div class="feature-icon">🎬</div><div class="feature-title">電影推薦</div><div class="feature-desc">專業電影建議</div></div>
            <div class="feature-card"><div class="feature-icon">❤️</div><div class="feature-title">情感支持</div><div class="feature-desc">陪你聊心事</div></div>
        </div>
        <a href="/webdemo" class="btn">開始聊天 →</a>
        <div class="footer"><p>Powered by AI | 智慧對話系統</p></div>
    </div>
    <script>
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
        createCircles();
    </script>
</body>
</html>
'''

# 聊天室 HTML（升級版）
WEBDEMO_HTML = '''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>AI 智慧聊天機器人</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Microsoft JhengHei', 'PingFang TC', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            overflow: hidden;
            position: relative;
        }
        .bg-animation { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; }
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
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
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
        .logo-text p { font-size: 0.8em; color: #666; }
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
        .status span { font-size: 0.85em; color: #2e7d32; }
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
        .chat-messages::-webkit-scrollbar { width: 6px; }
        .chat-messages::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
        .chat-messages::-webkit-scrollbar-thumb { background: #667eea; border-radius: 10px; }
        .message {
            display: flex;
            margin-bottom: 20px;
            animation: messageFadeIn 0.3s ease;
        }
        @keyframes messageFadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message.user { justify-content: flex-end; }
        .message.bot { justify-content: flex-start; }
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
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
            30% { transform: translateY(-10px); opacity: 1; }
        }
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
        .clear-btn { background: rgba(255, 107, 107, 0.9); }
        .clear-btn:hover { background: #ff6b6b; box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4); }
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
        @media (max-width: 768px) {
            .container { padding: 10px; }
            .message-bubble { max-width: 85%; }
            .logo-text h1 { font-size: 1.2em; }
            .chat-header { padding: 12px 18px; }
        }
    </style>
</head>
<body>
    <div class="bg-animation" id="bgAnimation"></div>
    <div class="container">
        <div class="chat-header">
            <div class="logo" onclick="location.href='/'">
                <div class="logo-icon">🧠</div>
                <div class="logo-text">
                    <h1>AI 智慧聊天</h1>
                    <p>更聰明更自然</p>
                </div>
            </div>
            <div class="status">
                <div class="status-dot"></div>
                <span>智慧在線</span>
            </div>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-avatar">🧠</div>
                <div class="message-bubble">
                    嗨！我是升級版AI 🤗<br>
                    我比以前更聰明了！<br>
                    可以跟我聊心事、問問題、講笑話～<br>
                    來試試看吧！
                    <div class="message-time" id="initTime"></div>
                </div>
            </div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="messageInput" class="chat-input" placeholder="試試問我：推薦電影、講笑話、心情不好..." onkeypress="handleKeyPress(event)">
            <button class="send-btn" onclick="sendMessage()">📤</button>
            <button class="send-btn clear-btn" onclick="clearChat()">🗑️</button>
        </div>
        <div class="quick-replies">
            <button class="quick-reply-btn" onclick="quickReply('你好')">👋 打招呼</button>
            <button class="quick-reply-btn" onclick="quickReply('講個笑話')">😄 笑話</button>
            <button class="quick-reply-btn" onclick="quickReply('推薦電影')">🎬 推薦電影</button>
            <button class="quick-reply-btn" onclick="quickReply('心情不好')">💔 求安慰</button>
            <button class="quick-reply-btn" onclick="quickReply('我好無聊')">😫 好無聊</button>
            <button class="quick-reply-btn" onclick="quickReply('你好聰明')">⭐ 誇獎</button>
        </div>
    </div>
    <script>
        const now = new Date();
        const timeStr = `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}`;
        document.getElementById('initTime').textContent = timeStr;
        let isTyping = false;
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
        function showTypingIndicator() {
            const messagesDiv = document.getElementById('chatMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot';
            typingDiv.id = 'typingIndicator';
            typingDiv.innerHTML = `<div class="message-avatar">🧠</div><div class="message-bubble typing"><span></span><span></span><span></span></div>`;
            messagesDiv.appendChild(typingDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            isTyping = true;
        }
        function hideTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) { indicator.remove(); }
            isTyping = false;
        }
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            addMessage(message, 'user');
            input.value = '';
            showTypingIndicator();
            try {
                const response = await fetch('/webdemo/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
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
        function addMessage(text, sender) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            const now = new Date();
            const timeStr = `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}`;
            const avatar = sender === 'user' ? '👤' : '🧠';
            messageDiv.innerHTML = `<div class="message-avatar">${avatar}</div><div class="message-bubble">${escapeHtml(text)}<div class="message-time">${timeStr}</div></div>`;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        function quickReply(text) {
            document.getElementById('messageInput').value = text;
            sendMessage();
        }
        function clearChat() {
            const messagesDiv = document.getElementById('chatMessages');
            const now = new Date();
            const timeStr = `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}`;
            messagesDiv.innerHTML = `<div class="message bot"><div class="message-avatar">🧠</div><div class="message-bubble">對話已清空！有什麼想聊的嗎？😊<div class="message-time">${timeStr}</div></div></div>`;
        }
        function handleKeyPress(event) {
            if (event.key === 'Enter') { sendMessage(); }
        }
        createCircles();
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return INDEX_HTML

@app.route("/webdemo")
def webdemo():
    return WEBDEMO_HTML

@app.route("/webdemo/api/chat", methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        message = data.get('message', '')
        if not message:
            return jsonify({'reply': '請輸入訊息內容～'})
        reply = chatbot.get_response(message)
        return jsonify({'reply': reply, 'status': 'success'})
    except Exception as e:
        return jsonify({'reply': '抱歉，處理您的訊息時發生錯誤', 'status': 'error'})

app = app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
