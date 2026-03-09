import feedparser
import requests
import time

# --- 配置区 ---
RSSHUB_BASE = "http://103.193.173.151:1200/"
SC_KEY = "SCT317875TktfM2bRrXLSRLDHQhLQFR9ov"

# 定义你想要抓取的“所有”分类
FEEDS = {
    "🛠️ 技术与开发": [
        f"{RSSHUB_BASE}/github/trending/daily/python",
        f"{RSSHUB_BASE}/arxiv/query/cat:cs.RO",
        f"{RSSHUB_BASE}/hackaday/blog",
        f"{RSSHUB_BASE}/v2ex/topics/latest",
    ],
    "📰 实时新闻": [
        f"{RSSHUB_BASE}/solidot/main",
        f"{RSSHUB_BASE}/36kr/newsflashes",
        f"{RSSHUB_BASE}/zaobao/realtime/china",
    ],
    "🎮 游戏资讯": [
        f"{RSSHUB_BASE}/epicgames/freegames",
        f"{RSSHUB_BASE}/steam/special",
        f"{RSSHUB_BASE}/gcores/category/1",
    ],
    "🎬 影视番剧": [
        f"{RSSHUB_BASE}/douban/movie/playing",
        f"{RSSHUB_BASE}/bangumi/calendar/today",
    ],
}


def get_feed_content():
    report = "# 🌍 每日全资讯汇总\n\n"
    for category, urls in FEEDS.items():
        report += f"## {category}\n"
        for url in urls:
            try:
                feed = feedparser.parse(url)
                # 每个源只取最新的 3 条，防止消息太长
                for entry in feed.entries[:3]:
                    report += f"* [{entry.title}]({entry.link})\n"
            except Exception as e:
                print(f"抓取失败: {url}, 错误: {e}")
        report += "\n---\n"
    return report


def send_to_wechat(content):
    url = f"https://sctapi.ftqq.com/{SC_KEY}.send"
    data = {"title": "🤖 你的私人日报已送达", "desp": content}
    requests.post(url, data=data)


if __name__ == "__main__":
    content = get_feed_content()
    send_to_wechat(content)
