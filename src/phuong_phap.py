"""
PHƯƠNG PHÁP ĐỀ XUẤT – nắn phối cảnh bằng homography từ 4 góc tờ A4, có tinh chỉnh góc.
Người phụ trách: N4. Hạn: bước 1, 3, 4, 5 trước 02/11; bước 2 trước 05/11; DLT tự viết trước 06/11.

Pipeline (xem mục B.1 bản Tuyên bố thách thức):
  Bước 1  tim_to_giay      : ảnh xám -> làm mờ -> Otsu -> đường viền lớn nhất -> approxPolyDP ra 4 đỉnh thô.
  Bước 2  tinh_chinh_goc   : với mỗi cạnh, lấy điểm Canny gần cạnh thô, khớp đường thẳng (cv2.fitLine),
                             góc mới = giao điểm hai đường kề nhau.
  Bước 3  tinh_homography  : H từ 4 cặp điểm ảnh <-> (0,0),(210,0),(210,297),(0,297) mm.
  Bước 4  nan_anh          : warpPerspective về ảnh nhìn thẳng, độ phân giải s px/mm.
  Bước 5  do_vat           : tách vật trên ảnh đã nắn, minAreaRect, chia s -> mm.

Hai công tắc bắt buộc (cho thí nghiệm E3):
  tham_so['nan_anh'] = False         -> bỏ bước 4, đo bằng một tỉ lệ duy nhất (như baseline)
  tham_so['tinh_chinh_goc'] = False  -> bỏ bước 2, dùng 4 đỉnh thô

KHÔNG đọc nhãn (labels.csv) trong file này. Hàm chỉ nhận ảnh.
"""
import numpy as np
import cv2

from src.cau_hinh import THAM_SO_DE_XUAT

A4_MM = np.array([[0, 0], [210, 0], [210, 297], [0, 297]], dtype=np.float64)


def sap_xep_4_goc(diem):
    """Sắp 4 điểm theo thứ tự: trên-trái, trên-phải, dưới-phải, dưới-trái (theo ảnh).
    Lưu ý khi ghép với A4_MM: cạnh 210 mm là cạnh ngắn của tờ giấy -> cần kiểm tra cạnh nào ngắn hơn."""
    diem = np.asarray(diem, dtype=np.float64).reshape(4, 2)
    s = diem.sum(1)
    d = np.diff(diem, axis=1).ravel()
    return np.array([diem[np.argmin(s)], diem[np.argmin(d)], diem[np.argmax(s)], diem[np.argmax(d)]])


def tim_to_giay(anh, tham_so):
    """Bước 1. Trả về (4 đỉnh thô shape (4,2) hoặc None, mặt nạ tờ giấy hoặc None)."""
    # TODO (N4)
    return None, None


def tinh_chinh_goc(anh, goc_tho, tham_so):
    """Bước 2. Trả về 4 góc đã tinh chỉnh shape (4,2). Lỗi thì trả lại goc_tho."""
    # TODO (N4)
    return goc_tho


def tinh_homography_dlt(diem_nguon, diem_dich):
    """Bước 3 (tự viết, DLT 4 điểm bằng numpy). Trả về H 3x3 với diem_dich ~ H * diem_nguon.
    Gợi ý: mỗi cặp điểm cho 2 phương trình -> ma trận A 8x9 -> nghiệm là vector kỳ dị
    ứng với giá trị kỳ dị nhỏ nhất (np.linalg.svd) -> reshape 3x3 -> chia H[2,2]."""
    # TODO (N4)
    raise NotImplementedError


def tinh_homography(goc_anh, tham_so):
    """Bước 3. H biến tọa độ ảnh -> tọa độ mm trên tờ giấy."""
    goc_anh = np.asarray(goc_anh, dtype=np.float64)
    if tham_so['dung_dlt_tu_viet']:
        return tinh_homography_dlt(goc_anh, A4_MM)
    H, _ = cv2.findHomography(goc_anh, A4_MM)
    return H


def nan_anh(anh, H, tham_so):
    """Bước 4. Trả về ảnh đã nắn kích thước (210*s, 297*s)."""
    # TODO (N4): S = diag(s, s, 1); cv2.warpPerspective(anh, S @ H, (int(210*s), int(297*s)))
    return None


def do_vat(anh_nan, tham_so):
    """Bước 5. Trả về (dai_mm, rong_mm) hoặc (None, None)."""
    # TODO (N4)
    return None, None


def do_kich_thuoc(anh, tham_so=None):
    """
    Đầu vào / đầu ra GIỐNG HỆT baseline.do_kich_thuoc:
      trả về (dai_mm, rong_mm, anh_trung_gian), dai_mm >= rong_mm, không đo được -> (None, None, ...).
    """
    tham_so = {**THAM_SO_DE_XUAT, **(tham_so or {})}
    anh_trung_gian = {'goc': anh}

    goc_tho, mat_na = tim_to_giay(anh, tham_so)
    if goc_tho is None:
        return None, None, anh_trung_gian

    goc = tinh_chinh_goc(anh, goc_tho, tham_so) if tham_so['tinh_chinh_goc'] else goc_tho

    if not tham_so['nan_anh']:
        # TODO (N4): nhánh ablation E3 – đo bằng một tỉ lệ duy nhất từ 4 góc, không nắn.
        return None, None, anh_trung_gian

    H = tinh_homography(goc, tham_so)
    anh_nan = nan_anh(anh, H, tham_so)
    anh_trung_gian['anh_nan'] = anh_nan
    if anh_nan is None:
        return None, None, anh_trung_gian

    dai, rong = do_vat(anh_nan, tham_so)
    if dai is None:
        return None, None, anh_trung_gian
    return max(dai, rong), min(dai, rong), anh_trung_gian
