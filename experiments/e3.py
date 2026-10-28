"""
E3: bỏ bớt thành phần (ablation)

So sánh trên tập eval, theo từng tầng:
  baseline          : cách đo thông thường
  day_du            : phương pháp đề xuất đầy đủ
  bo_nan_anh        : tắt bước nắn ảnh (tham_so nan_anh=False), kỳ vọng tụt về gần baseline
  bo_tinh_chinh_goc : tắt bước tinh chỉnh góc, kỳ vọng sai số tăng, rõ nhất ở tầng nặng

  python experiments/e3.py --du_lieu data/dataset_vat_phang
"""
import os

import _chung
from src import tien_ich, danh_gia

BIEN_THE = {
    'day_du': {},
    'bo_nan_anh': {'nan_anh': False},
    'bo_tinh_chinh_goc': {'tinh_chinh_goc': False},
}


def main():
    a = _chung.tham_so_dong_lenh(__doc__)
    ra = os.path.join(a.ra, 'e3')
    nhan = tien_ich.loc(tien_ich.doc_nhan(a.du_lieu), bo='eval')
    tat_ca = danh_gia.chay(danh_gia.lay_ham('baseline'), nhan, a.du_lieu, ten='baseline')
    for ten, ts in BIEN_THE.items():
        print('E3:', ten)
        tat_ca += danh_gia.chay(danh_gia.lay_ham('de_xuat'), nhan, a.du_lieu, tham_so=ts, ten=ten)
    tien_ich.ghi_csv(os.path.join(ra, 'ket_qua_e3.csv'), tat_ca, tien_ich.COT_KET_QUA)
    bang = danh_gia.tong_hop(tat_ca, theo=('phuong_phap', 'tang'))
    danh_gia.in_bang(bang)
    tien_ich.ghi_csv(os.path.join(ra, 'tong_hop_e3.csv'), bang)


if __name__ == '__main__':
    main()
