import json
import requests
from datetime import datetime

sites = []
lives = []
parses = []
url_set = set()  # 去重专用

# 超宽松关键词，不漏任何直播/解析接口
keywords = ["live", "player", "api", "m3u8", "hls", "vod", "点播", "直播", "解析"]

try:
    resp = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=15)
    if resp.status_code == 200:
        raw = resp.json()
        for item in raw:
            url = str(item.get("url", ""))
            title = str(item.get("title", ""))

            # 宽松模糊匹配
            if any(k in url.lower() or k in title for k in keywords):
                # 链接不重复才加入
                if url not in url_set:
                    url_set.add(url)
                    sites.append({"name": title, "url": url})

    # 通用直播线路
    lives = [
        {"name": "高清直播线路", "url": ""},
        {"name": "备用直播线路", "url": ""}
    ]

    # 全网通用宽松解析规则（不限域名）
    parses = [
        {"domain": "*", "rule": "m3u8通用解析"},
        {"domain": "*.cn", "rule": "国内线路解析"},
        {"domain": "*.com", "rule": "海外接口解析"}
    ]

except Exception as e:
    print("抓取出错：", e)

# 自动更新当天日期
data = {
    "sites": sites,
    "lives": lives,
    "parses": parses,
    "update_time": f"GitHub Actions 每周自动更新 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 宽松抓取+去重完成，无重复接口")
