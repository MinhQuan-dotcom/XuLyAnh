# Cơ sở lý thuyết và dự đoán điểm gãy

Người viết: N1. File này được commit trước khi chạy E4. Sau khi commit, mục 5 (dự đoán) không sửa nữa;
kết quả thật ghi ở mục 6.

## 1. Kỹ thuật đề xuất P

Pipeline gồm 5 bước:

1. Tìm tờ giấy (phần A): ảnh xám, làm mờ Gaussian, ngưỡng Otsu, lấy contour lớn nhất,
   approxPolyDP ra 4 góc thô.
2. Chỉnh lại góc (phần B): với mỗi cạnh giấy, lấy điểm biên Canny nằm gần cạnh thô (bỏ 10% ở hai đầu),
   khớp một đường thẳng bằng cv2.fitLine (hàm mất mát Huber), góc mới là giao điểm của hai cạnh kề nhau.
3. Tính homography H (phần C): từ 4 cặp điểm, 4 góc trong ảnh ứng với (0,0), (210,0), (210,297),
   (0,297) mm. Nhóm tự viết phép giải DLT bằng SVD và đối chiếu với cv2.findHomography.
4. Nắn ảnh (phần C): biến đổi ảnh bằng S·H, với S = diag(s, s, 1), ra ảnh nhìn thẳng có đúng s px/mm.
5. Đo vật (phần D): tách vật trên ảnh đã nắn bằng ngưỡng trên HSV, lấy hình chữ nhật bao nhỏ nhất,
   chia cạnh cho s ra mm.

Baseline dùng chung bước 1 và bước tách vật, nhưng đo trên ảnh gốc với một tỉ lệ duy nhất
(cạnh ngắn của hình chữ nhật bao tờ giấy chia 210 mm). Hai bên chỉ khác nhau ở cách đổi pixel sang mm.

## 2. Cơ chế: vì sao P khắc phục được góc nhìn

Với camera lỗ kim, mọi điểm nằm trên một mặt phẳng được chiếu lên ảnh bằng một phép biến đổi xạ ảnh
x' ~ H x (H là ma trận 3x3, 8 bậc tự do). 4 cặp điểm, không có 3 điểm nào thẳng hàng, là đủ để xác định H.

Thách thức C (góc nhìn) phá hỏng tỉ lệ cục bộ giữa ảnh và mặt bàn. Gọi θ là góc giữa trục camera
và pháp tuyến mặt bàn:

- Khi θ = 0, mặt bàn song song với cảm biến, mọi chỗ trên bàn cách camera như nhau, nên 1 mm ở đâu
  và theo hướng nào cũng chiếm cùng số pixel. Một tỉ lệ px/mm là đủ.
- Khi θ > 0, theo hướng nghiêng 1 mm chỉ còn chiếm khoảng cos θ lần so với hướng vuông góc,
  và phần bàn ở xa camera trông nhỏ hơn phần ở gần (số pixel trên 1 mm tỉ lệ với f / Z, Z là khoảng cách).
  Tỉ lệ px/mm không còn là hằng số, nó thay đổi theo vị trí và theo hướng.

Baseline giả định tỉ lệ là hằng số và giống nhau theo mọi hướng, nên sai số tăng theo θ, đo hụt nhiều nhất
theo hướng nghiêng, và cùng một vật đặt dọc hay ngang cho kết quả khác nhau.

P không đi tìm một tỉ lệ mà tìm cả H rồi dùng nó nắn ảnh. Sau khi nắn, mọi điểm trên mặt bàn nằm trong
một hệ toạ độ có đúng s px/mm ở mọi chỗ và mọi hướng. Về lý thuyết, kết quả đo của P không phụ thuộc θ,
vị trí hay hướng đặt vật, với hai điều kiện: vật nằm trên mặt phẳng bàn, và 4 góc giấy được tìm chính xác.

