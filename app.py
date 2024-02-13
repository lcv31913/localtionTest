from flask import Flask, render_template, request, jsonify
import requests
import threading
import schedule

app = Flask(__name__)

def send_line_notify(token, message):
    """
    发送 Line Notify 通知
    
    Args:
        token (str): 您的 Line Notify 令牌
        message (str): 要发送的消息内容
        
    Returns:
        bool: 发送是否成功
    """
    # Line Notify API 的 URL
    line_notify_api = 'https://notify-api.line.me/api/notify'

    # 请求头，包括令牌
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # 要发送的数据
    data = {
        'message': message
    }

    try:
        # 发送 POST 请求
        response = requests.post(line_notify_api, headers=headers, data=data)
        
        # 检查响应状态码
        if response.status_code == 200:
            print('Line Notify 通知发送成功')
            return True
        else:
            print('Line Notify 通知发送失败')
            return False
    except Exception as e:
        print(f'发送 Line Notify 通知时出错: {str(e)}')
        return False
    
def getRestaurants(BASE_URL, params):
    # 發送API請求並獲取餐廳資訊
    response = requests.get(BASE_URL, params=params)
    result = response.json()

    # 提取餐廳資訊
    restaurants = []
    for place in result.get('results', []):
        restaurant_info = {
            'name': place['name'],
            'address': place['vicinity'],
            'rating': place.get('rating', 'N/A')
        }        
        restaurants.append(restaurant_info)
    return jsonify(restaurants)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_location', methods=['POST'])
def get_location():
    if 'geolocation' in request.json:
        location = request.json['geolocation']
        latitude = location['latitude']
        longitude = location['longitude']

        api_key = 'AIzaSyDD-2lyfwWMqvCD3OKz4Kl6w_3HMlm6ftc'                
        base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        radius = 1000  # 搜索半徑，以米為單位
        selectType = 'restaurant'  # 餐廳類型
        location = str(latitude) + ',' + str(longitude)# 用戶的經緯度坐標，例如：37.7749,-122.4194

        params = {
            'location': location,
            'radius': radius,
            'type': selectType,
            'key': api_key,
            'language': 'zh-TW'
        }
        
        return getRestaurants(base_url, params)
    else:
        return jsonify({'error': '無法獲取位置信息, 只能慢慢想了~'})
    

def lineNotify_task():
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    #because of cloud server make time need sub 8HR.
    schedule.every().day.at("01:30").do(send_line_notify, "txQg266RVtbnMbUnwrx3KsWs7ZwoU22uKXGw49BXvBL", '起床了!吃飯啦，到這裡抽籤吧~~\nhttps://linenotify-400101.de.r.appspot.com')
    schedule.every().day.at("04:30").do(send_line_notify, "txQg266RVtbnMbUnwrx3KsWs7ZwoU22uKXGw49BXvBL", '中午了，吃飯啦，到這裡抽籤吧~~\nhttps://linenotify-400101.de.r.appspot.com')
    schedule.every().day.at("10:30").do(send_line_notify, "txQg266RVtbnMbUnwrx3KsWs7ZwoU22uKXGw49BXvBL", '晚上了，吃飯啦，到這裡抽籤吧~~\nhttps://linenotify-400101.de.r.appspot.com')
    
    send_line_notify("txQg266RVtbnMbUnwrx3KsWs7ZwoU22uKXGw49BXvBL", '~~~~')
    flask_thread = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8080})
    lineNotify_thread = threading.Thread(target=lineNotify_task);
    
    flask_thread.start()
    lineNotify_thread.start()
