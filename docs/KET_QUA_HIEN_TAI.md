# Kết quả hiện có (cập nhật tối 17/11)

Số liệu dưới đây chạy bằng code hiện tại trên `main` (đã gồm bản sửa `tach_vat` ngày 17/11).
Số chính thức cho báo cáo lấy từ file csv trong `results/` khi chạy lại theo `docs/HUONG_DAN_CHAY.md`.

## 1. Kiểm tra từng phần (ảnh tổng hợp, 286 ảnh)

| Phần | Kết quả |
|---|---|
| A tìm giấy | tìm được 100%, lệch góc trung bình 1.06 px |
| B chỉnh góc | 3.79 px còn 1.26 px |
| C homography + nắn | DLT đúng, nắn ảnh lệch 0.003 mm |
| D tách vật | tìm được 100%, vật mỏng lệch 1.67 px |
| E baseline + đồ thị | ĐẠT, kể cả khi ghép với A, D thật (`--that`) |

## 2. E2: khảo sát tham số

Đã viết thành `report/muc_8_1_e2.docx`. Tóm tắt:
- `canny_cao` (30-300): không ảnh hưởng, vì cạnh giấy trên nền tối rất rõ.
- `do_rong_dai_canh`: 1-2 px kém hơn, từ 4 px trở lên ổn định. Giữ 8.
- `do_phan_giai_nan` (s): s = 1 có MAE thấp nhất trên ảnh tổng hợp nhưng là do bù trừ sai số
  (phương pháp luôn đo dư, ảnh nắn thô làm vật nhỏ lại); trên dev ảnh thật s = 1 lại kém hơn. Giữ s = 4.

## 3. E3 trên ảnh tổng hợp (sai số trung bình chiều dài, mm)

| | nhẹ | trung bình | nặng |
|---|---|---|---|
| baseline | 4.02 | 14.17 | 13.03 |
| bỏ nắn ảnh | 4.24 | 14.37 | 13.12 |
| bỏ chỉnh góc | 0.71 | 1.02 | 1.56 |
| đầy đủ | 0.54 | 0.80 | 1.32 |

## 3b. E1 và E4 trên ảnh tổng hợp

Chi tiết và giải thích: `report/ly_thuyet.md` mục 6 và `report/Bao_cao_nhap.docx` mục 4, 8.4, 9.1.

- **E1, tầng nặng sai ít hơn tầng trung bình (13.03 so với 14.17 mm):** ở tầng nặng (39-51 độ) cạnh 297 mm bị co
  ngắn hơn cạnh 210 mm, nên baseline lấy nhầm cạnh 297 mm để chia 210 (48/48 ảnh, tầng trung bình chỉ 1/48).
  Chiều theo hướng nghiêng bị đo còn khoảng 0.71, chiều ngang lại gần đúng, nên MAE giảm. Bảng ở
  `results/e1/canh_ngan_baseline.csv`, `results/e1/ti_le_do_baseline.csv`.
- **E1, mép gần / mép xa:** bìa v03 ở 40 độ, baseline đo 102.0 mm (gần) và 54.2 mm (xa), thật 110; P đo 111.1 và 112.0.
- **E4a (60-70 độ):** đo được 100% ảnh; vật mỏng 0.1-0.5 mm sai 1.43 mm, vật 2-3 mm sai 4.86 mm.
- **E4b (vật dày):** góc gãy đo được sớm hơn dự đoán: 1 mm gãy ở 30 độ (dự đoán 45), 3/5/10 mm đã vượt 1 mm ở 0 độ.
  Nguyên nhân: sai số nền khoảng 0.55 mm và mặt trên vật dày trông to hơn theo D/(D - t). Mô hình sửa lại
  e ≈ 0.55 + L·t/D + t·tan θ khớp kết quả.

## 4. Ảnh thật (48 ảnh, chụp 06/11)

### 4.1. E3 trên tập đánh giá ảnh thật (sai số trung bình, mm; mỗi tầng 12 ảnh)