Bước chỉnh góc (phần B) nhắm vào điều kiện thứ hai. Góc lấy từ approxPolyDP chỉ dựa vào vài pixel đúng
chỗ góc, mà chỗ đó hay bị mờ, bo tròn hoặc răng cưa. Đường thẳng khớp từ hàng trăm điểm dọc theo cạnh
thì nhiễu từng điểm được trung bình đi, nên giao điểm ổn định hơn. Sai số góc truyền thẳng vào H, nên
góc tốt hơn phải cho phép đo tốt hơn, rõ nhất khi θ lớn (cạnh xa của giấy ngắn, ít pixel).

## 3. Nối về nền tảng môn học

- Chương 2: biến đổi hình học (homography, nắn ảnh, nội suy), lọc tuyến tính (Gaussian), toán tử điểm (ngưỡng).
- Chương 3: phát hiện cạnh Canny, khớp đường thẳng từ điểm biên.
- Chương 4: phân đoạn bằng ngưỡng và contour để tách tờ giấy và vật.

Không dùng mô hình học sâu hay hàm dựng sẵn nào để làm thay phần xử lý góc nhìn.
cv2.findHomography chỉ dùng để đối chiếu với hàm DLT tự viết.

## 4. Mức tính mới

- Kết hợp và điều chỉnh: thêm bước chỉnh góc bằng giao điểm đường thẳng khớp (Canny + fitLine Huber)
  vào pipeline nắn phối cảnh 4 điểm; tự cài DLT.
- Dự đoán định lượng: mục 5 đưa ra công thức và con số điểm gãy trước khi chạy E4, rồi E4 kiểm chứng
  chính các con số này.

Nắn phối cảnh từ 4 điểm là kiến thức đã có. Phần của nhóm là bước chỉnh góc, phân tích sai số và kiểm
chứng điểm gãy.

## 5. Dự đoán điểm gãy

Ngưỡng chấp nhận: sai số không quá e_max = 1 mm.

### 5.1. Thị sai do độ dày vật

H chỉ đúng cho điểm nằm trên mặt bàn. Mép trên của vật dày t nằm cao hơn mặt bàn, khi nắn bị đẩy ra
xa camera một đoạn khoảng t·tan(α), với α là góc giữa tia nhìn tới điểm đó và pháp tuyến mặt bàn
(ở giữa khung hình α gần bằng θ). P gãy khi t·tan(θ) > e_max:

    θ_gãy ≈ arctan(e_max / t)

| Độ dày t | θ_gãy dự đoán |
|---|---|
| 0.1 mm | khoảng 84 độ (không gãy trong khoảng chụp) |
| 1 mm | khoảng 45 độ |
| 3 mm | khoảng 18 độ |
| 5 mm | khoảng 11 độ |
| 10 mm | khoảng 6 độ |

Dự đoán thêm:
- Sai số do thị sai luôn là đo dư (vật to hơn thật), không đo hụt.
- Sai số nằm chủ yếu ở chiều theo hướng nghiêng: với vật đặt dọc, chiều dài sai nhiều hơn chiều rộng.
- Sai số tăng gần tuyến tính theo tan(θ).
- Với vật dày 10 mm, ngay ở θ = 0 cũng có thể gần ngưỡng: mép vật cách tâm ảnh khoảng 3 cm, camera
  cách khoảng 35 cm, nên α khoảng 5 độ, sai số khoảng 10·tan(5°) ≈ 0.9 mm.

### 5.2. Độ phân giải bị co theo hướng nghiêng

Nắn ảnh không thêm thông tin. Theo hướng nghiêng, 1 mm trên bàn chỉ chiếm khoảng s0·cos(θ) pixel ảnh gốc,
s0 là số px/mm khi chụp thẳng. Với ảnh tổng hợp (tiêu cự khoảng 1160 px, khoảng cách 330-380 mm),
s0 khoảng 3.1-3.5 px/mm. Nếu biên vật lệch khoảng 1 px ảnh gốc ở mỗi đầu, sai số đo khoảng
2 / (s0·cos θ) mm, vượt 1 mm khi cos θ < 2 / s0:

    θ_gãy ≈ 50-55 độ (với vật mỏng)

