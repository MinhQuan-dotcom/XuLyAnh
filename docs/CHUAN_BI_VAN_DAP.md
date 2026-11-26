# Chuẩn bị thuyết trình và vấn đáp

Thuyết trình chiếm 50% điểm, chấm cả phần trả lời Q&A. Thầy có thể hỏi bất kỳ ai về phần người đó đứng tên
(code và mục báo cáo). Ai không giải thích được phần mình là mất điểm cả nhóm.

Mỗi người: đọc phần của mình dưới đây, đọc lại các mục báo cáo tương ứng trong `report/Bao_cao_nhap.docx`,
mở code của mình ra đọc lại từng dòng, và tự trả lời to các câu hỏi mẫu (không nhìn tài liệu).

Số liệu trong file này lấy từ `docs/KET_QUA_HIEN_TAI.md` và báo cáo (code ngày 17/11, E2 bổ sung 26/11).

---

## Mọi người đều phải trả lời được

1. **Đề tài là gì, thách thức C là gì?** Đo dài/rộng vật trên tờ A4 từ ảnh điện thoại chụp nghiêng. C = góc nhìn,
   đo bằng góc nghiêng θ giữa trục camera và pháp tuyến mặt bàn. Ba tầng: nhẹ 0-15°, trung bình 15-35°, nặng 35-55°
   (thêm cực nặng 55-75° cho E4).
2. **Baseline sai thế nào?** Lấy một tỉ lệ px/mm từ cạnh ngắn tờ giấy chia 210 rồi đo trên ảnh gốc. Sai số chiều dài
   4,02 / 14,17 / 13,03 mm (tổng hợp), 4,09 / 15,67 / 12,39 mm (ảnh thật). Ba biểu hiện: sai tăng theo góc, phụ thuộc
   hướng đặt (dọc/ngang), phụ thuộc vị trí (mép gần/xa).
3. **P là gì, vì sao chạy được?** Tìm 4 góc giấy, chỉnh góc, tính homography H từ 4 góc, nắn ảnh về nhìn thẳng với
   đúng 4 px/mm, rồi đo. Sau khi nắn thì tỉ lệ ở mọi chỗ, mọi hướng đều như nhau, nên không còn phụ thuộc θ.
   Sai số P: 0,54 / 0,80 / 1,32 mm (tổng hợp), 1,17 / 1,61 / 2,27 mm (ảnh thật); giảm 7-18 lần và 3,5-10 lần.
4. **P gãy ở đâu?** Khi vật có độ dày (H chỉ đúng cho điểm nằm trên mặt bàn) và khi góc quá lớn (độ phân giải
   theo hướng nghiêng bị co). Vật mỏng giữ dưới 1 mm đến khoảng 50°, vật dày 2-3 mm vượt 1 mm từ tầng trung bình.
5. **Vì sao dùng ảnh tổng hợp?** Giảng viên đã cho phép. Ảnh tổng hợp biết chính xác θ và kích thước nên dùng để
   phát triển, kiểm tra từng phần và chạy E4 (cần góc 60-70° và vật dày tới 10 mm, khó chụp thật). Kết luận chính
   (E1, E3) đều có kết quả trên 48 ảnh tự chụp.
6. **Vì sao không dùng học sâu?** Đề yêu cầu kỹ thuật nối được về môn học; homography, Canny, Otsu đều thuộc
   chương 2-4. Bài toán có hình học rõ ràng (một mặt phẳng, một hình chữ nhật biết kích thước) nên không cần học.

---

## Quân (trưởng nhóm)

**Đứng tên:** code phần B `src/goc.py` (chỉnh góc), ghép pipeline `src/phuong_phap.py`, khung dự án.
Báo cáo mục 1, 5, 8.4 (E4), 9, 10, 11; `report/ly_thuyet.md`.

**Phải hiểu được:**
- Chỉnh góc: lấy điểm biên Canny trong dải 8 px quanh mỗi cạnh thô, bỏ 10% mỗi đầu cạnh, khớp đường thẳng bằng
  `cv2.fitLine` với hàm mất mát Huber, góc mới là giao điểm hai đường kề nhau. Nếu cạnh có ít hơn 10 điểm hoặc góc mới
  lệch quá 24 px so với góc thô thì giữ góc thô.
