"""
Data processing utilities
Tiện ích xử lý dữ liệu
"""

import pandas as pd
import numpy as np


class DataProcessor:
    """
    Xử lý dữ liệu đầu vào cho hệ thống chấm điểm
    """
    
    @staticmethod
    def delete_cols_and_rows(df):
        """
        Giữ lại các cột: taxcode, sector_unique_id, empl_qtty, yearreport, length_report
        và các cột bắt đầu bằng 'STD_RTD', còn lại xóa hết.
        """
        # Lấy các cột cần giữ
        keep_cols = ['taxcode', 'sector_unique_id', 'empl_qtty', 'yearreport', 'length_report']
        keep_cols += [col for col in df.columns if col.startswith('STD_RTD')]
        
        # Lọc DataFrame
        df_filtered = df[keep_cols].copy()
        return df_filtered
    
    @staticmethod
    def load_data(file_path, delimiter=','):
        """
        Tải dữ liệu từ file CSV
        """
        try:
            df = pd.read_csv(file_path, sep=delimiter)
            print(f"Đã tải {len(df)} dòng dữ liệu từ {file_path}")
            return df
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")
            return None
    
    @staticmethod
    def basic_info(df):
        """
        Hiển thị thông tin cơ bản về DataFrame
        """
        print("=== THÔNG TIN CƠ BẢN ===")
        print(f"Kích thước: {df.shape}")
        print(f"Số cột STD_RTD: {len([col for col in df.columns if col.startswith('STD_RTD')])}")
        
        if 'sector_label' in df.columns:
            print("\n=== PHÂN BỐ SECTOR ===")
            print(df['sector_label'].value_counts())
        
        print("\n=== THÔNG TIN MISSING DATA ===")
        missing_info = df.isnull().sum()
        missing_info = missing_info[missing_info > 0]
        if len(missing_info) > 0:
            print(missing_info.head(10))
        else:
            print("Không có missing data")
        
        print("\n=== SAMPLE DATA ===")
        print(df.head())
    
    @staticmethod
    def validate_data(df):
        """
        Kiểm tra tính hợp lệ của dữ liệu đầu vào
        """
        required_cols = ['taxcode', 'sector_unique_id', 'yearreport']
        missing_required = [col for col in required_cols if col not in df.columns]
        
        if missing_required:
            print(f"CẢNH BÁO: Thiếu cột bắt buộc: {missing_required}")
            return False
        
        # Kiểm tra có ít nhất một cột STD_RTD
        std_rtd_cols = [col for col in df.columns if col.startswith('STD_RTD')]
        if len(std_rtd_cols) == 0:
            print("CẢNH BÁO: Không có cột chỉ số tài chính (STD_RTD)")
            return False
        
        print(f"✅ Dữ liệu hợp lệ. Có {len(std_rtd_cols)} chỉ số tài chính.")
        return True
    
    @staticmethod
    def create_sample_data(n_rows=1000):
        """
        Tạo dữ liệu mẫu để test
        """
        np.random.seed(42)
        
        data = {
            'taxcode': [f'TC{i:06d}' for i in range(1, n_rows + 1)],
            'sector_unique_id': np.random.randint(1, 50, n_rows),
            'empl_qtty': np.random.randint(10, 1000, n_rows),
            'yearreport': np.random.choice([2020, 2021, 2022, 2023], n_rows),
            'length_report': np.random.randint(6, 24, n_rows),
            'sector_label': np.random.choice(['C', 'D', 'F', 'G'], n_rows)
        }
        
        # Tạo các chỉ số tài chính mẫu
        financial_indicators = [
            'STD_RTD1', 'STD_RTD2', 'STD_RTD3',  # Thanh khoản
            'STD_RTD10', 'STD_RTD11', 'STD_RTD12', 'STD_RTD13', 'STD_RTD14',  # Hiệu quả
            'STD_RTD20', 'STD_RTD21', 'STD_RTD22', 'STD_RTD23',  # Cấu trúc
            'STD_RTD30', 'STD_RTD31', 'STD_RTD32', 'STD_RTD33',  # Sinh lời
            'STD_RTD40', 'STD_RTD41', 'STD_RTD42',  # Tăng trưởng
            'STD_RTD50', 'STD_RTD60', 'STD_RTD61', 'STD_RTD77', 
            'STD_RTD96', 'STD_RTD97', 'STD_RTD148', 'STD_RTD26'  # Khác
        ]
        
        for indicator in financial_indicators:
            if indicator in ['STD_RTD20', 'STD_RTD21', 'STD_RTD22']:
                # Tỷ lệ nợ (0-1)
                data[indicator] = np.random.uniform(0, 1, n_rows)
            elif indicator in ['STD_RTD30', 'STD_RTD31', 'STD_RTD32']:
                # ROA, ROE, ROS (-0.5 to 0.5)
                data[indicator] = np.random.uniform(-0.5, 0.5, n_rows)
            elif indicator in ['STD_RTD40', 'STD_RTD41', 'STD_RTD42']:
                # Tốc độ tăng trưởng (-1 to 3)
                data[indicator] = np.random.uniform(-1, 3, n_rows)
            elif indicator == 'STD_RTD60':
                # Doanh thu (triệu VND)
                data[indicator] = np.random.uniform(1000, 100000, n_rows)
            elif indicator == 'STD_RTD61':
                # Lợi nhuận (-10000 to 20000)
                data[indicator] = np.random.uniform(-10000, 20000, n_rows)
            else:
                # Chỉ số khác
                data[indicator] = np.random.uniform(0, 10, n_rows)
        
        # Thêm một số missing values
        df = pd.DataFrame(data)
        for col in financial_indicators[:5]:
            mask = np.random.random(n_rows) < 0.1  # 10% missing
            df.loc[mask, col] = np.nan
        
        return df
    
    @staticmethod 
    def preprocess_columns(df):
        """
        Tiền xử lý các cột - giữ lại các cột cần thiết
        """
        return DataProcessor.delete_cols_and_rows(df)
