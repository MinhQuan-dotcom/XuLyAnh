# Hướng dẫn chụp ảnh thật (1 người làm)

> Đã chụp xong ngày 06/11/2026: 48 ảnh (không chụp được đợt 65 độ, đã bỏ 6 dòng đó khỏi
> `thu_tu_chup.csv`). Ghi chú của người chụp ở Drive, thư mục `anh_that/GHI_CHU.txt`.

Tổng cộng 54 ảnh, 8 vật, khoảng 1 tiếng. Hạn: trước 08/11.

## 1. Chuẩn bị

- Điện thoại (chỉ dùng 1 cái cho cả buổi).
- Vài tờ giấy A4 mới, phẳng, không nhăn.
- Mặt bàn hoặc tấm nền màu tối, không bóng (bìa đen, vải tối, mặt bàn gỗ sẫm).
- Băng keo giấy.
- Thước kẹp (mượn phòng lab hoặc mua loại rẻ).
- Giá đỡ điện thoại có khớp xoay. Không có thì kê bằng chồng sách và hộp.
- App đo độ nghiêng: Android tải "Bubble Level", iPhone dùng app Đo (Measure) > Thăng bằng.

8 vật, đều mỏng (dày không quá 2 mm), màu đậm, không bóng, không màu trắng:

| Mã | Gợi ý | Dùng cho |
|---|---|---|
| v1 | thẻ nhựa (thẻ ATM cũ, thẻ thành viên) | eval |
| v2 | thẻ nhựa khác màu | eval |
| v3 | miếng bìa màu dài (khoảng 100 x 30 mm) | eval |
| v4 | miếng bìa màu gần vuông (khoảng 50 x 50 mm) | eval |
| v5 | đồng xu | eval |
| v6 | nhãn dán, giấy note màu | eval |
| d1, d2 | 2 vật khác hẳn 6 vật trên (ví dụ thẻ xe, miếng mica) | dev |

Ghi lại vật nào là mã nào, đừng đổi vật giữa chừng.

## 2. Cài đặt điện thoại

- Camera chính, zoom 1x, không dùng chế độ chân dung, không flash, không HDR nếu tắt được.
- iPhone: Cài đặt > Camera > Định dạng > chọn **Tương thích nhất** (để ảnh ra JPG, không ra HEIC).
- Tắt tự chuyển macro (iPhone: Cài đặt > Camera > Điều khiển macro, tắt).
- Bật lưới (grid) cho dễ canh giữa.
- **Chụp dọc** (cầm máy đứng), cạnh dài tờ giấy nằm theo chiều dọc ảnh.

## 3. Sắp chỗ chụp

1. Dán tờ A4 xuống bàn bằng băng keo ở mép ngoài (đừng dán đè lên mặt giấy).
2. Đánh dấu tâm tờ giấy bằng 1 mẩu băng keo nhỏ ở mép, để lần nào cũng đặt vật vào giữa.
3. Đèn trần cố định, không đứng chắn đèn làm bóng đổ lên giấy.
4. Điện thoại cách tâm tờ giấy khoảng 35 cm. Cả 4 góc tờ giấy phải nằm trong khung, giấy chiếm khoảng 60-80% khung hình.
5. "Góc nghiêng" là độ nghiêng của điện thoại so với lúc nằm úp thẳng xuống giấy. 0 độ là chụp thẳng từ trên xuống. Đặt app đo nghiêng lên lưng điện thoại để đọc.
   Điện thoại nghiêng về phía người chụp (đứng ở cạnh ngắn của tờ giấy nhìn vào).

## 4. Đo kích thước vật (làm trước hoặc sau khi chụp đều được)

Mở file `tools/chup_anh/danh_muc_vat_that.csv` bằng Excel. Với mỗi vật đo bằng thước kẹp:
- `dai_mm`, `rong_mm`: chiều dài, chiều rộng. Đồng xu thì cả 2 ô ghi đường kính.
- `day_mm`: độ dày.
- Đo 2 lần, lấy trung bình, ghi 1 hoặc 2 chữ số thập phân.
- `ten`: ghi vật thật là gì (ví dụ "the ATM Vietcombank cu").

## 5. Chụp