### 5.3. Không tìm được 4 góc giấy

Khi θ rất lớn, cạnh xa của tờ giấy rất ngắn, approxPolyDP có thể không ra đúng 4 đỉnh và P hỏng hẳn.
Kiểm tra phần A trên ảnh tổng hợp cho thấy ở 60-70 độ vẫn tìm đủ 4 góc ở mọi ảnh. Vì vậy nhóm dự đoán
trường hợp này không xảy ra trên ảnh tổng hợp trong khoảng đã tạo (đến 70 độ), nhưng có thể xảy ra trên
ảnh thật ở khoảng 65 độ, do cạnh xa bị mờ, bị chói hoặc lẫn với nền.

### 5.4. Tổng hợp cho tập đánh giá

| Trường hợp | Dự đoán |
|---|---|
| Baseline | vượt 1 mm từ khoảng 10-15 độ, với mọi vật |
| P, vật rất mỏng (t <= 1 mm) | dưới 1 mm đến khoảng 45 độ (giới hạn bởi thị sai), sau đó tăng; hết đạt hẳn ở khoảng 50-55 độ |
| P, vật dày 2-3 mm | gãy sớm hơn, khoảng 18-27 độ |
| P, tầng cực nặng (60-70 độ) | sai số trung bình trên 1 mm |

Các con số này có thể sai. Nếu sai, nhóm sẽ phân tích nguyên nhân ở mục 6 và trong phần Thảo luận
của báo cáo.

## 6. Đối chiếu sau thí nghiệm

Viết ngày 17/11 sau khi chạy E4 (`python experiments/e4.py --du_lieu data/dataset_vat_phang`).
Số liệu lấy từ `results/e4/*.csv` và `results/e3/ket_qua_e3.csv`. Mục 5 giữ nguyên như lúc commit.

### 6.1. Thị sai do độ dày (dự đoán 5.1): đúng về dạng, sai về con số

Góc gãy đo được (góc nhỏ nhất mà sai số trung bình chiều dài vượt 1 mm, E4b):

| Độ dày t | Dự đoán | Đo được |
|---|---|---|
| 0.1 mm | không gãy (84°) | không gãy đến 45° (0.78 mm ở 45°) |
| 1 mm | 45° | 30° (1.05 mm); ở 15° đã sát ngưỡng (0.98 mm) |
| 3 mm | 18° | đã vượt ở 0° (1.08 mm) |
| 5 mm | 11° | đã vượt ở 0° (1.63 mm) |
| 10 mm | 6° | đã vượt ở 0° (2.41 mm) |

Những phần đúng:
- Sai số do độ dày luôn là đo dư: mọi ảnh trong E4b đều có sai số dương.
- Sai số nằm chủ yếu ở chiều theo hướng nghiêng: vật 10 mm ở 45°, đặt dọc thì chiều dài dư 12.5 mm,
  chiều rộng dư 2.4 mm; đặt ngang thì ngược lại (dài dư 3.1 mm, rộng dư 12.1 mm).
- Phần tăng thêm theo góc khớp với t·tan θ: vật 10 mm đặt dọc dư 2.5 / 4.3 / 7.2 / 12.5 mm ở 0 / 15 / 30 / 45°,
  phần tăng so với 0° là 1.8 / 4.7 / 10.1 mm, còn t·tan θ là 2.7 / 5.8 / 10.0 mm.

Những phần sai: góc gãy thực tế sớm hơn dự đoán, vì công thức θ_gãy = arctan(e_max / t) bỏ sót hai khoản:
1. Sai số nền khoảng 0.5-0.6 mm có sẵn ở mọi ảnh, kể cả vật 0.1 mm ở 0° (đo dư 0.5-0.65 mm). Nguyên nhân là
   biên vật bị nhòe 1-2 px sau khi làm mờ và nén JPEG, phần nhòe bị tính vào vật. Khoản này dùng hết khoảng
   một nửa ngưỡng 1 mm.
