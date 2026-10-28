# Cơ sở lý thuyết và dự đoán điểm gãy

Người viết: N1. Commit trước khi chạy E4.

> Bản này được commit trước khi chạy thí nghiệm. Sau khi commit, phần **Dự đoán** không được sửa.

## 1. Kỹ thuật đề xuất P
<!-- Tóm tắt 5 bước của pipeline (xem B.1 bản Tuyên bố thách thức). -->

## 2. Cơ chế: vì sao P khắc phục được góc nhìn
<!-- Mặt phẳng -> ảnh là phép biến đổi xạ ảnh H (8 bậc tự do, cần 4 điểm).
     Đại lượng C phá hỏng: tỉ lệ cục bộ (Jacobian) không còn hằng và đẳng hướng.
     Vì sao tinh chỉnh góc bằng đường thẳng khớp giảm sai số góc. -->

## 3. Nối về nền tảng môn học
<!-- Chương 2: biến đổi hình học, lọc, toán tử điểm. Chương 3: Canny, khớp đường thẳng. Chương 4: phân đoạn. -->

## 4. Mức tính mới
<!-- Phần nhóm tự thêm: tinh chỉnh góc, DLT tự viết, dự đoán định lượng + kiểm chứng. -->

## 5. Dự đoán điểm gãy
Ngưỡng chấp nhận: e_max = 1 mm.

| Cơ chế | Công thức / lập luận | Dự đoán cụ thể |
|---|---|---|
| Thị sai do độ dày t | sai số ~ t*tan(θ), nên θ_gãy ~ arctan(e_max / t) | t = 1 mm: ~45 độ; 3 mm: ~18 độ; 5 mm: ~11 độ; 10 mm: ~6 độ |
| Độ phân giải theo hướng bị co | sai số ~ 2 / (s0*cos θ) mm | s0 = .... px/mm (đo trên ảnh), θ_gãy ~ .... |
| Không tìm được 4 góc giấy | cạnh xa quá ngắn, quá mờ | khoảng 65-70 độ |
| Baseline | một tỉ lệ cho cả ảnh | vượt 1 mm từ khoảng 10-15 độ |

## 6. Đối chiếu sau thí nghiệm (điền sau E4, KHÔNG sửa mục 5)
<!-- Đúng / sai / đúng một phần, vì sao. -->
