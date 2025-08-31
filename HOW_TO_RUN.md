# 🚀 HƯỚNG DẪN CHẠY - Financial Scoring API v2.1

## 📋 Tổng quan Project

Hệ thống API tính toán **điểm số nhóm có trọng số** cho doanh nghiệp, sau đó **xếp hạng và gán điểm T1-T8**.

- **Logic**: Quy trình hai bước - tính điểm số thô, sau đó xếp hạng để gán điểm T-score.
- **Input**: Chấp nhận giá trị số thực và trọng số tùy chỉnh.
- **Output**: Trả về điểm T-score (T1=cao nhất, T8=thấp nhất) cho mỗi nhóm.
- **Batch Processing**: Hỗ trợ xử lý nhiều công ty trong một lần gọi.

## 🚀 Cách chạy Project

### 1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 2. **Start API Server**

```bash
python app.py
```

**Kết quả**: Server sẽ khởi động tại `http://localhost:5000`.

### 3. **Test API**

Bạn có thể sử dụng `curl` hoặc một tập lệnh Python để kiểm tra API.

#### **Test Endpoint `/process-groups`:**

Tạo một tệp `test_payload.json` với nội dung sau. Ví dụ này bao gồm hai công ty với các giá trị khác nhau cho `Profitability` để minh họa cách xếp hạng hoạt động.

```json
{
  "weights": {
    "STD_RTD8": 1.0
  },
  "companies": [
    {
      "taxcode": "0106512583",
      "scores": {
        "Profitability": [
          {"indicator": "STD_RTD8", "value": 0.15}
        ]
      }
    },
    {
      "taxcode": "0100109106",
      "scores": {
        "Profitability": [
          {"indicator": "STD_RTD8", "value": 0.25}
        ]
      }
    }
  ]
}
```

Thực thi lệnh `curl` sau:

```bash
curl -X POST http://localhost:5000/process-groups -H "Content-Type: application/json" --data @test_payload.json
```

**Kết quả mong đợi:**

Công ty `0100109106` có điểm `Profitability` cao hơn, vì vậy nó sẽ nhận được điểm `T1` (cao nhất). Công ty `0106512583` sẽ nhận được điểm `T8` (thấp nhất).

```json
{
  "results": [
    {
      "taxcode": "0106512583",
      ...
      "Profitability_TScore": "T8",
      ...
    },
    {
      "taxcode": "0100109106",
      ...
      "Profitability_TScore": "T1",
      ...
    }
  ]
}
```

## 🔗 Available Endpoints

| Method | Endpoint          | Description                                       |
| ------ | ----------------- | ------------------------------------------------- |
| POST   | `/process-groups` | Tính điểm nhóm và gán điểm T-score cho nhiều công ty. |
| GET    | `/health`         | Health check                                      |

## 📊 Data Format

- **Request**: API chấp nhận một danh sách các công ty, mỗi công ty có các chỉ số với giá trị số.
- **Response**: API trả về một danh sách các công ty, mỗi công ty có điểm T-score (ví dụ: `Profitability_TScore`: `"T1"`) cho mỗi nhóm.
