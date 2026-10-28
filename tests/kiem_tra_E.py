"""
Kiểm tra phần E: baseline.do_kich_thuoc và experiments/ve_do_thi.py
  python tests/kiem_tra_E.py                      (giả lập phần A, D bằng nhãn, dùng khi A, D chưa xong)
  python tests/kiem_tra_E.py --that               (dùng phần A, D thật, sau khi đã gộp A, D)
  thêm --du_lieu data/dataset_vat_phang để chạy đủ 286 ảnh

Chế độ giả lập: giay.tim_to_giay trả về 4 góc đúng, vat.tach_vat trả về đáy vật đúng (lấy từ nhãn).
Khi đó sai số còn lại chỉ do giả định "chụp thẳng" của baseline, đúng cái E1 cần cho thấy.

Đạt khi: baseline đo được mọi ảnh; ở góc gần 0 độ sai số TB < 1 mm; sai số tầng nặng > tầng nhẹ;
và ve_do_thi tạo được file PNG.
"""
import os
import sys

import cv2
import numpy as np

import _chung
from src import tien_ich, danh_gia, giay, vat, baseline

_hien_tai = {}


def _gia_lap_tim_to_giay(anh, tham_so):
    g = _chung.goc_giay_dung(_hien_tai['h'])
    m = np.zeros(anh.shape[:2], np.uint8)
    cv2.fillPoly(m, [np.round(g).astype(np.int32)], 255)
    return g, m


def _gia_lap_tach_vat(anh, mat_na=None, tham_so=None):
    return np.round(_chung.goc_vat_dung(_hien_tai['h'])).astype(np.int32).reshape(-1, 1, 2)


def _gia_lap_kich_thuoc_px(contour):
    (_, _), (w, h), _ = cv2.minAreaRect(contour.astype(np.float32))
    return max(w, h), min(w, h)


def main():
    that = '--that' in sys.argv
    if that:
        sys.argv.remove('--that')
    a = _chung.tham_so(__doc__)
    nhan = [h for h in _chung.doc_nhan(a) if h['bo'] in ('dev', 'eval')]
    if not that:
        giay.tim_to_giay = _gia_lap_tim_to_giay
        vat.tach_vat = _gia_lap_tach_vat
        vat.kich_thuoc_px = _gia_lap_kich_thuoc_px
        print('Chế độ giả lập phần A, D (thêm --that để dùng code thật)\n')

    kq = danh_gia.chay(baseline.do_kich_thuoc, nhan, a.du_lieu, ten='baseline',
                       goi_truoc=lambda h: _hien_tai.update(h=h))
    bang = danh_gia.tong_hop(kq, theo=('tang',))
    danh_gia.in_bang(bang)

    ok = [d for d in kq if d['do_duoc']]
    ti_le = len(ok) / max(len(kq), 1)
    goc0 = [d['sai_so_mm'] for d in ok if d['theta_deg'] < 2]
    tb = {d['tang']: d['mae_dai_mm'] for d in bang}
    sai0 = float(np.mean(goc0)) if goc0 else float('nan')
    tang_dan = tb.get('nang', 0) > tb.get('nhe', float('inf'))
    print(f'\nĐo được {100*ti_le:.0f}% ảnh; góc gần 0 độ: sai số TB {sai0:.2f} mm; '
          f'tầng nhẹ {tb.get("nhe")} mm -> tầng nặng {tb.get("nang")} mm')

    # đồ thị
    ra = os.path.join(_chung.GOC_REPO, 'results', 'kiem_tra')
    csv_path = os.path.join(ra, 'E_baseline.csv')
    png_path = os.path.join(ra, 'E_do_thi.png')
    tien_ich.ghi_csv(csv_path, kq, tien_ich.COT_KET_QUA)
    sys.path.insert(0, os.path.join(_chung.GOC_REPO, 'experiments'))
    import ve_do_thi
    if os.path.exists(png_path):
        os.remove(png_path)
    nhom = ve_do_thi.gom_theo_goc(ve_do_thi.doc_ket_qua([csv_path]))
    co_nhom = bool(nhom) and all(len(x) == len(y) and list(x) == sorted(x) for x, y in nhom.values())
    ve_do_thi.ve(nhom, png_path)
    co_png = os.path.exists(png_path)
    print(f'gom_theo_goc: {"đúng định dạng" if co_nhom else "chưa đúng / còn trống"}; '
          f'đồ thị: {png_path if co_png else "chưa tạo được"}')

    dat = ti_le == 1.0 and sai0 < 1.0 and tang_dan and co_nhom and co_png
    if that:   # dùng phần A, D thật thì cho sai số lớn hơn một chút
        dat = ti_le >= 0.95 and sai0 < 1.5 and tang_dan and co_nhom and co_png
    raise SystemExit(_chung.ket_luan(dat, 'baseline + đồ thị'))


if __name__ == '__main__':
    main()
