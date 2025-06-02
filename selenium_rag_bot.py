from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests

# === 設定 Chrome Driver ===
CHROMEDRIVER_PATH = r"C:\PYTHONC\chromedriver-win64\chromedriver.exe"  # ← 改成你的實際路徑

def start_browser():
    options = Options()
    options.add_argument("--headless")  # 無頭模式（不跳出視窗）
    options.add_argument("--disable-gpu")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# === 動態爬取 TechNews 首頁文章連結 ===
def crawl_articles():
    driver = start_browser()
    driver.get("https://technews.tw/")
    time.sleep(2)  # 等待 JS 載入內容

    # 取得頁面 HTML 解析
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    links = soup.select("h1.entry-title a")
    articles = []
    for link in links[:5]:
        title = link.text.strip()
        href = link['href']
        article = get_article_content(href)
        articles.append(title + "\n" + article)
    return articles

# === 文章內容擷取（requests 即可） ===
def get_article_content(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        content = soup.select_one("div.entry-content")
        return content.get_text(strip=True).replace("\n", "")[:1000]
    except Exception as e:
        return ""

# === 主程式測試 ===
if __name__ == "__main__":
    print("🚀 啟動 Selenium 動態爬蟲...")
    articles = crawl_articles()
    print(f"✅ 成功擷取 {len(articles)} 篇文章\n")

    for i, a in enumerate(articles, 1):
        print(f"--- 文章 {i} ---")
        print(a[:300] + "...\n")
