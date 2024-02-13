import requests

def get_lat_lng_from_address(address, api_key):
    """
    將地址轉換為經緯度坐標。

    Args:
        address (str): 要轉換的地址。
        api_key (str): 您的Google Geocoding API金鑰。

    Returns:
        tuple: 包含經度和緯度的元組 (latitude, longitude)。
        如果無法找到地址的經緯度坐標，則返回 (None, None)。
    """
    # Google Geocoding API 相關設定
    GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

    # 構建Geocoding API請求
    params = {
        'address': address,
        'key': api_key
    }

    # 發送API請求以獲取經緯度坐標
    response = requests.get(GEOCODE_URL, params=params)
    result = response.json()

    print(result)
    # 提取經緯度坐標
    if result['status'] == 'OK':
        location = result['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        return None, None


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

    # 餐廳資訊
    for restaurant in restaurants:
        print(f'餐廳名稱: {restaurant["name"]}')
        print(f'地址: {restaurant["address"]}')
        print(f'評分: {restaurant["rating"]}')
        print('-' * 30)

    
# 使用範例
if __name__ == "__main__":
    api_key = 'AIzaSyDD-2lyfwWMqvCD3OKz4Kl6w_3HMlm6ftc'
    address = '天主教輔仁大學'
    
    base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    radius = 1000  # 搜索半徑，以米為單位
    selectType = 'restaurant'  # 餐廳類型

    latitude, longitude = get_lat_lng_from_address(address, api_key)
    location = str(latitude) + ',' + str(longitude)# 用戶的經緯度坐標，例如：37.7749,-122.4194


    params = {
        'location': location,
        'radius': radius,
        'type': selectType,
        'key': api_key
    }
    getRestaurants(BASE_URL, params)
    
        
