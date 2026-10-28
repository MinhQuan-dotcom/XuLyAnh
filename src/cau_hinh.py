"""
Tham số mặc định của baseline và phương pháp đề xuất.

Quy ước:
- Mọi tham số đều nằm ở đây, không viết cứng con số trong code.
- Tham số chỉ được chọn trên tập dev (thí nghiệm E2). Không chỉnh theo kết quả trên tập eval.
- Khi chốt tham số sau E2, sửa giá trị ở đây và ghi ngày chốt vào comment.
"""

# ----------------------------------------------------------------- baseline (phần E)
THAM_SO_BASELINE = {
    'kich_thuoc_lam_mo': 5,        # kernel Gaussian (số lẻ) – phần A
    'co_mat_na': 10,               # px co mặt nạ giấy vào khi tách vật – phần D
    'dien_tich_toi_thieu': 200,    # px, bỏ vùng nhỏ hơn khi tách vật – phần D
}

# ----------------------------------------------------------------- phương pháp đề xuất
THAM_SO_DE_XUAT = {
    # Phần A: tìm tờ giấy
    'kich_thuoc_lam_mo': 5,
    # Phần D: tách vật (trên ảnh đã nắn)
    'co_mat_na': 10,
    'dien_tich_toi_thieu': 200,
    # Phần B: tinh chỉnh góc giấy
    'canny_thap': 50,
    'canny_cao': 150,
    'do_rong_dai_canh': 8,         # px: lấy điểm Canny cách cạnh thô không quá giá trị này
    'bo_dau_canh': 0.10,           # bỏ 10% chiều dài mỗi đầu cạnh khi khớp đường thẳng
    # Phần C: nắn ảnh
    'do_phan_giai_nan': 4.0,       # px/mm của ảnh sau khi nắn
    # Công tắc cho thí nghiệm E3 (ablation) – phương pháp PHẢI tôn trọng hai công tắc này
    'nan_anh': True,               # False: bỏ bước nắn, đo bằng một tỉ lệ duy nhất như baseline
    'tinh_chinh_goc': True,        # False: dùng thẳng 4 đỉnh thô của bước 1
    # Dùng hàm DLT tự viết thay cho cv2.findHomography
    'dung_dlt_tu_viet': False,
}

# ----------------------------------------------------------------- đánh giá
NGUONG_DAT_MM = 1.0                # sai số tối đa chấp nhận (e_max trong bản tuyên bố)
