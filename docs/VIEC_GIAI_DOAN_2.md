# Việc giai đoạn 2: phân tích kết quả và viết báo cáo (03/11 - 17/11)

Code A-E đã ghép xong và đều ĐẠT. Giai đoạn này không viết thêm thuật toán, chỉ chạy thí nghiệm,
xem kết quả, giải thích, và viết phần báo cáo của mình.

Trước khi làm: `git pull`, đọc `docs/HUONG_DAN_CHAY.md` (cách cài, tải dữ liệu, chạy lệnh).

Quy tắc chung:
- Mỗi người viết báo cáo vào **file Word riêng**: copy `report/Mau_bao_cao.docx` ra
  `report/muc_<số>_<tên>.docx`, chỉ viết phần mình. Không cùng sửa một file.
- Không sửa code trong `src/`. Thấy lỗi thì nhắn người viết phần đó.
- Cần đổi tham số trong `src/cau_hinh.py` thì nhắn Quân.
- `results/` không lên GitHub. Hình và bảng số cho báo cáo thì chép lên Drive chung, thư mục `ket_qua/<tên mình>/`.
- Mọi bảng số lấy từ file `tong_hop_*.csv`, không chép tay từ màn hình.
- Hình đặt tên `hinh_<mục>_<số>_<mô tả>.png`, ví dụ `hinh_4_1_baseline_theo_tang.png`.

---

## Người C: công trình liên quan, sơ đồ pipeline, phương pháp

Viết mục 3, 6, 7 của báo cáo. Hạn: 09/11.

### Việc 1. Tìm ít nhất 3 bài báo / hệ thống liên quan

Ghi vào `report/lien_quan.md` theo mẫu có sẵn (họ làm gì, nhóm kế thừa gì, nhóm làm khác gì).
Gợi ý chỗ bắt đầu (tự tìm đọc, ghi trích dẫn IEEE đúng theo bản gốc):
- Hartley & Zisserman, Multiple View Geometry in Computer Vision (chương về homography, DLT).
- Criminisi, Reid, Zisserman, "Single view metrology", IJCV 2000 (đo kích thước từ một ảnh).
- Zhang & He, "Whiteboard scanning and image enhancement", Digital Signal Processing 2007
  (tìm tứ giác bảng trắng rồi nắn phối cảnh, rất giống cách nhóm làm với tờ A4).
- Các app "đo bằng camera" hoặc quét tài liệu (CamScanner, Google Lens): tìm 4 góc tài liệu rồi nắn.
Từ khoá tìm: perspective rectification, document corner detection, object measurement reference object.

### Việc 2. Sơ đồ pipeline

Vẽ sơ đồ 5 bước (tìm giấy, chỉnh góc, homography, nắn ảnh, đo vật) bằng draw.io hoặc PowerPoint.
Mỗi bước kèm một ảnh nhỏ minh hoạ. Lấy ảnh trung gian bằng:

```bash
python experiments/e1.py --du_lieu data/dataset_vat_phang
```

hoặc nhờ D gửi ảnh trong `results/e2/trung_gian/`. Dùng sơ đồ này cho cả báo cáo và slide.

### Việc 3. Viết mục 6 (Phương pháp) và mục 7 (Thiết lập thực nghiệm)

- Mục 6: từng bước làm gì, tại sao chọn cách đó (đọc `report/ly_thuyet.md` mục 1-2 và docstring trong `src/`).
- Mục 7: tập dev / eval / tầng cực nặng / vật dày (số ảnh mỗi tầng), thước đo (sai số trung bình mm,
  % ảnh đạt sai số <= 1 mm, % ảnh đo được, thời gian mỗi ảnh), tham số dùng (lấy trong `src/cau_hinh.py`),
  tham số chỉ chọn trên tập dev, lệnh để chạy lại.
- Sau 12/11 (D chốt tham số trên ảnh thật) thì cập nhật lại số trong mục 7.

---

## Người D: khảo sát tham số (E2) và phân tích ca lỗi

Viết mục 8.1 và phần phân tích lỗi. Hạn: 09/11 (ảnh tổng hợp), 12/11 (ảnh thật).

### Việc 1. Mở rộng E2

Kết quả E2 hiện tại: đổi `canny_cao` (100/150/220) và `do_rong_dai_canh` (4/8/16) thì sai số
không đổi (1.14 mm), chỉ `do_phan_giai_nan` có ảnh hưởng. Như vậy chưa có gì để phân tích.

Sửa `LUOI` trong `experiments/e2.py` (chỉ D sửa file này), thử khoảng rộng hơn, ví dụ:

```python
LUOI = {
    'canny_cao': [30, 60, 100, 150, 220, 300],
    'do_rong_dai_canh': [1, 2, 4, 8, 16, 32],
    'do_phan_giai_nan': [1.0, 2.0, 3.0, 4.0, 6.0, 8.0],
}
```

```bash
python experiments/e2.py --du_lieu data/dataset_vat_phang
```

Mục tiêu: tìm khoảng giá trị mà tham số bắt đầu ảnh hưởng, rồi giải thích theo lý thuyết.
Ví dụ: `do_rong_dai_canh` quá nhỏ (1-2 px) thì góc thô lệch nhiều sẽ không lấy đủ điểm;
quá lớn thì dính cả biên vật và bóng. `do_phan_giai_nan` lớn hơn s0 (khoảng 3.3 px/mm) thì
không thêm thông tin, chỉ chậm hơn.

