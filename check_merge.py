import httpx
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCE_FILE = "sources.txt"
OUTPUT_JSON = "tvbox.json"
TIMEOUT = 6
MAX_WORKERS = 15
valid_sites = []

# 读取上游源
with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    source_urls = [line.strip() for line in f if line.strip()]

def fetch_single_source(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        resp = httpx.get(url, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        return data.get("sites", [])
    except Exception:
        return []

def test_site_api(site):
    name = site.get("name", "")
    api = site.get("api", "")
    if not api:
        return None
    try:
        httpx.head(api, timeout=TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
        return site
    except Exception:
        return None

# 拉取全部源
all_raw_sites = []
with ThreadPoolExecutor(max_workers=5) as executor:
    tasks = [executor.submit(fetch_single_source, u) for u in source_urls]
    for task in as_completed(tasks):
        all_raw_sites.extend(task.result())

# 过滤失效站点
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    tasks = [executor.submit(test_site_api, s) for s in all_raw_sites]
    for task in as_completed(tasks):
        res = task.result()
        if res and res not in valid_sites:
            valid_sites.append(res)

# 输出标准配置
final_config = {
    "sites": valid_sites,
    "lives": [],
    "parses": [],
    "update_time": "GitHub Actions 每周一自动更新"
}
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(final_config, f, ensure_ascii=False, indent=2)

print(f"有效站点数量：{len(valid_sites)}")
