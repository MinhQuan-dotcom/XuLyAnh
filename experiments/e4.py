"""
E4: kiểm tra điểm gãy

Hai phần:
  (a) Tầng cực nặng (thư mục e4_cucnang_55-75): sai số và tỉ lệ đo được theo góc nghiêng.
  (b) Vật dày (thư mục e4_vat_day): cùng mặt 60 x 40 mm, độ dày t khác nhau, ở nhiều góc.
      Tìm góc nhỏ nhất mà sai số trung bình vượt NGUONG_DAT_MM, so với dự đoán arctan(e_max / t).

  python experiments/e4.py --du_lieu data/dataset_vat_phang
"""
import math
import os
from collections import defaultdict

import _chung
from src import tien_ich, danh_gia
from src.cau_hinh import NGUONG_DAT_MM


def goc_tron(theta):
    """Gom góc về mốc gần nhất (5 độ) để gộp ảnh cùng mức nghiêng."""
    return int(5 * round(float(theta) / 5))


def main():
    a = _chung.tham_so_dong_lenh(__doc__)
    ra = os.path.join(a.ra, 'e4')
    nhan_all = tien_ich.doc_nhan(a.du_lieu)
    ham = danh_gia.lay_ham('de_xuat')

    # (a) tầng cực nặng
    nhan = tien_ich.loc(nhan_all, bo='e4_cucnang_55-75')
    kq = danh_gia.chay(ham, nhan, a.du_lieu, ten='de_xuat')
    for d in kq:
        d['goc'] = goc_tron(d['theta_deg'])
    print('E4a: tầng cực nặng')
    bang_a = danh_gia.tong_hop(kq, theo=('goc', 'huong'))
    danh_gia.in_bang(bang_a)
    tien_ich.ghi_csv(os.path.join(ra, 'e4a_cuc_nang.csv'), bang_a)

    # (b) vật dày
    nhan = tien_ich.loc(nhan_all, bo='e4_vat_day')
    kq = danh_gia.chay(ham, nhan, a.du_lieu, ten='de_xuat')
    for d in kq:
        d['goc'] = goc_tron(d['theta_deg'])
    tien_ich.ghi_csv(os.path.join(ra, 'e4b_ket_qua.csv'), kq)
    print('\nE4b: vật dày')
    bang_b = danh_gia.tong_hop(kq, theo=('day_mm', 'goc'))
    danh_gia.in_bang(bang_b)
    tien_ich.ghi_csv(os.path.join(ra, 'e4b_vat_day.csv'), bang_b)

    # Đối chiếu góc gãy với dự đoán
    theo_day = defaultdict(list)
    for d in bang_b:
        theo_day[d['day_mm']].append(d)
    doi_chieu = []
    for t, ds in sorted(theo_day.items(), key=lambda x: float(x[0])):
        gay = [d['goc'] for d in sorted(ds, key=lambda d: d['goc'])
               if not (d['mae_dai_mm'] <= NGUONG_DAT_MM)]          # NaN (không đo được) cũng tính là gãy
        du_doan = math.degrees(math.atan(NGUONG_DAT_MM / float(t))) if float(t) > 0 else 90.0
        doi_chieu.append({'day_mm': t, 'goc_gay_do_duoc': gay[0] if gay else '> goc lon nhat',
                          'goc_gay_du_doan': round(du_doan, 1)})
    print('\nĐối chiếu với dự đoán theta_gay = arctan(e_max / t)')
    danh_gia.in_bang(doi_chieu)
    tien_ich.ghi_csv(os.path.join(ra, 'e4_doi_chieu_du_doan.csv'), doi_chieu)


if __name__ == '__main__':
    main()
