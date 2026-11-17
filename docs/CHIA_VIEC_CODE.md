# Chia việc phần code (hạn 01/11)

Phần code chia làm 5 phần A, B, C, D, E. Mỗi người một phần, mỗi phần là 1-2 hàm trong một file riêng.
Chỗ cần viết có đánh dấu `TODO`, đầu vào đầu ra ghi ở docstring của hàm.

Mỗi phần có file kiểm tra riêng trong `tests/`. File kiểm tra lấy đáp án đúng từ `labels.csv` để thay
cho các phần khác, nên không cần chờ ai làm xong mới thử được. Chạy ra ĐẠT là xong.
File `src/phuong_phap.py` đã ghép sẵn, khi A, B, C, D đều đạt thì phương pháp chạy được luôn.

| Phần | Người làm | Nội dung | File | Kiểm tra |
|---|---|---|---|---|
| A | | Tìm tờ giấy: 4 góc và mặt nạ | `src/giay.py` | `python tests/kiem_tra_A.py` |
| B | | Chỉnh lại 4 góc bằng giao điểm các đường thẳng khớp theo cạnh | `src/goc.py` | `python tests/kiem_tra_B.py` |
| C | | Tự viết homography (DLT) và nắn ảnh | `src/hinh_hoc.py` | `python tests/kiem_tra_C.py` |
| D | | Tách vật khỏi giấy, đo kích thước theo pixel | `src/vat.py` | `python tests/kiem_tra_D.py` |
| E | | Baseline (ghép A và D) và vẽ đồ thị sai số | `src/baseline.py`, `experiments/ve_do_thi.py` | `python tests/kiem_tra_E.py` |

B và C khó hơn, nên để cho người chắc code và toán. E nhẹ nhất.

## Thế nào là đạt

- A: tìm được giấy ở ít nhất 95% ảnh (góc nghiêng đến 55 độ), sai số góc trung bình không quá 3 px.
- B: góc thô lệch khoảng 3-4 px, sau khi chỉnh còn không quá 1.5 px và giảm ít nhất 40%.
- C: DLT cho kết quả giống `cv2.findHomography`, ảnh nắn kích thước 1188 x 840, đo lại vật lệch dưới 0.2 mm.
- D: tìm được vật ở ít nhất 95% ảnh, với vật mỏng (dày không quá 1 mm) sai số trung bình không quá 3 px.
- E: baseline đo được tất cả ảnh, ở góc gần 0 độ sai dưới 1 mm, tầng nặng sai nhiều hơn tầng nhẹ, vẽ ra được file đồ thị.

## Các bước

```
git checkout main
git pull
git checkout -b phan-A          # đổi theo phần của mình
pip install -r requirements.txt

python tests/kiem_tra_A.py      # chạy nhanh trên 25 ảnh mẫu

# đạt trên ảnh mẫu rồi thì tải bộ đầy đủ (xem data/README.md) và chạy lại
python tests/kiem_tra_A.py --du_lieu data/dataset_vat_phang

git add src/giay.py
git commit -m "Phan A: tim to giay"
git push -u origin phan-A
```

Sau đó lên GitHub mở Pull Request vào `main`, ghi kết quả chạy kiểm tra vào phần mô tả.
Hình minh họa (đường viền, ảnh nắn, đồ thị) lưu trong `results/kiem_tra/`, mở ra xem cho chắc.

## Lưu ý

- Chỉ sửa file phần mình. Cần sửa file khác (kể cả `cau_hinh.py`) thì nhắn trưởng nhóm.
- Thêm tham số mới thì thêm vào `src/cau_hinh.py`.
- Code trong `src/` không đọc `labels.csv`, chỉ file trong `tests/` mới được đọc.
- Bí quá một buổi thì hỏi trong nhóm, đừng để tới hạn.

## Lịch

- 29/10: nhận phần, tạo nhánh, chạy thử file kiểm tra (ra CHƯA ĐẠT là bình thường).
- 30/10 tối: nhắn nhóm đã làm tới đâu, vướng gì.
- 01/11 21h: mở Pull Request, kèm kết quả kiểm tra trên bộ đầy đủ.
- 01/11 tối: trưởng nhóm merge, chạy `python tests/kiem_tra_E.py --that` và `python experiments/e3.py` để thử cả hệ thống.
