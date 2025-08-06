import os
import json
import random
import time
import urllib.request
import urllib.parse
from datetime import datetime
import getpass

import requests


def fetch_activities(token, pageindex, start_date=None, end_date=None):
    params = {
        'pageNo': pageindex,
        # 即使修改该值,返回的结果仍然是 20 条
        'pageSize': 20,
        'reqType': 0,
        'sort': 1
    }
    if start_date and end_date:
        params['beginTime'] = start_date.strftime("%Y-%m-%d")
        params['endTime'] = end_date.strftime("%Y-%m-%d")
    query_string = urllib.parse.urlencode(params)
    url = f"https://prod.zh.igpsport.com/service/web-gateway/web-analyze/activity/queryMyActivity?{query_string}"
    req = urllib.request.Request(url)
    req.add_header('Authorization', "Bearer " + token)
    with urllib.request.urlopen(req) as response:
        resp_json = json.loads(response.read().decode())
        if resp_json['code'] != 0:
            print(f"错误: 获取活动记录失败 {resp_json['message']}")
            return {'rows': []}
        # 直接返回分页数据
        return resp_json['data']


def download_file(url, filename, token):
    req = urllib.request.Request(url)
    req.add_header('Authorization', "Bearer " + token)
    with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
        out_file.write(response.read())


def login_username(username, password):
    # Get access token
    url = "https://prod.zh.igpsport.com/service/auth/account/login"
    data = json.dumps({'username': username, 'password': password, 'appId': 'igpsport-web'}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(req) as response:
        response_data = json.loads(response.read().decode())
        if response_data['code'] != 0:
            print(response_data['message'])
            return None
        access_token = response_data['data']['access_token']
    return access_token


def main():
    # Step 1: Choose a login method
    login_method = input("请选择登录方式 (1: token, 2: 用户名/密码): ")

    if login_method == '1':
        token = input("请输入token: ")
        token = token.strip()
    elif login_method == '2':
        # Get user input for username and password
        username = input("请输入用户名:")
        password = getpass.getpass("请输入密码:")  # Use getpass to hide password input
        if not username or not password:
            print("用户名和密码不能为空")
            return None
        # Perform login to get cookie
        token = login_username(username, password)
        if token is None:
            print("用户名或密码错误")
            return None
    else:
        print("无效的选择")
        return None

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
    # 用于去重
    downloaded_ride_ids = set()

    while True:
        data = fetch_activities(token, page, start_date, end_date)
        rows = data.get('rows', [])
        if not rows:
            break

        for item in rows:
            ride_id = item['rideId']
            if ride_id in downloaded_ride_ids:
                continue  # 已下载过，跳过
            start_time_str = item['startTime']  # 格式如"2023.05.27"
            # 统一文件名格式
            filename = f"downloads/{start_time_str.replace('.', '-')}-{ride_id}.fit"
            fit_url = item.get('fitOssPath')
            if not fit_url:
                continue
            download_file(fit_url, filename, token)
            downloaded_ride_ids.add(ride_id)  # 下载后加入集合
            total_downloaded += 1
            time.sleep(random.uniform(0.1, 0.2))  # Add random delay between downloads

        # 分页判断
        if page >= data.get('totalPage', 1):
            break
        page += 1
        time.sleep(random.uniform(0.1, 0.2))  # Add random delay between pages
    print(f"本次下载的文件数量: {total_downloaded}")


if __name__ == "__main__":
    main()
