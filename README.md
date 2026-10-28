# Đo kích thước vật từ ảnh chụp nghiêng, dùng tờ A4 làm vật tham chiếu

Bài tập lớn học phần **Xử lý ảnh và Thị giác máy tính (121036)**, Trường ĐH GTVT TP.HCM.
Nhóm: ........ · Lớp: ........

**Thách thức C:** góc nhìn. Khi điện thoại không vuông góc với mặt bàn, tỉ lệ pixel/mm thay đổi theo vị trí và hướng của vật, nên cách đo bằng một tỉ lệ duy nhất (baseline) sai dần theo góc nghiêng.
**Phương pháp đề xuất:** tìm 4 góc tờ A4, tinh chỉnh góc bằng giao điểm các đường thẳng khớp theo cạnh, ước lượng homography, nắn ảnh về nhìn thẳng rồi mới đo.

## Cài đặt

```bash
git clone <link repo>
cd <tên repo>
pip install -r requirements.txt
```
Cần Python 3.9 trở lên.

## Chạy thử trên dữ liệu mẫu

```bash
python -m src.danh_gia --du_lieu data/mau --phuong_phap baseline
python -m src.danh_gia --du_lieu data/mau --phuong_phap de_xuat
```
Khi baseline và phương pháp chưa được cài đặt xong, lệnh vẫn chạy nhưng tỉ lệ đo được là 0%.

## Chạy lại 4 thí nghiệm

Tải dữ liệu đầy đủ theo hướng dẫn trong [`data/README.md`](data/README.md), rồi:

```bash
python experiments/e1.py --du_lieu data/dataset_vat_phang   # chứng cứ thách thức (baseline theo tầng)
python experiments/e2.py --du_lieu data/dataset_vat_phang   # khảo sát tham số trên tập dev
python experiments/e3.py --du_lieu data/dataset_vat_phang   # ablation
python experiments/e4.py --du_lieu data/dataset_vat_phang   # điểm gãy
```
Kết quả (CSV và ảnh) nằm trong `results/e1` … `results/e4`. Với ảnh thật, thay `--du_lieu data/dataset_that`.

## Cấu trúc

```
src/
  giay.py          PHẦN A – tìm tờ giấy (4 góc + mặt nạ)
  goc.py           PHẦN B – tinh chỉnh góc giấy bằng đường thẳng khớp
  hinh_hoc.py      PHẦN C – homography (DLT tự viết) + nắn ảnh
  vat.py           PHẦN D – tách vật, đo kích thước pixel
  baseline.py      PHẦN E – baseline ghép A + D
  phuong_phap.py   phương pháp đề xuất ghép A + B + C + D (có sẵn)
  cau_hinh.py      tham số mặc định
  danh_gia.py      chấm điểm dùng chung (có sẵn)
  tien_ich.py      đọc nhãn, đọc ảnh, ghi CSV (có sẵn)
tests/             kiem_tra_A.py … kiem_tra_E.py – mỗi phần tự kiểm tra, không cần chờ phần khác
experiments/       e1.py … e4.py, ve_do_thi.py (PHẦN E)
data/mau/          25 ảnh mẫu + labels.csv
tools/             script sinh bộ ảnh tổng hợp
report/            lý thuyết, tài liệu liên quan, file Word mẫu báo cáo
docs/              QUY_UOC.md (quy ước), CHIA_VIEC_CODE.md (chia việc phần code)
```

## Phân công phần code

Xem [`docs/CHIA_VIEC_CODE.md`](docs/CHIA_VIEC_CODE.md).
