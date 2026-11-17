"""
Các bảng phân tích thêm cho báo cáo (mục 4, 8.2, 8.4, 9). Đọc kết quả đã có, chỉ chạy lại
baseline và P trên 6 ảnh minh_hoa_vi_tri.

Cần chạy trước:
  python experiments/e1.py --du_lieu data/dataset_vat_phang
  python experiments/e3.py --du_lieu data/dataset_vat_phang
  python experiments/e3.py --du_lieu data/dataset_that --ra results/that
  python experiments/e4.py --du_lieu data/dataset_vat_phang

  python experiments/phan_tich_them.py

Ghi ra:
  results/e1/canh_ngan_baseline.csv     baseline lấy tỉ lệ từ cạnh nào của tờ giấy, theo tầng
  results/e1/ti_le_do_baseline.csv      tỉ số đo/thật trung bình của baseline theo tầng và hướng
  results/e1/vi_tri_gan_xa.csv          cùng vật ở mép gần và mép xa tờ giấy (baseline và P)
  results/e3/theo_do_day.csv            P theo tầng và nhóm độ dày (gồm cả tầng cực nặng)
  results/e3/chenh_doc_ngang.csv        chênh lệch chiều dài giữa đặt dọc và đặt ngang
  results/that/e3/theo_huong_day_du.csv P trên ảnh thật theo tầng và hướng
  results/that/e3/sai_so_co_dau_theo_vat.csv
"""
import csv
import os
from collections import defaultdict

import numpy as np
import cv2

import _chung
from src import tien_ich, danh_gia

TANG = ['nhe', 'trung_binh', 'nang', 'cuc_nang']


def doc(p):
    with open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def tb(x):
    return round(float(np.mean(x)), 2) if len(x) else ''


def thu_tu(k):
    return [TANG.index(x) if x in TANG else str(x) for x in k]


def canh_ngan(du_lieu, ra):
    """Cạnh ngắn của minAreaRect bao tờ giấy (dùng để lấy tỉ lệ ở baseline) là cạnh 210 mm hay cạnh 297 mm."""
    nhan = [d for d in doc(os.path.join(du_lieu, 'labels.csv')) if d['bo'] == 'eval']
    dem = defaultdict(lambda: [0, 0, []])
    for d in nhan:
        q = np.array([[float(d[f'a4_g{i}_{c}']) for c in 'uv'] for i in range(1, 5)], np.float32)
        hop = cv2.boxPoints(cv2.minAreaRect(q))
        canh = [hop[(i + 1) % 4] - hop[i] for i in range(4)]
        v = canh[int(np.argmin([np.linalg.norm(c) for c in canh]))]
        # g1-g2 là cạnh 210 mm nằm ngang gần camera; cạnh ngắn nằm dọc ảnh nghĩa là cạnh 297 mm bị co
        dem[d['tang']][0] += 1
        dem[d['tang']][1] += int(abs(v[1]) > abs(v[0]))
        dem[d['tang']][2].append(float(d['theta_deg']))
    bang = [{'tang': t, 'so_anh': n, 'so_anh_lay_canh_297': k,
             'theta_min': round(min(th), 1), 'theta_max': round(max(th), 1)}
            for t, (n, k, th) in sorted(dem.items(), key=lambda x: TANG.index(x[0]))]
    tien_ich.ghi_csv(os.path.join(ra, 'e1', 'canh_ngan_baseline.csv'), bang)
    danh_gia.in_bang(bang)


def ti_le_baseline(ra):
    r = doc(os.path.join(ra, 'e1', 'ket_qua_baseline.csv'))
    g = defaultdict(list)
    for d in r:
        g[(d['tang'], d['huong'])].append(d)
    bang = []
    for (t, h), v in sorted(g.items(), key=lambda x: thu_tu(x[0])):
        bang.append({'tang': t, 'huong': h, 'so_anh': len(v),
                     'ti_le_dai': round(float(np.mean([float(x['dai_do']) / float(x['dai_that']) for x in v])), 3),
                     'ti_le_rong': round(float(np.mean([float(x['rong_do']) / float(x['rong_that']) for x in v])), 3)})
    tien_ich.ghi_csv(os.path.join(ra, 'e1', 'ti_le_do_baseline.csv'), bang)
    danh_gia.in_bang(bang)


def vi_tri(du_lieu, ra):
    nhan = tien_ich.loc(tien_ich.doc_nhan(du_lieu), bo='minh_hoa_vi_tri')
    bang = []
    for ten in ['baseline', 'de_xuat']:
        for d in danh_gia.chay(danh_gia.lay_ham(ten), nhan, du_lieu, ten=ten):
            ten_file = os.path.basename(d['file'])
            bang.append({'phuong_phap': ten, 'vat': d['vat'], 'vi_tri': 'gan' if '_gan' in ten_file else 'xa',
                         'theta_deg': d['theta_deg'], 'dai_that': d['dai_that'], 'rong_that': d['rong_that'],
                         'dai_do': d['dai_do'], 'rong_do': d['rong_do']})
    tien_ich.ghi_csv(os.path.join(ra, 'e1', 'vi_tri_gan_xa.csv'), bang)
    danh_gia.in_bang(bang)


