# Phần C: homography và nắn ảnh
# Người làm: Đoàn
# Kiểm tra: python tests/kiem_tra_C.py
# Ý tưởng: Dùng thuật toán DLT (Direct Linear Transformation) để tự tính ma trận 
# homography từ các cặp điểm tương ứng bằng cách thiết lập hệ phương trình Ah = 0 
# và giải bằng phân rã SVD, sau đó kết hợp với tỷ lệ pixel để nắn ảnh chính diện.

import numpy as np
import cv2

# 4 góc tờ A4 theo mm, cùng thứ tự với giay.sap_xep_4_got
A4_MM = np.array([[0, 0], [210, 0], [210, 297], [0, 297]], dtype=np.float64)


def tinh_homography_dlt(diem_nguon, diem_dich):
    """
    Tính homography bằng DLT, không dùng cv2.findHomography.
    diem_nguon, diem_dich: mảng (4, 2) (hoặc nhiều điểm hình)
    Trả về H (3, 3) với H[2, 2] = 1.
    """
    n = diem_nguon.shape[0]
    A = []
    for i in range(n):
        x, y = diem_nguon[i]
        u, v = diem_dich[i]
        # Mỗi cặp điểm (x, y) -> (u, v) cho 2 dòng của ma trận A:
        A.append([-x, -y, -1,  0,  0,  0,  x * u,  y * u,  u])
        A.append([ 0,  0,  0, -x, -y, -1,  x * v,  y * v,  v])
    
    A = np.array(A, dtype=np.float64)
    
    # Giải bằng SVD, h là dòng cuối của Vt
    _, _, Vt = np.linalg.svd(A)
    h = Vt[-1]
    
    # Reshape về ma trận (3, 3) và chuẩn hóa sao cho H[2, 2] = 1
    H = h.reshape(3, 3)
    if H[2, 2] != 0:
        H = H / H[2, 2]
    return H


def tinh_homography(goc_anh, tu_viet=False):
    """
    H chuyển tọa độ ảnh (px) sang tọa độ trên tờ giấy (mm)
    """
    goc_anh = np.asarray(goc_anh, dtype=np.float64)
    if tu_viet:
        return tinh_homography_dlt(goc_anh, A4_MM)
    
    H, _ = cv2.findHomography(goc_anh, A4_MM)
    return H


def nan_anh(anh, goc, s, tu_viet=False):
    """
    Nắn ảnh về nhìn thẳng từ giấy.
    goc: 4 góc giấy (4, 2) theo thứ tự trên-trái, trên-phải, dưới-phải, dưới-trái
    s: số pixel trên 1 mm (ví dụ 4)
    Trả về (anh_nan, M):
        anh_nan: ảnh cao round(297*s), rộng round(210*s)
        M: ma trận (3, 3) chuyển tọa độ ảnh gốc sang tọa độ ảnh nắn
    Gợi ý: M = diag(s, s, 1) @ H, rồi cv2.warpPerspective.
    """
    H = tinh_homography(goc, tu_viet=tu_viet)
    if H is None:
        return None, None
        
    rong = round(210 * s)
    cao = round(297 * s)
    
    # Tính ma trận biến đổi M = diag(s, s, 1) @ H
    S = np.diag([s, s, 1.0])
    M = S @ H
    
    # Nắn ảnh bằng cv2.warpPerspective
    anh_nan = cv2.warpPerspective(anh, M, (rong, cao))
    return anh_nan, M
 
