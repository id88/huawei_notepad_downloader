import json
import requests
import time
import random
import os
from datetime import datetime

def generate_trace_id():
    # 这里需要根据情况修改
    unknown_number = "01234_02"
    timestamp = str(int(time.time()))
    random_value = str(random.randint(10000000, 99999999))
    return f"{unknown_number}_{timestamp}_{random_value}"

def fetch_note_data(guid):
    url = "https://cloud.huawei.com/notepad/note/query"

    # 从浏览器中复制请求头
    headers = {'Accept': 'application/json, text/plain, */*'}

    payload = {
        "ctagNoteInfo": "",
        "startCursor": "66821", # 这里需要根据情况修改
        "guid": guid,
        "kind": "note",
        "traceId": generate_trace_id()
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            # print(json.dumps(response.json(), indent=4, ensure_ascii=False))
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}, 响应内容: {response.text}")
            return None
    except requests.RequestException as e:
        print(f"请求发生异常: {e}")
        return None

def parse_and_save_note_data(data):
    content_data = json.loads(data['rspInfo']['data'])['content']
    # print(json.dumps(content_data, indent=4, ensure_ascii=False))

    # 提取文件名
    data1 = ""
    try:
        data5 = json.loads(content_data.get("data5", "{}"))
        data1 = data5.get("data1", "")
    except json.JSONDecodeError:
        pass

    modified_timestamp = content_data.get("modified", 0)
    created_timestamp = content_data.get("created", 0)

    if data1:
        # print('data1:', data1)
        file_name = f"{data1}.txt"
    elif modified_timestamp:
        # print('modified_timestamp:', modified_timestamp)
        modified_date = datetime.fromtimestamp(modified_timestamp / 1000).strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{modified_date}.txt"
    else:
        # print('created_timestamp:', created_timestamp)
        created_date = datetime.fromtimestamp(created_timestamp / 1000).strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{created_date}.txt"

    # 提取内容
    raw_content = content_data['content']
    content = raw_content.split("Text|")[-1]

    # 确保保存目录存在
    save_dir = "notepad"
    os.makedirs(save_dir, exist_ok=True)

    # 保存文件
    file_path = os.path.join(save_dir, file_name)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"已保存文件: {file_path}")
    except OSError:
        timestamp_fallback = str(int(time.time()))
        fallback_file_name = f"{timestamp_fallback}.txt"
        fallback_file_path = os.path.join(save_dir, fallback_file_name)
        with open(fallback_file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"文件名非法，已使用时间戳保存文件: {fallback_file_path}")

def load_guids(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
        return []

if __name__ == "__main__":
    # response_data = fetch_note_data('FswZgvxxxxxxxxxxxxxaw')
    # # print(json.dumps(response_data, indent=4, ensure_ascii=False))
    # if response_data:
    #     parse_and_save_note_data(response_data)

    guids = load_guids("guids.txt")

    for guid in guids:
        print(f"正在处理 GUID: {guid}")
        response_data = fetch_note_data(guid)
        if response_data:
            parse_and_save_note_data(response_data)