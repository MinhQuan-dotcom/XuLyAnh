# Đổi tên ảnh chụp thật theo thứ tự trong thu_tu_chup.csv, xếp vào đúng thư mục và tạo labels.csv
#
# Cách dùng (chạy ở thư mục gốc repo):
#   python tools/chup_anh/doi_ten_anh.py --anh_goc "D:/anh_chup"
#
# --anh_goc : thư mục chứa ảnh chép từ điện thoại (đúng 54 ảnh, chụp đúng thứ tự)
# --ra      : thư mục kết quả, mặc định data/dataset_that
#
# Ảnh được sắp theo tên file (IMG_0001, IMG_0002, ...) nên phải chụp đúng thứ tự,
# chụp hỏng thì xoá ngay trên điện thoại rồi chụp lại.
# Ảnh được thu nhỏ để cạnh dài = 1600 px cho giống bộ ảnh tổng hợp (các tham số tính theo pixel).

import argparse
import csv
import os
import re
import sys

import cv2

THU_MUC_NAY = os.path.dirname(os.path.abspath(__file__))
CANH_DAI = 1600

# giống cột của labels.csv bộ tổng hợp; các cột toạ độ và camera để trống
COT = ['file', 'bo', 'tang', 'vat', 'hinh', 'dai_mm', 'rong_mm', 'day_mm', 'theta_deg', 'huong',
       'vi_tri', 'yaw_vat_deg', 'khoang_cach_mm', 'azim_deg', 'roll_deg', 'xoay_giay_deg',
       'fx', 'fy', 'cx', 'cy'] + [f'a4_g{i}_{c}' for i in range(1, 5) for c in 'uv'] \
      + [f'vat_g{i}_{c}' for i in range(1, 5) for c in 'uv']


def doc_csv(duong_dan):
    # đọc được cả file Excel lưu ra (có BOM, phân cách bằng dấu ; hoặc ,)
    with open(duong_dan, encoding='utf-8-sig') as f:
        noi_dung = f.read()
    dau = ';' if noi_dung.splitlines()[0].count(';') > noi_dung.splitlines()[0].count(',') else ','
    return list(csv.DictReader(noi_dung.splitlines(), delimiter=dau))


def so_thuc(x):
    return float(str(x).strip().replace(',', '.'))


def sap_tu_nhien(ten):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', ten)]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--anh_goc', required=True)
    p.add_argument('--ra', default='data/dataset_that')
    p.add_argument('--thu_tu', default=os.path.join(THU_MUC_NAY, 'thu_tu_chup.csv'))
    p.add_argument('--danh_muc', default=os.path.join(THU_MUC_NAY, 'danh_muc_vat_that.csv'))
    a = p.parse_args()

    thu_tu = doc_csv(a.thu_tu)
    vat = {d['vat'].strip(): d for d in doc_csv(a.danh_muc)}

    # kiểm tra đã đo đủ kích thước vật chưa
    thieu = [v for v in sorted({r['vat'] for r in thu_tu})
             if v not in vat or not all(str(vat[v].get(c, '')).strip() for c in ('dai_mm', 'rong_mm', 'day_mm'))]
    if thieu:
        sys.exit(f'Chưa điền kích thước (dai_mm, rong_mm, day_mm) cho vật: {", ".join(thieu)} '
                 f'trong {a.danh_muc}')

    tat_ca = sorted(os.listdir(a.anh_goc), key=sap_tu_nhien)
    heic = [f for f in tat_ca if f.lower().endswith(('.heic', '.heif'))]
    if heic:
        sys.exit('Có ảnh .HEIC (iPhone). Vào Cài đặt > Camera > Định dạng, chọn "Tương thích nhất" '
                 'rồi chụp lại, hoặc đổi sang JPG trước.')
    anh = [f for f in tat_ca if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if len(anh) != len(thu_tu):
        sys.exit(f'Có {len(anh)} ảnh nhưng thu_tu_chup.csv có {len(thu_tu)} dòng. '
                 f'Kiểm tra lại: thiếu ảnh, thừa ảnh chụp hỏng, hay lẫn ảnh khác.')

    hang = []
    dung_goc_du_kien = 0
    for f, r in zip(anh, thu_tu):
        img = cv2.imread(os.path.join(a.anh_goc, f))
        if img is None:
            sys.exit(f'Không đọc được ảnh {f}')
        h, w = img.shape[:2]
        if w > h:
            print(f'  Chú ý: {f} là ảnh ngang, nên chụp dọc (cạnh dài tờ giấy theo chiều dọc ảnh)')
        k = CANH_DAI / max(h, w)
        if k < 1:
            img = cv2.resize(img, (round(w * k), round(h * k)), interpolation=cv2.INTER_AREA)

        goc_du_kien = int(so_thuc(r['goc_du_kien']))
        if str(r.get('goc_do', '')).strip():
            theta = so_thuc(r['goc_do'])
        else:
            theta = goc_du_kien
            dung_goc_du_kien += 1

        ten = f"{r['vat']}_t{goc_du_kien:02d}_{r['huong']}.jpg"
        thu_muc = os.path.join(a.ra, r['thu_muc'])
        os.makedirs(thu_muc, exist_ok=True)
        cv2.imwrite(os.path.join(thu_muc, ten), img, [cv2.IMWRITE_JPEG_QUALITY, 92])

        v = vat[r['vat']]
        dong = {c: '' for c in COT}
        dong.update({
            'file': f"{r['thu_muc']}/{ten}", 'bo': r['bo'], 'tang': r['tang'], 'vat': r['vat'],
            'hinh': v.get('hinh', 'chu_nhat').strip() or 'chu_nhat',
            'dai_mm': max(so_thuc(v['dai_mm']), so_thuc(v['rong_mm'])),
            'rong_mm': min(so_thuc(v['dai_mm']), so_thuc(v['rong_mm'])),
            'day_mm': so_thuc(v['day_mm']), 'theta_deg': theta, 'huong': r['huong'], 'vi_tri': 'giua',
        })
        hang.append(dong)
        print(f'  {f}  ->  {dong["file"]}')

    with open(os.path.join(a.ra, 'labels.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COT)
        w.writeheader()
        w.writerows(hang)
    with open(os.path.join(a.ra, 'danh_muc_vat.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['vat', 'ten', 'hinh', 'dai_mm', 'rong_mm', 'day_mm'])
        for k_, v in vat.items():
            w.writerow([k_, v.get('ten', ''), v.get('hinh', ''), v['dai_mm'], v['rong_mm'], v['day_mm']])

    print(f'\nXong: {len(hang)} ảnh trong {a.ra}')
    if dung_goc_du_kien:
        print(f'Có {dung_goc_du_kien} ảnh chưa điền goc_do, đang lấy tạm góc dự kiến.')
    print('Chạy thử: python -m src.danh_gia --du_lieu', a.ra, '--phuong_phap baseline')


if __name__ == '__main__':
    main()
