"""Phần dùng chung cho các file kiểm tra: đọc nhãn đúng (ground truth) từ bộ ảnh tổng hợp.

Các file kiểm tra được PHÉP đọc tọa độ góc trong labels.csv (để chấm điểm từng phần).
Code trong src/ thì KHÔNG được đọc.
"""
import argparse
import os
import sys

import numpy as np

GOC_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if GOC_REPO not in sys.path:
    sys.path.insert(0, GOC_REPO)

from src import tien_ich            # noqa: E402
from src.giay import sap_xep_4_goc  # noqa: E402


def tham_so(mo_ta):
    p = argparse.ArgumentParser(description=mo_ta)
    p.add_argument('--du_lieu', default=os.path.join(GOC_REPO, 'data', 'mau'),
                   help='thư mục có labels.csv (mặc định data/mau; chạy kỹ hơn: data/dataset_vat_phang)')
    p.add_argument('--bo', default=None, help='chỉ kiểm tra một bộ: dev, eval, ...')
    return p.parse_args()


def doc_nhan(a):
    nhan = tien_ich.doc_nhan(a.du_lieu)
    if a.bo:
        nhan = tien_ich.loc(nhan, bo=a.bo)
    if 'a4_g1_u' not in nhan[0] or nhan[0]['a4_g1_u'] in ('', None):
        sys.exit('Bộ dữ liệu này không có tọa độ góc (ảnh thật?). Hãy dùng bộ ảnh tổng hợp.')
    return nhan


def goc_giay_dung(h):
    """4 góc tờ giấy đúng, thứ tự trên-trái, trên-phải, dưới-phải, dưới-trái."""
    p = np.array([[float(h[f'a4_g{i}_u']), float(h[f'a4_g{i}_v'])] for i in range(1, 5)])
    return sap_xep_4_goc(p)


def goc_vat_dung(h):
    """4 góc hình chữ nhật bao đáy vật, pixel ảnh gốc."""
    return np.array([[float(h[f'vat_g{i}_u']), float(h[f'vat_g{i}_v'])] for i in range(1, 5)])


def ket_luan(dat, mo_ta):
    print('\n' + ('ĐẠT' if dat else 'CHƯA ĐẠT') + ' – ' + mo_ta)
    return 0 if dat else 1
