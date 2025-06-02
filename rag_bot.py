# 匯入相關套件
import requests
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os

# 直接在程式碼中寫入 API key（請換成你的實際 key）
OPENAI_API_KEY = ""

# === 第一步：爬取網站文章 ===
def crawl_articles():
    url = "https://technews.tw/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 取得文章標題與連結
    links = soup.select("h1.entry-title a")
    articles = []
    for link in links[:5]:  # 只抓前5篇
        title = link.text.strip()
        href = link['href']
        article = get_article_content(href)
        articles.append(title + "\n" + article)
    return articles

# === 第二步：抓取文章內容 ===
def get_article_content(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        # 抓正文內容
        content = soup.select_one("div.entry-content")
        return content.get_text(strip=True).replace("\n", "")[:1000]  # 限制字數避免太長
    except Exception as e:
        return ""

# === 第三步：切片並建立向量資料庫 ===
def build_vector_db(articles):
    docs = [Document(page_content=a) for a in articles]
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)  # 傳入 API key
    vectordb = FAISS.from_documents(split_docs, embeddings)
    return vectordb

# === 第四步：建立問答系統 ===
def create_qa_chain(vectordb):
    retriever = vectordb.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY),
        retriever=retriever
    )
    return qa_chain

# === 第五步：主流程 ===
def main():
    print("📥 開始爬取最新技術新聞...")
    articles = crawl_articles()
    print(f"✅ 成功抓取 {len(articles)} 篇文章")

    print("🔧 建立向量資料庫中...")
    vectordb = build_vector_db(articles)

    print("🤖 問答機器人已就緒！請輸入你的問題：")
    qa = create_qa_chain(vectordb)

    while True:
        query = input("📌 問題（輸入 'exit' 離開）：")
        if query.lower() == "exit":
            break
        answer = qa.run(query)
        print("💡 AI 回答：", answer)

if __name__ == "__main__":
    main()
