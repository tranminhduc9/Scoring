"""
API Service cho hệ thống chấm điểm tài chính v2.0
Tính toán điểm nhóm dựa trên giá trị số và trọng số.
"""

import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

# Import thuật toán tính điểm và các file cấu hình
from field_score import field_score, assign_scores_field
from config.field_mapping import FIELD_MAPPING
from config.good_bad_mapping import GOOD_BAD_MAPPING

class FinancialScoringAPI:
    """
    Flask API cho hệ thống chấm điểm tài chính.
    """
    
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        
    def setup_routes(self):
        """Thiết lập các route API"""
        
        @self.app.route('/process-groups', methods=['POST'])
        def process_groups():
            """
            API xử lý và tính điểm nhóm cho nhiều công ty dựa trên giá trị số.
            
            Request body:
            {
                "weights": {
                    "STD_RTD92": 1.0,
                    "STD_RTD93": 0.8,
                    ...
                },
                "correlation_matrices": {
                    "Liquidity": [[1.0, 0.8], [0.8, 1.0]],
                    ...
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
                    }
                ]
            }
            """
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400

                weights = data.get('weights')
                # correlation_matrices = data.get('correlation_matrices') # Tạm thời chưa sử dụng
                companies_data = data.get('companies', [])

                if not companies_data:
                    return jsonify({"error": "List of 'companies' is required"}), 400

                # Chuẩn bị dữ liệu để đưa vào DataFrame
                records = []
                for company in companies_data:
                    record = {
                        'taxcode': company.get('taxcode'),
                        'sector_unique_id_raw': company.get('sector_unique_id_raw')
                    }
                    for group, indicators in company.get('scores', {}).items():
                        for indicator_data in indicators:
                            indicator_name = indicator_data.get('indicator')
                            value = indicator_data.get('value')
                            if indicator_name:
                                record[indicator_name] = value
                    records.append(record)
                
                if not records:
                    return jsonify({"results": []})

                # Tạo DataFrame từ dữ liệu của tất cả các công ty
                input_df = pd.DataFrame(records)

                # Bước 1: Gọi hàm tính điểm số thô có trọng số
                numeric_scores_df = field_score(
                    input_df,
                    FIELD_MAPPING,
                    GOOD_BAD_MAPPING,
                    weights
                )

                # Bước 2: Gán điểm T-Score dựa trên điểm số thô
                t_scores_df = assign_scores_field(
                    numeric_scores_df,
                    FIELD_MAPPING
                )

                # Chuyển đổi kết quả DataFrame cuối cùng thành định dạng JSON mong muốn
                t_scores_df.replace({np.nan: None}, inplace=True)
                response_data = t_scores_df.to_dict(orient='records')
                
                return jsonify({"results": response_data}), 200
                
            except Exception as e:
                # Ghi log lỗi ở đây sẽ tốt hơn trong môi trường production
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({"status": "healthy", "service": "Financial Scoring API v2.0"}), 200
    
    def get_app(self):
        """Lấy Flask app instance"""
        return self.app
    
    def run(self, host='0.0.0.0', port=5000, debug=True):
        """Chạy Flask server"""
        self.app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    # Để chạy server, sử dụng app.py
    print("Financial Scoring API Module v2.0")
    print("This module provides the API logic. Run app.py to start the server.")
