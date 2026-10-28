# Chia việc phần code – hạn 01/11/2026

Phần code được cắt thành **5 phần độc lập A–E**. Mỗi phần có:
- một file cần viết, trong đó tên hàm, đầu vào, đầu ra, gợi ý từng bước **đã ghi sẵn** (tìm chữ `TODO`);
- một file kiểm tra riêng trong `tests/`. Chạy ra **ĐẠT** là xong phần đó.

Không ai phải chờ ai: các file kiểm tra lấy dữ liệu đúng từ nhãn (`labels.csv`) để thay cho các phần khác chưa xong.
Phần ghép `src/phuong_phap.py` đã viết sẵn – khi A, B, C, D cùng đạt, phương pháp đề xuất tự chạy.

## Bảng chia việc

| Phần | Người | Viết gì | File | Kiểm tra | Độ khó |
|---|---|---|---|---|---|
| **A** | ........ | Tìm tờ giấy: 4 góc + mặt nạ | `src/giay.py` → `tim_to_giay` | `python tests/kiem_tra_A.py` | ★★☆ |
| **B** | ........ | Tinh chỉnh 4 góc bằng giao điểm đường thẳng khớp theo cạnh (Canny + fitLine) | `src/goc.py` → `tinh_chinh_goc` | `python tests/kiem_tra_B.py` | ★★★ |
| **C** | ........ | Tự viết homography bằng DLT (numpy, SVD) + nắn ảnh | `src/hinh_hoc.py` → `tinh_homography_dlt`, `nan_anh` | `python tests/kiem_tra_C.py` | ★★★ |
| **D** | ........ | Tách vật khỏi giấy (HSV + hình thái), đo cạnh bằng minAreaRect | `src/vat.py` → `tach_vat`, `kich_thuoc_px` | `python tests/kiem_tra_D.py` | ★★☆ |
| **E** | ........ | Baseline (ghép A + D, tính tỉ lệ px/mm) + vẽ đồ thị sai số theo góc | `src/baseline.py` → `do_kich_thuoc`; `experiments/ve_do_thi.py` → `gom_theo_goc`, `ve` | `python tests/kiem_tra_E.py` | ★☆☆ |

Gợi ý chia: B và C cho hai người chắc toán và code nhất; E cho trưởng nhóm (phần nhẹ, vì trưởng nhóm còn duyệt
Pull Request và viết lý thuyết).

## Điều kiện ĐẠT của từng phần

| Phần | Điều kiện |
|---|---|
| A | Tìm được giấy ở ≥ 95% ảnh (góc ≤ 55°), sai số góc trung bình ≤ 3 px |
| B | Từ góc thô lệch ~3,8 px, sau tinh chỉnh sai số ≤ 1,5 px và giảm ≥ 40% |
| C | DLT biến đúng 4 góc (lệch < 1e-4 mm), khớp cv2.findHomography; ảnh nắn 1188 × 840, đo lại vật lệch < 0,2 mm |
| D | Tìm được vật ở ≥ 95% ảnh, vật mỏng (≤ 1 mm) sai số trung bình ≤ 3 px |
| E | Baseline đo được 100% ảnh, ở ~0° sai < 0,5 mm, tầng nặng sai hơn tầng nhẹ; vẽ được đồ thị PNG |

Các ngưỡng này đã được thử: làm được bằng OpenCV cơ bản trong khoảng 20–40 dòng code mỗi phần.

## Cách làm từng bước

```bash
git checkout main
git pull
git checkout -b phan-A            # đổi A thành phần của mình
pip install -r requirements.txt

# viết code trong file của mình, chạy kiểm tra nhanh trên 25 ảnh mẫu:
python tests/kiem_tra_A.py

# khi đã ĐẠT trên ảnh mẫu, tải bộ ảnh đầy đủ (data/README.md) và chạy lại:
python tests/kiem_tra_A.py --du_lieu data/dataset_vat_phang

git add src/giay.py
git commit -m "Phan A: tim to giay"
git push -u origin phan-A
# lên GitHub mở Pull Request vào main, dán kết quả dòng ĐẠT vào phần mô tả
```

Ảnh minh họa (đường viền, ảnh nắn, đồ thị) được lưu trong `results/kiem_tra/` – mở ra xem bằng mắt.

## Quy tắc

- **Chỉ sửa file của phần mình.** Cần sửa file khác (kể cả `cau_hinh.py`) thì nhắn trưởng nhóm.
- Tham số mới thêm vào `src/cau_hinh.py` (cả `THAM_SO_BASELINE` lẫn `THAM_SO_DE_XUAT` nếu dùng chung).
- Không đọc `labels.csv` trong `src/`. Chỉ file trong `tests/` được đọc nhãn.
- Không viết hàm trả về sai định dạng: xem đầu vào / đầu ra ghi trong docstring.
- Kẹt quá một buổi thì hỏi trong nhóm, đừng ôm đến hạn.

## Mốc thời gian

| Ngày | Việc |
|---|---|
| 29/10 | Nhận phần, tạo nhánh, chạy thử file kiểm tra (ra CHƯA ĐẠT là bình thường) |
| 30/10 tối | Nhắn nhóm 1 dòng: đã làm đến đâu, kẹt gì |
| 01/11 21h | Mở Pull Request kèm dòng ĐẠT trên bộ ảnh đầy đủ |
| 01/11 tối | Trưởng nhóm gộp, chạy `python tests/kiem_tra_E.py --that` và `python experiments/e3.py` để kiểm tra cả hệ thống |
