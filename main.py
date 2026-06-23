import json
import requests
from datetime import datetime

# ====================== 爬虫逻辑区 ======================
sites = []
lives = []
parses = []

# 示例：抓取公开测试接口数据，你可以替换成自己目标网址
try:
    resp = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10)
    if resp.status_code == 200:
        raw_data = resp.json()
        # 截取部分数据填入 sites
        for item in raw_data[:3]:
            sites.append({
                "id": item["id"],
                "title": item["title"]
            })
except Exception as e:
    print(f"抓取失败：{e}")

# 模拟 lives、parses 数据，可自行替换爬虫逻辑
lives = [{"name": "测试直播1", "url": "https://xxx.com/live1"}]
parses = [{"domain": "demo.com", "rule": "regex_parse"}]
# ======================================================

# 组装最终JSON结构
output_data = {
    "sites": sites,
    "lives": lives,
    "parses": parses,
    "update_time": "GitHub Actions 每周一自动更新"
}

# 写入 data.json，格式化、中文不乱码
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("data.json 生成完成")
