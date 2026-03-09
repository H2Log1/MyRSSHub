import feedparser
import requests
import os
import datetime

# --- 配置区 ---
# 从 GitHub Secrets 读取 Key
SC_KEY = os.environ.get("SC_KEY")
# 替换为你服务器的公网 IP
SERVER_IP = "103.193.173.151"
RSSHUB_URL = f"http://{SERVER_IP}:1200"

FEEDS = {
    "🛠️ 技术论坛": [
        ["V2EX最新", "/v2ex/topics/latest"],
        ["GitHub Python趋势", "/github/trending/daily/python"],
        ["GitHub C++趋势", "/github/trending/daily/c++"],
        ["arXiv机器人学", "/arxiv/query/cat:cs.RO"],
        ["IEEE Spectrum机器人学", "/ieee/spectrum/topic/robotics"],
        ["深度学习", "/arxiv/query/cat:cs.LG"],
    ],
    "🎮 游戏/白嫖": [
        ["Epic免费游戏", "/epicgames/freegames"],
        ["Steam每日特惠", "/steam/special"],
        ["机核网资讯", "/gcores/category/1"],
    ],
    "📰 实时新闻": [
        ["36Kr快讯", "/36kr/newsflashes"],
        ["联合早报", "/zaobao/realtime/china"],
    ],
}


def fetch_news():
    today = datetime.date.today().strftime("%Y-%m-%d")
    content = f"# 🤖 每日全资讯汇总 ({today})\n\n"

    for cat, items in FEEDS.items():
        content += f"## {cat}\n"
        for name, path in items:
            url = f"{RSSHUB_URL}{path}"
            try:
                # 延长超时时间，防止服务器响应慢
                feed = feedparser.parse(url)
                if not feed.entries:
                    continue
                content += f"**【{name}】**\n"
                for entry in feed.entries[:3]:
                    content += f"* [{entry.title}]({entry.link})\n"
            except Exception as e:
                print(f"抓取 {name} 失败: {e}")
        content += "\n---\n"
    return content


def push(text):
    if not SC_KEY:
        print("错误：未找到 SC_KEY")
        return
    url = f"https://sctapi.ftqq.com/{SC_KEY}.send"
    requests.post(url, data={"title": "☕ 你的私人报刊已送达", "desp": text})


if __name__ == "__main__":
    push(fetch_news())
