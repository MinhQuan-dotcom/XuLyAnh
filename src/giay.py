# Phần A: tìm tờ giấy A4 trong ảnh
# Người làm: ........
# Kiểm tra: python tests/kiem_tra_A.py

import numpy as np
import cv2


def sap_xep_4_goc(diem):
    # Sắp 4 điểm theo thứ tự trên-trái, trên-phải, dưới-phải, dưới-trái.
    # Sắp theo góc quanh trọng tâm rồi lấy cạnh có y nhỏ nhất làm cạnh trên,
    # để không bị sai khi giấy nghiêng nhiều (thành hình thang dẹt).
    diem = np.asarray(diem, dtype=np.float64).reshape(4, 2)
    tam = diem.mean(0)
    diem = diem[np.argsort(np.arctan2(diem[:, 1] - tam[1], diem[:, 0] - tam[0]))]
    i = int(np.argmin([diem[k, 1] + diem[(k + 1) % 4, 1] for k in range(4)]))
    return np.roll(diem, -i, axis=0)


def tim_to_giay(anh, tham_so):
    """
    Tìm tờ giấy trắng trên nền bàn tối.

    anh: ảnh BGR
    tham_so: dict, dùng 'kich_thuoc_lam_mo'
    Trả về (goc, mat_na):
      goc: mảng (4, 2) tọa độ 4 góc, đã sắp bằng sap_xep_4_goc
      mat_na: ảnh uint8 cùng cỡ với anh, 255 trong tờ giấy, 0 ngoài
    Không tìm thấy thì trả (None, None).

    Hướng làm: ảnh xám -> GaussianBlur -> threshold Otsu -> findContours -> lấy contour lớn nhất
    -> approxPolyDP (epsilon khoảng 0.02 * chu vi) phải ra 4 điểm.
    Chú ý: chụp nghiêng nhiều (từ khoảng 55 độ) thì bức tường sáng phía sau lọt vào ảnh,
    có thể to hơn tờ giấy, nên bỏ các contour chạm mép ảnh.
    """
    # TODO
    return None, None