- Vì sao Huber: bình phương tối thiểu bị vài điểm lạc (băng keo, bóng) kéo lệch; Huber phạt tuyến tính khi phần dư lớn.
- Dự đoán điểm gãy (viết ngày 03/11, chạy E4 ngày 17/11): θ_gãy = arctan(e_max / t), và giới hạn độ phân giải
  2/(s0·cos θ) với s0 ≈ 3,1-3,5 px/mm.
- Kết quả E4: t = 1 mm gãy ở 30° (dự đoán 45°); t ≥ 3 mm vượt 1 mm ngay ở 0° (dự đoán 18 / 11 / 6°). Dạng đúng
  (luôn đo dư, theo hướng nghiêng, tăng theo tan θ), con số sai vì bỏ sót sai số nền ≈ 0,55 mm và độ phóng to mặt trên
  vật L·t/D. Mô hình sửa: e ≈ 0,55 + L·t/D + t·tan θ (t = 10, L = 60, θ = 45° cho 12,3 mm, đo được 12,5 mm).
- Mức tính mới: nhóm nhận mức 3 (dự đoán định lượng trước, E4 kiểm chứng).

**Câu hỏi dễ bị hỏi:**
- *Bước chỉnh góc của em có tác dụng không?* Ảnh tổng hợp: có, sai số góc 3,67 → 1,30 px, bỏ bước này MAE tăng
  18-31% (0,54 → 0,71 mm ở tầng nhẹ). Ảnh thật: không, hai cấu hình gần bằng nhau, P đầy đủ còn kém 0,01-0,09 mm.
  Lý do: mép giấy thật không thẳng (dán băng keo trên vải, mép vồng), nên đường thẳng khớp theo cả cạnh không tốt hơn
  góc lấy đúng tại chỗ. Phải nói thẳng điều này, đừng né.
- *Dự đoán sai thì sao?* Đề cho phép dự đoán sai nếu kiểm chứng nghiêm túc và giải thích được; nhóm đã chỉ ra hai
  khoản bị bỏ sót và mô hình sửa lại khớp số đo.
- *Giả định yếu nhất?* Vật nằm trên mặt phẳng giấy. Vật dày 3 mm đã sai quá 1 mm khi chụp thẳng.
- *Tại sao nhận mức 3 mà không phải mức 2?* Mức 2 là ghép chỉnh góc vào nắn bốn điểm có lý do. Mức 3 cần thêm dự đoán
  định lượng viết trước và thực nghiệm kiểm chứng chính dự đoán đó: nhóm có công thức θ_gãy, commit 03/11, E4 chạy
  17/11 kiểm chứng, đúng phần độ phân giải, sai con số phần thị sai và giải thích được.

---

## An (Trương Tấn An)

**Đứng tên:** code phần A `src/giay.py` (tìm tờ giấy); chụp 48 ảnh thật và đo nhãn; báo cáo mục 2 (Dữ liệu).

**Phải hiểu được:**
- Tìm giấy: ảnh xám → làm mờ Gaussian 5×5 → ngưỡng Otsu → `findContours` → bỏ đường viền chạm mép ảnh và vùng nhỏ
  hơn 3% ảnh → lấy vùng lớn nhất → `approxPolyDP` quét epsilon 0,5-5% chu vi đến khi ra 4 đỉnh lồi → sắp 4 góc theo
  góc quanh trọng tâm.
- Vì sao Otsu chạy tốt: giấy trắng trên nền tối, lược đồ xám có 2 đỉnh tách xa. E2: kernel làm mờ 1-21 đều tìm được
  100% ảnh, MAE không đổi; kernel 21 làm góc thô lệch 3,3 px nhưng bước chỉnh góc sửa lại.
