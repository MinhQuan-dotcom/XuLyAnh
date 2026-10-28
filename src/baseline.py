"""
PHẦN E (1/2) – BASELINE: cách đo thông thường, giả định ảnh chụp thẳng.
Người làm: ........   Hạn: 01/11   Kiểm tra: python tests/kiem_tra_E.py

Baseline GHÉP các hàm của phần A và D – không viết lại chúng:
  1. goc, mat_na = giay.tim_to_giay(anh, tham_so)                       (phần A)
  2. ti_le (px/mm) = cạnh ngắn của cv2.minAreaRect(goc) / 210
  3. contour = vat.tach_vat(anh, mat_na, tham_so)                         (phần D)
  4. dai_px, rong_px = vat.kich_thuoc_px(contour)                         (phần D)
  5. trả về dai_px / ti_le, rong_px / ti_le

Phần E KHÔNG cần chờ A và D: tests/kiem_tra_E.py thay tạm A và D bằng kết quả lấy từ nhãn.
BẮT BUỘC gọi theo dạng giay.tim_to_giay(...) và vat.tach_vat(...) (import module, không
`from src.giay import tim_to_giay`) để file kiểm tra thay tạm được.

Đầu vào / đầu ra theo docs/QUY_UOC.md:
  do_kich_thuoc(anh, tham_so=None) -> (dai_mm, rong_mm, anh_trung_gian)
  không đo được -> (None, None, anh_trung_gian)
"""
import numpy as np
import cv2

from src import giay, vat
from src.cau_hinh import THAM_SO_BASELINE


def ve_ket_qua(anh, goc=None, contour=None):
    """(Có sẵn) Vẽ 4 góc giấy (đỏ) và đường viền vật (xanh) lên bản sao của ảnh – dùng làm ảnh trung gian."""
    out = anh.copy()
    if goc is not None:
        for x, y in np.asarray(goc):
            cv2.circle(out, (int(round(x)), int(round(y))), 8, (0, 0, 255), 3)
        cv2.polylines(out, [np.round(goc).astype(np.int32).reshape(-1, 1, 2)], True, (0, 0, 255), 2)
    if contour is not None:
        cv2.drawContours(out, [contour], -1, (0, 200, 0), 2)
    return out


def do_kich_thuoc(anh, tham_so=None):
    tham_so = {**THAM_SO_BASELINE, **(tham_so or {})}
    anh_trung_gian = {'goc': anh}

    # TODO (Phần E): ghép các bước 1-5 ở đầu file.
    # Nhớ thêm ảnh trung gian, ví dụ anh_trung_gian['ket_qua'] = ve_ket_qua(anh, goc, contour)

    return None, None, anh_trung_gian
