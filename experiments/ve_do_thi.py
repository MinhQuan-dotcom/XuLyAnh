"""
PHẦN E (2/2) – Vẽ đồ thị sai số theo góc nghiêng.
Người làm: ........ (cùng người làm baseline)   Hạn: 01/11   Kiểm tra: python tests/kiem_tra_E.py

Đồ thị chính của báo cáo và slide: trục ngang là góc nghiêng (độ), trục dọc là sai số (mm).
Mỗi phương pháp (cột 'phuong_phap') một màu, nét liền = đặt dọc, nét đứt = đặt ngang.
Kẻ một đường ngang ở NGUONG_DAT_MM (1 mm).

Chạy:
  python experiments/ve_do_thi.py results/e3/ket_qua_e3.csv --ra results/do_thi_sai_so.png
  (có thể đưa nhiều file CSV cùng lúc; mọi file theo cột tien_ich.COT_KET_QUA)
"""
import argparse
import csv

import _chung  # noqa: F401  (thêm thư mục gốc vào sys.path)
from src.cau_hinh import NGUONG_DAT_MM


def doc_ket_qua(cac_file):
    """(Có sẵn) Đọc và gộp các file CSV kết quả, chỉ giữ ảnh đo được. Trả về list dict, số đã đổi sang float."""
    hang = []
    for f in cac_file:
        with open(f, encoding='utf-8') as fh:
            for h in csv.DictReader(fh):
                if h['do_duoc'] != '1':
                    continue
                h['theta_deg'] = float(h['theta_deg'])
                h['sai_so_mm'] = float(h['sai_so_mm'])
                hang.append(h)
    return hang


def gom_theo_goc(hang, buoc=5):
    """
    Gom kết quả thành từng nhóm (phuong_phap, huong), trong mỗi nhóm lấy TRUNG BÌNH sai_so_mm theo góc
    đã làm tròn về bội số của `buoc` độ.
    Đầu ra: dict {(phuong_phap, huong): ([goc1, goc2, ...], [sai_so_tb1, sai_so_tb2, ...])}, góc tăng dần.
    """
    # TODO (Phần E)
    return {}


def ve(nhom, duong_dan_png, tieu_de='Sai số đo theo góc nghiêng'):
    """
    Vẽ đồ thị bằng matplotlib từ kết quả của gom_theo_goc và lưu ra file PNG (dpi 150).
    Gợi ý: import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
           mỗi phương pháp một màu; huong == 'doc' nét liền '-o', 'ngang' nét đứt '--s'
           plt.axhline(NGUONG_DAT_MM, ...) ; nhãn trục có đơn vị; chú thích (legend); lưới nhạt.
    """
    # TODO (Phần E)
    pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument('cac_file', nargs='+')
    p.add_argument('--ra', default='results/do_thi_sai_so.png')
    p.add_argument('--buoc', type=int, default=5)
    a = p.parse_args()
    ve(gom_theo_goc(doc_ket_qua(a.cac_file), a.buoc), a.ra)
    print('Đã lưu', a.ra)


if __name__ == '__main__':
    main()
