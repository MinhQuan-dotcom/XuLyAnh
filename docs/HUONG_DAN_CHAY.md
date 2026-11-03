# Hướng dẫn chạy code và kiểm tra

Mọi lệnh chạy trong Git Bash (hoặc terminal của VS Code), đứng ở thư mục gốc repo `XuLyAnh`.

## 1. Cài đặt (làm 1 lần)

```bash
git pull
python -m pip install -r requirements.txt
python -c "import cv2, numpy, matplotlib; print(cv2.__version__)"
```

Dòng cuối in ra số phiên bản là được.

Bật UTF-8 cho Python để in được tiếng Việt (không bật thì dễ bị lỗi `UnicodeEncodeError` trên Windows):

```bash
echo 'export PYTHONUTF8=1' >> ~/.bashrc
source ~/.bashrc
```

## 2. Tải bộ ảnh tổng hợp đầy đủ (làm 1 lần)

```bash
python -m pip install gdown
gdown 1QYRKUxnb0PcF7RHkw_yJgH5MzCJtojsO -O data/dataset_vat_phang.zip
python -c "import zipfile; zipfile.ZipFile('data/dataset_vat_phang.zip').extractall('data')"
ls data/dataset_vat_phang
```

File tải về khoảng 54 MB. `ls` phải thấy `labels.csv`, `dev`, `eval`, `e4_cucnang_55-75`, `e4_vat_day`.
Không tải bộ đầy đủ thì các lệnh bên dưới bỏ phần `--du_lieu ...` đi, sẽ chạy trên 25 ảnh mẫu `data/mau`.

## 3. Kiểm tra từng phần

```bash
python tests/kiem_tra_A.py --du_lieu data/dataset_vat_phang
python tests/kiem_tra_B.py --du_lieu data/dataset_vat_phang
python tests/kiem_tra_C.py --du_lieu data/dataset_vat_phang
python tests/kiem_tra_D.py --du_lieu data/dataset_vat_phang
python tests/kiem_tra_E.py --du_lieu data/dataset_vat_phang
```

Dòng cuối mỗi lệnh ghi ĐẠT hoặc CHƯA ĐẠT. Muốn chỉ xem dòng kết luận thì thêm `| tail -2` vào cuối lệnh.

| Phần | Kiểm tra cái gì | Kết quả hiện tại |
|---|---|---|
| A `giay.py` | tìm 4 góc tờ giấy | tìm được 100%, lệch 1.06 px |
| B `goc.py` | chỉnh lại 4 góc | 3.79 px còn 1.26 px |
| C `hinh_hoc.py` | homography (DLT tự viết) + nắn ảnh | DLT đúng, nắn ảnh lệch 0.003 mm |
| D `vat.py` | tách vật, đo pixel | tìm được 100%, vật mỏng lệch 1.65 px |
| E `baseline.py`, `ve_do_thi.py` | baseline + vẽ đồ thị | ĐẠT |

Ảnh để xem bằng mắt nằm trong `results/kiem_tra/` (viền vật, ảnh nắn, đồ thị).

## 4. Kiểm tra ghép

```bash
python tests/kiem_tra_E.py --that --du_lieu data/dataset_vat_phang
```

`--that` là dùng code thật của phần A và D (không phải ảnh thật). ĐẠT nghĩa là baseline chạy được khi ghép.

## 5. Chạy thí nghiệm

```bash
python experiments/e1.py --du_lieu data/dataset_vat_phang
python experiments/e2.py --du_lieu data/dataset_vat_phang
python experiments/e3.py --du_lieu data/dataset_vat_phang
python experiments/e4.py --du_lieu data/dataset_vat_phang
```

**Không chạy `e4.py` trước khi `report/ly_thuyet.md` đã có trên GitHub** (dự đoán điểm gãy phải có trước thí nghiệm).

| Lệnh | Làm gì | Kết quả ở đâu |
|---|---|---|
| `e1.py` | baseline trên tập eval, sai số theo tầng và hướng đặt vật, lưu các ảnh đo sai nhiều nhất | `results/e1/`, ảnh lỗi ở `results/e1/anh_loi/` |
| `e2.py` | thử 3 giá trị cho mỗi tham số trên tập dev | `results/e2/tong_hop_e2.csv`, ảnh trung gian ở `results/e2/trung_gian/` |
| `e3.py` | so baseline, phương pháp đầy đủ, bỏ nắn ảnh, bỏ chỉnh góc | `results/e3/tong_hop_e3.csv` |
| `e4.py` | tầng cực nặng và vật dày, so góc gãy với dự đoán | `results/e4/` |

`e2.py` và `e3.py` chạy mất vài phút.

Kết quả E3 hiện tại (sai số trung bình chiều dài, mm):

| | nhẹ | trung bình | nặng |
|---|---|---|---|
| baseline | 4.02 | 14.18 | 13.03 |
| bỏ nắn ảnh | 4.24 | 14.39 | 13.13 |
| bỏ chỉnh góc | 0.71 | 0.99 | 1.52 |
| đầy đủ | 0.52 | 0.78 | 1.29 |

## 6. Vẽ đồ thị

```bash
python experiments/ve_do_thi.py results/e3/ket_qua_e3.csv --ra results/do_thi_e3.png
python experiments/ve_do_thi.py results/e1/ket_qua_baseline.csv --ra results/do_thi_e1.png
```

## 7. Khi có ảnh thật

Sau khi chạy `tools/chup_anh/doi_ten_anh.py` (xem `docs/HUONG_DAN_CHUP.md`), ảnh thật nằm ở `data/dataset_that`.
Chạy lại các thí nghiệm, chỉ đổi đường dẫn:

```bash
python -m src.danh_gia --du_lieu data/dataset_that --phuong_phap baseline
python -m src.danh_gia --du_lieu data/dataset_that --phuong_phap de_xuat
python experiments/e1.py --du_lieu data/dataset_that
python experiments/e3.py --du_lieu data/dataset_that
```

Các file trong `tests/` chỉ chạy được với ảnh tổng hợp (cần toạ độ góc trong nhãn), ảnh thật sẽ báo không có toạ độ, đó là bình thường.

## 8. Lưu kết quả

Thư mục `results/` không đưa lên GitHub. Chạy xong thì nén lại, đưa lên Drive chung để cả nhóm lấy số liệu và hình cho báo cáo.

## Lỗi hay gặp

| Lỗi | Cách sửa |
|---|---|
| `ModuleNotFoundError: No module named 'cv2'` | chưa cài thư viện, chạy lại mục 1 |
| `UnicodeEncodeError: 'charmap' codec ...` | chưa bật UTF-8, xem mục 1 |
| `FileNotFoundError: ... labels.csv` | chưa tải hoặc chưa giải nén bộ ảnh, xem mục 2 |
| `git push` bị từ chối (rejected) | chạy `git pull` rồi `git push` lại |
| Tải bộ ảnh chỉ vài MB | tải nhầm file, kiểm tra lại link trong `data/README.md` |