| | nhẹ dài | nhẹ rộng | trung bình dài | trung bình rộng | nặng dài | nặng rộng |
|---|---|---|---|---|---|---|
| baseline | 4.09 | 4.03 | 15.67 | 13.90 | 12.39 | 13.42 |
| bỏ nắn ảnh | 3.88 | 3.88 | 15.55 | 13.82 | 12.24 | 13.33 |
| bỏ chỉnh góc | 1.16 | 0.96 | 1.53 | 1.08 | 2.18 | 1.68 |
| đầy đủ | 1.17 | 0.96 | 1.61 | 1.12 | 2.27 | 1.62 |

- Phương pháp giảm sai số khoảng 3.5-10 lần so với baseline trên ảnh thật, nhưng sai số lớn hơn ảnh tổng hợp.
- **Bước chỉnh góc (phần B) không giúp gì trên ảnh thật** (đầy đủ và bỏ chỉnh góc gần như bằng nhau), trong khi
  trên ảnh tổng hợp nó giúp rõ. Cần giải thích ở phần Thảo luận: mép giấy thật không thẳng tuyệt đối
  (giấy hơi vồng trên vải, băng keo ở mép), nên đường thẳng khớp theo cạnh không chính xác hơn góc thô.

### 4.2. Theo hướng đặt vật (phương pháp đầy đủ)

| Tầng | dọc: dài / rộng | ngang: dài / rộng |
|---|---|---|
| nhẹ (10°) | 1.71 / 0.80 | 0.63 / 1.13 |
| trung bình (30°) | 2.33 / 0.76 | 0.89 / 1.48 |
| nặng (50°) | 3.19 / 0.83 | 1.34 / 2.41 |

Kích thước theo trục dài tờ giấy luôn bị đo dư nhiều hơn (cột dài khi đặt dọc, cột rộng khi đặt ngang).

### 4.3. Các nguyên nhân sai số đã thấy

**a) Tách vật hỏng với thẻ màu nhạt và thẻ xám (đã sửa 17/11).** Trước khi sửa, thẻ sinh viên v2 (mặt sau xanh nhạt)
đo rộng khoảng 37 mm (thật 54), thẻ xám v1 ở một ảnh 30° chỉ bắt được mép thẻ. Nguyên nhân: ngưỡng cố định
S > 60 hoặc V < 80; thẻ xanh nhạt có S thấp, thẻ xám đậm có V khoảng 95. Đã sửa trong `src/vat.py`: ngưỡng tối
tính theo độ sáng giấy (`he_so_v = 0.5`), thêm đóng hình thái 7x7. Sai số chiều rộng trên ảnh thật giảm từ
1.5-7.6 mm xuống 0.8-2.4 mm; ảnh tổng hợp gần như không đổi. `he_so_v` chọn theo lý lẽ (vật tối hơn một nửa
độ sáng giấy), không chỉnh theo tập đánh giá; trên tập dev giá trị 0-0.7 cho kết quả chênh không quá 0.04 mm.
Đã thử thêm tiêu chí khác màu Lab nhưng bỏ vì bắt cả bóng của vật, làm sai số tăng.

**b) Đo dư theo trục dài tờ giấy khoảng 2-4%**, kể cả ở góc 10°, nên không phải do góc nghiêng. Tờ giấy đo lại
208 x 298 mm (đúng khổ A4 trong sai số thước), nên không phải do kích thước giấy. Nghi ngờ: giấy vồng trên vải,
méo ống kính, kích thước vật chỉ đo tới 1 mm. Sai số có dấu theo vật: v1 thẻ đen +4.2 mm dài, v3 bìa +2.1 mm,
còn v2, v4, v6 gần 0.

**c) Nắp chai v5 đo to dần theo góc** (28.75 -> 30.5 -> 31.25 mm, thật 29 mm): thị sai do độ dày,
đúng dự đoán 5.1 trong `report/ly_thuyet.md`.

Hạn chế của dữ liệu thật cần ghi trong báo cáo: kích thước vật chỉ đo tới 1 mm, góc ghi tròn 10/30/50,
ảnh có bị cắt hoặc zoom (mỗi ảnh một cỡ), không có tầng 65°.
