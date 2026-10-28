"""
Kiểm tra PHẦN D – vat.tach_vat và vat.kich_thuoc_px (trên ảnh gốc).
  python tests/kiem_tra_D.py
  python tests/kiem_tra_D.py --du_lieu data/dataset_vat_phang

Mặt nạ tờ giấy được tạo từ 4 góc đúng trong nhãn (không cần phần A). Kích thước pixel của vật được so
với hình chữ nhật bao đáy vật đúng.
Đạt khi: tìm được vật ở >= 95% ảnh, và với vật mỏng (dày <= 1 mm) sai số TB <= 3 px.
(Vật dày hơn có mặt bên lộ ra nên to hơn đáy – đó là thị sai, không tính là lỗi của phần D.)
"""
import os
from collections import defaultdict

import cv2
import numpy as np

import _chung
from src import tien_ich, vat


def main():
    a = _chung.tham_so(__doc__)
    nhan = _chung.doc_nhan(a)
    ra = os.path.join(_chung.GOC_REPO, 'results', 'kiem_tra')
    os.makedirs(ra, exist_ok=True)
    n = tim = 0
    sai_mong, theo_day = [], defaultdict(list)
    da_luu = 0
    for h in nhan:
        anh = tien_ich.doc_anh(a.du_lieu, h['file'])
        g = _chung.goc_giay_dung(h)
        mat_na = np.zeros(anh.shape[:2], np.uint8)
        cv2.fillPoly(mat_na, [np.round(g).astype(np.int32)], 255)
        n += 1
        c = vat.tach_vat(anh, mat_na, None)
        if c is None:
            continue
        d, r = vat.kich_thuoc_px(c)
        if d is None:
            continue
        tim += 1
        (_, _), (w, hh), _ = cv2.minAreaRect(_chung.goc_vat_dung(h).astype(np.float32))
        sai = (abs(max(d, r) - max(w, hh)) + abs(min(d, r) - min(w, hh))) / 2
        theo_day[h['day_mm']].append(sai)
        if h['day_mm'] <= 1.0:
            sai_mong.append(sai)
        if da_luu < 3:
            out = anh.copy()
            cv2.drawContours(out, [c], -1, (0, 255, 0), 2)
            cv2.imwrite(os.path.join(ra, f'D_{os.path.basename(h["file"])}'), out)
            da_luu += 1
    print(f'{"độ dày (mm)":<14}{"số ảnh":>8}{"sai số TB (px)":>16}')
    for t in sorted(theo_day):
        print(f'{t:<14}{len(theo_day[t]):>8}{np.mean(theo_day[t]):>16.2f}')
    ti_le = tim / max(n, 1)
    tb = np.mean(sai_mong) if sai_mong else float('inf')
    print('Ảnh có đường viền vật: results/kiem_tra/D_*.jpg')
    raise SystemExit(_chung.ket_luan(ti_le >= 0.95 and tb <= 3.0,
                                     f'tìm được {100*ti_le:.0f}% (cần >= 95%), vật mỏng sai số TB {tb:.2f} px (cần <= 3)'))


if __name__ == '__main__':
    main()