- Vì sao phải sắp 4 góc theo góc quanh trọng tâm: cách sắp theo tổng/hiệu tọa độ bị đảo thứ tự khi giấy nghiêng 70°.
- Dữ liệu thật: iPhone 14, 06/11/2026, đèn trần, không flash, giấy dán băng keo trên vải đen, cách khoảng 35 cm;
  góc đo bằng app Đo (Thăng bằng), làm tròn 0/10/30/50°. 12 ảnh dev (d1, d2), 36 ảnh eval (v1-v6 × 3 góc × 2 hướng).
  Nhãn đo bằng thước, làm tròn 1 mm. Giấy đo được 208 × 298 mm, dùng 210 × 297.
- Tổng hợp: 286 ảnh, script `tools/render_vat_phang.py` seed 2026, camera lỗ kim f ≈ 1160 px, cách 330-380 mm.
- Tiêu chí phân tầng: `data/PHAN_TANG.md`.

**Câu hỏi dễ bị hỏi:**
- *Sao không có ảnh thật ở 65°?* Không giữ máy ổn định và đọc được góc; tầng cực nặng chỉ có ảnh tổng hợp.
- *Nhãn chỉ chính xác 1 mm thì sai số 1 mm có ý nghĩa không?* Sai số nhãn tới 0,5 mm, nên ngưỡng đạt ≤ 1 mm trên ảnh
  thật là khắt khe; nhóm đã ghi rõ trong báo cáo.
- *Làm sao chắc khác biệt giữa các tầng là do góc?* Cùng vật, cùng giấy, cùng đèn, cùng khoảng cách, vật ở giữa giấy;
  chỉ thay đổi góc.
- *6 ảnh chụp thử bị lỗi gì?* Vật trắng thì không tách được khỏi giấy; mặt bàn lóa làm sai góc giấy. Đây là giả định
  về nền và ánh sáng, không thuộc thách thức C.

---

## Đoàn

**Đứng tên:** code phần C `src/hinh_hoc.py` (DLT tự viết, nắn ảnh); báo cáo mục 3 (Công trình liên quan),
mục 6 (Phương pháp), mục 7 (Thiết lập thực nghiệm); `report/lien_quan.md`.

**Phải hiểu được:**
- Homography: ma trận 3×3, 8 bậc tự do (9 phần tử, bỏ 1 vì nhân hằng số không đổi), mỗi cặp điểm cho 2 phương
  trình nên cần 4 cặp, không 3 điểm nào thẳng hàng.
- DLT: dựng ma trận A 8×9, giải A·h = 0 bằng SVD, h là vectơ kỳ dị ứng với giá trị kỳ dị nhỏ nhất. Hàm tự viết cho
  cùng kết quả với `cv2.findHomography`, ảnh nắn lệch 0,003 mm.
- Nắn: M = S·H với S = diag(s, s, 1), s = 4 px/mm, ảnh nắn 840 × 1188; `warpPerspective` nội suy tuyến tính.
- 4 công trình: Hartley & Zisserman [1] (DLT, nắn), Criminisi [2] (đo từ một ảnh), Liebowitz [3] (nắn metric),
  Zhang & He [4] (quét bảng trắng: Hough → tứ giác → nắn). Mỗi bài nhóm kế thừa gì, làm khác gì (mục 3).
- Mục 7: dev 48 tổng hợp + 12 thật chỉ để chọn tham số; eval 144 tổng hợp + 36 thật; thước đo MAE dài/rộng theo
  tầng, % ảnh ≤ 1 mm, % đo được, chênh dọc/ngang, thời gian (P khoảng 30 ms/ảnh).

**Câu hỏi dễ bị hỏi:**
- *Tại sao không dùng RANSAC?* Chỉ có đúng 4 điểm (4 góc giấy), RANSAC cần nhiều hơn số điểm tối thiểu để loại
  điểm sai. Nhóm làm 4 điểm đó chính xác hơn bằng bước chỉnh góc.
- *Pipeline dùng hàm tự viết hay OpenCV?* Thí nghiệm gọi `cv2.findHomography`; hàm tự viết cho cùng kết quả và bật được
  bằng `dung_dlt_tu_viet`. Hàm tự viết để chứng minh hiểu thuật toán.
