"""
BASELINE – cách đo thông thường (giả định ảnh chụp thẳng).
Người phụ trách: N3. Hạn: 01/11.

Ý tưởng: tìm tờ giấy, lấy chiều rộng của nó (pixel) chia cho 210 mm ra MỘT tỉ lệ px/mm cho cả ảnh,
rồi đo vật bằng hình chữ nhật bao nhỏ nhất trên ảnh gốc. Cách này đúng khi chụp thẳng, sai dần khi
chụp nghiêng – đó chính là điều thí nghiệm E1 cần cho thấy.

Các bước gợi ý:
  1. Chuyển ảnh xám, làm mờ Gaussian (tham_so['kich_thuoc_lam_mo']).
  2. Phân ngưỡng Otsu để tách tờ giấy trắng khỏi nền tối; lấy đường viền lớn nhất = tờ giấy.
  3. cv2.minAreaRect(đường viền giấy) -> cạnh ngắn (px) / 210 mm = ti_le (px/mm).
  4. Tách vật: trong vùng tờ giấy, điểm ảnh khác màu trắng của giấy (ví dụ ngưỡng trên kênh
     bão hòa S của HSV hoặc độ sáng thấp hơn giấy). Lấy đường viền lớn nhất bên trong giấy.
  5. cv2.minAreaRect(đường viền vật) -> (w, h) px -> chia ti_le -> mm.

KHÔNG đọc nhãn (labels.csv) trong file này. Hàm chỉ nhận ảnh.
"""
import numpy as np
import cv2

from src.cau_hinh import THAM_SO_BASELINE


def do_kich_thuoc(anh, tham_so=None):
    """
    Đầu vào : anh – ảnh BGR (numpy array) đọc bằng cv2.imread.
              tham_so – dict, mặc định THAM_SO_BASELINE.
    Đầu ra  : (dai_mm, rong_mm, anh_trung_gian)
              dai_mm >= rong_mm. Không đo được thì trả (None, None, anh_trung_gian).
              anh_trung_gian: dict {ten_buoc: anh BGR} để vẽ hình cho báo cáo.
    """
    tham_so = {**THAM_SO_BASELINE, **(tham_so or {})}
    anh_trung_gian = {'goc': anh}

    # TODO (N3): cài đặt các bước 1-5 ở đầu file.

    return None, None, anh_trung_gian
