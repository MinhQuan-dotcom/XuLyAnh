# Phần E: baseline - cách đo thông thường, coi như ảnh chụp thẳng
# Người làm: ........
# Kiểm tra: python tests/kiem_tra_E.py
#
# Các bước (dùng lại hàm của phần A và D, không viết lại):
#   1. goc, mat_na = giay.tim_to_giay(anh, tham_so)
#   2. ti_le (px/mm) = cạnh ngắn của cv2.minAreaRect(goc) / 210
#   3. contour = vat.tach_vat(anh, mat_na, tham_so)
#   4. dai_px, rong_px = vat.kich_thuoc_px(contour)
#   5. trả về dai_px / ti_le, rong_px / ti_le
#
# Gọi hàm dạng giay.tim_to_giay(...), vat.tach_vat(...) (import cả module) để file kiểm tra
# thay tạm được khi phần A, D chưa xong.

import numpy as np
import cv2

from src import giay, vat
from src.cau_hinh import THAM_SO_BASELINE


def ve_ket_qua(anh, goc=None, contour=None):
    # Vẽ góc giấy (đỏ) và viền vật (xanh) lên bản sao của ảnh để xem kết quả
    out = anh.copy()
    if goc is not None:
        for x, y in np.asarray(goc):
            cv2.circle(out, (int(round(x)), int(round(y))), 8, (0, 0, 255), 3)
        cv2.polylines(out, [np.round(goc).astype(np.int32).reshape(-1, 1, 2)], True, (0, 0, 255), 2)
    if contour is not None:
        cv2.drawContours(out, [contour], -1, (0, 200, 0), 2)
    return out


def do_kich_thuoc(anh, tham_so=None):
    # Trả về (dai_mm, rong_mm, anh_trung_gian), không đo được thì (None, None, anh_trung_gian)
    tham_so = {**THAM_SO_BASELINE, **(tham_so or {})}
    anh_trung_gian = {'goc': anh}

    # TODO: làm các bước 1-5 ở trên
    # nhớ lưu ảnh kết quả: anh_trung_gian['ket_qua'] = ve_ket_qua(anh, goc, contour)

    return None, None, anh_trung_gian
