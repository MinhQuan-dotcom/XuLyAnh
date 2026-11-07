# Kết quả hiện có (cập nhật 07/11)

File này tóm tắt số liệu đã chạy được, để C, D, E biết đang ở đâu khi làm giai đoạn 2.
Số chính thức cho báo cáo vẫn phải lấy từ file csv trong `results/` khi mỗi người tự chạy lại.

## 1. Kiểm tra từng phần (ảnh tổng hợp, 286 ảnh)

| Phần | Kết quả |
|---|---|
| A tìm giấy | tìm được 100%, lệch góc trung bình 1.06 px |
| B chỉnh góc | 3.79 px còn 1.26 px |
| C homography + nắn | DLT đúng, nắn ảnh lệch 0.003 mm |
| D tách vật | tìm được 100%, vật mỏng lệch 1.65 px |
| E baseline + đồ thị | ĐẠT, kể cả khi ghép với A, D thật (`--that`) |

## 2. E3 trên ảnh tổng hợp (sai số trung bình chiều dài, mm)

| | nhẹ | trung bình | nặng |
|---|---|---|---|
| baseline | 4.02 | 14.18 | 13.03 |
| bỏ nắn ảnh | 4.24 | 14.39 | 13.13 |
| bỏ chỉnh góc | 0.71 | 0.99 | 1.52 |
| đầy đủ | 0.52 | 0.78 | 1.29 |

## 3. Ảnh thật (48 ảnh, chụp 06/11)

Dữ liệu: `data/dataset_that/` (tải từ Drive, xem `data/README.md`). Thông tin chụp và kích thước vật
trong `tools/chup_anh/danh_muc_vat_that.csv` và file `GHI_CHU.txt` trên Drive.

Sai số trung bình (mm), chạy bằng code hiện tại trên `main`:

| Tầng | Hướng | Baseline dài | Baseline rộng | Phương pháp dài | Phương pháp rộng |
|---|---|---|---|---|---|
| nhẹ (10°) | dọc | 5.24 | 5.86 | 1.70 | 3.44 |
| nhẹ (10°) | ngang | 2.94 | 7.11 | 0.64 | 3.45 |
| trung bình (30°) | dọc | 21.12 | 12.43 | 2.27 | 3.46 |
| trung bình (30°) | ngang | 9.09 | 20.41 | 2.27 | 7.59 |
| nặng (50°) | dọc | 21.38 | 9.23 | 2.90 | 1.45 |
| nặng (50°) | ngang | 3.76 | 21.01 | 1.24 | 4.91 |

Phương pháp vẫn tốt hơn baseline rõ ràng (chiều dài 0.6-2.9 mm so với 2.9-21 mm), nhưng kém hơn trên ảnh
tổng hợp. Có 3 nguyên nhân đã thấy:

**a) Tách vật hỏng với thẻ sinh viên v2 (phần D).** Chiều rộng đo được khoảng 37 mm, thật là 54 mm, ở cả 6 ảnh.
Thẻ có phần nền trắng, ngưỡng cố định (S > 60 hoặc V < 80) chỉ bắt được phần có màu. Thêm 1 ảnh thẻ đen
`v1_t30_ngang` rộng 46/70 mm (nghi mặt thẻ bị phản sáng). Đây là phần lớn sai số chiều rộng ở bảng trên.
Hướng sửa (D thử, so sánh trước/sau): đóng hình thái (MORPH_CLOSE) kích thước lớn hơn, lấy bao lồi
(convexHull) của các vùng, hoặc ngưỡng V tính theo độ sáng của giấy trong ảnh thay vì số cố định 80.

**b) Đặt dọc luôn đo dư khoảng 3%, đặt ngang gần đúng**, kể cả ở góc 10°, nên không phải do góc nghiêng.
Ví dụ thẻ đen dài 121 mm: đặt dọc đo 126-132 mm, đặt ngang 121-122 mm. Nghi ngờ: tờ giấy thật không đúng
297 mm, băng keo dán đè lên góc giấy, giấy vồng trên vải, hoặc méo ống kính. Đang chờ An đo lại tờ giấy.

**c) Nắp chai v5 đo to dần theo góc** (28.75 -> 30.5 -> 31.25 mm, thật 29 mm): thị sai do độ dày,
đúng dự đoán 5.1 trong `report/ly_thuyet.md`.

Hạn chế của dữ liệu thật cần ghi trong báo cáo: kích thước vật chỉ đo tới 1 mm, góc ghi tròn 10/30/50,
ảnh có bị cắt hoặc zoom (mỗi ảnh một cỡ), không có tầng 65°.
