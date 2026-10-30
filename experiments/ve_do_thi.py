"""
Phần E (2/2): vẽ đồ thị sai số theo góc nghiêng
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
import os

import _chung  # để import được src
from src.cau_hinh import NGUONG_DAT_MM


def doc_ket_qua(cac_file):
    """Đọc và gộp các file CSV kết quả, chỉ giữ ảnh đo được. Trả về list dict, số đã đổi sang float."""
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
    Gom kết quả thành từng nhóm (phuong_phap, huong), trong mỗi nhóm lấy trung bình sai_so_mm theo góc
    đã làm tròn về bội số của `buoc` độ.
    Đầu ra: dict {(phuong_phap, huong): ([goc1, goc2, ...], [sai_so_tb1, sai_so_tb2, ...])}, góc tăng dần.
    """
    if buoc <= 0:
        raise ValueError('buoc phải là số nguyên dương')

    tong = {}
    dem = {}
    for h in hang:
        khoa = (h.get('phuong_phap', ''), h.get('huong', ''))
        goc = round(float(h['theta_deg']) / buoc) * buoc
        sai_so = float(h['sai_so_mm'])
        if khoa not in tong:
            tong[khoa] = {}
            dem[khoa] = {}
        tong[khoa][goc] = tong[khoa].get(goc, 0.0) + sai_so
        dem[khoa][goc] = dem[khoa].get(goc, 0) + 1

    ket_qua = {}
    for khoa, gia_tri in tong.items():
        cac_goc = sorted(gia_tri)
        cac_sai_so = [gia_tri[goc] / dem[khoa][goc] for goc in cac_goc]
        ket_qua[khoa] = (cac_goc, cac_sai_so)
    return ket_qua



def ve(nhom, duong_dan_png, tieu_de='Sai số đo theo góc nghiêng'):
    """
    Vẽ đồ thị bằng matplotlib từ kết quả của gom_theo_goc và lưu ra file PNG (dpi 150).
    Gợi ý: import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
           mỗi phương pháp một màu; huong == 'doc' nét liền '-o', 'ngang' nét đứt '--s'
           plt.axhline(NGUONG_DAT_MM, ...) ; nhãn trục có đơn vị; chú thích (legend); lưới nhạt.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    mau = {}
    danh_sach_phuong_phap = list(dict.fromkeys(khoa[0] for khoa in nhom))
    bang_mau = plt.get_cmap('tab10')
    for i, phuong_phap in enumerate(danh_sach_phuong_phap):
        mau[phuong_phap] = bang_mau(i % 10)

    fig, ax = plt.subplots(figsize=(8, 5))
    for (phuong_phap, huong), (cac_goc, cac_sai_so) in sorted(nhom.items(), key=lambda x: str(x[0])):
        kieu_net = '-o' if huong == 'doc' else '--s'
        ax.plot(cac_goc, cac_sai_so, kieu_net, color=mau[phuong_phap],
                label=f'{phuong_phap} - {huong}')

    ax.axhline(NGUONG_DAT_MM, color='red', linestyle=':', linewidth=1.5,
               label=f'Ngưỡng đạt {NGUONG_DAT_MM:g} mm')
    ax.set_title(tieu_de)
    ax.set_xlabel('Góc nghiêng (độ)')
    ax.set_ylabel('Sai số (mm)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    os.makedirs(os.path.dirname(os.path.abspath(duong_dan_png)), exist_ok=True)
    fig.savefig(duong_dan_png, dpi=150)
    plt.close(fig)


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
