from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    questions_answers = {
        "apple": "蘋果",
        "banana": "香蕉",
        "cat": "貓",
        "dog": "狗",
        "elephant": "大象",
        "flower": "花",
        "guitar": "吉他",
        "house": "房子",
        "ice": "冰",
        "tiger": "虎",
        "jacket": "夾克",
        "keyboard": "鍵盤",
        "lemon": "檸檬",
        "monkey": "猴子",
        "notebook": "筆記本",
        "orange": "橙子",
        "piano": "鋼琴",
        "queen": "女王",
        "rabbit": "兔子",
        "sun": "太陽",
        "tree": "樹",
        "umbrella": "雨傘",
        "violin": "小提琴",
        "whale": "鯨魚",
        "xylophone": "木琴",
        "yacht": "遊艇",
        "zebra": "斑馬",
        "bread": "麵包",
        "car": "車",
        "duck": "鴨子",
        "book": "書",
        "chair": "椅子",
        "desk": "書桌",
        "egg": "蛋",
        "fan": "電風扇",
        "glasses": "眼鏡",
        "hat": "帽子",
        "ink": "墨水",
        "jewel": "珠寶",
        "kite": "風箏",
        "lamp": "燈",
        "mirror": "鏡子",
        "nail": "釘子",
        "ocean": "海洋",
        "pen": "筆",
        "quilt": "被子",
        "ring": "戒指",
        "sand": "沙",
        "telephone": "電話",
        "vase": "花瓶",
        "window": "窗戶",
        "zoo": "動物園",
        "ball": "球",
        "camera": "相機",
        "drum": "鼓",
        "envelope": "信封",
        "flag": "旗子",
        "glove": "手套",
        "hammer": "錘子",
        "island": "島嶼",
        "jar": "罐子",
        "key": "鑰匙",
        "ladder": "梯子",
        "mountain": "山",
        "newspaper": "報紙",
        "oven": "烤箱",
        "pizza": "披薩",
        "quill": "羽毛筆",
        "rocket": "火箭",
        "sock": "襪子",
        "train": "火車",
        "vulture": "禿鷲",
        "wallet": "錢包",
        "x-ray": "X光",
        "yogurt": "優格",
        "zipper": "拉鍊",
        "milk": "牛奶",
        "tea": "茶",
        "coffee": "咖啡",
        "sugar": "糖",
        "salt": "鹽",
        "pepper": "胡椒",
        "butter": "奶油",
        "cheese": "起司",
        "grape": "葡萄",
        "peach": "水蜜桃",
        "cherry": "櫻桃",
        "strawberry": "草莓",
        "watermelon": "西瓜",
        "pineapple": "鳳梨",
        "mango": "芒果",
        "kiwi": "奇異果",
        "coconut": "椰子",
        "broccoli": "花椰菜",
        "carrot": "胡蘿蔔",
        "tomato": "番茄",
        "potato": "馬鈴薯",
        "onion": "洋蔥",
        "pepper (vegetable)": "辣椒",
        "lettuce": "生菜",
        "cabbage": "高麗菜",
        "corn": "玉米",
        "rice": "米",
        "noodles": "麵",
        "soup": "湯",
        "meat": "肉",
        "fish": "魚",
        "shrimp": "蝦",
        "crab": "螃蟹",
        "eggplant": "茄子",
        "mushroom": "香菇",
        "bicycle": "腳踏車",
        "motorcycle": "摩托車",
        "bus": "公車",
        "train station": "車站",
        "airport": "機場",
        "road": "道路",
        "bridge": "橋",
        "tunnel": "隧道",
        "traffic light": "紅綠燈",
        "crosswalk": "斑馬線",
        "helmet": "安全帽",
        "seatbelt": "安全帶",
        "steering wheel": "方向盤",
        "gasoline": "汽油",
        "engine": "引擎",
        "wheel": "輪子",
        "brake": "煞車",
        "你最近感覺怎麼樣？": "我有點疲憊但還好。",
        "你今天心情好嗎？": "還可以，有點壓力。",
        "你喜歡現在的工作嗎？": "還算可以，但有改善空間。",
        "你有常運動嗎？": "最近比較少。",
        "你最近有什麼煩惱？": "主要是生活壓力和未來的不確定。",
        "你會感到孤單嗎？": "有時候會。",
        "你喜歡一個人還是與人相處？": "看情況，有時候喜歡安靜。",
        "你希望改變些什麼？": "希望能變得更有自律。",
        "你最近有開心的事嗎？": "朋友來找我聊天讓我很開心。",
        "你如何放鬆自己？": "聽音樂和看書。",
        "你是否容易感到焦慮？": "是的，尤其是遇到新挑戰時。",
        "你有與人傾訴的對象嗎？": "有幾位好朋友可以聊聊。",
        "你多久與家人聯絡一次？": "每週至少一次。",
        "你對未來有計畫嗎？": "正在規劃下一步。",
        "你曾經有過什麼成就讓你驕傲？": "自己一個人完成了一個大型專案。",
        "你有什麼興趣？": "畫畫、寫作和戶外活動。",
        "你想對自己說些什麼？": "不要放棄，慢慢來。",
        "你對生活滿意嗎？": "有些地方需要努力改進。",
        "你希望成為什麼樣的人？": "更有耐心、更正向的人。",
        "你曾經因為什麼感到感激？": "家人對我的支持。",
        "你害怕什麼？": "失敗和被拒絕。",
        "你常常懷疑自己嗎？": "有時候會。",
        "你是否會逃避壓力？": "有時會拖延。",
        "你試過寫日記嗎？": "有時會寫下心情。",
        "你覺得自己夠努力嗎？": "還可以，但可以更好。",
        "你曾經覺得無助嗎？": "是的，尤其是在壓力大時。",
        "你認為快樂是什麼？": "內心平靜和與人連結。",
        "你想學習什麼新技能？": "彈吉他或煮菜。",
        "你對朋友有信任感嗎？": "大多數朋友可以信任。",
        "你有明確的生活目標嗎？": "目前還在探索中。"
    }

    if msg in questions_answers:
        #print(f"{english_word} 的中文翻譯是：{words_dict[english_word]}")
    
        line_bot_api.reply_message(event.reply_token, TextSendMessage(questions_answers[msg]))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))
       
         

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
