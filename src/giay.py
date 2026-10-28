"""
PHẦN A – Tìm tờ giấy A4 trong ảnh.
Người làm: ........   Hạn: 01/11   Kiểm tra: python tests/kiem_tra_A.py

Dùng chung cho cả baseline và phương pháp đề xuất.
"""
import numpy as np
import cv2


def sap_xep_4_goc(diem):
    """(Có sẵn) Sắp 4 điểm theo thứ tự trong ảnh: trên-trái, trên-phải, dưới-phải, dưới-trái.
    Sắp theo góc quanh trọng tâm (theo chiều kim đồng hồ trên ảnh), rồi chọn cạnh có y nhỏ nhất làm cạnh
    trên. Đúng cả khi tờ giấy bị nghiêng mạnh thành hình thang dẹt."""
    diem = np.asarray(diem, dtype=np.float64).reshape(4, 2)
    tam = diem.mean(0)
    diem = diem[np.argsort(np.arctan2(diem[:, 1] - tam[1], diem[:, 0] - tam[0]))]
    i = int(np.argmin([diem[k, 1] + diem[(k + 1) % 4, 1] for k in range(4)]))
    return np.roll(diem, -i, axis=0)


def tim_to_giay(anh, tham_so):
    """
    Tìm tờ giấy A4 (trắng, nằm trên nền tối).

    Đầu vào
      anh     : ảnh BGR (numpy uint8, H x W x 3)
      tham_so : dict, dùng tham_so['kich_thuoc_lam_mo'] (số lẻ, ví dụ 5)
    Đầu ra
      (goc, mat_na)
      goc    : numpy float64 shape (4, 2) – 4 góc tờ giấy (x, y) theo pixel, ĐÃ sắp bằng sap_xep_4_goc
               (trên-trái, trên-phải, dưới-phải, dưới-trái). Không tìm thấy -> None.
      mat_na : numpy uint8 H x W, 255 bên trong tờ giấy, 0 bên ngoài. Không tìm thấy -> None.

    Gợi ý các bước
      1. cv2.cvtColor sang ảnh xám, cv2.GaussianBlur.
      2. cv2.threshold(..., cv2.THRESH_BINARY + cv2.THRESH_OTSU): giấy trắng thành 255.
      3. cv2.findContours, lấy đường viền có diện tích lớn nhất.
      4. cv2.approxPolyDP với epsilon = 0.02 * chu vi. Nếu không ra đúng 4 điểm, thử tăng/giảm epsilon
         vài lần; vẫn không được thì trả (None, None).
      5. mat_na: cv2.drawContours (hoặc fillPoly) đường viền giấy lên ảnh đen, tô đầy 255.

    Lưu ý 1: ở góc nghiêng lớn (>= 55°) bức tường sáng phía sau lọt vào ảnh và có thể to hơn tờ giấy.
    Nên bỏ các đường viền chạm mép ảnh, hoặc chọn đường viền lớn nhất mà approxPolyDP ra đúng 4 đỉnh.
    Lưu ý 2: vật nằm TRÊN giấy có thể làm đường viền giấy bị lõm vào nếu vật chạm mép giấy.
    Dùng đường viền ngoài (RETR_EXTERNAL) và approxPolyDP sẽ bỏ qua phần lõm nhỏ.
    """
    # TODO (Phần A)
    return None, None