2. Mặt trên của vật dày nằm gần camera hơn mặt bàn, nên trông to hơn theo tỉ lệ khoảng D / (D - t), với D là
   khoảng cách camera (330-380 mm). Khoản này có ngay cả ở θ = 0: vật 60 mm dày 10 mm dư khoảng 60·10/350 ≈ 1.7 mm.
   Dự đoán ở mục 5.1 có nhắc tới sai số ở θ = 0 nhưng tính theo góc lệch tia nhìn ở mép vật (0.9 mm) chứ không
   tính độ phóng to này.

Mô hình sửa lại: e(θ) ≈ e0 + L·t/D + t·tan θ, với e0 ≈ 0.55 mm. Ví dụ t = 10 mm, L = 60 mm, θ = 45°:
0.55 + 1.7 + 10 ≈ 12.3 mm, đo được 12.5 mm. Với t = 1 mm, điều kiện e < 1 mm cho θ_gãy ≈ 16°, gần với kết quả đo
(0.98 mm ở 15°, 1.05 mm ở 30°).

### 6.2. Độ phân giải bị co (dự đoán 5.2): đúng

Vật mỏng (t ≤ 0.5 mm) trên ảnh tổng hợp, phương pháp đầy đủ:

| Góc | Sai số TB chiều dài | Tỉ lệ ảnh đạt ≤ 1 mm |
|---|---|---|
| 4-13° | 0.49 mm | 100% |
| 21-31° | 0.57 mm | 94% |
| 39-51° | 0.73 mm | 69% |
| 59-71° | 1.43 mm | 6% |

Vật mỏng giữ dưới 1 mm đến khoảng 50° và vượt ngưỡng ở 60-70°, khớp khoảng dự đoán 50-55°.

### 6.3. Không tìm được 4 góc giấy (dự đoán 5.3): đúng trên ảnh tổng hợp, chưa kiểm được trên ảnh thật

Ở 60° và 70° phương pháp vẫn tìm đủ 4 góc và đo được 100% ảnh (E4a, 48 ảnh). Ảnh thật không có tầng 65°
(không chụp được), nên phần dự đoán cho ảnh thật chưa kiểm chứng.

### 6.4. Tổng hợp cho tập đánh giá (dự đoán 5.4)

| Trường hợp | Dự đoán | Kết quả | Đánh giá |
|---|---|---|---|
| Baseline | vượt 1 mm từ 10-15° | vượt ngay từ 4-6° (sai số TB 2.0 mm, chỉ 4% ảnh đạt) | sai: gãy sớm hơn |
| P, vật t ≤ 1 mm | dưới 1 mm đến khoảng 45°, hết đạt ở 50-55° | vật t ≤ 0.5 mm: 0.73 mm ở 39-51°, 1.43 mm ở 60-70°; vật t = 1-1.2 mm: 0.91 mm ở 39-51° | đúng |
| P, vật dày 2-3 mm | gãy ở 18-27° | 0.70 mm ở 4-13°, 1.23 mm ở 21-31° | đúng |
| P, tầng cực nặng | trên 1 mm | 1.43-4.86 mm tuỳ độ dày | đúng |

Baseline gãy sớm hơn dự đoán vì ngoài hệ số cos θ còn có chênh lệch khoảng cách: tỉ lệ px/mm lấy từ cạnh gần
camera của tờ giấy, còn vật nằm giữa tờ giấy, xa hơn khoảng 150·sin θ mm. Ở 5° chênh khoảng 13 mm trên 350 mm,
tức vật bị đo nhỏ đi khoảng 3% (đo được: 2.8%), đủ vượt 1 mm với vật dài 60-110 mm.

Ảnh thật cho cùng xu hướng: nắp chai v5 (dày 2 mm) đo dài 28.75 / 30.5 / 31.25 mm ở 10 / 30 / 50°
(thật 29 mm), tăng theo góc và luôn theo trục nghiêng như dự đoán 5.1.