Vẽ mỗi tham số một đồ thị nhỏ (trục ngang giá trị tham số, trục dọc sai số mm), có thể vẽ bằng Excel
từ `results/e2/tong_hop_e2.csv`.

### Việc 2. Ảnh trung gian

Trong `results/e2/trung_gian/` có ảnh từng bước cho mỗi giá trị tham số. Chọn 1 bộ đẹp
(ảnh gốc, góc thô, góc đã chỉnh, ảnh nắn, kết quả) cho báo cáo, gửi C dùng cho sơ đồ pipeline.

### Việc 3. Phân tích ca lỗi

```bash
python experiments/e3.py --du_lieu data/dataset_vat_phang
```

Mở `results/e3/ket_qua_e3.csv` bằng Excel, lọc `phuong_phap = day_du`, sắp xếp theo `sai_so_mm` giảm dần.
Lấy khoảng 5 ảnh sai nhiều nhất, mở ảnh ra xem, ghi lại vì sao sai (vật dày? góc lớn? vật tròn?
tách vật dính bóng?). Đây là phần "phân tích thất bại trung thực" thầy chấm ở trục 3.

### Việc 4. Ảnh thật (từ 10/11)

Chạy lại E2 trên tập dev của ảnh thật, chọn bộ tham số tốt nhất, nhắn Quân sửa `src/cau_hinh.py`
(hạn 12/11). Các thí nghiệm khác chạy sau khi đã chốt tham số.

---

## Người E: chứng cứ thách thức (E1) và so sánh với baseline (E3)

Viết mục 4, 8.2, 8.3. Hạn: 09/11 (ảnh tổng hợp), 13/11 (ảnh thật).

### Việc 1. E1: baseline sai theo tầng

```bash
python experiments/e1.py --du_lieu data/dataset_vat_phang
python experiments/ve_do_thi.py results/e1/ket_qua_baseline.csv --ra results/do_thi_e1.png
```

- Bảng sai số theo tầng và theo hướng đặt vật: `results/e1/tong_hop_tang_huong.csv`.
- Chọn ít nhất 3 ảnh baseline đo sai rõ trong `results/e1/anh_loi/`, mỗi ảnh chú thích 1-2 câu
  (đo hụt bao nhiêu, vì sao).
- Tìm 1 cặp ảnh cùng vật, cùng góc, đặt dọc và ngang, cho thấy baseline cho 2 kết quả khác nhau.
- Mở thư mục `data/dataset_vat_phang/minh_hoa_vi_tri/`: cùng vật đặt mép gần và mép xa tờ giấy.
  Chạy baseline trên 6 ảnh này để có số liệu cho ý "tỉ lệ thay đổi theo vị trí".

### Việc 2. Giải thích chỗ lạ

Baseline ở tầng trung bình (14.18 mm) sai hơn tầng nặng (13.03 mm), trong khi lý thuyết nói sai số phải
tăng theo góc. Tìm nguyên nhân: xem bảng theo hướng (dọc/ngang) từng tầng, xem ảnh. Gợi ý: baseline lấy
tỉ lệ từ cạnh ngắn của hình chữ nhật bao tờ giấy; khi nghiêng nhiều tờ giấy thành hình thang dẹt,
cạnh ngắn của hình bao có thể đổi từ cạnh 210 mm sang cạnh 297 mm bị co, làm tỉ lệ sai theo kiểu khác.
Kiểm tra giả thuyết này rồi viết vào mục 4.

### Việc 3. E3: so sánh và ablation

```bash
python experiments/e3.py --du_lieu data/dataset_vat_phang
python experiments/ve_do_thi.py results/e3/ket_qua_e3.csv --ra results/do_thi_e3.png
```

Viết mục 8.2 và 8.3 từ `results/e3/tong_hop_e3.csv`:
- Phương pháp đầy đủ so với baseline theo từng tầng (giảm bao nhiêu lần).
- Bỏ nắn ảnh thì sai số quay về gần baseline, chứng tỏ bước nắn là phần khắc phục góc nhìn.
- Bỏ chỉnh góc thì sai số tăng, rõ nhất ở tầng nặng, chứng tỏ phần B có đóng góp.

### Việc 4. Ảnh thật (từ 12/11, sau khi D chốt tham số)

Chạy lại E1, E3 với `--du_lieu data/dataset_that`, so với kết quả ảnh tổng hợp, cập nhật bảng
và đồ thị trong báo cáo (hạn 13/11).

---

## Lịch chung

| Ngày | Việc |
|---|---|
| 03/11 | Quân commit `ly_thuyet.md` (xong thì mới chạy E4) |
| 07/11 | A gửi ảnh thật |
| 09/11 | C, D, E xong phân tích trên ảnh tổng hợp, có bảng số và hình |
| 12/11 | D chốt tham số trên ảnh thật |
| 13/11 | E xong E1, E3 trên ảnh thật; Quân xong E4 |
| 16/11 | Chốt code |
| 17/11 | Nộp bản nháp mục báo cáo (file Word riêng) |
