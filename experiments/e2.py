"""
E2: khảo sát tham số

Mỗi lần chỉ thay MỘT tham số (các tham số khác giữ mặc định trong src/cau_hinh.py), mỗi tham số
thử ít nhất 3 giá trị, chạy trên tập DEV. Lưu ảnh trung gian của một ảnh mẫu cho mỗi giá trị
để trình bày song song ảnh và chỉ số trong báo cáo.

  python experiments/e2.py --du_lieu data/dataset_vat_phang
"""
import os

import _chung
from src import tien_ich, danh_gia

# Tham số cần khảo sát, ít nhất một tham số cho mỗi bước chính của pipeline:
#   tìm giấy: kich_thuoc_lam_mo | chỉnh góc: canny_cao, do_rong_dai_canh
#   nắn ảnh: do_phan_giai_nan   | tách vật: nguong_s, he_so_v
LUOI = {
    'kich_thuoc_lam_mo': [1, 3, 5, 9, 15, 21],
    'canny_cao': [30, 60, 100, 150, 220, 300],
    'do_rong_dai_canh': [1, 2, 4, 8, 16, 32],
    'do_phan_giai_nan': [1.0, 2.0, 3.0, 4.0, 6.0, 8.0],
    'nguong_s': [20, 40, 60, 80, 100, 140],
    'he_so_v': [0.0, 0.3, 0.4, 0.5, 0.6, 0.7],
}
ANH_MAU = 0       # chỉ số ảnh trong tập dev dùng để lưu ảnh trung gian


def main():
    a = _chung.tham_so_dong_lenh(__doc__)
    ra = os.path.join(a.ra, 'e2')
    nhan = tien_ich.loc(tien_ich.doc_nhan(a.du_lieu), bo='dev')
    ham = danh_gia.lay_ham('de_xuat')
    tong = []
    for ten, gia_tri in LUOI.items():
        for g in gia_tri:
            print(f'E2: {ten} = {g}')
            kq = danh_gia.chay(ham, nhan, a.du_lieu, tham_so={ten: g}, ten=f'{ten}={g}')
            ok = [d for d in kq if d['do_duoc']]
            for dong in danh_gia.tong_hop(kq, theo=('phuong_phap',)):
                dong['tham_so'] = ten
                dong['gia_tri'] = g
                # sai số có dấu (dương: đo dư), để biết MAE giảm là do đo đúng hơn hay do bù trừ
                dong['sai_so_dai_co_dau_mm'] = round(sum(d['dai_do'] - d['dai_that'] for d in ok) / max(len(ok), 1), 2)
                dong['sai_so_rong_co_dau_mm'] = round(sum(d['rong_do'] - d['rong_that'] for d in ok) / max(len(ok), 1), 2)
                tong.append(dong)
            # ảnh trung gian của một ảnh mẫu
            if nhan:
                h = nhan[ANH_MAU]
                _, _, tg = ham(tien_ich.doc_anh(a.du_lieu, h['file']), {ten: g})
                tien_ich.luu_anh_trung_gian(os.path.join(ra, 'trung_gian', f'{ten}_{g}'), 'mau', tg)
    danh_gia.in_bang(tong)
    tien_ich.ghi_csv(os.path.join(ra, 'tong_hop_e2.csv'), tong)


if __name__ == '__main__':
    main()
