# Đo kích thước vật từ ảnh chụp nghiêng, dùng tờ A4 làm vật tham chiếu

Bài tập lớn học phần **Xử lý ảnh và Thị giác máy tính (121036)**, Trường ĐH GTVT TP.HCM.
Nhóm: M ·

**Thách thức C:** góc nhìn. Khi điện thoại không vuông góc với mặt bàn, tỉ lệ pixel/mm thay đổi theo vị trí và hướng của vật, nên cách đo bằng một tỉ lệ duy nhất (baseline) sai dần theo góc nghiêng.
**Phương pháp đề xuất:** tìm 4 góc tờ A4, tinh chỉnh góc bằng giao điểm các đường thẳng khớp theo cạnh, ước lượng homography, nắn ảnh về nhìn thẳng rồi mới đo.

## Cài đặt

```bash
git clone <https://github.com/MinhQuan-dotcom/XuLyAnh.git>
cd <XuLyAnh>
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
  cau_hinh.py      tham số mặc định của baseline và phương pháp        (N3, N4)
  baseline.py      cách đo thông thường                                 (N3)
  phuong_phap.py   phương pháp đề xuất, 5 bước                          (N4)
  danh_gia.py      chấm điểm dùng chung, tổng hợp theo tầng             (N1, N3)
  tien_ich.py      đọc nhãn, đọc ảnh, ghi CSV, lưu ảnh trung gian       (N1)
experiments/       e1.py … e4.py – script tái tạo 4 thí nghiệm          (N3, N4, N5)
data/mau/          20 ảnh mẫu + labels.csv
tools/             script sinh bộ ảnh tổng hợp
report/            bản nháp lý thuyết, tài liệu liên quan, file Word mẫu báo cáo
docs/QUY_UOC.md    quy ước chung của nhóm – ĐỌC TRƯỚC KHI CODE
results/           kết quả chạy (không đưa lên GitHub)
```

## Phân công

| Người | Phần việc | File chính |
|---|---|---|
| N1 | Trưởng nhóm, lý thuyết, dự đoán điểm gãy | `report/ly_thuyet.md`, `src/danh_gia.py` |
| N2 | Dữ liệu: chụp ảnh, đo kích thước thật, làm nhãn | `data/` |
| N3 | Baseline, E1, tài liệu liên quan | `src/baseline.py`, `experiments/e1.py`, `report/lien_quan.md` |
| N4 | Phương pháp đề xuất, E2 | `src/phuong_phap.py`, `experiments/e2.py` |
| N5 | E3, E4, README, gộp báo cáo | `experiments/e3.py`, `experiments/e4.py` |

Chi tiết hạn từng việc xem file kế hoạch của nhóm.
