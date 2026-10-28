"""
PHƯƠNG PHÁP ĐỀ XUẤT – ghép các phần A, B, C, D. (Có sẵn – không cần sửa, trừ khi nhóm thống nhất.)

  1. giay.tim_to_giay        (A)  4 góc thô + mặt nạ
  2. goc.tinh_chinh_goc      (B)  tinh chỉnh góc        – tắt bằng tham_so['tinh_chinh_goc'] = False
  3-4. hinh_hoc.nan_anh      (C)  homography + nắn ảnh  – tắt bằng tham_so['nan_anh'] = False
  5. vat.tach_vat + kich_thuoc_px (D) trên ảnh đã nắn, chia s -> mm

Khi tắt nắn ảnh (ablation E3), đo như baseline nhưng dùng 4 góc (đã/không tinh chỉnh) để lấy tỉ lệ.
"""
import numpy as np
import cv2

from src import giay, goc as goc_mod, hinh_hoc, vat
from src.baseline import ve_ket_qua
from src.cau_hinh import THAM_SO_DE_XUAT


def do_kich_thuoc(anh, tham_so=None):
    tham_so = {**THAM_SO_DE_XUAT, **(tham_so or {})}
    anh_trung_gian = {'goc': anh}

    goc, mat_na = giay.tim_to_giay(anh, tham_so)
    if goc is None:
        return None, None, anh_trung_gian
    anh_trung_gian['goc_tho'] = ve_ket_qua(anh, goc)

    if tham_so['tinh_chinh_goc']:
        goc = goc_mod.tinh_chinh_goc(anh, goc, tham_so)
        anh_trung_gian['goc_tinh_chinh'] = ve_ket_qua(anh, goc)

    if not tham_so['nan_anh']:
        (_, _), (w, h), _ = cv2.minAreaRect(np.asarray(goc, dtype=np.float32))
        ti_le = min(w, h) / 210.0
        contour = vat.tach_vat(anh, mat_na, tham_so)
        if contour is None:
            return None, None, anh_trung_gian
        anh_trung_gian['ket_qua'] = ve_ket_qua(anh, goc, contour)
        d, r = vat.kich_thuoc_px(contour)
        if d is None:
            return None, None, anh_trung_gian
        return d / ti_le, r / ti_le, anh_trung_gian

    s = tham_so['do_phan_giai_nan']
    anh_nan, M = hinh_hoc.nan_anh(anh, goc, s, tham_so['dung_dlt_tu_viet'])
    if anh_nan is None:
        return None, None, anh_trung_gian
    anh_trung_gian['anh_nan'] = anh_nan

    contour = vat.tach_vat(anh_nan, None, tham_so)
    if contour is None:
        return None, None, anh_trung_gian
    anh_trung_gian['ket_qua'] = ve_ket_qua(anh_nan, None, contour)
    d, r = vat.kich_thuoc_px(contour)
    if d is None:
        return None, None, anh_trung_gian
    return d / s, r / s, anh_trung_gian
