# Phần D: tách vật khỏi tờ giấy và đo kích thước theo pixel
# Người làm: ........
# Kiểm tra: python tests/kiem_tra_D.py

# Baseline gọi trên ảnh gốc, phương pháp của nhóm gọi trên ảnh đã nắn.

import cv2
import numpy as np


def tach_vat(anh, mat_na=None, tham_so=None):
    """
    Tách vật thể khỏi nền giấy.

    Args:
        anh: Ảnh đầu vào dạng BGR.
        mat_na: Mask giấy, pixel 255 là vùng giấy.
               Nếu None thì xem toàn bộ ảnh là vùng giấy.
        tham_so: Dictionary chứa các tham số tùy chỉnh.

    Returns:
        Contour lớn nhất của vật thể hoặc None nếu không tìm thấy.
    """
    if anh is None or anh.size == 0:
        return None

    if len(anh.shape) != 3 or anh.shape[2] != 3:
        return None

    tham_so = tham_so or {}

    co_mat_na = int(tham_so.get("co_mat_na", 10))
    dien_tich_toi_thieu = float(
        tham_so.get("dien_tich_toi_thieu", 200)
    )
    nguong_s = int(tham_so.get("nguong_s", 60))
    nguong_v = int(tham_so.get("nguong_v", 80))

    chieu_cao, chieu_rong = anh.shape[:2]

    # 1. Tạo mask vùng giấy
    if mat_na is None:
        mask_giay = np.full(
            (chieu_cao, chieu_rong),
            255,
            dtype=np.uint8
        )
    else:
        if mat_na.shape[:2] != (chieu_cao, chieu_rong):
            return None

        if len(mat_na.shape) == 3:
            mask_giay = cv2.cvtColor(
                mat_na,
                cv2.COLOR_BGR2GRAY
            )
        else:
            mask_giay = mat_na.copy()

        _, mask_giay = cv2.threshold(
            mask_giay,
            127,
            255,
            cv2.THRESH_BINARY
        )

    # 2. Erosion mask giấy để loại bỏ vùng sát biên giấy
    if co_mat_na > 0:
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (2 * co_mat_na + 1, 2 * co_mat_na + 1)
        )

        mask_giay = cv2.erode(
            mask_giay,
            kernel,
            iterations=1
        )

    # 3. Chuyển ảnh sang HSV
    hsv = cv2.cvtColor(anh, cv2.COLOR_BGR2HSV)

    # Tách các pixel có màu bão hòa hoặc có độ sáng thấp
    kenh_s = hsv[:, :, 1]
    kenh_v = hsv[:, :, 2]

    mask_mau = cv2.inRange(
        kenh_s,
        nguong_s + 1,
        255
    )

    mask_toi = cv2.inRange(
        kenh_v,
        0,
        nguong_v - 1
    )

    # 4. Kết hợp hai điều kiện:
    # S > nguong_s HOẶC V < nguong_v
    mask_vat = cv2.bitwise_or(
        mask_mau,
        mask_toi
    )

    # 5. Chỉ giữ vùng nằm bên trong giấy
    mask_vat = cv2.bitwise_and(
        mask_vat,
        mask_giay
    )

    # 6. Tìm contour bên ngoài
    contours, _ = cv2.findContours(
        mask_vat.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # 7. Lọc contour theo diện tích
    contours_hop_le = [
        contour
        for contour in contours
        if cv2.contourArea(contour) >= dien_tich_toi_thieu
    ]

    if not contours_hop_le:
        return None

    # 8. Lấy contour có diện tích lớn nhất
    contour_lon_nhat = max(
        contours_hop_le,
        key=cv2.contourArea
    )

    return contour_lon_nhat


def kich_thuoc_px(contour):
    """
    Tính chiều dài và chiều rộng vật thể theo pixel
    bằng hình chữ nhật xoay nhỏ nhất (minAreaRect).

    Returns:
        (dai_px, rong_px), trong đó dai_px >= rong_px.
        Nếu contour không hợp lệ thì trả về (None, None).
    """
    if contour is None:
        return None, None

    if len(contour) < 3:
        return None, None

    diem = np.asarray(contour, dtype=np.float32)

    if not np.all(np.isfinite(diem)):
        return None, None

    # Tìm hình chữ nhật xoay nhỏ nhất
    hinh_chu_nhat = cv2.minAreaRect(diem)

    # minAreaRect trả về:
    # ((center_x, center_y), (width, height), angle)
    (_, _), (rong, cao), goc = hinh_chu_nhat

    if not np.isfinite(rong) or not np.isfinite(cao):
        return None, None

    if rong <= 0 or cao <= 0:
        return None, None

    dai_px = max(rong, cao)
    rong_px = min(rong, cao)

    return float(dai_px), float(rong_px)