"""Phần dùng chung cho các script thí nghiệm: thêm thư mục gốc repo vào sys.path, đọc tham số dòng lệnh."""
import argparse
import os
import sys

GOC_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if GOC_REPO not in sys.path:
    sys.path.insert(0, GOC_REPO)


def tham_so_dong_lenh(mo_ta, du_lieu_mac_dinh='data/dataset_vat_phang'):
    p = argparse.ArgumentParser(description=mo_ta)
    p.add_argument('--du_lieu', default=du_lieu_mac_dinh, help='thư mục chứa labels.csv và ảnh')
    p.add_argument('--ra', default='results', help='thư mục ghi kết quả')
    return p.parse_args()
