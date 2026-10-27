"""
E1 – Chứng cứ thách thức. Người phụ trách: N3 (chạy), N5 (script). Hạn trên ảnh thật: 10/11.

Chạy baseline trên tập eval đã phân tầng, báo sai số theo từng tầng và từng hướng đặt vật,
rồi lấy ra các ảnh baseline đo sai nhiều nhất (ít nhất 3 ảnh) kèm ảnh trung gian để đưa vào báo cáo.

  python experiments/e1.py --du_lieu data/dataset_vat_phang
"""
import os
import shutil

import _chung
from src import tien_ich, danh_gia

SO_ANH_LOI = 5


def main():
    a = _chung.tham_so_dong_lenh(__doc__)
    ra = os.path.join(a.ra, 'e1')
    nhan = tien_ich.loc(tien_ich.doc_nhan(a.du_lieu), bo='eval')
    print(f'E1: baseline trên {len(nhan)} ảnh eval')
    kq = danh_gia.chay(danh_gia.lay_ham('baseline'), nhan, a.du_lieu, ten='baseline')
    tien_ich.ghi_csv(os.path.join(ra, 'ket_qua_baseline.csv'), kq, tien_ich.COT_KET_QUA)

    for theo in [('tang',), ('tang', 'huong')]:
        bang = danh_gia.tong_hop(kq, theo)
        print('\nTheo', ' + '.join(theo))
        danh_gia.in_bang(bang)
        tien_ich.ghi_csv(os.path.join(ra, 'tong_hop_' + '_'.join(theo) + '.csv'), bang)

    # Ảnh đo sai nhiều nhất (và ảnh không đo được)
    loi = sorted([d for d in kq if d['do_duoc']], key=lambda d: -d['sai_so_mm'])[:SO_ANH_LOI]
    loi += [d for d in kq if not d['do_duoc']][:SO_ANH_LOI]
    thu_muc_loi = os.path.join(ra, 'anh_loi')
    os.makedirs(thu_muc_loi, exist_ok=True)
    ham = danh_gia.lay_ham('baseline')
    for d in loi:
        shutil.copy(os.path.join(a.du_lieu, d['file']), thu_muc_loi)
        _, _, trung_gian = ham(tien_ich.doc_anh(a.du_lieu, d['file']))
        tien_to = os.path.splitext(os.path.basename(d['file']))[0]
        tien_ich.luu_anh_trung_gian(thu_muc_loi, tien_to, trung_gian)
    tien_ich.ghi_csv(os.path.join(thu_muc_loi, 'danh_sach.csv'), loi, tien_ich.COT_KET_QUA)
    print(f'\nĐã lưu {len(loi)} ảnh lỗi vào {thu_muc_loi}')


if __name__ == '__main__':
    main()
