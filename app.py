from flask import Flask, request, render_template, jsonify
from datetime import datetime
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
            "幾歲": ["我是AI，永遠18歲！😄", "數位世界裡，時間沒有意義～", "我昨天剛出生，但已經學會很多了！"],
            "做什麼": ["我在陪你聊天啊！", "我的工作就是回答你的問題～", "學習新知識和幫助別人！"],
            "厲害": ["謝謝誇獎！我會繼續努力的！", "還好啦～還在學習中！", "你也很厲害呀！"]
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

@app.route("/")
def index():
    """首頁"""
    return render_template("index.html")

@app.route("/webdemo")
def webdemo():
    """聊天機器人主頁面"""
    return render_template("webdemo.html")

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

# 為了 Vercel 部署
app = app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
