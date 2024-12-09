import os
import json
import random
import time
import urllib.request
import urllib.parse
from datetime import datetime
import getpass

import requests


def fetch_activities(cookie, pageindex):
    url = f"https://my.igpsport.com/Activity/MyActivityList?pageindex={pageindex}"
    req = urllib.request.Request(url)
    req.add_header('Cookie', cookie)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def download_file(url, filename, cookie):
    req = urllib.request.Request(url)
    req.add_header('Cookie', cookie)
    with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
        out_file.write(response.read())


def login_username(username, password):
    # Step 1: Get access token
    url = "https://prod.zh.igpsport.com/service/auth/account/login"
    data = json.dumps({'username': username, 'password': password, 'appId': 'igpsport-web'}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(req) as response:
        response_data = json.loads(response.read().decode())
        if response_data['code'] != 0:
            print(response_data['message'])
            return None
        access_token = response_data['data']['access_token']

    # Step 2: Use access token to get cookie
    token_url = f"https://my.igpsport.com/auth/tokenlogin?token={access_token}"
    headers = {
        'Host': 'my.igpsport.com',
        'Cookie': 'lang=zh',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }
    response = requests.get(token_url, headers=headers, allow_redirects=False)
    return response.headers['Set-Cookie']


def main():
    # Step 1: Choose login method
    login_method = input("请选择登录方式 (1: Cookie, 2: 用户名/密码): ")

    if login_method == '1':
        # Get user input for cookie
        cookie = input("请输入Cookie: ")
    elif login_method == '2':
        # Get user input for username and password
        username = input("请输入用户名:")
        password = getpass.getpass("请输入密码:")  # Use getpass to hide password input
        # Perform login to get cookie
        cookie = login_username(username, password)
        if cookie is None:
            print("用户名或密码错误")
            return
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
    page = 1

    not_break = True

    while not_break:
        data = fetch_activities(cookie, page)
        if not data['item']:
            break

        for item in data['item']:
            ride_id = item['RideId']
            record_time_str = item['StartTimeString']
            record_time = datetime.strptime(record_time_str, "%Y-%m-%d")
            if (start_date is not None) and (end_date is not None):
                if record_time < start_date:
                    not_break = False
                    break
                if record_time > end_date:
                    continue
            download_url = f"https://my.igpsport.com/fit/activity?type=0&rideid={ride_id}"
            filename = f"downloads/{record_time_str}-{ride_id}.fit"
            download_file(download_url, filename, cookie)
            total_downloaded += 1
            time.sleep(random.uniform(4, 6))  # Add random delay between downloads

        page += 1
        time.sleep(random.uniform(0.5, 1))  # Add random delay between pages
    print(f"本次下载的文件数量: {total_downloaded}")


if __name__ == "__main__":
    main()