Chụp **đúng thứ tự** trong file `tools/chup_anh/thu_tu_chup.csv` (cột `stt` từ 1 đến 54).
Ảnh sau này được đổi tên theo thứ tự chụp, nên:
- **Chụp hỏng thì xoá ngay trên điện thoại rồi chụp lại** (mờ, thiếu góc giấy, tay lọt vào).
- Không chụp ảnh khác xen giữa.

Cách làm: cố định 1 góc, chụp hết các vật ở góc đó, rồi mới đổi góc.

| Đợt | Góc | Vật | Mỗi vật | Số ảnh | stt |
|---|---|---|---|---|---|
| 1 | 10 độ | v1 đến v6 | dọc, rồi ngang | 12 | 1-12 |
| 2 | 30 độ | v1 đến v6 | dọc, rồi ngang | 12 | 13-24 |
| 3 | 50 độ | v1 đến v6 | dọc, rồi ngang | 12 | 25-36 |
| 4 | 65 độ | v1 đến v6 | chỉ dọc | 6 | 37-42 |
| 5 | 0 độ | d1, d2 | dọc, rồi ngang | 4 | 43-46 |
| 6 | 30 độ | d1, d2 | dọc, rồi ngang | 4 | 47-50 |
| 7 | 50 độ | d1, d2 | dọc, rồi ngang | 4 | 51-54 |

- **dọc**: cạnh dài của vật song song với cạnh dài tờ giấy (chĩa về phía điện thoại).
- **ngang**: xoay vật 90 độ, cạnh dài vật song song cạnh ngắn tờ giấy.
- Đồng xu tròn thì "dọc" và "ngang" chụp y như nhau, vẫn chụp đủ 2 tấm.
- Mỗi tấm: đặt vật vào tâm giấy, chạm vào tờ giấy trên màn hình để lấy nét, rồi chụp.

Mỗi lần chỉnh xong góc, đọc góc thật trên app và ghi lại (ví dụ đợt 2 đo được 31 độ).
Sau buổi chụp mở `thu_tu_chup.csv`, điền góc thật vào cột `goc_do` cho mọi dòng của đợt đó.
Không ghi thì script lấy góc dự kiến, nhưng ghi thì kết quả chính xác hơn.

## 6. Sau khi chụp

1. Chép **ảnh gốc** từ điện thoại sang máy bằng cáp USB hoặc Google Drive (bản gốc).
   **Không gửi qua Zalo/Messenger** vì ảnh bị nén.
   Bỏ 54 ảnh vào một thư mục riêng, không lẫn ảnh khác, ví dụ `D:/anh_chup`.
2. Lưu lại 2 file csv đã điền (Excel hỏi định dạng thì chọn CSV).
3. Ở thư mục gốc repo chạy:
   ```
   python tools/chup_anh/doi_ten_anh.py --anh_goc "D:/anh_chup"
   ```
   Script kiểm tra đủ 54 ảnh, đủ kích thước vật, rồi đổi tên, thu nhỏ ảnh, xếp vào
   `data/dataset_that/` và tạo `labels.csv`.
4. Chạy thử:
   ```
   python -m src.danh_gia --du_lieu data/dataset_that --phuong_phap baseline
   ```
5. Mở vài ảnh trong `data/dataset_that/` xem đúng tên chưa (ví dụ `v3_t50_ngang.jpg` phải là
   miếng bìa dài, chụp nghiêng nhiều, nằm ngang).
6. Nén thư mục `data/dataset_that` thành zip, đưa lên Drive (chế độ ai có link đều xem được),
   gửi link cho trưởng nhóm. Commit 2 file csv đã điền lên GitHub (ảnh thì không commit).

## Lỗi hay gặp

- Script báo số ảnh không khớp: có ảnh thừa (chụp hỏng chưa xoá) hoặc thiếu. Xem lại theo thứ tự trong `thu_tu_chup.csv`.
- Script báo ảnh .HEIC: chỉnh định dạng camera như mục 2 rồi chụp lại, hoặc đổi sang JPG.
- Ảnh bị chói ở giữa tờ giấy: dời đèn hoặc đổi chỗ, giấy không được loá trắng hết.
