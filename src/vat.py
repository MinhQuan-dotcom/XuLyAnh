"""
PHẦN D – Tách vật khỏi tờ giấy và đo kích thước theo pixel.
Người làm: ........   Hạn: 01/11   Kiểm tra: python tests/kiem_tra_D.py

Dùng chung: baseline gọi trên ẢNH GỐC, phương pháp đề xuất gọi trên ẢNH ĐÃ NẮN.
Phần D KHÔNG cần chờ phần A: file kiểm tra tạo mặt nạ tờ giấy từ nhãn.
"""
import numpy as np
import cv2


def tach_vat(anh, mat_na=None, tham_so=None):
    """
    Tìm đường viền của vật (vật có màu / tối, nằm trên giấy trắng).

    Đầu vào
      anh     : ảnh BGR
      mat_na  : numpy uint8 cùng kích thước, 255 = vùng tờ giấy; None = cả ảnh là giấy (ảnh đã nắn) –
                khi đó bỏ một viền 'co_mat_na' pixel quanh mép ảnh vì mép có thể lẫn chút nền bàn
      tham_so : dict (có thể None), dùng 'co_mat_na' – số pixel co mặt nạ vào để bỏ mép giấy
                (mặc định 10), 'dien_tich_toi_thieu' – bỏ vùng nhỏ hơn (pixel, mặc định 200)
    Đầu ra
      contour : numpy int32 shape (N, 1, 2) như cv2.findContours trả về – đường viền vật lớn nhất.
                Không tìm thấy -> None.

    Gợi ý các bước
      1. Giấy trắng: độ bão hòa thấp, độ sáng cao. Vật: bão hòa cao HOẶC tối.
         hsv = cv2.cvtColor(anh, cv2.COLOR_BGR2HSV); vat = (S > ngưỡng) | (V < ngưỡng)
         (Ngưỡng nên tính theo màu giấy trong ảnh, ví dụ trung vị V của vùng mặt nạ trừ đi một khoảng.)
      2. Nếu có mat_na: co mặt nạ (cv2.erode) rồi AND với ảnh vật, để không lấy nhầm nền bàn ở mép.
      3. Mở hình thái (cv2.morphologyEx MORPH_OPEN) bỏ nhiễu nhỏ, đóng (MORPH_CLOSE) lấp lỗ.
      4. cv2.findContours (RETR_EXTERNAL), lấy đường viền diện tích lớn nhất.
    Lưu ý: bóng của vật trên giấy hơi tối – đừng để ngưỡng V nuốt luôn bóng (vật sẽ to ra).
    """
    # TODO (Phần D)
    return None


def kich_thuoc_px(contour):
    """
    Đầu vào : contour từ tach_vat
    Đầu ra  : (dai_px, rong_px) với dai_px >= rong_px – hai cạnh của cv2.minAreaRect(contour).
    """
    # TODO (Phần D)
    return None, None
