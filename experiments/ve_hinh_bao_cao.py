"""
Vẽ các hình dùng trong báo cáo (mục 4, 6, 8.2, 8.4) từ kết quả E1, E3, E4 đã chạy.

Chạy sau khi đã có:
  results/e3/ket_qua_e3.csv, results/that/e3/ket_qua_e3.csv  (e3.py trên ảnh tổng hợp và ảnh thật)
  results/e4/e4b_ket_qua.csv                                  (e4.py)

  python experiments/ve_hinh_bao_cao.py
Hình lưu vào results/hinh_bao_cao/. Cần chạy e2.py trước nếu muốn có hình 8.2.
"""
import argparse
import csv
import os
import sys
from collections import defaultdict

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, GOC)
from src import baseline, phuong_phap, giay, vat, hinh_hoc, goc as goc_mod  # noqa: E402
from src.cau_hinh import THAM_SO_DE_XUAT  # noqa: E402

plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#dddddd',
                     'grid.linewidth': 0.6, 'axes.axisbelow': True})
XANH, CAM = '#2a78d6', '#eb6834'
RAMP = ['#86b6ef', '#5598e7', '#2a78d6', '#1c5cab', '#104281']   # độ dày tăng dần
TEN_TANG = [('nhe', 'Nhẹ'), ('trung_binh', 'Trung bình'), ('nang', 'Nặng')]


def doc_csv(p):
    with open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def thu_nho(anh, cao=420):
    h, w = anh.shape[:2]
    return cv2.resize(anh, (int(w * cao / h), cao), interpolation=cv2.INTER_AREA)


def ghep_ngang(ds_anh, khoang=12):
    cao = min(640, min(a.shape[0] for a in ds_anh))
    ds_anh = [thu_nho(a, cao) for a in ds_anh]
    trang = np.full((cao, khoang, 3), 255, np.uint8)
    out = []
    for i, a in enumerate(ds_anh):
        if i:
            out.append(trang)
        out.append(a)
    return np.hstack(out)


def hinh_ket_qua(ham, duong_dan, khoa='ket_qua'):
    anh = cv2.imread(duong_dan)
    dai, rong, tg = ham(anh)
    return tg.get(khoa, anh), dai, rong


def bieu_do_e3(ra):
    """MAE chiều dài theo tầng, baseline và phương pháp đầy đủ, ảnh tổng hợp và ảnh thật."""
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    for ax, (p, tieu_de) in zip(axs, [('results/e3/ket_qua_e3.csv', 'Ảnh tổng hợp (144 ảnh)'),
                                      ('results/that/e3/ket_qua_e3.csv', 'Ảnh thật (36 ảnh)')]):
        r = doc_csv(os.path.join(GOC, p))
        g = defaultdict(list)
        for d in r:
            g[(d['phuong_phap'], d['tang'])].append(float(d['sai_so_dai']))
        x = np.arange(3)
        for k, (pp, ten, mau) in enumerate([('baseline', 'Baseline', CAM), ('day_du', 'Phương pháp P', XANH)]):
            y = [np.mean(g[(pp, t)]) for t, _ in TEN_TANG]
            b = ax.bar(x + (k - 0.5) * 0.36, y, 0.34, color=mau, label=ten, edgecolor='white', linewidth=1)
            for xi, yi in zip(x + (k - 0.5) * 0.36, y):
                ax.text(xi, yi + 0.3, f'{yi:.2f}', ha='center', va='bottom', fontsize=8, color='#333333')
        ax.set_xticks(x, [n for _, n in TEN_TANG])
        ax.set_ylim(0, 18)
        ax.grid(axis='x', visible=False)
        ax.set_title(tieu_de, fontsize=10)
        ax.set_xlabel('Tầng góc nghiêng')
    axs[0].set_ylabel('Sai số TB chiều dài (mm)')
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, loc='lower center', ncol=2)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(os.path.join(ra, 'hinh_8_3_so_sanh_e3.png'), dpi=200)
    plt.close(fig)


