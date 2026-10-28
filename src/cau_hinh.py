# Tham số mặc định. Không ghi số cứng trong code, để hết ở đây.
# Tham số chỉ chọn dựa trên tập dev (E2). Chốt xong thì sửa ở đây và ghi lại ngày.

THAM_SO_BASELINE = {
    'kich_thuoc_lam_mo': 5,        # kernel Gaussian, số lẻ (phần A)
    'co_mat_na': 10,               # px, co mặt nạ giấy khi tách vật (phần D)
    'dien_tich_toi_thieu': 200,    # px, bỏ vùng nhỏ hơn khi tách vật (phần D)
}

THAM_SO_DE_XUAT = {
    # phần A
    'kich_thuoc_lam_mo': 5,
    # phần D
    'co_mat_na': 10,
    'dien_tich_toi_thieu': 200,
    # phần B
    'canny_thap': 50,
    'canny_cao': 150,
    'do_rong_dai_canh': 8,         # px, chỉ lấy điểm biên gần cạnh thô
    'bo_dau_canh': 0.10,           # bỏ 10% mỗi đầu cạnh khi khớp đường thẳng
    # phần C
    'do_phan_giai_nan': 4.0,       # px / mm của ảnh nắn
    'dung_dlt_tu_viet': False,     # True: dùng hàm DLT tự viết thay cho cv2.findHomography
    # công tắc cho E3
    'nan_anh': True,
    'tinh_chinh_goc': True,
}

NGUONG_DAT_MM = 1.0                # sai số chấp nhận được (e_max)
