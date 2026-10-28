"""
Kiểm tra phần B: goc.tinh_chinh_goc
  python tests/kiem_tra_B.py
  python tests/kiem_tra_B.py --du_lieu data/dataset_vat_phang

Lấy 4 góc đúng từ nhãn, cộng nhiễu ngẫu nhiên (lệch khoảng 3 pixel) làm "góc thô", gọi tinh_chinh_goc,
rồi so sai số trước và sau.
Đạt khi: sai số TB sau tinh chỉnh <= 1.5 px VÀ giảm ít nhất 40% so với góc thô.
"""
from collections import defaultdict

import numpy as np

import _chung
from src import tien_ich, goc
from src.cau_hinh import THAM_SO_DE_XUAT

DO_NHIEU_PX = 3.0


def main():
    a = _chung.tham_so(__doc__)
    nhan = _chung.doc_nhan(a)
    rng = np.random.default_rng(0)
    truoc, sau = defaultdict(list), defaultdict(list)
    for h in nhan:
        anh = tien_ich.doc_anh(a.du_lieu, h['file'])
        dung = _chung.goc_giay_dung(h)
        tho = dung + rng.normal(0, DO_NHIEU_PX, dung.shape)
        moi = np.asarray(goc.tinh_chinh_goc(anh, tho.copy(), THAM_SO_DE_XUAT), dtype=np.float64)
        if moi.shape != (4, 2):
            raise SystemExit(f'Sai định dạng: tinh_chinh_goc phải trả về numpy (4, 2), nhận được {moi.shape}')
        truoc[h['tang']].append(float(np.mean(np.linalg.norm(tho - dung, axis=1))))
        sau[h['tang']].append(float(np.mean(np.linalg.norm(moi - dung, axis=1))))

    print(f'{"tầng":<12}{"số ảnh":>8}{"trước (px)":>12}{"sau (px)":>10}')
    for tang in truoc:
        print(f'{tang:<12}{len(truoc[tang]):>8}{np.mean(truoc[tang]):>12.2f}{np.mean(sau[tang]):>10.2f}')
    tb_truoc = np.mean([x for v in truoc.values() for x in v])
    tb_sau = np.mean([x for v in sau.values() for x in v])
    raise SystemExit(_chung.ket_luan(tb_sau <= 1.5 and tb_sau <= 0.6 * tb_truoc,
                                     f'sai số TB {tb_truoc:.2f} px -> {tb_sau:.2f} px (cần <= 1.5 px và giảm >= 40%)'))


if __name__ == '__main__':
    main()
