# 📊 Financial Scoring API Documentation v2.1

## 🌟 Overview

API hệ thống chấm điểm tài chính phiên bản 2.1. Hệ thống này được thiết kế để tính toán **điểm số nhóm có trọng số** từ dữ liệu tài chính số thô, sau đó chuyển đổi các điểm số đó thành **thang điểm T1-T8**.

- **Input**: Nhận giá trị số thực của các chỉ số tài chính.
- **Logic**:
    1.  Tính toán điểm trung bình có trọng số cho từng nhóm chỉ số.
    2.  Xếp hạng các điểm số nhóm trên toàn bộ các công ty trong yêu cầu để gán điểm T1 (cao nhất) đến T8 (thấp nhất).
- **Features**: Hỗ trợ xử lý hàng loạt, trọng số tùy chỉnh.

## 🔗 API Endpoints

### 1. Process Groups (Main API)

Xử lý, tính điểm nhóm có trọng số và gán điểm T-score cho một hoặc nhiều công ty.

**🔗 Endpoint:** `POST /process-groups`

**📤 Request Body:**

```json
{
  "weights": {
    "STD_RTD92": 1.0,
    "STD_RTD93": 0.8,
    "STD_RTD8": 1.2
  },
  "companies": [
    {
      "taxcode": "0106512583",
      "sector_unique_id_raw": 32900,
      "scores": {
        "Liquidity": [
          {"indicator": "STD_RTD92", "value": 1.5},
          {"indicator": "STD_RTD93", "value": 2.1}
        ],
        "Profitability": [
          {"indicator": "STD_RTD8", "value": 0.15}
        ]
      }
    },
    {
      "taxcode": "0100109106",
      "sector_unique_id_raw": 46630,
      "scores": {
        "Liquidity": [
          {"indicator": "STD_RTD92", "value": 1.8}
        ],
        "Profitability": [
          {"indicator": "STD_RTD8", "value": 0.25}
        ]
      }
    }
  ]
}
```

**📥 Response Body:**

Phản hồi chứa điểm T-score cho mỗi nhóm.

```json
{
  "results": [
    {
      "taxcode": "0106512583",
      "sector_unique_id_raw": 32900,
      "yearreport": null,
      "Leverage_Debt_TScore": null,
      "Efficiency_TScore": null,
      "Scale_TScore": null,
      "Profitability_TScore": "T8",
      "Growth_TScore": null,
      "Liquidity_TScore": "T8"
    },
    {
      "taxcode": "0100109106",
      "sector_unique_id_raw": 46630,
      "yearreport": null,
      "Leverage_Debt_TScore": null,
      "Efficiency_TScore": null,
      "Scale_TScore": null,
      "Profitability_TScore": "T1",
      "Growth_TScore": null,
      "Liquidity_TScore": "T1"
    }
  ]
}
```

**🔍 Logic**:

1.  API nhận một danh sách các công ty.
2.  Nó sử dụng hàm `field_score` để tính toán **điểm số thô có trọng số** cho mỗi nhóm.
3.  Sau đó, nó sử dụng hàm `assign_scores_field` để so sánh các điểm số thô của tất cả các công ty trong yêu cầu. Dựa trên sự so sánh này, nó chia các công ty thành 8 nhóm và gán điểm T-score tương ứng (T1 cho nhóm có điểm số thô cao nhất, T8 cho nhóm thấp nhất).
4.  Kết quả cuối cùng là điểm T-score cho mỗi nhóm của mỗi công ty.

### 2. Health Check

Kiểm tra tình trạng hoạt động của API.

**🔗 Endpoint:** `GET /health`

**📥 Response:**

```json
{
  "status": "healthy",
  "service": "Financial Scoring API v2.1"
}
```

## 📝 Notes

- **Two-Step Process**: Việc chấm điểm bao gồm tính toán điểm số thô và sau đó là xếp hạng để gán điểm T-score.
- **Relative Ranking**: Điểm T-score của một công ty phụ thuộc vào điểm số của các công ty khác trong cùng một yêu cầu.
- **Batch Processing**: API được thiết kế để hoạt động hiệu quả nhất khi xử lý một lô các công ty, vì điều này cung cấp một mẫu lớn hơn để xếp hạng và gán điểm T-score một cách có ý nghĩa.
