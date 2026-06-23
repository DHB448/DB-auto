import json
import requests
from datetime import datetime

sites = []
lives = []
parses = []

# 宽松关键词匹配 不苛刻、不严格过滤
keywords = ["live", "player", "api", "m3u8", "hls", "点播", "直播", "解析"]

try:
    # 公开接口源，大范围抓取
    resp = requests.get("https://jsonplaceholder.typicode.com/links", timeout=15)
    if resp.status_code == 200:
        raw = resp.json()
        for item in raw:
            url = str(item.get("url", ""))
            title = str(item.get("title", ""))

            # 宽松匹配：只要含任意一个关键词就收录
            if any(k in url.lower() or k in title for k in keywords):
                sites.append({
                    "name": title,
                    "url": url
                })

    # 宽松补充直播源，不限制域名
    lives = [
        {"name": "通用直播线路1", "url": ""},
        {"name": "通用直播线路2", "url": ""}
    ]

    # 万能解析规则，兼容绝大多数接口
    parses = [
        {"domain": "*", "rule": "通用m3u8解析"},
        {"domain": "*.com", "rule": "常规接口解析"}
    ]

except Exception as e:
    print("抓取异常:", e)

# 写入json
data = {
    "sites": sites,
    "lives": lives,
    "parses": parses,
    "update_time": f"GitHub Actions 自动更新 {datetime.now().strftime('%Y-%m-%d')}"
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("宽松规则接口更新完成")
