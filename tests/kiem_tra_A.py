"""
Kiểm tra phần A: giay.tim_to_giay
  python tests/kiem_tra_A.py                                   (25 ảnh mẫu, nhanh)
  python tests/kiem_tra_A.py --du_lieu data/dataset_vat_phang  (286 ảnh, trước khi mở Pull Request)

Đạt khi: tìm được giấy ở >= 95% ảnh có góc nghiêng <= 55 độ, và sai số góc trung bình <= 3 pixel.
Tầng cực nặng (60-70 độ) chỉ in ra để xem, không tính vào kết quả vì đó là vùng điểm gãy của E4.
"""
from collections import defaultdict

import numpy as np

import _chung
from src import tien_ich, giay
from src.cau_hinh import THAM_SO_DE_XUAT


def main():
    a = _chung.tham_so(__doc__)
    nhan = _chung.doc_nhan(a)
    theo_tang = defaultdict(lambda: {'n': 0, 'tim_duoc': 0, 'sai_so': []})
    loi_dinh_dang = []
    for h in nhan:
        anh = tien_ich.doc_anh(a.du_lieu, h['file'])
        goc, mat_na = giay.tim_to_giay(anh, THAM_SO_DE_XUAT)
        t = theo_tang[h['tang']]
        t['n'] += 1
        if goc is None:
            continue
        goc = np.asarray(goc, dtype=np.float64)
        if goc.shape != (4, 2) or mat_na is None or mat_na.shape != anh.shape[:2]:
            loi_dinh_dang.append(h['file'])
            continue
        t['tim_duoc'] += 1
        dung = _chung.goc_giay_dung(h)
        t['sai_so'].append(float(np.mean(np.linalg.norm(giay.sap_xep_4_goc(goc) - dung, axis=1))))
        # mặt nạ phải phủ tâm tờ giấy
        cx, cy = dung.mean(0).astype(int)
        if mat_na[cy, cx] == 0 and h['tang'] != 'cuc_nang':
            loi_dinh_dang.append(h['file'] + ' (mặt nạ không phủ tâm giấy)')

    print(f'{"tầng":<12}{"số ảnh":>8}{"tìm được":>10}{"sai số TB (px)":>16}{"lớn nhất":>10}')
    tong_n = tong_tim = 0
    tat_ca = []
    for tang, t in theo_tang.items():
        ss = t['sai_so']
        print(f'{tang:<12}{t["n"]:>8}{t["tim_duoc"]:>10}{(np.mean(ss) if ss else float("nan")):>16.2f}'
              f'{(np.max(ss) if ss else float("nan")):>10.2f}')
        if tang != 'cuc_nang':
            tong_n += t['n']; tong_tim += t['tim_duoc']; tat_ca += ss
    if loi_dinh_dang:
        print('\nSai định dạng đầu ra:', *loi_dinh_dang[:10], sep='\n  ')
    ti_le = tong_tim / max(tong_n, 1)
    tb = np.mean(tat_ca) if tat_ca else float('inf')
    raise SystemExit(_chung.ket_luan(ti_le >= 0.95 and tb <= 3.0 and not loi_dinh_dang,
                                     f'tìm được {100*ti_le:.0f}% (cần >= 95%), sai số TB {tb:.2f} px (cần <= 3)'))


if __name__ == '__main__':
    main()
