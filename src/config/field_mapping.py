# Phân nhóm các chỉ số tài chính - Updated theo dữ liệu mới

FIELD_MAPPING = {
    "Leverage_Debt": [  # Đòn bẩy và Khả năng trả nợ
        "STD_RTD146",  # FFO / Nợ vay
        "STD_RTD71",   # Hệ số Nợ vay/Vốn CSH - PTC
        "STD_RTD96",   # Tổng nợ vay thuần/EBITDA
        "STD_RTD97",   # EBITDA/Chi phí lãi vay
        "STD_RTD98",   # CFO/Tổng nợ vay
        "STD_RTD99",   # Lợi nhuận hoạt động/ Lãi vay
        "STD_RTD1",    # Tổng tài sản/Vốn chủ sở hữu
        "STD_RTD72",   # Hệ số EBIT/Nợ vay
        "STD_RTD148"   # Tổng nợ vay/EBITDA
    ],
    
    "Efficiency": [  # Hiệu quả hoạt động
        "STD_RTD74",  # Vòng quay khoản phải thu
        "STD_RTD76",  # Vòng quay vốn lưu động
        "STD_RTD77",  # EBITDA/Tổng Tài sản
        "STD_RTD78",  # Vòng quay tổng tài sản
        "STD_RTD81",  # Chu kỳ tiền mặt
        "STD_RTD64",  # Vòng quay khoản phải trả
        "STD_RTD75"   # Vòng quay hàng tồn kho
    ],
    
    "Scale": [  # Quy mô
        "STD_RTD13",   # Tổng tài sản (TTS)
        "STD_RTD14",   # Vốn chủ sở hữu (Vốn CSH)
        "STD_RTD31",   # Doanh thu hoạt động TTM
        "empl_qtty"    # Số lượng nhân viên
    ],
    
    "Profitability": [  # Khả Năng Sinh Lời
        "STD_RTD26",  # Biên lợi nhuận trước lãi vay, thuế và khấu hao
        "STD_RTD8",   # ROA
        "STD_RTD82",  # Tỷ suất sinh lời trên vốn kinh doanh (ROCE)
        "STD_RTD83",  # Biên lợi nhuận trước lãi vay và thuế
        "STD_RTD84",  # Biên lợi nhuận hoạt động
        "STD_RTD85",  # Biên lợi nhuận gộp
        "STD_RTD86",  # Biên LNST
        "STD_RTD9"    # ROE
    ],
    
    "Growth": [  # Khả Năng Tăng Trưởng
        "STD_RTD11",  # Lợi nhuận sau thuế (YoY)
        "STD_RTD28",  # Doanh thu TTM (YoY)
        "STD_RTD87",  # EBIT TTM (YoY)
        "STD_RTD88",  # Tăng trưởng tài sản
        "STD_RTD89"   # Tăng trưởng vốn chủ sở hữu
    ],
    
    "Liquidity": [  # Khả Năng Thanh Khoản
        "STD_RTD118", # Thanh khoản - Dòng tiền
        "STD_RTD92",  # Chỉ số thanh toán ngắn hạn
        "STD_RTD93",  # Chỉ số thanh toán nhanh
        "STD_RTD94",  # Chỉ số thanh toán tức thời
        "STD_RTD95",  # CFO/Nợ ngắn hạn
        "STD_RTD147"  # (FFO + Cash) / Nợ vay ngắn hạn
    ]
}

# Các chỉ số trung gian (không tham gia chấm điểm trực tiếp)
INTERMEDIATE_FIELDS = [
    "STD_RTD60",  # EBITDA
    "STD_RTD61"   # Tổng nợ vay thuần
]
