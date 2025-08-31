"""
Core scoring engine for financial data
Chuyển đổi từ notebook sang module Python
"""

import numpy as np
import pandas as pd
from scipy.stats import shapiro
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import RobustScaler


class FinancialScorer:
    """
    Hệ thống chấm điểm tài chính T1-T8
    """
    
    def __init__(self, special_zero_fields=None):
        self.special_zero_fields = special_zero_fields or ['STD_RTD97', 'STD_RTD77', 'STD_RTD26']
    
    def handle_special_zero_fields(self, series, score_col):
        """Xử lý các giá trị <= 0 (Để là T1 - cao nhất)."""
        mask_zero = series <= 0
        score_col.loc[mask_zero] = "T1"  # T1 = cao nhất
        pos_series = series[~mask_zero].dropna()
        return pos_series

    def handle_special_cases_rtd96(self, df, field, score_col):
        """Xử lý đặc biệt cho STD_RTD96."""
        if "STD_RTD61" not in df.columns or "STD_RTD60" not in df.columns:
            return df[field].dropna()
        
        series = df[field]
        mask_rtd61_le0 = df["STD_RTD61"] <= 0
        mask_rtd61_gt0_rtd60_le0 = (df["STD_RTD61"] > 0) & (df["STD_RTD60"] <= 0)
        
        score_col.loc[mask_rtd61_le0] = "T8"  # T8 = thấp nhất
        score_col.loc[mask_rtd61_gt0_rtd60_le0] = "T1"  # T1 = cao nhất
        
        return series[~(mask_rtd61_le0 | mask_rtd61_gt0_rtd60_le0)].dropna()

    def handle_special_cases_rtd148(self, df, field, score_col):
        """Xử lý đặc biệt cho STD_RTD148."""
        if "STD_RTD60" not in df.columns:
            return df[field].dropna()
        
        series = df[field]
        mask_rtd60_le0 = df["STD_RTD60"] <= 0
        score_col.loc[mask_rtd60_le0] = "T1"  # T1 = cao nhất
        
        return series[~mask_rtd60_le0].dropna()

    def assign_scores_normal_distribution(self, series_non_na, direction, lower_cut, upper_cut, score_col):
        """Chia thang điểm theo phân vị nếu dữ liệu gần chuẩn."""
        q_low, q_high = series_non_na.quantile([lower_cut, upper_cut])
        inlier_mask = (series_non_na >= q_low) & (series_non_na <= q_high)
        series_inliers = series_non_na[inlier_mask]

        if series_inliers.nunique() < 2:
            if direction == "high_good":
                score_col.loc[series_inliers.index] = "T4"
                score_col.loc[series_non_na.index[series_non_na < q_low]] = "T8"  # Giá trị thấp -> điểm thấp
                score_col.loc[series_non_na.index[series_non_na > q_high]] = "T1"  # Giá trị cao -> điểm cao
            else:
                score_col.loc[series_inliers.index] = "T4"
                score_col.loc[series_non_na.index[series_non_na < q_low]] = "T1"  # Giá trị thấp -> điểm cao
                score_col.loc[series_non_na.index[series_non_na > q_high]] = "T8"  # Giá trị cao -> điểm thấp
            return score_col

        bins = np.percentile(series_inliers.unique(), np.linspace(0, 100, 9))
        bins = np.unique(bins)
        # T1 = cao nhất, T8 = thấp nhất
        # high_good: giá trị cao -> điểm cao (T1), giá trị thấp -> điểm thấp (T8)
        # low_good: giá trị thấp -> điểm cao (T1), giá trị cao -> điểm thấp (T8)
        labels = [f"T{i}" for i in range(1, 9)] if direction == "high_good" else [f"T{i}" for i in range(8, 0, -1)]

        cat_inliers = pd.cut(series_inliers, bins=bins, labels=labels[:len(bins)-1], include_lowest=True)
        score_col.loc[series_inliers.index] = cat_inliers

        min_bin, max_bin = bins[0], bins[-1]

        score_col.loc[series_non_na.index[series_non_na < min_bin]] = labels[0]
        score_col.loc[series_non_na.index[series_non_na > max_bin]] = labels[-1]

        return score_col

    def assign_scores_df(self, df, good_bad_mapping, lower_cut=0.05, upper_cut=0.95):
        """Hàm chính để gán thang điểm T1–T8."""
        score_data = df.copy()

        for field, direction in good_bad_mapping.items():
            if field not in df.columns:
                continue

            series = df[field]
            score_col = pd.Series(index=series.index, dtype="object")

            # Xử lý đặc biệt
            if field in self.special_zero_fields:
                series_non_na = self.handle_special_zero_fields(series, score_col)
            elif field == "STD_RTD96":
                series_non_na = self.handle_special_cases_rtd96(df, field, score_col)
            elif field == "STD_RTD148":
                series_non_na = self.handle_special_cases_rtd148(df, field, score_col)
            else:
                series_non_na = series.dropna()

            if series_non_na.empty or len(series_non_na) < 3:
                score_data[field + "_Tscore"] = score_col
                continue

            # Kiểm tra tính chuẩn (chỉ lấy mẫu để test)
            sample_size = min(5000, len(series_non_na))
            stat, p_value = shapiro(series_non_na.sample(sample_size))
            is_normal = p_value > 0.01

            score_col = self.assign_scores_normal_distribution(
                series_non_na, direction, lower_cut, upper_cut, score_col
            )

            score_data[field + "_Tscore"] = score_col

        # Xóa cột gốc
        for col in good_bad_mapping.keys():
            if col in score_data.columns:
                score_data.drop(columns=[col], inplace=True)

        return score_data

    def assign_field_normal_distribution(self, series_non_na, lower_cut, upper_cut, score_col):
        """Chia thang điểm theo phân vị cho điểm nhóm. T1=cao nhất, T8=thấp nhất."""
        q_low, q_high = series_non_na.quantile([lower_cut, upper_cut])
        inlier_mask = (series_non_na >= q_low) & (series_non_na <= q_high)
        series_inliers = series_non_na[inlier_mask]

        if series_inliers.nunique() < 2:
            score_col.loc[series_inliers.index] = "T4"
            score_col.loc[series_non_na.index[series_non_na < q_low]] = "T8"  # Giá trị thấp -> điểm thấp
            score_col.loc[series_non_na.index[series_non_na > q_high]] = "T1"  # Giá trị cao -> điểm cao
            return score_col

        bins = np.percentile(series_inliers.unique(), np.linspace(0, 100, 9))
        bins = np.unique(bins)
        # T1=cao nhất, T8=thấp nhất: giá trị cao -> T1, giá trị thấp -> T8
        labels = [f"T{i}" for i in range(1, 9)]  # T1, T2, T3, ..., T8

        cat_inliers = pd.cut(series_inliers, bins=bins, labels=labels[:len(bins)-1], include_lowest=True)
        score_col.loc[series_inliers.index] = cat_inliers

        min_bin, max_bin = bins[0], bins[-1]

        score_col.loc[series_non_na.index[series_non_na < min_bin]] = labels[0]  # T1 cho giá trị thấp
        score_col.loc[series_non_na.index[series_non_na > max_bin]] = labels[-1]  # T8 cho giá trị cao

        return score_col

    def assign_scores_field(self, field_scores, group_field_mapping, lower_cut=0.05, upper_cut=0.95):
        """Chia lại thang điểm T1-T8 cho từng nhóm trong field_scores theo phân vị."""
        result = field_scores[['taxcode', 'sector_unique_id', 'yearreport']].copy()
        
        for group in group_field_mapping.keys():
            if f"{group}_Score" not in field_scores.columns:
                result[f"{group}_TScore"] = ""
                continue
                
            series = field_scores[f"{group}_Score"]
            score_col = pd.Series(index=series.index, dtype="object")
            
            score_col = self.assign_field_normal_distribution(
                series.dropna(), 
                lower_cut=lower_cut, 
                upper_cut=upper_cut, 
                score_col=score_col
            )
            result[f"{group}_TScore"] = score_col
            
        return result
