import requests
import schedule
import threading

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

def lineNotify_task():
    while True:
        schedule.run_pending()
        
if __name__ == '__main__':
    schedule.every().day.at("12:54").do(send_line_notify, "txQg266RVtbnMbUnwrx3KsWs7ZwoU22uKXGw49BXvBL", '中午了，吃飯啦，到這裡抽籤吧~~\nhttps://140.136.146.81/')
    lineNotify_thread = threading.Thread(target=lineNotify_task);
    lineNotify_thread.start()
    send_line_notify("txQg266RVtbnMbUnwrx3KsWs7ZwoU22uKXGw49BXvBL", "~")

