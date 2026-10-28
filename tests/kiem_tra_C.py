"""
Kiểm tra PHẦN C – hinh_hoc.tinh_homography_dlt và hinh_hoc.nan_anh.
  python tests/kiem_tra_C.py
  python tests/kiem_tra_C.py --du_lieu data/dataset_vat_phang

1. DLT tự viết: 4 góc giấy (đúng, từ nhãn) phải biến chính xác thành 4 góc A4 (mm), sai lệch < 1e-4 mm,
   và biến các điểm bên trong tờ giấy giống cv2.findHomography (lệch < 1e-3 mm).
2. Nắn ảnh: dùng 4 góc đúng, s = 4 px/mm. Ảnh nắn phải có kích thước 1188 x 840. Biến 4 góc đáy vật
   (từ nhãn) bằng M rồi đo cạnh -> phải ra đúng kích thước thật, sai lệch TB < 0.2 mm.
   Ảnh nắn mẫu lưu ở results/kiem_tra/C_*.jpg để nhìn bằng mắt.
"""
import os

import cv2
import numpy as np

import _chung
from src import tien_ich, hinh_hoc

S = 4.0


def bien_diem(M, p):
    q = np.c_[p, np.ones(len(p))] @ M.T
    return q[:, :2] / q[:, 2:3]


def main():
    a = _chung.tham_so(__doc__)
    nhan = _chung.doc_nhan(a)
    ra = os.path.join(_chung.GOC_REPO, 'results', 'kiem_tra')
    os.makedirs(ra, exist_ok=True)

    # 1. DLT
    dat_dlt = True
    try:
        sai_dlt, sai_cv = [], []
        for h in nhan:
            g = _chung.goc_giay_dung(h)
            H = np.asarray(hinh_hoc.tinh_homography_dlt(g, hinh_hoc.A4_MM), dtype=np.float64)
            Hc, _ = cv2.findHomography(g, hinh_hoc.A4_MM)
            sai_dlt.append(np.max(np.abs(bien_diem(H, g) - hinh_hoc.A4_MM)))
            luoi = np.array([[x, y] for x in np.linspace(0.2, 0.8, 3) for y in np.linspace(0.2, 0.8, 3)])
            diem = g[0] + luoi[:, :1] * (g[1] - g[0]) + luoi[:, 1:] * (g[3] - g[0])   # điểm bên trong tờ giấy
            sai_cv.append(np.max(np.abs(bien_diem(H, diem) - bien_diem(Hc, diem))))
        print(f'DLT: sai lệch lớn nhất tại 4 góc = {max(sai_dlt):.2e} mm, khác cv2.findHomography = {max(sai_cv):.2e} mm')
        dat_dlt = max(sai_dlt) < 1e-4 and max(sai_cv) < 1e-3
    except NotImplementedError:
        print('DLT: chưa viết (NotImplementedError)')
        dat_dlt = False

    # 2. Nắn ảnh
    sai_mm, da_luu = [], 0
    for h in nhan:
        anh = tien_ich.doc_anh(a.du_lieu, h['file'])
        anh_nan, M = hinh_hoc.nan_anh(anh, _chung.goc_giay_dung(h), S)
        if anh_nan is None or M is None:
            print('nan_anh chưa trả về kết quả (None)')
            sai_mm = [float('inf')]
            break
        if anh_nan.shape[:2] != (round(297 * S), round(210 * S)):
            print('Sai kích thước ảnh nắn:', anh_nan.shape[:2], 'cần', (round(297 * S), round(210 * S)))
            sai_mm = [float('inf')]
            break
        p = bien_diem(np.asarray(M, dtype=np.float64), _chung.goc_vat_dung(h)) / S
        canh = sorted([np.linalg.norm(p[1] - p[0]), np.linalg.norm(p[2] - p[1])])
        sai_mm.append(abs(canh[1] - h['dai_mm']) + abs(canh[0] - h['rong_mm']))
        if da_luu < 3 and h['theta_deg'] > 30:
            cv2.imwrite(os.path.join(ra, f'C_{os.path.basename(h["file"])}'), anh_nan)
            da_luu += 1
    tb = float(np.mean(sai_mm))
    print(f'Nắn ảnh: sai lệch kích thước TB = {tb:.3f} mm trên {len(sai_mm)} ảnh')
    raise SystemExit(_chung.ket_luan(dat_dlt and tb < 0.2,
                                     f'DLT {"đúng" if dat_dlt else "chưa đúng"}; nắn ảnh sai lệch {tb:.3f} mm (cần < 0.2)'))


if __name__ == '__main__':
    main()
