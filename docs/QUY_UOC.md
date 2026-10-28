# Quy ước code của nhóm

Mọi người đọc qua trước khi code để ghép lại không bị lệch. Muốn đổi gì thì báo nhóm trước.

## Hàm đo

Baseline và phương pháp của nhóm đều có hàm:

```python
def do_kich_thuoc(anh, tham_so=None):
    ...
    return dai_mm, rong_mm, anh_trung_gian
```

- `anh` là ảnh BGR đọc bằng `cv2.imread`. Hàm chỉ nhận ảnh, không đọc `labels.csv`.
- `tham_so` là dict, chỉ truyền tham số muốn đổi, còn lại lấy trong `src/cau_hinh.py`.
- Trả về `dai_mm >= rong_mm`, đơn vị mm. Vật tròn thì dài = rộng = đường kính.
- Không đo được thì trả `(None, None, anh_trung_gian)`, không raise lỗi.
- `anh_trung_gian` là dict tên bước -> ảnh, dùng để lấy hình cho báo cáo và cho E2.

## Tham số

- Để hết trong `src/cau_hinh.py`, không ghi số cứng trong code.
- Chỉ chỉnh tham số dựa trên tập `dev`. Không chạy trên `eval` rồi sửa tham số cho đẹp (thầy có nói).
- Phương pháp phải có 2 công tắc `nan_anh` và `tinh_chinh_goc` để làm E3.

## Dữ liệu

- Code trong `src/` không được dùng các cột `a4_g...`, `vat_g...`, `fx`, `fy`, `cx`, `cy`, `azim_deg`,
  `roll_deg`, `xoay_giay_deg`, `yaw_vat_deg` của `labels.csv`. Mấy cột này chỉ để kiểm tra (trong `tests/`),
  ảnh thật sẽ không có.
- Ảnh không đẩy lên GitHub, trừ `data/mau`.

## Kết quả

- Script thí nghiệm ghi csv theo các cột trong `tien_ich.COT_KET_QUA`, vào `results/<tên thí nghiệm>/`.
- Bảng số trong báo cáo lấy từ file `tong_hop_*.csv`, không chép tay.
- Không đẩy `results/` lên GitHub, ai cần thì chạy lại.

## Git

- Mỗi người làm trên nhánh của phần mình: `phan-A`, `phan-B`, ..., phần lý thuyết là `ly-thuyet`.
- Trước khi làm thì `git pull`.
- Làm xong thì chạy file kiểm tra của phần mình, rồi mở Pull Request vào `main`. Trưởng nhóm xem rồi merge.
- Commit ghi ngắn gọn làm gì, ví dụ `Them buoc tinh chinh goc`, `Sua loi khong tim thay vat tron`.
- Không commit ảnh, file zip, thư mục `results/`.

## Đặt tên

- Tên hàm, biến: tiếng Việt không dấu, chữ thường, nối bằng `_` (ví dụ `tim_to_giay`, `ti_le_px_mm`).
- Ảnh tự chụp: `<mã vật>_t<góc>_<doc|ngang>.jpg`, ví dụ `v03_t30_doc.jpg`, giống bộ tổng hợp.
- Hình cho báo cáo: `hinh_<mục>_<số>_<mô tả>.png`, ví dụ `hinh_4_1_baseline_theo_tang.png`.

## Dự đoán điểm gãy

`report/ly_thuyet.md` phải commit lên `main` trước khi chạy E4. Ngày giờ commit là bằng chứng dự đoán
có trước thí nghiệm. Sau đó không sửa phần dự đoán nữa, nếu kết quả sai thì giải thích ở phần thảo luận.
