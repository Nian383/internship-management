import requests

def test_homepage():
    url="http://127.0.0.1:8000/"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            print(f"✅ 首页访问成功！状态码："[response.status_code])
        else:
            print (f"❌ 首页访问失败!状态码："[response.status_code])
    except Exception as e:
        print("❌ 请求出错：",e)
if __name__ == '__main__':
    test_homepage()
