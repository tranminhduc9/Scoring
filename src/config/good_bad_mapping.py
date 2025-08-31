# Mapping định hướng chấm điểm cho từng chỉ số
# "high_good": giá trị cao = điểm tốt (T8)
# "low_good": giá trị thấp = điểm tốt (T8)

# Mapping định hướng chấm điểm cho từng chỉ số - Updated theo tín hiệu mới

GOOD_BAD_MAPPING = {
    # Đòn bẩy và Khả năng trả nợ
    "STD_RTD146": "high_good",   # FFO / Nợ vay - Cao hơn → tốt hơn
    "STD_RTD71": "low_good",     # Hệ số Nợ vay/Vốn CSH - Thấp hơn → tốt hơn
    "STD_RTD96": "low_good",     # Tổng nợ vay thuần/EBITDA - Thấp hơn → tốt hơn
    "STD_RTD97": "high_good",    # EBITDA/Chi phí lãi vay - Cao hơn → tốt hơn
    "STD_RTD98": "high_good",    # CFO/Tổng nợ vay - Cao hơn → tốt hơn
    "STD_RTD99": "high_good",    # Lợi nhuận hoạt động/ Lãi vay - Cao hơn → tốt hơn
    "STD_RTD1": "low_good",      # Tổng tài sản/Vốn chủ sở hữu - Thấp hơn → tốt hơn
    "STD_RTD72": "high_good",    # Hệ số EBIT/Nợ vay - Cao hơn → tốt hơn
    "STD_RTD148": "low_good",    # Tổng nợ vay/EBITDA - Thấp hơn → tốt hơn
    
    # Hiệu quả hoạt động
    "STD_RTD74": "high_good",    # Vòng quay khoản phải thu - Cao hơn → tốt hơn
    "STD_RTD76": "high_good",    # Vòng quay vốn lưu động - Cao hơn → tốt hơn
    "STD_RTD77": "high_good",    # EBITDA/Tổng Tài sản - Cao hơn → tốt hơn
    "STD_RTD78": "high_good",    # Vòng quay tổng tài sản - Cao hơn → tốt hơn
    "STD_RTD81": "low_good",     # Chu kỳ tiền mặt - Thấp hơn → tốt hơn
    "STD_RTD64": "low_good",     # Vòng quay khoản phải trả - Thấp hơn → tốt hơn
    "STD_RTD75": "high_good",    # Vòng quay hàng tồn kho - Cao hơn → tốt hơn
    
    # Quy mô (cao hơn = quy mô lớn hơn, thường tốt hơn)
    "STD_RTD13": "high_good",    # Tổng tài sản
    "STD_RTD14": "high_good",    # Vốn chủ sở hữu
    "STD_RTD31": "high_good",    # Doanh thu hoạt động TTM
    "empl_qtty": "high_good",    # Số lượng nhân viên
    
    # Khả Năng Sinh Lời
    "STD_RTD26": "high_good",    # Biên lợi nhuận trước lãi vay, thuế và khấu hao
    "STD_RTD8": "high_good",     # ROA
    "STD_RTD82": "high_good",    # ROCE
    "STD_RTD83": "high_good",    # Biên lợi nhuận trước lãi vay và thuế
    "STD_RTD84": "high_good",    # Biên lợi nhuận hoạt động
    "STD_RTD85": "high_good",    # Biên lợi nhuận gộp
    "STD_RTD86": "high_good",    # Biên LNST
    "STD_RTD9": "high_good",     # ROE
    
    # Khả Năng Tăng Trưởng
    "STD_RTD11": "high_good",    # Lợi nhuận sau thuế (YoY)
    "STD_RTD28": "high_good",    # Doanh thu TTM (YoY)
    "STD_RTD87": "high_good",    # EBIT TTM (YoY)
    "STD_RTD88": "high_good",    # Tăng trưởng tài sản
    "STD_RTD89": "high_good",    # Tăng trưởng vốn chủ sở hữu
    
    # Khả Năng Thanh Khoản
    "STD_RTD118": "high_good",   # Thanh khoản - Dòng tiền
    "STD_RTD92": "high_good",    # Chỉ số thanh toán ngắn hạn
    "STD_RTD93": "high_good",    # Chỉ số thanh toán nhanh
    "STD_RTD94": "high_good",    # Chỉ số thanh toán tức thời
    "STD_RTD95": "high_good",    # CFO/Nợ ngắn hạn
    "STD_RTD147": "high_good"    # (FFO + Cash) / Nợ vay ngắn hạn
}