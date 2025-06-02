from fastapi.testclient import TestClient  # 匯入 FastAPI 測試用的 HTTP 客戶端
from main import (
    app,
    SessionLocal,
    UserTable,
)  # 匯入主程式中的 app、資料庫 session 與模型
import os  # 用來檢查檔案是否存在

client = TestClient(app)  # 建立測試用的 FastAPI client 實例


# 每次測試前清空資料庫，保持資料一致性
def clear_db():
    db = SessionLocal()
    db.query(UserTable).delete()  # 刪除所有 UserTable 的資料
    db.commit()
    db.close()


# 測試建立使用者功能
def test_create_user():
    clear_db()
    # 送出 POST 請求建立使用者
    response = client.post("/user", json={"name": "TestUser", "age": 30})
    assert response.status_code == 200  # 檢查狀態碼是否為 200 OK
    assert response.json()["user"]["name"] == "TestUser"  # 確認回傳的使用者名稱正確


# 測試建立使用者時缺少必要欄位的錯誤處理
def test_create_user_missing_fields():
    clear_db()
    # 缺少 age 欄位
    response = client.post("/user", json={"name": "NoAge"})
    assert response.status_code == 422  # 應回傳驗證錯誤 Unprocessable Entity

    # 缺少 name 欄位
    response = client.post("/user", json={"age": 20})
    assert response.status_code == 422


# 測試成功刪除已存在的使用者
def test_delete_existing_user():
    clear_db()
    # 先建立一位使用者
    client.post("/user", json={"name": "ToDelete", "age": 25})
    # 然後刪除他
    response = client.delete("/user/ToDelete")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Deleted 1 user(s) named ToDelete"
    }  # 確認回傳訊息


# 測試取得所有使用者資料
def test_get_users():
    clear_db()
    # 新增一位使用者
    client.post("/user", json={"name": "A", "age": 20})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()["users"]) > 0  # 確認回傳有使用者資料


# 測試上傳有效的 CSV 檔案
def test_upload_csv():
    clear_db()
    csv_path = "C:/Restful/backend/backend_users.csv"  # 指定測試用的 CSV 路徑

    assert os.path.exists(csv_path), "CSV file not found"  # 確保檔案存在

    with open(csv_path, "rb") as f:
        response = client.post(
            "/upload_csv", files={"file": ("users.csv", f, "text/csv")}
        )

    assert response.status_code == 200
    data = response.json()
    assert "message" in data  # 確認回傳訊息中包含 "message"


# 測試上傳錯誤格式的 CSV 檔案
def test_upload_invalid_csv_format():
    clear_db()
    invalid_content = "這不是一個有效的 CSV 檔案"
    response = client.post(
        "/upload_csv",
        files={"file": ("invalid_file.txt", invalid_content, "text/plain")},
    )
    assert response.status_code == 400  # 錯誤格式應回傳 400 Bad Request
    assert "CSV 欄位名稱錯誤" in response.json()["detail"]  # 檢查錯誤訊息是否正確


# 測試平均年齡 API 功能
def test_average_age():
    clear_db()
    csv_path = "C:/Restful/backend/backend_users.csv"
    with open(csv_path, "rb") as f:
        client.post("/upload_csv", files={"file": ("users.csv", f, "text/csv")})

    response = client.get("/average_age")
    assert response.status_code == 200  # 確認可以成功取得平均年齡資料


# 測試當資料庫為空時，平均年齡 API 的回傳內容
def test_average_age_empty():
    clear_db()  # 清空所有資料
    response = client.get("/average_age")
    assert response.status_code == 200
    assert response.json() == {
        "message": "No users to calculate average"
    }  # 檢查提示訊息
