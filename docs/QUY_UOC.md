# Quy ước chung của nhóm

Chia việc phần code: xem [`CHIA_VIEC_CODE.md`](CHIA_VIEC_CODE.md).

Đọc hết trang này trước khi viết dòng code đầu tiên. Ai muốn đổi quy ước thì nhắn trưởng nhóm trước.

## 1. Hàm đo – baseline và phương pháp đề xuất phải giống nhau

```python
def do_kich_thuoc(anh, tham_so=None):
    ...
    return dai_mm, rong_mm, anh_trung_gian
```

- `anh`: ảnh BGR đọc bằng `cv2.imread`. Hàm **chỉ nhận ảnh**, không đọc `labels.csv`.
- `tham_so`: dict, chỉ cần truyền những tham số muốn đổi; tham số còn lại lấy mặc định trong `src/cau_hinh.py`.
- Trả về `dai_mm >= rong_mm`, đơn vị mm. Vật tròn thì dài = rộng = đường kính.
- Không đo được (không tìm thấy giấy hoặc vật) thì trả `(None, None, anh_trung_gian)`, **không** ném lỗi.
- `anh_trung_gian`: dict `{ten_buoc: anh}` theo thứ tự các bước, ví dụ `{'goc': ..., 'nguong': ..., 'duong_vien': ..., 'anh_nan': ...}`. Thí nghiệm E2 và hình minh họa trong báo cáo lấy từ đây.

## 2. Tham số

- Mọi con số (ngưỡng, kích thước kernel, độ phân giải…) nằm trong `src/cau_hinh.py`, không viết cứng trong code.
- **Chỉ chọn tham số trên tập `dev`.** Không chạy thử trên `eval` rồi sửa tham số cho đẹp. Đây là quy định của thầy.
- Phương pháp đề xuất phải tôn trọng 2 công tắc `nan_anh` và `tinh_chinh_goc` (cho thí nghiệm E3).

## 3. Dữ liệu và nhãn

- Cấu trúc thư mục và cột `labels.csv` xem `data/README.md`. Ảnh thật dùng đúng cấu trúc đó.
- Các cột `a4_g…`, `vat_g…`, `fx/fy/cx/cy`, `azim_deg`, `roll_deg`, `xoay_giay_deg`, `yaw_vat_deg` chỉ để **kiểm tra**. Code phương pháp không được dùng.
- Ảnh không đưa lên GitHub (trừ `data/mau/`). Ảnh để trên Google Drive.

## 4. Kết quả

- Script thí nghiệm ghi CSV với các cột trong `tien_ich.COT_KET_QUA`, vào `results/<tên thí nghiệm>/`.
- Bảng số đưa vào báo cáo lấy từ các file `tong_hop_*.csv`, không chép tay.
- `results/` không đưa lên GitHub; ai cần thì tự chạy lại script.

## 5. Git

- Mỗi người làm trên nhánh riêng theo phần: `phan-A`, `phan-B`, … (lý thuyết: `ly-thuyet`).
- Trước khi gộp vào `main`: chạy `python -m src.danh_gia --du_lieu data/mau --phuong_phap <...>` không lỗi, rồi mở Pull Request. Một người khác xem và bấm merge.
- Lời commit viết tiếng Việt, ngắn, nói làm gì: `Them buoc tinh chinh goc giay`, `Sua loi khong tim thay vat tron`.
- Không commit ảnh lớn, file `.zip`, thư mục `results/`.

## 6. Đặt tên

- Tên hàm, tên biến: tiếng Việt không dấu, chữ thường, nối bằng `_` (`tim_to_giay`, `ti_le_px_mm`).
- Tên file ảnh thật: `<mã vật>_t<góc>_<doc|ngang>[_<so>].jpg`, ví dụ `v03_t30_doc.jpg`, giống bộ tổng hợp.
- Hình cho báo cáo: `hinh_<mục>_<số>_<mô tả>.png`, ví dụ `hinh_4_1_baseline_theo_tang.png`.

## 7. Dự đoán điểm gãy

`report/ly_thuyet.md` phải được commit lên `main` **trước khi** chạy E4 (hạn 03/11). Ngày giờ commit là bằng chứng dự đoán được viết trước thí nghiệm. Sau đó không sửa phần dự đoán; kết quả sai thì giải thích ở mục Thảo luận.