- *Vì sao chọn s = 4?* Ảnh gốc chỉ có khoảng 3,1-3,5 px/mm; s lớn hơn không thêm thông tin mà chậm hơn, s nhỏ hơn mất
  chi tiết. s = 1 có MAE thấp trên ảnh tổng hợp là do bù trừ (xem phần Dương).
- *Nhóm khác gì Zhang & He?* Không cần Hough trên cả ảnh vì đã có cạnh thô; biết khổ A4 nên không phải ước lượng tỉ lệ
  khung.
- *Tham số chọn ở đâu?* Chỉ trên tập dev (E2), không chỉnh trên tập eval; ngoại lệ là bước tách vật sửa 17/11, đã
  ghi rõ ở mục 9.4.

---

## Dương

**Đứng tên:** code phần D `src/vat.py` (tách vật, đo); báo cáo mục 8.1 (E2) và phần sửa lỗi tách vật ở mục 9.4.

**Phải hiểu được:**
- Tách vật trên ảnh nắn: bỏ viền 10 px, đổi HSV; vật = (S > 60) hoặc (V < max(80, 0,5 × V trung vị của giấy));
  mở 3×3 bỏ nhiễu, đóng 7×7 nối mảng màu rời; lấy đường viền lớn nhất ≥ 200 px; `minAreaRect` → dài, rộng ÷ s.
- Sửa ngày 17/11: thẻ sinh viên v2 (mặt sau xanh nhạt, S thấp) bị đo rộng 37 mm thay vì 54; thẻ đen v1 (thực tế xám
  đậm, V ≈ 95) chỉ bắt được mép. Thêm ngưỡng V theo độ sáng giấy và phép đóng 7×7: MAE rộng ảnh thật 1,5-7,6 →
  0,8-2,4 mm. Đã thử tiêu chí màu Lab, bỏ vì bắt cả bóng.
- E2 (6 tham số, mỗi tham số 6 giá trị, Bảng 8.1-8.6, Hình 8.2):
  - Canny 30-300: không ảnh hưởng (cạnh giấy tương phản cao).
  - Độ rộng dải: 1-2 px kém hơn, từ 4 px ổn định, giữ 8.
  - s: s = 1 MAE thấp nhất nhưng do bù trừ: sai số có dấu luôn dương (+0,66 ở s = 1, +1,16 ở s = 4), ảnh nắn thô làm vật
    nhỏ lại bù phần đo dư; trên dev ảnh thật s = 1 lại kém hơn (rộng 2,29 so với 1,90 mm).
  - nguong_s: 20 hỏng (lấy cả giấy, 64,8 mm); 40-140 MAE giảm nhưng lại là bù trừ (có dấu +1,45 → +0,46); trên ảnh
    thật 140 chỉ đo được 25% ảnh vì bìa nâu có S ≈ 110. Giữ 60.
  - he_so_v: gần như không đổi vì vật trong dev đều có màu; hạn chế của tập dev.

**Câu hỏi dễ bị hỏi:**
- *Sao không chọn s = 1 hay nguong_s = 140 khi MAE thấp hơn?* Vì sai số có dấu cho thấy đó là hai lỗi ngược chiều bù
  nhau, và trên ảnh thật thì cách bù này hỏng. Đây là điểm quan trọng nhất của phần E2.
- *Sửa tách vật sau khi xem tập đánh giá là chỉnh trên tập đánh giá à?* Có nguy cơ, nhóm đã ghi rõ ở 9.4. Hệ số 0,5
  chọn theo lý lẽ (vật tối là tối hơn nửa độ sáng giấy), trên dev các giá trị 0-0,5 chênh không quá 0,04 mm.
- *Tại sao dùng HSV mà không dùng ảnh xám?* Vật màu có thể sáng gần bằng giấy nhưng khác giấy ở độ bão hòa; vật tối
  thì khác ở độ sáng. Hai tiêu chí bổ sung nhau.
- *Vật trắng thì sao?* Không tách được; đó là giả định nền/vật có màu khác trắng.

