"""
Financial Scoring System - Complete system for testing and development
Hệ thống chấm điểm tài chính hoàn chỉnh
"""

import pandas as pd
import numpy as np
from src.config.good_bad_mapping import GOOD_BAD_MAPPING
from src.config.field_mapping import group_field_mapping
from src.core.scoring import FinancialScorer
from src.core.correlation import CorrelationAnalyzer
from src.utils.data_processor import DataProcessor
from src.api.scoring_api import GroupCorrelationScorer, process_company_scoring


class FinancialScoringSystem:
    """
    Hệ thống chấm điểm tài chính hoàn chỉnh
    Tích hợp tất cả các module - dùng cho testing và development
    """
    
    def __init__(self, correlation_threshold=0.9, lower_cut=0.05, upper_cut=0.95):
        self.correlation_threshold = correlation_threshold
        self.lower_cut = lower_cut
        self.upper_cut = upper_cut
        
        # Khởi tạo các component
        self.scorer = FinancialScorer()
        self.correlation_analyzer = CorrelationAnalyzer(correlation_threshold)
        self.data_processor = DataProcessor()
        
        print("🔧 FinancialScoringSystem đã được khởi tạo")
        print(f"   📊 Ngưỡng tương quan: {correlation_threshold}")
        print(f"   📈 Cắt outlier: {lower_cut:.1%} - {upper_cut:.1%}")
    
    def load_and_preprocess(self, file_path, delimiter=','):
        """Bước 1: Tải và tiền xử lý dữ liệu"""
        print("\n" + "="*50)
        print("🔄 BƯỚC 1: TẢI VÀ TIỀN XỬ LÝ DỮ LIỆU")
        print("="*50)
        
        # Tải dữ liệu
        df = self.data_processor.load_data(file_path, delimiter)
        if df is None:
            return None
        
        # Hiển thị thông tin cơ bản
        self.data_processor.basic_info(df)
        
        # Kiểm tra tính hợp lệ
        if not self.data_processor.validate_data(df):
            return None
        
        # Lọc cột cần thiết
        df_filtered = self.data_processor.preprocess_columns(df)
        print(f"\n✅ Đã lọc từ {df.shape[1]} cột xuống {df_filtered.shape[1]} cột")
        
        return df_filtered
    
    def individual_scoring(self, df):
        """Bước 2: Chấm điểm từng chỉ số T1-T8"""
        print("\n" + "="*50)
        print("🎯 BƯỚC 2: CHẤM ĐIỂM TỪNG CHỈ SỐ")
        print("="*50)
        
        # Lọc chỉ các chỉ số có trong dữ liệu
        available_mapping = {k: v for k, v in GOOD_BAD_MAPPING.items() if k in df.columns}
        print(f"📋 Sẽ chấm điểm cho {len(available_mapping)} chỉ số")
        
        # Chấm điểm
        scored_df = self.scorer.assign_scores_df(
            df, available_mapping, self.lower_cut, self.upper_cut
        )
        
        print(f"✅ Hoàn thành chấm điểm cá nhân")
        print(f"   📊 Kết quả: {scored_df.shape[1]} cột (bao gồm {len(available_mapping)} cột _Tscore)")
        
        return scored_df
    
    def correlation_analysis(self, df, show_plots=False):
        """Bước 3: Phân tích tương quan và điều chỉnh trọng số"""
        print("\n" + "="*50)
        print("🔍 BƯỚC 3: PHÂN TÍCH TƯƠNG QUAN")
        print("="*50)
        
        # Phân tích tương quan
        correlation_results = self.correlation_analyzer.analyze_correlation_by_group(
            df, group_field_mapping, show_plots
        )
        
        # Điều chỉnh trọng số
        weights = self.correlation_analyzer.adjust_weights_for_correlation(
            df, group_field_mapping
        )
        
        print(f"\n✅ Hoàn thành phân tích tương quan")
        print(f"   ⚖️  Đã điều chỉnh trọng số cho {len(weights)} chỉ số")
        
        return weights, correlation_results
    
    def group_scoring(self, scored_df, weights):
        """Bước 4: Tính điểm nhóm"""
        print("\n" + "="*50)
        print("📊 BƯỚC 4: TÍNH ĐIỂM NHÓM")
        print("="*50)
        
        field_scores = self.correlation_analyzer.field_score(
            scored_df, group_field_mapping, weights
        )
        
        print(f"📈 Đã tính điểm thô cho {len(group_field_mapping)} nhóm:")
        
        return field_scores
    
    def final_scoring(self, field_scores):
        """Bước 5: Điểm số cuối cùng"""
        print("\n" + "="*50)
        print("🏆 BƯỚC 5: ĐIỂM SỐ CUỐI CÙNG")
        print("="*50)
        
        final_scores = self.scorer.assign_scores_field(
            field_scores, group_field_mapping, self.lower_cut, self.upper_cut
        )
        
        print("✅ Hoàn thành chuyển đổi thang điểm T1-T8")
        
        return final_scores
    
    def process_file(self, file_path, delimiter=','):
        """Xử lý hoàn chỉnh một file từ đầu đến cuối"""
        print("🚀 BẮT ĐẦU XỬ LÝ FILE:", file_path)
        
        # Bước 1: Tải và tiền xử lý
        df = self.load_and_preprocess(file_path, delimiter)
        if df is None:
            return None
        
        # Bước 2: Chấm điểm cá nhân
        scored_df = self.individual_scoring(df)
        
        # Bước 3: Phân tích tương quan
        weights, correlation_results = self.correlation_analysis(df, False)
        
        # Bước 4: Tính điểm nhóm
        field_scores = self.group_scoring(scored_df, weights)
        
        # Bước 5: Điểm cuối cùng
        final_scores = self.final_scoring(field_scores)
        
        print("\n📋 THỐNG KÊ KẾT QUẢ:")
        print(f"   📄 File: {file_path}")
        print(f"   📊 Số dòng: {len(final_scores)}")
        print(f"   🎯 Số nhóm điểm: {len([c for c in final_scores.columns if c.endswith('_TScore')])}")
        
        return {
            'final_scores': final_scores,
            'field_scores': field_scores, 
            'scored_individual': scored_df,
            'weights': weights,
            'correlation_results': correlation_results,
            'original_data': df
        }
    
    def create_sample_and_process(self, n_rows=1000, save_sample=True):
        """Tạo dữ liệu mẫu và xử lý"""
        print(f"🔧 TẠO DỮ LIỆU MẪU ({n_rows} dòng)")
        
        sample_data = self.data_processor.create_sample_data(n_rows)
        
        if save_sample:
            sample_path = "data/sample_data.csv"
            sample_data.to_csv(sample_path, index=False)
            print(f"💾 Đã lưu dữ liệu mẫu: {sample_path}")
            
            # Xử lý file mẫu
            return self.process_file(sample_path)
        else:
            # Xử lý trực tiếp DataFrame
            print("\n🚀 XỬ LÝ DỮ LIỆU MẪU TRỰC TIẾP")
            
            # Bỏ qua bước load file, xử lý trực tiếp
            scored_df = self.individual_scoring(sample_data)
            weights, correlation_results = self.correlation_analysis(sample_data, False)
            field_scores = self.group_scoring(scored_df, weights)
            final_scores = self.final_scoring(field_scores)
            
            return {
                'final_scores': final_scores,
                'field_scores': field_scores,
                'scored_individual': scored_df,
                'weights': weights,
                'correlation_results': correlation_results,
                'original_data': sample_data
            }
    
    def process_with_new_algorithm(self, df, epsilon=0.1):
        """Xử lý chấm điểm với thuật toán mới sử dụng API"""
        print("\n" + "="*60)
        print("🚀 XỬ LÝ VỚI THUẬT TOÁN MỚI (API-BASED)")
        print("="*60)
        
        # Bước 1: Xử lý cá nhân như cũ
        print("1️⃣ Chấm điểm cá nhân...")
        scored_df = self.individual_scoring(df)
        
        # Bước 2: Phân tích tương quan
        print("2️⃣ Phân tích tương quan...")
        correlation_results = self.correlation_analyzer.analyze_correlation_by_group(
            df, group_field_mapping, show_plots=False
        )
        
        # Bước 3: Chuẩn bị dữ liệu cho API mới
        print("3️⃣ Chuẩn bị dữ liệu cho thuật toán mới...")
        
        # Tạo correlation matrices từ kết quả phân tích
        group_correlation_matrices = {}
        for group, result in correlation_results.items():
            group_correlation_matrices[group] = result['correlation_matrix']
        
        # Tạo group scores từ scored_df - CHUYỂN THÀNH LIST
        group_scores = {}
        for group, fields in group_field_mapping.items():
            scores_list = []
            for field in fields:
                tscore_col = f"{field}_Tscore"
                if tscore_col in scored_df.columns:
                    # Lấy điểm mode của field này
                    mode_score = scored_df[tscore_col].mode()
                    if not mode_score.empty:
                        scores_list.append(mode_score.iloc[0])
                    else:
                        scores_list.append("T4")  # Default
            group_scores[group] = scores_list  # List format
        
        # Bước 4: Áp dụng thuật toán mới
        print("4️⃣ Áp dụng thuật toán correlation với epsilon...")
        print(f"   📊 Epsilon: {epsilon}")
        print(f"   🎯 Correlation threshold: {1 - epsilon}")
        
        final_group_scores = process_company_scoring(
            group_correlation_matrices,
            group_scores,
            epsilon=epsilon
        )
        
        print("✅ Hoàn thành xử lý với thuật toán mới!")
        
        # Tạo DataFrame kết quả
        result_df = df[['taxcode', 'sector_unique_id', 'yearreport']].copy()
        for group, score in final_group_scores.items():
            result_df[f"{group}_FinalScore"] = score
        
        return {
            'final_scores_new': result_df,
            'group_scores_input': group_scores,
            'final_group_scores': final_group_scores,
            'correlation_matrices': group_correlation_matrices,
            'correlation_results': correlation_results,
            'epsilon': epsilon,
            'correlation_threshold': 1 - epsilon
        }


# Convenience functions
def quick_score(file_path, delimiter=','):
    """Hàm tiện ích để chấm điểm nhanh một file"""
    system = FinancialScoringSystem()
    return system.process_file(file_path, delimiter)


def quick_score_new_algorithm(file_path, epsilon=0.1, delimiter=','):
    """Hàm tiện ích để chấm điểm với thuật toán mới"""
    system = FinancialScoringSystem()
    df = system.data_processor.load_data(file_path, delimiter)
    if df is not None:
        df = system.data_processor.preprocess_columns(df)
        return system.process_with_new_algorithm(df, epsilon)
    return None
