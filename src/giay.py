# Phần A: tìm tờ giấy A4 trong ảnh
# Người làm: An
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


def _xap_xi_tu_giac(contour):
    """Tìm 4 đỉnh tứ giác từ contour bằng cách quét epsilon tăng dần."""
    chu_vi = cv2.arcLength(contour, True)
    # Quét epsilon từ nhỏ đến lớn để giữ độ chính xác góc cao nhất
    for he_so in np.linspace(0.005, 0.05, 91):
        xap_xi = cv2.approxPolyDP(contour, he_so * chu_vi, True)
        if len(xap_xi) == 4 and cv2.isContourConvex(xap_xi):
            return xap_xi.reshape(4, 2).astype(np.float64)

    # Dự phòng 1: tìm trên bao lồi (convex hull)
    hull = cv2.convexHull(contour)
    chu_vi_hull = cv2.arcLength(hull, True)
    for he_so in np.linspace(0.01, 0.08, 71):
        xap_xi = cv2.approxPolyDP(hull, he_so * chu_vi_hull, True)
        if len(xap_xi) == 4 and cv2.isContourConvex(xap_xi):
            return xap_xi.reshape(4, 2).astype(np.float64)

    # Dự phòng 2: hình chữ nhật xoay diện tích nhỏ nhất
    hop = cv2.minAreaRect(contour)
    goc_hop = cv2.boxPoints(hop)
    return goc_hop.astype(np.float64)


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
    if anh is None:
        return None, None

    h, w = anh.shape[:2]
    ksize = int(tham_so.get('kich_thuoc_lam_mo', 5)) if tham_so else 5
    if ksize % 2 == 0:
        ksize += 1

    # 1. Tiền xử lý: chuyển xám và làm mờ Gauss giảm nhiễu
    xam = cv2.cvtColor(anh, cv2.COLOR_BGR2GRAY)
    lam_mo = cv2.GaussianBlur(xam, (ksize, ksize), 0)

    # 2. Ngưỡng hóa Otsu tách giấy sáng khỏi nền bàn tối
    _, nhi_phan = cv2.threshold(lam_mo, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 3. Tìm các đường viền ngoài
    duong_viens, _ = cv2.findContours(nhi_phan, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not duong_viens:
        return None, None

    # 4. Lọc các đường viền hợp lệ (bỏ vùng tường chạm mép ảnh và vùng quá nhỏ)
    dien_tich_nho_nhat = (h * w) * 0.03
    ung_vien = []
    khoang_cach_mep = 3

    for c in duong_viens:
        x_box, y_box, w_box, h_box = cv2.boundingRect(c)
        # Bỏ contour chạm sát biên ảnh (như bức tường ở phía trên)
        if (x_box <= khoang_cach_mep or y_box <= khoang_cach_mep or
                x_box + w_box >= w - khoang_cach_mep or y_box + h_box >= h - khoang_cach_mep):
            continue

        dien_tich = cv2.contourArea(c)
        if dien_tich < dien_tich_nho_nhat:
            continue

        ung_vien.append((dien_tich, c))

    # Dự phòng nếu tất cả contour đều chạm mép (ảnh đặc biệt hoặc không có tường)
    if not ung_vien:
        for c in duong_viens:
            dien_tich = cv2.contourArea(c)
            if dien_tich >= dien_tich_nho_nhat:
                ung_vien.append((dien_tich, c))

    if not ung_vien:
        return None, None

    # Lấy đường viền có diện tích lớn nhất (tờ giấy A4)
    ung_vien.sort(key=lambda item: item[0], reverse=True)
    duong_vien_giay = ung_vien[0][1]

    # 5. Xấp xỉ đa giác 4 đỉnh
    bon_goc = _xap_xi_tu_giac(duong_vien_giay)
    if bon_goc is None:
        return None, None

    # 6. Sắp xếp 4 góc theo thứ tự chuẩn
    goc_chuan = sap_xep_4_goc(bon_goc)

    # 7. Tạo mặt nạ nhị phân phủ toàn bộ diện tích tờ giấy
    mat_na = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mat_na, [np.int32(np.round(goc_chuan))], 255)

    return goc_chuan, mat_na