def nhom_day(t):
    t = float(t)
    return 'mong_0.1-0.5' if t <= 0.5 else ('vua_0.76-1.2' if t <= 1.2 else 'day_2-3')


def theo_do_day(ra):
    r = [d for d in doc(os.path.join(ra, 'e3', 'ket_qua_e3.csv')) if d['phuong_phap'] == 'day_du']
    r += [dict(d, tang='cuc_nang') for d in doc(os.path.join(ra, 'e4', 'e4a_ket_qua.csv'))]
    g = defaultdict(list)
    for d in r:
        g[(d['tang'], nhom_day(d['day_mm']))].append(d)
    bang = []
    for (t, n), v in sorted(g.items(), key=lambda x: thu_tu(x[0])):
        th = [float(x['theta_deg']) for x in v]
        bang.append({'tang': t, 'nhom_day': n, 'so_anh': len(v),
                     'theta': f'{min(th):.0f}-{max(th):.0f}',
                     'mae_dai_mm': tb([float(x['sai_so_dai']) for x in v]),
                     'mae_rong_mm': tb([float(x['sai_so_rong']) for x in v]),
                     'sai_so_dai_co_dau_mm': tb([float(x['dai_do']) - float(x['dai_that']) for x in v]),
                     'dat_<=1mm_%': round(100 * float(np.mean([float(x['sai_so_mm']) <= 1 for x in v])), 1)})
    tien_ich.ghi_csv(os.path.join(ra, 'e3', 'theo_do_day.csv'), bang)
    danh_gia.in_bang(bang)


def chenh_doc_ngang(ra):
    bang = []
    for bo, p in [('tong_hop', os.path.join(ra, 'e3', 'ket_qua_e3.csv')),
                  ('that', os.path.join(ra, 'that', 'e3', 'ket_qua_e3.csv'))]:
        r = doc(p)
        for pp in ['baseline', 'day_du']:
            cap = defaultdict(dict)
            for d in r:
                if d['phuong_phap'] == pp:
                    cap[d['file'].replace('_doc', '').replace('_ngang', '')][d['huong']] = float(d['dai_do'])
            for t in TANG[:3]:
                ds = [abs(v['doc'] - v['ngang']) for k, v in cap.items() if len(v) == 2 and f'/tang' in k
                      and t == {'tang1': 'nhe', 'tang2': 'trung_binh', 'tang3': 'nang'}[k.split('/')[1][:5]]]
                bang.append({'bo_anh': bo, 'phuong_phap': pp, 'tang': t, 'so_cap': len(ds),
                             'chenh_dai_tb_mm': tb(ds)})
    tien_ich.ghi_csv(os.path.join(ra, 'e3', 'chenh_doc_ngang.csv'), bang)
    danh_gia.in_bang(bang)


def that(ra):
    r = [d for d in doc(os.path.join(ra, 'that', 'e3', 'ket_qua_e3.csv')) if d['phuong_phap'] == 'day_du']
    g = defaultdict(list)
    for d in r:
        g[(d['tang'], d['huong'])].append(d)
    bang = [{'tang': t, 'huong': h, 'so_anh': len(v),
             'mae_dai_mm': tb([float(x['sai_so_dai']) for x in v]),
             'mae_rong_mm': tb([float(x['sai_so_rong']) for x in v])}
            for (t, h), v in sorted(g.items(), key=lambda x: thu_tu(x[0]))]
    tien_ich.ghi_csv(os.path.join(ra, 'that', 'e3', 'theo_huong_day_du.csv'), bang)
    danh_gia.in_bang(bang)

    g = defaultdict(list)
    for d in r:
        g[d['vat']].append(d)
    bang = []
    for v, ds in sorted(g.items()):
        # sai số theo trục dài tờ giấy: chiều dài khi đặt dọc, chiều rộng khi đặt ngang
        truc_dai = [float(x['dai_do']) - float(x['dai_that']) if x['huong'] == 'doc'
                    else float(x['rong_do']) - float(x['rong_that']) for x in ds]
        bang.append({'vat': v, 'so_anh': len(ds), 'day_mm': ds[0]['day_mm'],
                     'sai_so_dai_co_dau_mm': tb([float(x['dai_do']) - float(x['dai_that']) for x in ds]),
                     'sai_so_rong_co_dau_mm': tb([float(x['rong_do']) - float(x['rong_that']) for x in ds]),
                     'sai_so_theo_truc_dai_giay_mm': tb(truc_dai)})
    tien_ich.ghi_csv(os.path.join(ra, 'that', 'e3', 'sai_so_co_dau_theo_vat.csv'), bang)
    danh_gia.in_bang(bang)


def main():
    a = _chung.tham_so_dong_lenh(__doc__)
    canh_ngan(a.du_lieu, a.ra)
    ti_le_baseline(a.ra)
    vi_tri(a.du_lieu, a.ra)
    theo_do_day(a.ra)
    chenh_doc_ngang(a.ra)
    that(a.ra)


if __name__ == '__main__':
    main()
