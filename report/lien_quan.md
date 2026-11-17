# Công trình liên quan

Trích dẫn theo chuẩn IEEE, số thứ tự khớp với danh mục tài liệu tham khảo của báo cáo.

---

### [1] Multiple View Geometry in Computer Vision (sách)
- **Trích dẫn IEEE:** R. Hartley and A. Zisserman, *Multiple View Geometry in Computer Vision*, 2nd ed. Cambridge, U.K.: Cambridge Univ. Press, 2004.
- **Họ làm gì:** Trình bày phép biến đổi xạ ảnh giữa hai mặt phẳng (homography 3x3, 8 bậc tự do), thuật toán DLT
  giải H từ ít nhất 4 cặp điểm bằng SVD, chuẩn hoá toạ độ trước khi giải, và cách nắn ảnh một mặt phẳng về dạng nhìn thẳng.
- **Nhóm kế thừa gì:** Mô hình camera lỗ kim, công thức DLT (nhóm tự cài trong `src/hinh_hoc.py` và so với
  `cv2.findHomography`), ý tưởng ghép ma trận co giãn S = diag(s, s, 1) với H để ra ảnh nắn có tỉ lệ cố định.
- **Nhóm làm khác gì:** Sách dùng nhiều cặp điểm và ước lượng bền vững (RANSAC). Nhóm chỉ có đúng 4 điểm là 4 góc
  tờ A4, nên không loại được điểm sai bằng RANSAC; thay vào đó nhóm làm chính xác 4 điểm đó bằng bước khớp đường thẳng.

### [2] Single view metrology
- **Trích dẫn IEEE:** A. Criminisi, I. Reid, and A. Zisserman, "Single view metrology," *Int. J. Comput. Vis.*, vol. 40, no. 2, pp. 123-148, 2000.
- **Họ làm gì:** Đo đạc từ một ảnh phối cảnh duy nhất, chỉ cần đường chân trời của một mặt phẳng tham chiếu và
  một điểm tụ. Đo được tỉ lệ độ dài, diện tích trên mặt phẳng và chiều cao so với mặt phẳng, không cần biết tiêu cự
  hay tư thế camera; có phân tích lan truyền sai số cho từng phép đo.
- **Nhóm kế thừa gì:** Bài toán giống nhau: đo kích thước thật từ một ảnh nghiêng nhờ hình học của mặt phẳng.
  Ý tưởng phân tích sai số trước rồi mới đo cũng giống cách nhóm đưa dự đoán điểm gãy trước khi chạy E4.
- **Nhóm làm khác gì:** Bài báo cần người dùng chọn đường thẳng song song để tìm điểm tụ. Nhóm dùng một vật có kích
  thước biết trước (tờ A4) nên ra thẳng phép đo tuyệt đối (mm) và tự động hoàn toàn. Nhóm chỉ đo vật nằm trên mặt
  phẳng; phần đo chiều cao của bài báo không dùng, và chính độ cao của vật (độ dày) là nguồn gây gãy mà E4 kiểm tra.

### [3] Metric rectification for perspective images of planes
- **Trích dẫn IEEE:** D. Liebowitz and A. Zisserman, "Metric rectification for perspective images of planes," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 1998, pp. 482-488.
- **Họ làm gì:** Nắn ảnh một mặt phẳng về đúng hình dạng thật (giữ góc và tỉ lệ độ dài) theo từng tầng: xạ ảnh,
  affine, rồi metric; dùng các ràng buộc như góc vuông, tỉ lệ độ dài đã biết, điểm tụ.
- **Nhóm kế thừa gì:** Khái niệm "nắn metric": sau khi nắn, đo độ dài trên ảnh nắn là đo trên mặt phẳng thật.
  Đây là cơ sở để phương pháp P đo vật bằng một tỉ lệ s duy nhất trên ảnh đã nắn.
- **Nhóm làm khác gì:** Bài báo nắn từ các ràng buộc hình học rời rạc (góc vuông, điểm tụ). Nhóm có sẵn một hình
  chữ nhật biết kích thước (tờ A4), nên dùng thẳng 4 góc của nó, đơn giản hơn nhưng phụ thuộc hoàn toàn vào việc
  tìm đúng 4 góc.

### [4] Whiteboard scanning and image enhancement
- **Trích dẫn IEEE:** Z. Zhang and L.-W. He, "Whiteboard scanning and image enhancement," *Digit. Signal Process.*, vol. 17, no. 2, pp. 414-432, 2007.
- **Họ làm gì:** Hệ thống chụp bảng trắng bằng máy ảnh: tìm biên bảng, dùng biến đổi Hough tìm các đường thẳng,
  ghép thành tứ giác, ước lượng tỉ lệ khung thật của bảng, nắn về hình chữ nhật và chỉnh màu.
- **Nhóm kế thừa gì:** Cách tìm tứ giác từ đường thẳng thay vì từ đỉnh đa giác: góc là giao điểm của hai cạnh.
  Bước chỉnh góc của nhóm (phần B) theo đúng ý này.
- **Nhóm làm khác gì:** Nhóm không dùng Hough mà khớp đường thẳng bằng `cv2.fitLine` với hàm mất mát Huber trên các
  điểm biên Canny nằm gần cạnh thô (đã có cạnh thô từ phần A nên không cần tìm đường trên cả ảnh). Bài báo phải ước
  lượng tỉ lệ khung của bảng vì không biết kích thước; nhóm biết trước tờ A4 là 210 x 297 mm nên đo được mm thật.

---

Tài liệu khác được trích trong báo cáo (giáo trình và các thuật toán dùng trong pipeline, mục 5 và 6):

- [5] R. Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed. Cham, Switzerland: Springer, 2022.
- [6] N. Otsu, "A threshold selection method from gray-level histograms," *IEEE Trans. Syst., Man, Cybern.*, vol. 9, no. 1, pp. 62-66, 1979.
- [7] S. Suzuki and K. Abe, "Topological structural analysis of digitized binary images by border following," *Comput. Vis. Graph. Image Process.*, vol. 30, no. 1, pp. 32-46, 1985.
- [8] D. H. Douglas and T. K. Peucker, "Algorithms for the reduction of the number of points required to represent a digitized line or its caricature," *Cartographica*, vol. 10, no. 2, pp. 112-122, 1973.
- [9] J. Canny, "A computational approach to edge detection," *IEEE Trans. Pattern Anal. Mach. Intell.*, vol. PAMI-8, no. 6, pp. 679-698, 1986.
- [10] P. J. Huber, "Robust estimation of a location parameter," *Ann. Math. Statist.*, vol. 35, no. 1, pp. 73-101, 1964.
