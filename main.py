# 匯入 FastAPI 框架、檔案上傳與錯誤處理相關模組
from fastapi import FastAPI, UploadFile, File, HTTPException

# 匯入資料驗證模組 Pydantic，用來定義資料結構
from pydantic import BaseModel

# 匯入 SQLAlchemy 的資料庫建構工具
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# 匯入 pandas 處理 CSV 與 io 處理檔案流
import pandas as pd
import io

# 設定 SQLite 資料庫路徑
DATABASE_URL = "sqlite:///./users.db"

# 建立資料庫引擎，SQLite 特別需要加入 check_same_thread=False
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 建立資料庫 session 工具
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 建立資料表基礎類別
Base = declarative_base()


# 定義資料庫中的 UserTable 資料表結構
class UserTable(Base):
    __tablename__ = "users"  # 資料表名稱為 users
    id = Column(Integer, primary_key=True, index=True)  # 主鍵，自動遞增
    name = Column(String, index=True)  # 使用者名稱
    age = Column(Integer)  # 使用者年齡


# 建立資料表（如果尚未存在）
Base.metadata.create_all(bind=engine)

# 建立 FastAPI 應用實例
app = FastAPI()


# 定義使用者模型，用於接收與驗證輸入資料（name, age）
class User(BaseModel):
    name: str
    age: int


# 建立單筆使用者的 API：POST /user
@app.post("/user")
def create_user(user: User):
    db = SessionLocal()  # 建立資料庫 session
    db_user = UserTable(name=user.name, age=user.age)  # 建立 UserTable 實例
    db.add(db_user)  # 新增到資料庫 session
    db.commit()  # 提交變更
    db.close()  # 關閉 session
    return {"message": "User added", "user": user}  # 回傳訊息與新增的使用者資料


# 刪除指定使用者名稱的 API：DELETE /user/{name}
@app.delete("/user/{name}")
def delete_user(name: str):
    db = SessionLocal()
    # 根據名稱查詢並刪除使用者，回傳刪除筆數
    deleted = db.query(UserTable).filter(UserTable.name == name).delete()
    db.commit()
    db.close()
    return {"message": f"Deleted {deleted} user(s) named {name}"}  # 回傳刪除結果


# 取得所有使用者的 API：GET /users
@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(UserTable).all()  # 查詢所有使用者
    db.close()
    # 回傳使用者清單（只包含 name 與 age）
    return {"users": [{"name": user.name, "age": user.age} for user in users]}


# 上傳 CSV 檔案並匯入使用者資料：POST /upload_csv
@app.post("/upload_csv")
def upload_csv(file: UploadFile = File(...)):
    try:
        # 將檔案內容讀取並解碼成 UTF-8 字串
        content = file.file.read().decode("utf-8")

        # 使用 pandas 解析 CSV 內容為 DataFrame
        data = pd.read_csv(io.StringIO(content))

        # 檢查是否包含正確欄位名稱
        if "Name" not in data.columns or "Age" not in data.columns:
            raise HTTPException(
                status_code=400, detail="CSV 欄位名稱錯誤，請確保包含 'Name' 和 'Age'"
            )

        db = SessionLocal()
        # 逐列插入每一筆使用者資料
        for _, row in data.iterrows():
            db_user = UserTable(name=row["Name"], age=int(row["Age"]))
            db.add(db_user)
        db.commit()
        db.close()

        return {"message": "CSV file processed"}  # 回傳成功訊息

    except Exception as e:
        # 發生任何錯誤則回傳 HTTP 400 與錯誤內容
        raise HTTPException(status_code=400, detail=f"解析 CSV 失敗: {str(e)}")


# 計算平均年齡（依照名稱第一個字分組）：GET /average_age
@app.get("/average_age")
def average_age():
    db = SessionLocal()
    users = db.query(UserTable).all()  # 查詢所有使用者
    db.close()

    if not users:
        return {"message": "No users to calculate average"}  # 若無使用者則回傳提示訊息

    # 將使用者資料轉為 pandas DataFrame
    df = pd.DataFrame([{"name": u.name, "age": u.age} for u in users])

    # 根據使用者名稱的第一個字母分組
    df["group"] = df["name"].apply(lambda x: x[0])

    # 計算每一組的平均年齡，四捨五入至小數點第二位
    result = df.groupby("group")["age"].mean().round(2).to_dict()

    return {"average_age_by_group": result}  # 回傳分組平均年齡字典
