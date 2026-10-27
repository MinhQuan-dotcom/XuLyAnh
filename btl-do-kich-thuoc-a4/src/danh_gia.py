"""
Chấm điểm dùng chung cho baseline và phương pháp đề xuất.
Người phụ trách: N1 (khung), N3 (bổ sung nếu cần).

Chạy thử từ thư mục gốc repo:
  python -m src.danh_gia --du_lieu data/mau --phuong_phap baseline
  python -m src.danh_gia --du_lieu data/dataset_vat_phang --phuong_phap de_xuat --bo eval
"""
import argparse
import math
import os
import time
from collections import defaultdict

from src import tien_ich
from src.cau_hinh import NGUONG_DAT_MM


def lay_ham(ten):
    if ten == 'baseline':
        from src.baseline import do_kich_thuoc
    elif ten == 'de_xuat':
        from src.phuong_phap import do_kich_thuoc
    else:
        raise ValueError('phuong_phap phải là baseline hoặc de_xuat')
    return do_kich_thuoc


def chay(ham_do, nhan, thu_muc_du_lieu, tham_so=None, ten='', luu_trung_gian=None):
    """Chạy ham_do trên từng ảnh trong nhan. Trả về list dict theo tien_ich.COT_KET_QUA.
    luu_trung_gian: thư mục để lưu ảnh trung gian (None = không lưu)."""
    ket_qua = []
    for i, h in enumerate(nhan):
        anh = tien_ich.doc_anh(thu_muc_du_lieu, h['file'])
        t0 = time.perf_counter()
        try:
            dai, rong, trung_gian = ham_do(anh, tham_so)
        except Exception as e:                      # một ảnh lỗi không làm dừng cả lượt chạy
            print('  Lỗi ở', h['file'], ':', e)
            dai, rong, trung_gian = None, None, {}
        ms = (time.perf_counter() - t0) * 1000
        do_duoc = dai is not None and rong is not None
        if do_duoc:
            dai, rong = max(dai, rong), min(dai, rong)
        dong = {
            'file': h['file'], 'phuong_phap': ten, 'bo': h['bo'], 'tang': h['tang'],
            'huong': h.get('huong', ''), 'vat': h.get('vat', ''), 'theta_deg': h['theta_deg'],
            'day_mm': h.get('day_mm', ''), 'dai_that': h['dai_mm'], 'rong_that': h['rong_mm'],
            'dai_do': round(dai, 2) if do_duoc else '', 'rong_do': round(rong, 2) if do_duoc else '',
            'sai_so_dai': round(abs(dai - h['dai_mm']), 2) if do_duoc else '',
            'sai_so_rong': round(abs(rong - h['rong_mm']), 2) if do_duoc else '',
            'sai_so_mm': round(max(abs(dai - h['dai_mm']), abs(rong - h['rong_mm'])), 2) if do_duoc else '',
            'do_duoc': int(do_duoc), 'thoi_gian_ms': round(ms, 1),
        }
        ket_qua.append(dong)
        if luu_trung_gian and trung_gian:
            tien_to = os.path.splitext(os.path.basename(h['file']))[0]
            tien_ich.luu_anh_trung_gian(luu_trung_gian, tien_to, trung_gian)
        if (i + 1) % 50 == 0:
            print(f'  {i + 1}/{len(nhan)} ảnh')
    return ket_qua


def _tb(x):
    return sum(x) / len(x) if x else float('nan')


def tong_hop(ket_qua, theo=('tang', 'huong')):
    """Gom kết quả theo các cột trong `theo`. Mỗi nhóm cho: số ảnh, % đo được, MAE dài/rộng (mm),
    % ảnh có sai số <= NGUONG_DAT_MM, thời gian trung bình."""
    nhom = defaultdict(list)
    for d in ket_qua:
        nhom[tuple(d[c] for c in theo)].append(d)
    bang = []
    def _khoa_sap_xep(k):
        out = []
        for x in k:
            try:
                out.append((0, float(x), ''))
            except (TypeError, ValueError):
                out.append((1, 0.0, str(x)))
        return tuple(out)
    for khoa in sorted(nhom, key=_khoa_sap_xep):
        ds = nhom[khoa]
        ok = [d for d in ds if d['do_duoc']]
        dong = {c: v for c, v in zip(theo, khoa)}
        dong.update({
            'so_anh': len(ds),
            'ti_le_do_duoc_%': round(100 * len(ok) / len(ds), 1),
            'mae_dai_mm': round(_tb([d['sai_so_dai'] for d in ok]), 2),
            'mae_rong_mm': round(_tb([d['sai_so_rong'] for d in ok]), 2),
            f'dat_<={NGUONG_DAT_MM:g}mm_%': round(100 * sum(d['sai_so_mm'] <= NGUONG_DAT_MM for d in ok) / len(ds), 1),
            'thoi_gian_tb_ms': round(_tb([d['thoi_gian_ms'] for d in ds]), 1),
        })
        bang.append(dong)
    return bang


def in_bang(bang):
    if not bang:
        print('(trống)')
        return
    cot = list(bang[0].keys())
    rong = [max(len(str(c)), *(len(_fmt(d[c])) for d in bang)) for c in cot]
    print('  '.join(str(c).ljust(w) for c, w in zip(cot, rong)))
    for d in bang:
        print('  '.join(_fmt(d[c]).ljust(w) for c, w in zip(cot, rong)))


def _fmt(v):
    if isinstance(v, float) and math.isnan(v):
        return '-'
    return str(v)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--du_lieu', default='data/dataset_vat_phang')
    p.add_argument('--phuong_phap', default='baseline', choices=['baseline', 'de_xuat'])
    p.add_argument('--bo', default=None, help='dev | eval | e4_cucnang_55-75 | e4_vat_day ... (mặc định: tất cả)')
    p.add_argument('--ra', default='results')
    a = p.parse_args()

    nhan = tien_ich.loc(tien_ich.doc_nhan(a.du_lieu), bo=a.bo)
    print(f'Chạy {a.phuong_phap} trên {len(nhan)} ảnh...')
    kq = chay(lay_ham(a.phuong_phap), nhan, a.du_lieu, ten=a.phuong_phap)
    ten_file = f'{a.phuong_phap}_{a.bo or "tat_ca"}.csv'
    tien_ich.ghi_csv(os.path.join(a.ra, ten_file), kq, tien_ich.COT_KET_QUA)
    bang = tong_hop(kq)
    in_bang(bang)
    tien_ich.ghi_csv(os.path.join(a.ra, 'tong_hop_' + ten_file), bang)


if __name__ == '__main__':
    main()
