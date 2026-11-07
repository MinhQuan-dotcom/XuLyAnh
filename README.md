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
python -m pip install -r requirements.txt
```

Dùng Python 3.9 trở lên. Trên Windows nên bật UTF-8 để in được tiếng Việt (làm 1 lần trong Git Bash):

```
echo 'export PYTHONUTF8=1' >> ~/.bashrc
source ~/.bashrc
```

## Dữ liệu

| Bộ | Số ảnh | Ở đâu |
|---|---|---|
| `data/mau` | 25 ảnh tổng hợp | có sẵn trong repo, dùng để chạy thử |
| `data/dataset_vat_phang` | 286 ảnh tổng hợp | tải từ Drive, xem `data/README.md` |
| `data/dataset_that` | 48 ảnh tự chụp | tải từ Drive, xem `data/README.md` |

Ảnh tổng hợp biết chính xác góc nghiêng và kích thước, dùng để phát triển, kiểm tra từng phần và cho E4.
Ảnh tự chụp là tập đánh giá chính (3 tầng góc 10, 30, 50 độ và tập dev; không có tầng cực nặng).

## Chạy thử

```
python -m src.danh_gia --du_lieu data/mau --phuong_phap baseline
python -m src.danh_gia --du_lieu data/mau --phuong_phap de_xuat
```

## Kiểm tra từng phần (chỉ chạy trên ảnh tổng hợp)

```
python tests/kiem_tra_A.py --du_lieu data/dataset_vat_phang
```

Đổi `A` thành `B`, `C`, `D`, `E`. Kiểm tra ghép baseline với code thật của A và D:
`python tests/kiem_tra_E.py --that --du_lieu data/dataset_vat_phang`.
Các file này cần toạ độ góc trong nhãn nên không chạy được với ảnh thật.

## Thí nghiệm

Trên ảnh tổng hợp:

```
python experiments/e1.py --du_lieu data/dataset_vat_phang
python experiments/e2.py --du_lieu data/dataset_vat_phang
python experiments/e3.py --du_lieu data/dataset_vat_phang
python experiments/e4.py --du_lieu data/dataset_vat_phang
```

Trên ảnh thật (lưu kết quả riêng vào `results/that`; không có E4 vì ảnh thật không có tầng cực nặng):

```
python -m src.danh_gia --du_lieu data/dataset_that --phuong_phap baseline --ra results/that
python -m src.danh_gia --du_lieu data/dataset_that --phuong_phap de_xuat --ra results/that
python experiments/e1.py --du_lieu data/dataset_that --ra results/that
python experiments/e2.py --du_lieu data/dataset_that --ra results/that
python experiments/e3.py --du_lieu data/dataset_that --ra results/that
```

Vẽ đồ thị sai số theo góc:

```
python experiments/ve_do_thi.py results/e3/ket_qua_e3.csv --ra results/do_thi_e3.png
```

Kết quả (csv, ảnh) nằm trong `results/`, thư mục này không đưa lên GitHub.

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
tools/          script tạo bộ ảnh tổng hợp, công cụ đổi tên ảnh chụp thật (chup_anh/)
report/         lý thuyết, công trình liên quan, file Word mẫu báo cáo
docs/           tuyên bố thách thức, hướng dẫn, kết quả, chia việc
```

Tài liệu trong `docs/`:
- `Tuyen_bo_thach_thuc.docx`: tuyên bố thách thức (đề tài)
- `HUONG_DAN_CHAY.md`: cài đặt, tải dữ liệu, các lệnh chạy, lỗi hay gặp
- `KET_QUA_HIEN_TAI.md`: số liệu đã có (ảnh tổng hợp và ảnh thật)
- `VIEC_GIAI_DOAN_2.md`: việc của từng người giai đoạn 2
- `HUONG_DAN_CHUP.md`: cách chụp ảnh thật
- `QUY_UOC.md`, `CHIA_VIEC_CODE.md`: quy ước code, chia việc phần code
