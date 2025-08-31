"""
Correlation analysis and weight adjustment module
Xử lý tương quan và điều chỉnh trọng số
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class CorrelationAnalyzer:
    """
    Phân tích tương quan và điều chỉnh trọng số
    """
    
    def __init__(self, threshold=0.9):
        self.threshold = threshold
    
    def analyze_correlation_by_group(self, df, group_field_mapping, show_plots=True):
        """
        Phân tích tương quan theo từng nhóm chỉ số
        """
        correlation_results = {}
        
        for group, fields in group_field_mapping.items():
            cols = [f for f in fields if f in df.columns]
            if len(cols) < 2:
                continue
            
            # Tính ma trận tương quan
            corr = df[cols].corr()
            
            if show_plots:
                # Vẽ heatmap
                plt.figure(figsize=(max(8, len(cols)*0.5), max(6, len(cols)*0.5)))
                sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
                plt.title(f'Correlation matrix: {group}')
                plt.show()
            
            # Tìm các cặp có tương quan mạnh
            pairs = []
            for i in range(len(cols)):
                for j in range(i+1, len(cols)):
                    val = corr.iloc[i, j]
                    if pd.notna(val) and abs(val) > self.threshold:
                        pairs.append((cols[i], cols[j], val))
            
            correlation_results[group] = {
                'correlation_matrix': corr,
                'high_correlation_pairs': pairs,
                'fields': cols
            }
            
            print(f"Các cặp chỉ số trong nhóm '{group}' có tương quan |corr| > {self.threshold}:")
            if pairs:
                for a, b, v in pairs:
                    print(f"  {a} - {b}: corr = {v:.2f}")
            else:
                print("  Không có cặp nào.")
            print("-" * 40)
        
        return correlation_results
    
    def adjust_weights_for_correlation(self, df, group_field_mapping, base_weight=1.0):
        """
        Điều chỉnh trọng số dựa trên tương quan giữa các chỉ số trong cùng một nhóm.
        """
        weights = {}

        for group, fields in group_field_mapping.items():
            cols = [f for f in fields if f in df.columns]
            if not cols:
                continue

            # Tính ma trận tương quan tuyệt đối
            corr = df[cols].corr().abs()
            visited = set()

            for i, col in enumerate(cols):
                if col in visited:
                    continue

                # Tìm cụm biến có tương quan cao với col (bao gồm chính nó)
                cluster = [col]
                for j in range(i + 1, len(cols)):
                    other = cols[j]
                    if other in visited:
                        continue
                    if corr.loc[col, other] > self.threshold:
                        cluster.append(other)

                # Nếu cụm có nhiều biến → chia đều trọng số
                if len(cluster) > 1:
                    w_each = base_weight / len(cluster)
                    for c in cluster:
                        weights[f"{c}_Tscore"] = w_each
                        visited.add(c)
                else:
                    # Không có cụm → giữ weight=base_weight
                    weights[f"{col}_Tscore"] = base_weight
                    visited.add(col)

            # Nếu còn biến chưa gán trọng số
            for c in cols:
                if f"{c}_Tscore" not in weights:
                    weights[f"{c}_Tscore"] = base_weight

        return weights
    
    def field_score(self, df, group_field_mapping, weights=None):
        """
        Tính điểm tổng hợp theo nhóm chỉ số, trả về DataFrame gồm:
        taxcode, sector_unique_id, yearreport và 6 cột điểm nhóm.
        """
        # Các cột thông tin cần giữ
        info_cols = ['taxcode', 'sector_unique_id', 'yearreport']
        result = df[info_cols].copy()

        for group, fields in group_field_mapping.items():
            # Lọc các field thực sự có trong df
            valid_fields = [f for f in fields if f in df.columns]
            if not valid_fields:
                result[f"{group}_Score"] = np.nan
                continue

            # Lấy trọng số
            if weights is None:
                group_weights = {col: 1.0 for col in valid_fields}
            else:
                group_weights = {col: weights.get(col, 1.0) for col in valid_fields}

            # Tính tổng có trọng số
            weighted_sum = pd.Series(0, index=df.index, dtype=float)
            total_weight = pd.Series(0, index=df.index, dtype=float)
            
            for col in valid_fields:
                w = group_weights.get(col, 1.0)
                weighted_sum += df[col].fillna(0) * w
                total_weight += w * df[col].notna().astype(float)
            
            with np.errstate(divide='ignore', invalid='ignore'):
                group_raw = weighted_sum / total_weight
                group_raw[total_weight == 0] = np.nan

            result[f"{group}_Score"] = group_raw

        return result
