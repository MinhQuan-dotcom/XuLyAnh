# Phần D: tách vật khỏi tờ giấy và đo kích thước theo pixel
# Người làm: ........
# Kiểm tra: python tests/kiem_tra_D.py
#
# Baseline gọi trên ảnh gốc, phương pháp của nhóm gọi trên ảnh đã nắn.

import numpy as np
import cv2


def tach_vat(anh, mat_na=None, tham_so=None):
    """
    Tìm contour của vật (vật có màu hoặc tối, nằm trên giấy trắng).

    anh: ảnh BGR
    mat_na: uint8, 255 là vùng tờ giấy. None nghĩa là cả ảnh là giấy (ảnh đã nắn),
            khi đó bỏ một viền 'co_mat_na' px quanh mép vì mép có thể dính nền bàn.
    tham_so: có thể None. Dùng 'co_mat_na' (mặc định 10) và 'dien_tich_toi_thieu' (mặc định 200).
    Trả về contour lớn nhất (dạng như cv2.findContours trả về), không có thì None.

    Hướng làm: đổi sang HSV, giấy thì S thấp V cao, vật thì S cao hoặc V thấp.
    Co mặt nạ lại (erode) để không lấy nhầm mép bàn, mở/đóng hình thái để bỏ nhiễu,
    findContours lấy contour lớn nhất.
    Chú ý bóng của vật hơi tối, ngưỡng V thấp quá sẽ lấy luôn bóng làm vật to ra.
    """
    # TODO
    return None


def kich_thuoc_px(contour):
    # Trả về (dai_px, rong_px), dai_px >= rong_px, lấy từ cv2.minAreaRect
    # TODO
    return None, None
