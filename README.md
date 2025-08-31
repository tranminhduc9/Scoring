# 📊 Financial Scoring API System v2.1

Hệ thống API tính toán **điểm số nhóm có trọng số** cho các doanh nghiệp dựa trên dữ liệu tài chính số thô và trả về kết quả dưới dạng **thang điểm T1-T8**.

## 🌟 Tính năng chính

- ✅ **API REST** để tính điểm tài chính theo nhóm.
- ✅ **Two-Step Scoring**:
    1.  Tính toán điểm trung bình có trọng số cho từng nhóm chỉ số.
    2.  Xếp hạng các điểm số đó để gán điểm T1 (cao nhất) đến T8 (thấp nhất).
- ✅ **Numeric Input**: Chấp nhận giá trị số thực cho các chỉ số.
- ✅ **Batch Processing**: Hỗ trợ xử lý nhiều công ty trong một lần gọi API.
- ✅ **Custom Weights**: Cho phép chỉ định trọng số tùy chỉnh cho từng chỉ số tài chính.
- ✅ **Relative Ranking**: Điểm T-score cuối cùng có tính tương đối, dựa trên hiệu suất của các công ty trong cùng một yêu cầu.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Server

```bash
python app.py
```

### 3. Test API

Sử dụng một tập lệnh Python hoặc `curl` để gửi yêu cầu đến điểm cuối `/process-groups`.

```bash
# Ví dụ sử dụng curl
curl -X POST http://localhost:5000/process-groups \
  -H "Content-Type: application/json" \
  -d '{
    "weights": {"STD_RTD92": 1.0, "STD_RTD8": 1.2},
    "companies": [
      {
        "taxcode": "0106512583",
        "scores": {
          "Liquidity": [{"indicator": "STD_RTD92", "value": 1.5}],
          "Profitability": [{"indicator": "STD_RTD8", "value": 0.15}]
        }
      },
      {
        "taxcode": "0100109106",
        "scores": {
          "Liquidity": [{"indicator": "STD_RTD92", "value": 1.8}],
          "Profitability": [{"indicator": "STD_RTD8", "value": 0.25}]
        }
      }
    ]
  }'
```

## 🔗 API Endpoints

| Method | Endpoint          | Description                                      |
| ------ | ----------------- | ------------------------------------------------ |
| POST   | `/process-groups` | Tính điểm nhóm và gán điểm T-score cho nhiều công ty. |
| GET    | `/health`         | Health check                                     |

## 🧪 Usage Example (Python)

```python
import requests
import json

api_url = "http://localhost:5000/process-groups"

request_payload = {
  "companies": [
    {
      "taxcode": "0106512583",
      "scores": { "Profitability": [{"indicator": "STD_RTD8", "value": 0.15}] }
    },
    {
      "taxcode": "0100109106",
      "scores": { "Profitability": [{"indicator": "STD_RTD8", "value": 0.25}] }
    }
  ]
}

response = requests.post(api_url, json=request_payload)

print(f"Status Code: {response.status_code}")
print("Response JSON:")
print(json.dumps(response.json(), indent=2))

# Expected Response (Profitability_TScore):
# Company 1 (lower value) -> T8
# Company 2 (higher value) -> T1
```

## 📖 Documentation

- **API Documentation**: `API_DOCUMENTATION.md`
- **Running Guide**: `HOW_TO_RUN.md`
