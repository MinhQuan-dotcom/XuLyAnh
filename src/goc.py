"""
PHẦN B – Tinh chỉnh 4 góc tờ giấy bằng giao điểm của các đường thẳng khớp theo cạnh.
Người làm: ........   Hạn: 01/11   Kiểm tra: python tests/kiem_tra_B.py

Đây là phần "nhóm tự thêm" của phương pháp (mức tính mới). Phần B KHÔNG cần chờ phần A:
file kiểm tra lấy góc đúng từ nhãn, cộng nhiễu vài pixel làm "góc thô" để thử.
"""
import numpy as np
import cv2


def giao_diem(duong1, duong2):
    """(Có sẵn) Giao điểm của 2 đường thẳng, mỗi đường dạng (vx, vy, x0, y0) như cv2.fitLine trả về.
    Trả về numpy (x, y) hoặc None nếu hai đường song song."""
    vx1, vy1, x1, y1 = [float(v) for v in np.ravel(duong1)]
    vx2, vy2, x2, y2 = [float(v) for v in np.ravel(duong2)]
    A = np.array([[vx1, -vx2], [vy1, -vy2]])
    if abs(np.linalg.det(A)) < 1e-9:
        return None
    t = np.linalg.solve(A, np.array([x2 - x1, y2 - y1]))
    return np.array([x1 + t[0] * vx1, y1 + t[0] * vy1])


def tinh_chinh_goc(anh, goc_tho, tham_so):
    """
    Đầu vào
      anh     : ảnh BGR
      goc_tho : numpy (4, 2) – 4 góc thô theo thứ tự trên-trái, trên-phải, dưới-phải, dưới-trái
      tham_so : dict, dùng
                'canny_thap', 'canny_cao'  – ngưỡng Canny
                'do_rong_dai_canh'         – chỉ lấy điểm cạnh cách cạnh thô không quá bấy nhiêu pixel
                'bo_dau_canh'              – bỏ tỉ lệ này ở mỗi đầu cạnh (gần góc) khi khớp đường
    Đầu ra
      numpy (4, 2) – 4 góc đã tinh chỉnh, CÙNG thứ tự. Cạnh nào không đủ điểm thì trả lại goc_tho.

    Gợi ý các bước
      1. Ảnh xám -> cv2.Canny -> lấy tọa độ các điểm cạnh (np.argwhere hoặc np.nonzero).
      2. Với mỗi cạnh i (nối goc_tho[i] và goc_tho[(i+1) % 4]):
         - tính khoảng cách từ mỗi điểm cạnh tới đoạn thẳng đó, và vị trí chiếu t (0 = đầu, 1 = cuối);
         - giữ điểm có khoảng cách <= do_rong_dai_canh và bo_dau_canh <= t <= 1 - bo_dau_canh;
         - cv2.fitLine(diem, cv2.DIST_L2, 0, 0.01, 0.01) -> đường thẳng (vx, vy, x0, y0).
           (Có thể thử cv2.DIST_HUBER để bớt ảnh hưởng của điểm nhiễu – nêu trong E2.)
      3. Góc mới thứ i = giao_diem(đường của cạnh (i-1), đường của cạnh i).
    """
    # TODO (Phần B)
    return np.asarray(goc_tho, dtype=np.float64)
