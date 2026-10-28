# Phần C: homography và nắn ảnh
# Người làm: ........
# Kiểm tra: python tests/kiem_tra_C.py

import numpy as np
import cv2

# 4 góc tờ A4 theo mm, cùng thứ tự với giay.sap_xep_4_goc
A4_MM = np.array([[0, 0], [210, 0], [210, 297], [0, 297]], dtype=np.float64)


def tinh_homography_dlt(diem_nguon, diem_dich):
    """
    Tự tính homography bằng DLT, không dùng cv2.findHomography.
    diem_nguon, diem_dich: mảng (4, 2) (hoặc nhiều điểm hơn)
    Trả về H (3, 3) với H[2, 2] = 1.

    Mỗi cặp điểm (x, y) -> (u, v) cho 2 dòng của ma trận A:
      [-x, -y, -1,  0,  0,  0, x*u, y*u, u]
      [ 0,  0,  0, -x, -y, -1, x*v, y*v, v]
    Giải bằng SVD, h là dòng cuối của Vt, rồi reshape (3, 3) và chia cho h[8].
    """
    # TODO
    raise NotImplementedError


def tinh_homography(goc_anh, tu_viet=False):
    # H chuyển tọa độ ảnh (px) sang tọa độ trên tờ giấy (mm)
    goc_anh = np.asarray(goc_anh, dtype=np.float64)
    if tu_viet:
        return tinh_homography_dlt(goc_anh, A4_MM)
    H, _ = cv2.findHomography(goc_anh, A4_MM)
    return H


def nan_anh(anh, goc, s, tu_viet=False):
    """
    Nắn ảnh về nhìn thẳng tờ giấy.
    goc: 4 góc giấy (4, 2) theo thứ tự trên-trái, trên-phải, dưới-phải, dưới-trái
    s: số pixel trên 1 mm của ảnh nắn (ví dụ 4)
    Trả về (anh_nan, M):
      anh_nan: ảnh cao round(297*s), rộng round(210*s)
      M: ma trận (3, 3) chuyển tọa độ ảnh gốc sang tọa độ ảnh nắn

    Gợi ý: M = diag(s, s, 1) @ H, rồi cv2.warpPerspective.
    """
    # TODO
    return None, None
