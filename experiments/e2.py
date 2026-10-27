"""
E2 – Khảo sát tham số. Người phụ trách: N4. Hạn trên ảnh thật: 12/11.

Mỗi lần chỉ thay MỘT tham số (các tham số khác giữ mặc định trong src/cau_hinh.py), mỗi tham số
thử ít nhất 3 giá trị, chạy trên tập DEV. Lưu ảnh trung gian của một ảnh mẫu cho mỗi giá trị
để trình bày song song ảnh và chỉ số trong báo cáo.

  python experiments/e2.py --du_lieu data/dataset_vat_phang
"""
import os

import _chung
from src import tien_ich, danh_gia

# Tham số cần khảo sát: {ten_tham_so: [các giá trị]}. N4 sửa danh sách này nếu cần.
LUOI = {
    'canny_cao': [100, 150, 220],
    'do_rong_dai_canh': [4, 8, 16],
    'do_phan_giai_nan': [2.0, 4.0, 8.0],
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
            for dong in danh_gia.tong_hop(kq, theo=('phuong_phap',)):
                dong['tham_so'] = ten
                dong['gia_tri'] = g
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
