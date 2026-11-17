# Phần B: chỉnh lại 4 góc tờ giấy cho chính xác hơn
# Người làm: Quân
# Kiểm tra: python tests/kiem_tra_B.py
#
# Ý tưởng: góc lấy từ approxPolyDP hay lệch vài pixel vì góc giấy bị mờ / bo tròn.
# Mỗi cạnh giấy có rất nhiều điểm biên, khớp một đường thẳng qua các điểm đó rồi lấy
# giao điểm 2 cạnh kề nhau làm góc mới thì sẽ ổn định hơn.

import numpy as np
import cv2


def giao_diem(duong1, duong2):
    # Giao điểm 2 đường thẳng dạng (vx, vy, x0, y0) như cv2.fitLine trả về.
    # Hai đường song song thì trả None.
    vx1, vy1, x1, y1 = [float(v) for v in np.ravel(duong1)]
    vx2, vy2, x2, y2 = [float(v) for v in np.ravel(duong2)]
    A = np.array([[vx1, -vx2], [vy1, -vy2]])
    if abs(np.linalg.det(A)) < 1e-9:
        return None
    t = np.linalg.solve(A, np.array([x2 - x1, y2 - y1]))
    return np.array([x1 + t[0] * vx1, y1 + t[0] * vy1])


def lay_diem_bien(anh, tham_so):
    # Chạy Canny, trả về toạ độ (x, y) của tất cả điểm biên, dạng mảng (N, 2)
    if anh.ndim == 3:
        xam = cv2.cvtColor(anh, cv2.COLOR_BGR2GRAY)
    else:
        xam = anh
    bien = cv2.Canny(xam, tham_so['canny_thap'], tham_so['canny_cao'])
    ys, xs = np.nonzero(bien)
    return np.stack([xs, ys], axis=1).astype(np.float64)


def diem_gan_canh(diem, a, b, tham_so):
    # Lọc các điểm biên nằm sát đoạn thẳng a -> b (cạnh thô của tờ giấy).
    # d: khoảng cách vuông góc tới đường a-b
    # t: vị trí chiếu lên đoạn, 0 là ở a, 1 là ở b
    ab = b - a
    dai = np.linalg.norm(ab)
    if dai < 1e-6:
        return np.empty((0, 2))
    u = ab / dai                       # vector đơn vị theo cạnh
    n = np.array([-u[1], u[0]])        # vector pháp tuyến
    t = (diem - a) @ u / dai
    d = np.abs((diem - a) @ n)
    bo = tham_so['bo_dau_canh']        # bỏ 2 đầu cạnh vì ở gần góc biên bị cong
    chon = (d <= tham_so['do_rong_dai_canh']) & (t >= bo) & (t <= 1 - bo)
    return diem[chon]


def tinh_chinh_goc(anh, goc_tho, tham_so):
    """
    anh: ảnh BGR
    goc_tho: mảng (4, 2), thứ tự trên-trái, trên-phải, dưới-phải, dưới-trái
    tham_so: dùng 'canny_thap', 'canny_cao', 'do_rong_dai_canh', 'bo_dau_canh'
    Trả về mảng (4, 2) cùng thứ tự. Cạnh nào không đủ điểm thì trả lại goc_tho.
    """
    goc_tho = np.asarray(goc_tho, dtype=np.float64).reshape(4, 2)
    diem = lay_diem_bien(anh, tham_so)
    if len(diem) == 0:
        return goc_tho

    # khớp đường thẳng cho từng cạnh i: goc_tho[i] -> goc_tho[i+1]
    duong = []
    for i in range(4):
        a, b = goc_tho[i], goc_tho[(i + 1) % 4]
        gan = diem_gan_canh(diem, a, b, tham_so)
        if len(gan) < 10:              # quá ít điểm thì không tin được
            return goc_tho
        # DIST_HUBER: giống bình phương tối thiểu nhưng ít bị kéo lệch bởi điểm nhiễu
        duong.append(cv2.fitLine(gan.astype(np.float32), cv2.DIST_HUBER, 0, 0.01, 0.01))

    # góc i là giao của cạnh (i-1) và cạnh i
    goc_moi = []
    for i in range(4):
        p = giao_diem(duong[i - 1], duong[i])
        if p is None:
            return goc_tho
        goc_moi.append(p)
    goc_moi = np.array(goc_moi)

    # nếu góc mới chạy quá xa góc thô thì coi như khớp sai, giữ góc thô
    lech = np.linalg.norm(goc_moi - goc_tho, axis=1)
    if np.any(lech > 3 * tham_so['do_rong_dai_canh']):
        return goc_tho
    return goc_moi