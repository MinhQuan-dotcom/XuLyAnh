# Phần B: chỉnh lại 4 góc tờ giấy cho chính xác hơn
# Người làm: ........
# Kiểm tra: python tests/kiem_tra_B.py
#
# Ý tưởng: góc lấy từ approxPolyDP hay lệch vài pixel vì góc giấy bị mờ / bo tròn.
# Mỗi cạnh giấy có rất nhiều điểm biên, khớp một đường thẳng qua các điểm đó rồi lấy
# giao điểm 2 cạnh kề nhau làm góc mới thì sẽ ổn định hơn.

import numpy as np
import cv2


def giao_diem(duong1, duong2):
    # Giao điểm 2 đường thẳng dạng (vx, vy, x0, y0) như cv2.fitLine trả về.
    # Hai đường song song thì trả None.
    vx1, vy1, x1, y1 = [float(v) for v in np.ravel(duong1)]
    vx2, vy2, x2, y2 = [float(v) for v in np.ravel(duong2)]
    A = np.array([[vx1, -vx2], [vy1, -vy2]])
    if abs(np.linalg.det(A)) < 1e-9:
        return None
    t = np.linalg.solve(A, np.array([x2 - x1, y2 - y1]))
    return np.array([x1 + t[0] * vx1, y1 + t[0] * vy1])


def tinh_chinh_goc(anh, goc_tho, tham_so):
    """
    anh: ảnh BGR
    goc_tho: mảng (4, 2), thứ tự trên-trái, trên-phải, dưới-phải, dưới-trái
    tham_so: dùng 'canny_thap', 'canny_cao', 'do_rong_dai_canh', 'bo_dau_canh'
    Trả về mảng (4, 2) cùng thứ tự. Cạnh nào không đủ điểm thì trả lại goc_tho.

    Hướng làm:
    - Canny lấy điểm biên.
    - Với cạnh i (từ goc_tho[i] đến goc_tho[(i+1)%4]): giữ các điểm cách cạnh không quá
      'do_rong_dai_canh' px, bỏ một đoạn 'bo_dau_canh' ở hai đầu (gần góc), rồi cv2.fitLine.
    - Góc mới i = giao_diem(cạnh i-1, cạnh i).
    """
    # TODO
    return np.asarray(goc_tho, dtype=np.float64)
