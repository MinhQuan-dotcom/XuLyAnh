# Đo kích thước vật từ ảnh chụp nghiêng (dùng tờ A4 làm chuẩn)

Bài tập lớn môn Xử lý ảnh và Thị giác máy tính (121036) - ĐH GTVT TP.HCM.
Nhóm: ........  Lớp: ........

Đề tài: chụp một vật đặt trên tờ giấy A4 rồi đo chiều dài, chiều rộng của vật (mm).
Khó khăn chính là ảnh thường bị chụp nghiêng, nên nếu chỉ lấy một tỉ lệ pixel/mm cho cả ảnh
(cách làm thông thường, gọi là baseline) thì càng nghiêng càng sai.
Nhóm làm theo hướng: tìm 4 góc tờ giấy, chỉnh lại góc cho chính xác, tính homography để nắn ảnh
về nhìn thẳng rồi mới đo.

## Cài đặt

```
git clone https://github.com/MinhQuan-dotcom/XuLyAnh.git
cd XuLyAnh
pip install -r requirements.txt
```

Dùng Python 3.9 trở lên.

## Chạy thử

Trong repo có sẵn 25 ảnh mẫu ở `data/mau`:

```
python -m src.danh_gia --du_lieu data/mau --phuong_phap baseline
python -m src.danh_gia --du_lieu data/mau --phuong_phap de_xuat
```

Bộ ảnh đầy đủ (286 ảnh) để trên Drive, xem cách tải ở `data/README.md`. Có bộ đầy đủ rồi thì chạy
các thí nghiệm:

```
python experiments/e1.py --du_lieu data/dataset_vat_phang
python experiments/e2.py --du_lieu data/dataset_vat_phang
python experiments/e3.py --du_lieu data/dataset_vat_phang
python experiments/e4.py --du_lieu data/dataset_vat_phang
```

Kết quả nằm trong thư mục `results/`.

## Các thư mục

```
src/            code chính
  giay.py         tìm tờ giấy (phần A)
  goc.py          chỉnh lại 4 góc giấy (phần B)
  hinh_hoc.py     homography, nắn ảnh (phần C)
  vat.py          tách vật, đo kích thước pixel (phần D)
  baseline.py     cách đo thông thường (phần E)
  phuong_phap.py  ghép các phần lại thành phương pháp của nhóm
  cau_hinh.py     các tham số
  danh_gia.py     tính sai số, tổng hợp theo tầng
  tien_ich.py     đọc nhãn, đọc ảnh, ghi csv
tests/          file kiểm tra cho từng phần A-E
experiments/    e1-e4 và vẽ đồ thị
data/           ảnh mẫu + hướng dẫn tải dữ liệu
tools/          script tạo bộ ảnh tổng hợp
report/         nháp báo cáo
docs/           quy ước code, chia việc
```

Chia việc phần code: xem `docs/CHIA_VIEC_CODE.md`. Quy ước chung: `docs/QUY_UOC.md`.