---

## Bảo

**Đứng tên:** code phần E `src/baseline.py`, `experiments/ve_do_thi.py`; báo cáo mục 4 (E1), 8.2, 8.3 (E3).

**Phải hiểu được:**
- Baseline: dùng chung bước tìm giấy (A) và tách vật (D) với P, chỉ khác cách đổi px → mm: cạnh ngắn hình chữ nhật
  bao giấy ÷ 210. Nhờ vậy khác biệt giữa baseline và P chỉ do xử lý góc nhìn.
- E1 (mục 4): 3 ảnh lỗi (v1 30°: 87,4 × 65,5 so với 121 × 70; v2 50°: 55,5 × 51,5 so với 85 × 54; v3 50°:
  77,1 × 73,5 so với 107 × 79). Cùng vật xoay dọc/ngang chênh 19,9 mm. Cùng vật mép gần/xa: 102,0 và 54,2 mm (thật 110),
  P đo 111,1 và 112,0.
- **Vì sao tầng nặng sai ít hơn tầng trung bình** (câu chắc chắn bị hỏi): khi nghiêng nhiều, cạnh 297 mm bị co ngắn
  hơn cạnh 210 mm nên baseline lấy nhầm cạnh 297 để chia 210 (48/48 ảnh tầng nặng, 1/48 tầng trung bình). Chiều theo
  hướng nghiêng bị đo còn khoảng 0,71 lần, còn chiều ngang lại gần đúng (cos 45° × 1,41 ≈ 1), nên MAE thấp hơn.
- E3 (mục 8.2, 8.3): bỏ nắn ảnh → sai số về gần baseline (14,37 so với 14,17 ở tầng trung bình) ⇒ bước nắn là thứ
  giải quyết C. Bỏ chỉnh góc → tổng hợp tăng 18-31%, ảnh thật không đổi.
- Chênh dọc/ngang: baseline 0,91 / 5,83 / 18,12 mm, P 0,19 / 0,33 / 0,87 mm (tổng hợp); ảnh thật P vẫn chênh 1,8-3,0 mm
  vì v1, v3 bị đo dư theo trục dài tờ giấy (+6,2 và +3,1 mm).

**Câu hỏi dễ bị hỏi:**
- *Baseline có phải cố tình làm yếu không?* Không: đây là cách làm phổ biến (một tỉ lệ từ vật tham chiếu), và dùng chung
  phần tìm giấy, tách vật với P.
- *Làm sao chứng minh lỗi do góc chứ không do tách vật?* Trong ảnh lỗi, viền vật tách đúng; các yếu tố khác giữ cố
  định giữa các tầng; bỏ nắn ảnh thì lỗi quay lại dù tách vật y hệt.
- *Ablation nói gì về phần B?* Trên ảnh thật phần B không giúp; thành phần chịu lực là bước nắn.
- *Vì sao ảnh thật sai hơn ảnh tổng hợp?* Nhãn chỉ 1 mm; v1, v3 đo dư theo trục dài giấy (bóng của vật đen, mặt bên
  vật dày 2 mm); giấy không phẳng; tách vật khó hơn.

---

## Gợi ý chia phần thuyết trình

| Phần | Người | Nội dung |
|---|---|---|
| Mở đầu | Quân | Bài toán, thách thức C, tuyên bố A/B/C, giả định |
| Dữ liệu | An | Hai bộ ảnh, cách chụp, phân tầng, nhãn |
| E1 | Bảo | Baseline sai theo tầng, ảnh lỗi, dọc/ngang, gần/xa, vì sao tầng nặng thấp hơn |
| Lý thuyết + phương pháp | Đoàn | Homography, DLT, pipeline 5 bước, công trình liên quan |
| E2 | Dương | Khảo sát tham số, bù trừ sai số, sửa tách vật |
| E3 + so sánh | Bảo | Bảng theo tầng, ablation |
| E4 + thảo luận + kết luận | Quân | Dự đoán, kết quả, mô hình sửa lại, giả định yếu nhất |