def bieu_do_e4(ra):
    """Sai số chiều dài (vật đặt dọc) theo góc nghiêng, mỗi đường một độ dày."""
    r = [d for d in doc_csv(os.path.join(GOC, 'results/e4/e4b_ket_qua.csv')) if d['huong'] == 'doc']
    g = defaultdict(dict)
    for d in r:
        g[float(d['day_mm'])][int(d['goc'])] = float(d['dai_do']) - float(d['dai_that'])
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for mau, (t, v) in zip(RAMP, sorted(g.items())):
        x = sorted(v)
        ax.plot(x, [v[i] for i in x], color=mau, lw=2, marker='o', ms=5, label=f't = {t:g} mm')
    ax.axhline(1.0, color='#555555', lw=1, ls='--', label='ngưỡng 1 mm')
    ax.set_xticks([0, 15, 30, 45])
    ax.set_xlabel('Góc nghiêng θ (độ)')
    ax.set_ylabel('Sai số có dấu, chiều dài (mm)')
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(ra, 'hinh_8_4_vat_day_e4.png'), dpi=200)
    plt.close(fig)


def _e2_chi_so(p, ten, g):
    for d in doc_csv(p):
        if d['tham_so'] == ten and float(d['gia_tri']) == float(g):
            return d
    return None


def _cat_quanh(anh, tam, r):
    x, y = int(round(tam[0])), int(round(tam[1]))
    h, w = anh.shape[:2]
    x0, y0 = max(0, x - r), max(0, y - r)
    return anh[y0:min(h, y + r), x0:min(w, x + r)], (x0, y0)


def _ve_goc(anh, goc, goc_that, r=45, phong=6):
    """Cắt vùng quanh góc giấy xa camera, phóng to; đỏ: góc tìm được, xanh lá: góc thật (nhãn)."""
    goc = np.asarray(goc, float)
    i = int(np.argmin(np.linalg.norm(goc - goc_that, axis=1)))
    cat, (x0, y0) = _cat_quanh(anh, goc_that, r)
    cat = cv2.resize(cat, None, fx=phong, fy=phong, interpolation=cv2.INTER_NEAREST)
    for (px, py), mau in [(goc[i], (0, 0, 255)), (goc_that, (0, 170, 0))]:
        c = (int((px - x0 + 0.5) * phong), int((py - y0 + 0.5) * phong))
        cv2.drawMarker(cat, c, mau, cv2.MARKER_CROSS, 40, 3)
    return cat, float(np.linalg.norm(goc[i] - goc_that))


def _ve_vat(anh_nan, contour, s, cao=360):
    out = anh_nan.copy()
    if contour is not None:
        cv2.drawContours(out, [contour], -1, (0, 0, 255), max(1, int(s / 2)))
    x, y, w, h = cv2.boundingRect(contour) if contour is not None else (0, 0, out.shape[1], out.shape[0])
    m = int(12 * s)
    out = out[max(0, y - m):y + h + m, max(0, x - m):x + w + m]
    return cv2.resize(out, (int(out.shape[1] * cao / out.shape[0]), cao), interpolation=cv2.INTER_NEAREST)


