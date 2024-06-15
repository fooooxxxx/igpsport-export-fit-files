import os
import json
import urllib.request
import urllib.parse
from datetime import datetime


def fetch_activities(cookie, pageindex):
    url = f"https://my.igpsport.com/Activity/MyActivityList?pageindex={pageindex}"
    req = urllib.request.Request(url)
    req.add_header('Cookie', cookie)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def download_file(url, filename):
    urllib.request.urlretrieve(url, filename)


def login(username, password):
    url = "https://my.igpsport.com/Auth/Login"
    data = urllib.parse.urlencode({'username': username, 'password': password}).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req) as response:
        return response.headers['Set-Cookie']


def main():
    # Step 1: Choose login method
    login_method = input("请选择登录方式 (1: Cookie, 2: 用户名/密码): ")

    if login_method == '1':
        # Get user input for cookie
        cookie = input("请输入Cookie: ")
    elif login_method == '2':
        # Get user input for username and password
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        # Perform login to get cookie
        cookie = login(username, password)
    else:
        print("无效的选择")
        return

    # Step 2: Get user input for date range
    date_range = input("请输入时间范围 (格式如: 2023-01-01~2024-01-01，留空表示全部下载): ")
    start_date = None
    end_date = None
    if date_range:
        start_date_str, end_date_str = date_range.split("~")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Create directory for downloads
    os.makedirs("downloads", exist_ok=True)

    total_downloaded = 0
    pageindex = 1

    while True:
        data = fetch_activities(cookie, pageindex)
        if not data['item']:
            break

        for item in data['item']:
            ride_id = item['RideId']
            start_time_str = item['StartTimeString']
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d")

            if (start_date is None or start_date <= start_time) and (end_date is None or start_time <= end_date):
                download_url = f"https://my.igpsport.com/fit/activity?type=0&rideid={ride_id}"
                filename = f"downloads/{start_time_str}-{ride_id}.fit"
                download_file(download_url, filename)
                total_downloaded += 1

        pageindex += 1

    print(f"本次下载的文件数量: {total_downloaded}")


if __name__ == "__main__":
    main()
