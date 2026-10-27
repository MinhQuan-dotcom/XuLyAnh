"""
Hàm dùng chung: đọc nhãn, đọc ảnh, ghi CSV, lưu ảnh trung gian.
Người phụ trách: N1 (khung). Ai cần thêm hàm dùng chung thì thêm vào đây và báo nhóm.
"""
import csv
import os

import cv2

# Các cột số trong labels.csv
_COT_SO = ['dai_mm', 'rong_mm', 'day_mm', 'theta_deg', 'yaw_vat_deg', 'khoang_cach_mm']

# Các cột chỉ dùng để KIỂM TRA, phương pháp KHÔNG được đọc (ảnh thật sẽ không có)
COT_CAM = ('a4_g', 'vat_g', 'fx', 'fy', 'cx', 'cy', 'azim_deg', 'roll_deg', 'xoay_giay_deg', 'yaw_vat_deg')

# Cột của file kết quả – mọi script thí nghiệm ghi đúng các cột này
COT_KET_QUA = ['file', 'phuong_phap', 'bo', 'tang', 'huong', 'vat', 'theta_deg', 'day_mm',
               'dai_that', 'rong_that', 'dai_do', 'rong_do',
               'sai_so_dai', 'sai_so_rong', 'sai_so_mm', 'do_duoc', 'thoi_gian_ms']


def doc_nhan(thu_muc_du_lieu):
    """Đọc labels.csv trong thư mục dữ liệu, trả về list dict (cột số đã đổi sang float)."""
    duong_dan = os.path.join(thu_muc_du_lieu, 'labels.csv')
    with open(duong_dan, encoding='utf-8') as f:
        hang = list(csv.DictReader(f))
    for h in hang:
        for c in _COT_SO:
            if c in h and h[c] not in ('', None):
                h[c] = float(h[c])
    return hang


def loc(nhan, bo=None, tang=None):
    """Lọc nhãn theo bộ (dev, eval, e4_cucnang_55-75, e4_vat_day...) và/hoặc tầng."""
    def khop(gia_tri, dieu_kien):
        if dieu_kien is None:
            return True
        if isinstance(dieu_kien, (list, tuple, set)):
            return gia_tri in dieu_kien
        return gia_tri == dieu_kien
    return [h for h in nhan if khop(h['bo'], bo) and khop(h['tang'], tang)]


def doc_anh(thu_muc_du_lieu, file):
    anh = cv2.imread(os.path.join(thu_muc_du_lieu, file))
    if anh is None:
        raise FileNotFoundError(os.path.join(thu_muc_du_lieu, file))
    return anh


def ghi_csv(duong_dan, hang, cot=None):
    os.makedirs(os.path.dirname(duong_dan) or '.', exist_ok=True)
    if not hang:
        print('Không có dòng nào để ghi:', duong_dan)
        return
    cot = cot or list(hang[0].keys())
    with open(duong_dan, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cot, extrasaction='ignore')
        w.writeheader()
        w.writerows(hang)


def luu_anh_trung_gian(thu_muc, tien_to, anh_trung_gian):
    """Lưu từng ảnh trong dict {ten_buoc: anh} thành <tien_to>_<so>_<ten_buoc>.jpg."""
    os.makedirs(thu_muc, exist_ok=True)
    for i, (ten, anh) in enumerate(anh_trung_gian.items(), 1):
        if anh is None:
            continue
        cv2.imwrite(os.path.join(thu_muc, f'{tien_to}_{i}_{ten}.jpg'), anh)