def e2_song_song(ra, th, that):
    """Hình E2: mỗi hàng một tham số, ba giá trị (thấp, đã chọn, cao), ảnh kết quả và chỉ số đặt cạnh nhau."""
    csv_th = os.path.join(GOC, 'results/e2/tong_hop_e2.csv')
    csv_that = os.path.join(GOC, 'results/that/e2/tong_hop_e2.csv')
    if not (os.path.exists(csv_th) and os.path.exists(csv_that)):
        return
    f_th = 'dev/d1_the_thanh_vien_t45_doc.jpg'
    nhan = {d['file']: d for d in doc_csv(os.path.join(th, 'labels.csv'))}[f_th]
    anh_th = cv2.imread(os.path.join(th, f_th))
    goc_that = np.array([float(nhan['a4_g3_u']), float(nhan['a4_g3_v'])])
    anh_that = cv2.imread(os.path.join(that, 'dev/d1_t30_doc.jpg'))
    TS = THAM_SO_DE_XUAT

    hang = []   # (nhãn hàng, [(ảnh, tiêu đề)])
    o = []
    for g in [1, 5, 21]:
        goc, _ = giay.tim_to_giay(anh_th, {**TS, 'kich_thuoc_lam_mo': g})
        im, e = _ve_goc(anh_th, goc, goc_that)
        d = _e2_chi_so(csv_th, 'kich_thuoc_lam_mo', g)
        o.append((im, f'ksize = {g}: góc thô lệch {e:.1f} px\nMAE dài {float(d["mae_dai_mm"]):.2f} mm'))
    hang.append(('Tìm giấy\n(kích thước làm mờ)', o))
    for ten, ds, nhan_h in [('canny_cao', [30, 150, 300], 'Chỉnh góc\n(ngưỡng Canny cao)'),
                            ('do_rong_dai_canh', [1, 8, 32], 'Chỉnh góc\n(độ rộng dải, px)')]:
        o = []
        goc_tho, _ = giay.tim_to_giay(anh_th, TS)
        for g in ds:
            goc = goc_mod.tinh_chinh_goc(anh_th, goc_tho, {**TS, ten: g})
            im, e = _ve_goc(anh_th, goc, goc_that)
            d = _e2_chi_so(csv_th, ten, g)
            o.append((im, f'{g}: góc lệch {e:.1f} px\nMAE dài {float(d["mae_dai_mm"]):.2f} mm'))
        hang.append((nhan_h, o))
    o = []
    goc_tho, _ = giay.tim_to_giay(anh_th, TS)
    goc = goc_mod.tinh_chinh_goc(anh_th, goc_tho, TS)
    for g in [1.0, 4.0, 8.0]:
        nan, _ = hinh_hoc.nan_anh(anh_th, goc, g)
        ct = vat.tach_vat(nan, None, {**TS, 'do_phan_giai_nan': g})
        d = _e2_chi_so(csv_th, 'do_phan_giai_nan', g)
        o.append((_ve_vat(nan, ct, g), f's = {g:g} px/mm\nMAE dài {float(d["mae_dai_mm"]):.2f}, có dấu {float(d["sai_so_dai_co_dau_mm"]):+.2f} mm'))
    hang.append(('Nắn ảnh\n(độ phân giải s)', o))
    goc_tho, _ = giay.tim_to_giay(anh_that, TS)
    goc = goc_mod.tinh_chinh_goc(anh_that, goc_tho, TS)
    nan, _ = hinh_hoc.nan_anh(anh_that, goc, 4.0)
    for ten, ds, nhan_h in [('nguong_s', [20, 60, 140], 'Tách vật, ảnh thật\n(ngưỡng S)'),
                            ('he_so_v', [0.0, 0.5, 0.7], 'Tách vật, ảnh thật\n(hệ số V)')]:
        o = []
        for g in ds:
            ct = vat.tach_vat(nan, None, {**TS, ten: g})
            d = _e2_chi_so(csv_that, ten, g)
            o.append((_ve_vat(nan, ct, 4.0), f'{g:g}: đo được {float(d["ti_le_do_duoc_%"]):.0f}%\nMAE dài {float(d["mae_dai_mm"]):.2f}, rộng {float(d["mae_rong_mm"]):.2f} mm'))
        hang.append((nhan_h, o))

    fig, axs = plt.subplots(len(hang), 3, figsize=(7.2, 2.25 * len(hang)))
    for r, (nhan_h, o) in enumerate(hang):
        for c, (im, td) in enumerate(o):
            ax = axs[r, c]
            ax.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
            ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
            for sp in ax.spines.values():
                sp.set_visible(True); sp.set_color('#999999')
            ax.set_title(td.replace('.', ','), fontsize=7.5)
        axs[r, 0].set_ylabel(nhan_h, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(ra, 'hinh_8_e2_song_song.png'), dpi=170)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--that', default='data/dataset_that')
    ap.add_argument('--tong_hop', default='data/dataset_vat_phang')
    ap.add_argument('--ra', default='results/hinh_bao_cao')
    a = ap.parse_args()
    ra = os.path.join(GOC, a.ra)
    os.makedirs(ra, exist_ok=True)
    that = os.path.join(GOC, a.that)
    th = os.path.join(GOC, a.tong_hop)
    bl = baseline.do_kich_thuoc
    pp = phuong_phap.do_kich_thuoc

    # Mục 6: các bước của P trên một ảnh thật
    anh = cv2.imread(os.path.join(that, 'eval/tang2_trungbinh_15-35/v3_t30_doc.jpg'))
    _, _, tg = pp(anh)
    buoc = [tg['goc'], tg['goc_tho'], tg['goc_tinh_chinh'], tg['anh_nan'], tg['ket_qua']]
    cv2.imwrite(os.path.join(ra, 'hinh_6_1_cac_buoc.png'), ghep_ngang(buoc))

    # Mục 4: ba ảnh baseline đo sai trên ảnh thật
    ds = []
    for f in ['tang2_trungbinh_15-35/v1_t30_doc.jpg', 'tang3_nang_35-55/v2_t50_doc.jpg',
              'tang3_nang_35-55/v3_t50_doc.jpg']:
        im, dai, rong = hinh_ket_qua(bl, os.path.join(that, 'eval', f))
        ds.append(im)
        print(f, f'baseline {dai:.1f} x {rong:.1f} mm')
    cv2.imwrite(os.path.join(ra, 'hinh_4_1_baseline_sai.png'), ghep_ngang(ds))

    # Mục 4: cùng vật, cùng góc, đặt dọc và đặt ngang
    ds = []
    for f in ['v1_t30_doc.jpg', 'v1_t30_ngang.jpg']:
        im, dai, rong = hinh_ket_qua(bl, os.path.join(that, 'eval/tang2_trungbinh_15-35', f))
        ds.append(im)
        print(f, f'baseline {dai:.1f} x {rong:.1f} mm')
    cv2.imwrite(os.path.join(ra, 'hinh_4_2_doc_ngang.png'), ghep_ngang(ds))

    # Mục 4: cùng vật, cùng góc, mép gần và mép xa tờ giấy (ảnh tổng hợp)
    ds = []
    for f in ['v03_bia_do_dai_t40_doc_gan.jpg', 'v03_bia_do_dai_t40_doc_xa.jpg']:
        im, dai, rong = hinh_ket_qua(bl, os.path.join(th, 'minh_hoa_vi_tri', f))
        ds.append(im)
        print(f, f'baseline {dai:.1f} x {rong:.1f} mm')
    cv2.imwrite(os.path.join(ra, 'hinh_4_3_gan_xa.png'), ghep_ngang(ds))

    # Mục 8.1: ảnh trung gian của E2 với tham số đã chọn (ảnh tổng hợp)
    tg_e2 = os.path.join(GOC, 'results/e2/trung_gian/do_phan_giai_nan_4.0')
    if os.path.isdir(tg_e2):
        ds = [cv2.imread(os.path.join(tg_e2, f'mau_{i}_{k}.jpg')) for i, k in
              enumerate(['goc', 'goc_tho', 'goc_tinh_chinh', 'anh_nan', 'ket_qua'], 1)]
        if all(x is not None for x in ds):
            cv2.imwrite(os.path.join(ra, 'hinh_8_2_trung_gian_e2.png'), ghep_ngang(ds))

    e2_song_song(ra, th, that)
    bieu_do_e3(ra)
    bieu_do_e4(ra)
    print('Đã lưu hình vào', ra)


if __name__ == '__main__':
    main()
