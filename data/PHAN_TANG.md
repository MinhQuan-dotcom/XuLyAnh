# Phân tầng tập đánh giá

Thách thức C là góc nhìn. Cường độ của C đo bằng **góc nghiêng θ**: góc giữa trục quang của camera và
pháp tuyến mặt bàn (θ = 0 là chụp thẳng từ trên xuống).

- Ảnh tổng hợp: θ là tham số dựng cảnh (giá trị danh định ± 1° ngẫu nhiên), ghi chính xác trong cột `theta_deg`.
- Ảnh tự chụp: θ đặt và đọc bằng chức năng Thăng bằng của ứng dụng Đo trên iPhone lúc chụp, ghi tròn 0 / 10 / 30 / 50°
  (sai lệch khoảng ±1°).

Các yếu tố khác được giữ gần như cố định giữa các tầng: cùng bộ vật, cùng tờ A4, vật đặt giữa tờ giấy, camera cách
tâm giấy khoảng 330–380 mm, cùng điều kiện ánh sáng. Vì vậy khác biệt giữa các tầng chỉ do θ.

## Tiêu chí

| Tầng | Cột `tang` | θ | Ý nghĩa |
|---|---|---|---|
| Nhẹ | `nhe` | 0–15° | gần như chụp thẳng |
| Trung bình | `trung_binh` | 15–35° | chụp nhanh bằng một tay |
| Nặng | `nang` | 35–55° | tờ giấy thành hình thang rõ |
| Cực nặng | `cuc_nang` | 55–75° | chỉ dùng cho E4 (tìm điểm gãy) |

## Số ảnh

Tập phát triển (`bo = dev`) tách riêng, dùng vật khác, chỉ để chọn tham số (E2).

| Bộ ảnh | Tầng | Thư mục | θ thực tế | Số ảnh | Vật |
|---|---|---|---|---|---|
| Tổng hợp | dev | `dev/` | 0–56° (6 góc danh định 0, 10, 25, 35, 45, 55) | 48 | d1–d4 |
| Tổng hợp | nhẹ | `eval/tang1_nhe_0-15/` | 4,0–12,9° | 48 | v01–v12, mỗi vật 2 góc × 2 hướng |
| Tổng hợp | trung bình | `eval/tang2_trungbinh_15-35/` | 21,1–30,9° | 48 | v01–v12 |
| Tổng hợp | nặng | `eval/tang3_nang_35-55/` | 39,1–50,9° | 48 | v01–v12 |
| Tổng hợp | cực nặng | `e4_cucnang_55-75/` | 59,1–70,8° | 48 | v01–v12 (E4) |
| Tổng hợp | vật dày | `e4_vat_day/` | 0 / 15 / 30 / 45° | 40 | 5 miếng dày 0,1–10 mm (E4) |
| Tự chụp | dev | `dev/` | 0 / 30 / 50° | 12 | d1, d2 |
| Tự chụp | nhẹ | `eval/tang1_nhe_0-15/` | 10° | 12 | v1–v6, mỗi vật 2 hướng |
| Tự chụp | trung bình | `eval/tang2_trungbinh_15-35/` | 30° | 12 | v1–v6 |
| Tự chụp | nặng | `eval/tang3_nang_35-55/` | 50° | 12 | v1–v6 |

Bộ tự chụp không có tầng cực nặng (ở khoảng 65° không giữ máy ổn định để đọc góc được).

## Tra cứu

Mỗi ảnh có một dòng trong `labels.csv` của bộ dữ liệu, các cột dùng để phân tầng: `bo` (dev / eval / ...),
`tang`, `theta_deg`, `huong` (doc / ngang). Đếm lại số ảnh mỗi tầng:

```
python -c "import csv,collections; print(collections.Counter((d['bo'], d['tang']) for d in csv.DictReader(open('data/dataset_vat_phang/labels.csv'))))"
```
