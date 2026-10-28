"""
PHẦN C – Homography và nắn ảnh.
Người làm: ........   Hạn: 01/11   Kiểm tra: python tests/kiem_tra_C.py

Phần C KHÔNG cần chờ phần A: file kiểm tra lấy 4 góc đúng từ nhãn để thử.
"""
import numpy as np
import cv2

# Kích thước tờ A4 (mm), thứ tự góc khớp với giay.sap_xep_4_goc: trên-trái, trên-phải, dưới-phải, dưới-trái
A4_MM = np.array([[0, 0], [210, 0], [210, 297], [0, 297]], dtype=np.float64)


def tinh_homography_dlt(diem_nguon, diem_dich):
    """
    Tự viết phép tính homography bằng DLT (Direct Linear Transform), KHÔNG dùng cv2.findHomography.

    Đầu vào : diem_nguon, diem_dich – numpy (4, 2) (hoặc nhiều hơn 4 điểm)
    Đầu ra  : H – numpy (3, 3), sao cho [x', y', 1] ~ H @ [x, y, 1], đã chuẩn hóa H[2, 2] = 1

    Gợi ý
      Mỗi cặp (x, y) -> (x', y') cho 2 hàng của ma trận A:
        [-x, -y, -1,  0,  0,  0, x*x', y*x', x']
        [ 0,  0,  0, -x, -y, -1, x*y', y*y', y']
      Nghiệm h là vector kỳ dị phải ứng với giá trị kỳ dị nhỏ nhất:
        _, _, Vt = np.linalg.svd(A);  h = Vt[-1]
      H = h.reshape(3, 3) / h[8]
      (Nâng cao, nên làm: chuẩn hóa tọa độ trước (Hartley normalization) để ổn định số.)
    """
    # TODO (Phần C)
    raise NotImplementedError


def tinh_homography(goc_anh, tu_viet=False):
    """(Có sẵn) H biến tọa độ ảnh (px) -> tọa độ trên tờ giấy (mm)."""
    goc_anh = np.asarray(goc_anh, dtype=np.float64)
    if tu_viet:
        return tinh_homography_dlt(goc_anh, A4_MM)
    H, _ = cv2.findHomography(goc_anh, A4_MM)
    return H


def nan_anh(anh, goc, s, tu_viet=False):
    """
    Nắn ảnh về nhìn thẳng tờ giấy.

    Đầu vào
      anh     : ảnh BGR
      goc     : numpy (4, 2) – 4 góc giấy (trên-trái, trên-phải, dưới-phải, dưới-trái), pixel
      s       : độ phân giải ảnh nắn, pixel / mm (ví dụ 4.0)
      tu_viet : True thì dùng tinh_homography_dlt
    Đầu ra
      (anh_nan, M)
      anh_nan : ảnh BGR kích thước (cao = round(297*s), rộng = round(210*s)); 1 mm = s pixel theo mọi hướng
      M       : numpy (3, 3) biến tọa độ ảnh gốc (px) -> tọa độ ảnh nắn (px)

    Gợi ý
      H = tinh_homography(goc, tu_viet)            # ảnh -> mm
      S = np.diag([s, s, 1.0])                     # mm -> pixel ảnh nắn
      M = S @ H
      anh_nan = cv2.warpPerspective(anh, M, (rộng, cao), flags=cv2.INTER_LINEAR)
    """
    # TODO (Phần C)
    return None, None
