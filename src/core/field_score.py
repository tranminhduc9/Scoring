import pandas as pd
import numpy as np

def field_score(data_df, group_field_mapping, good_bad_mapping, weights=None):
    
    """
    Tính điểm tổng hợp theo nhóm chỉ số từ DataFrame, trả về DataFrame gồm:
    taxcode, sector_unique_id_raw và các cột điểm nhóm.

    Parameters:
        data_df: pandas DataFrame (dữ liệu gốc)
        group_field_mapping: dict {group: [fields]}
        good_bad_mapping: dict {field: 'high' or 'low'}
        weights: dict {field: weight}, nếu None thì mỗi field có weight=1

    Return:
        DataFrame gồm các cột: taxcode, sector_unique_id_raw, <group>_Score
    """
    
    # Lấy các cột thông tin tồn tại trong DataFrame
    info_cols = ['taxcode', 'sector_unique_id_raw', 'yearreport']
    valid_info_cols = [col for col in info_cols if col in data_df.columns]
    result_df = data_df[valid_info_cols].copy()

    for group, fields in group_field_mapping.items():
        # Lọc các field thực sự có trong data_df
        valid_fields = [f for f in fields if f in data_df.columns]
        if not valid_fields:
            result_df[f"{group}_Score"] = np.nan
            continue

        # Lấy trọng số (mặc định 1.0)
        if weights is None:
            group_weights = {col: 1.0 for col in valid_fields}
        else:
            group_weights = {col: weights.get(col, 1.0) for col in valid_fields}

        # Xác định hướng tốt (good_bad_mapping) để áp dấu
        signs = {}
        for col in valid_fields:
            direction = good_bad_mapping.get(col, "")
            is_low_good = isinstance(direction, str) and "low" in direction.lower()
            signs[col] = -1.0 if is_low_good else 1.0

        # Tính tổng có trọng số và tổng trọng số
        weighted_sum = pd.Series(0.0, index=data_df.index)
        total_abs_weight = pd.Series(0.0, index=data_df.index)

        for field in valid_fields:
            w = group_weights[field]
            # Bỏ qua các trường có trọng số bằng 0 để không ảnh hưởng đến mẫu số
            if w == 0:
                continue

            values = pd.to_numeric(data_df[field], errors='coerce')
            s = signs[field]
            
            # Cộng vào tổng có trọng số, bỏ qua NaN
            weighted_sum += (values * w * s).fillna(0)
            
            # Cộng vào tổng trọng số tuyệt đối cho các giá trị không phải NaN
            total_abs_weight += (~values.isna()) * np.abs(w)

        # Tính điểm trung bình có trọng số, tránh chia cho 0
        group_score = weighted_sum.divide(total_abs_weight).replace([np.inf, -np.inf], np.nan)
        result_df[f"{group}_Score"] = group_score

    return result_df


def assign_scores_field(field_scores_df, group_field_mapping):
    """
    Chia thang điểm T1–T8 cho từng nhóm theo khoảng min–max của toàn bộ dữ liệu.
    - Chia đều thành 8 phần
    - Cao nhất → T1, thấp nhất → T8
    """
    # Lấy các cột thông tin tồn tại
    info_cols = ['taxcode', 'sector_unique_id_raw', 'yearreport']
    valid_info_cols = [col for col in info_cols if col in field_scores_df.columns]
    result_df = field_scores_df[valid_info_cols].copy()

    for group in group_field_mapping.keys():
        score_col_name = f"{group}_Score"
        t_score_col_name = f"{group}_TScore"

        if score_col_name not in field_scores_df.columns:
            result_df[t_score_col_name] = ""
            continue

        series = field_scores_df[score_col_name].dropna()
        
        # Khởi tạo cột TScore
        result_df[t_score_col_name] = pd.Series(dtype='object')

        if series.empty:
            continue

        min_val, max_val = series.min(), series.max()

        if min_val == max_val:
            # Nếu tất cả giá trị bằng nhau -> gán T4
            result_df.loc[series.index, t_score_col_name] = "T4"
            continue

        # Tạo 8 bins từ min đến max
        bins = np.linspace(min_val, max_val, 9)
        
        # Nhãn: T8 (thấp nhất) -> T1 (cao nhất)
        labels = [f"T{i}" for i in range(8, 0, -1)]

        # Dùng pd.cut để gán nhãn
        t_scores = pd.cut(series, bins=bins, labels=labels, include_lowest=True)
        
        result_df.loc[series.index, t_score_col_name] = t_scores.astype(str)

    return result_df
