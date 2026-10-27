"""
Sinh bo anh tong hop cho de tai: do kich thuoc vat tren to giay A4 khi chup nghieng.

Canh: to giay A4 tren mat ban go sam, mot vat (the nhua, mieng bia, dong xu...) dat tren giay,
chup bang camera lo kim (mo phong camera chinh dien thoai) nghieng goc theta so voi phap tuyen mat ban.

Don vi the gioi: mm. Truc: X sang phai (canh 210 mm), Y ra xa camera (canh 297 mm), Z huong len.
Tam to A4 gan goc toa do.

Chay:  python render_vat_phang.py <thu_muc_ra> [seed] [so_tien_trinh]
Cung seed -> cung bo anh.
"""
import sys, os, csv, math
import numpy as np
import cv2

OUT_W, OUT_H = 1200, 1600          # anh doc nhu dien thoai
SS = 2                             # supersampling
FOV_V_DEG = 69.0
A4W, A4H = 210.0, 297.0

# ------------------------------------------------------------------ danh muc vat
# ten, hinh, dai, rong, day (mm), mau BGR, kieu in tren mat
VAT = {
    # bo phat trien (4 vat)
    'd1_the_thanh_vien': ('chu_nhat', 85.6, 54.0, 0.76, (120, 60, 20), 'the'),
    'd2_mieng_bia_cam': ('chu_nhat', 70.0, 35.0, 1.0, (30, 110, 230), 'tron'),
    'd3_mieng_mica_xanh': ('chu_nhat', 50.0, 50.0, 2.0, (90, 140, 40), 'tron'),
    'd4_dong_xu': ('tron', 25.0, 25.0, 1.8, (60, 120, 150), 'xu'),
    # bo danh gia (12 vat)
    'v01_the_ngan_hang': ('chu_nhat', 85.6, 54.0, 0.76, (40, 40, 45), 'the'),
    'v02_the_xe': ('chu_nhat', 70.0, 45.0, 0.5, (150, 90, 30), 'the'),
    'v03_bia_do_dai': ('chu_nhat', 110.0, 30.0, 1.0, (40, 35, 180), 'tron'),
    'v04_bia_xanhla': ('chu_nhat', 60.0, 40.0, 1.0, (60, 150, 50), 'tron'),
    'v05_bia_tim': ('chu_nhat', 95.0, 65.0, 1.2, (120, 50, 110), 'tron'),
    'v06_giay_mau_vang': ('chu_nhat', 80.0, 20.0, 0.1, (30, 190, 230), 'tron'),
    'v07_giay_mau_xanh': ('chu_nhat', 45.0, 45.0, 0.1, (170, 110, 20), 'tron'),
    'v08_nhan_dan': ('chu_nhat', 64.0, 38.0, 0.2, (50, 80, 200), 'nhan'),
    'v09_mica_den': ('chu_nhat', 100.0, 50.0, 2.0, (30, 30, 30), 'tron'),
    'v10_mica_xanhduong': ('chu_nhat', 75.0, 25.0, 3.0, (160, 70, 20), 'tron'),
    'v11_dong_xu_lon': ('tron', 30.0, 30.0, 2.0, (70, 140, 170), 'xu'),
    'v12_nap_tron': ('tron', 40.0, 40.0, 2.5, (40, 40, 160), 'tron'),
    # bo vat day cho E4: cung mat 60 x 40 mm, khac do day
    'e_day_0.1mm': ('chu_nhat', 60.0, 40.0, 0.1, (40, 120, 200), 'tron'),
    'e_day_1mm': ('chu_nhat', 60.0, 40.0, 1.0, (40, 120, 200), 'tron'),
    'e_day_3mm': ('chu_nhat', 60.0, 40.0, 3.0, (40, 120, 200), 'tron'),
    'e_day_5mm': ('chu_nhat', 60.0, 40.0, 5.0, (40, 120, 200), 'tron'),
    'e_day_10mm': ('chu_nhat', 60.0, 40.0, 10.0, (40, 120, 200), 'tron'),
}
DEV = [k for k in VAT if k.startswith('d')]
EVAL = [k for k in VAT if k.startswith('v')]
DAY = [k for k in VAT if k.startswith('e_')]

# ------------------------------------------------------------------ texture mat ban + giay
TEX_RES = 3.0
TEX_X0, TEX_X1 = -500.0, 500.0
TEX_Y0, TEX_Y1 = -420.0, 900.0


def smooth_noise(h, w, scale, rng):
    small = rng.standard_normal((max(2, int(h / scale)), max(2, int(w / scale)))).astype(np.float32)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)


def make_table(rng):
    h = int((TEX_Y1 - TEX_Y0) * TEX_RES)
    w = int((TEX_X1 - TEX_X0) * TEX_RES)
    base = np.array([(38, 44, 52), (30, 32, 36), (34, 40, 50)][rng.integers(3)], np.float32)
    grain = cv2.resize(rng.standard_normal((h // 6, 40)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    blot = smooth_noise(h, w, 120, rng)
    fine = rng.standard_normal((h, w)).astype(np.float32)
    lum = 1.0 + 0.06 * grain + 0.06 * blot + 0.03 * fine
    return base[None, None, :] * lum[..., None]


def world_to_tex(pts):
    pts = np.asarray(pts, np.float64)
    return np.stack([(pts[:, 0] - TEX_X0) * TEX_RES, (TEX_Y1 - pts[:, 1]) * TEX_RES], 1)


def paper_corners(rot_deg, off):
    a = math.radians(rot_deg)
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    c = np.array([[-A4W / 2, -A4H / 2], [A4W / 2, -A4H / 2], [A4W / 2, A4H / 2], [-A4W / 2, A4H / 2]])
    return c @ R.T + off


def draw_paper(tex, corners, rng):
    h, w = tex.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    cv2.fillPoly(mask, [np.round(world_to_tex(corners) * 16).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=4)
    m = mask.astype(np.float32)[..., None] / 255.0
    white = np.array([226, 230, 232], np.float32) * rng.uniform(0.97, 1.02)
    paper = white[None, None, :] * (1.0 + 0.012 * rng.standard_normal((h, w, 1)).astype(np.float32))
    return tex * (1 - m) + paper * m


def add_shadow(tex, foot, t, light):
    """Bong mem cua vat (nguon sang diem tren tran) + bong tiep xuc o mep vat."""
    h, w = tex.shape[:2]
    top = []
    for x, y in foot:
        s = light[2] / (light[2] - t)
        top.append(light[:2] + s * (np.array([x, y]) - light[:2]))
    pts = np.vstack([foot, np.array(top)])
    hull = cv2.convexHull(np.round(world_to_tex(pts) * 16).astype(np.int32))
    m = np.zeros((h, w), np.float32)
    cv2.fillPoly(m, [hull], 1.0, lineType=cv2.LINE_AA, shift=4)
    m = cv2.GaussianBlur(m, (0, 0), (1.5 + 0.8 * t) * TEX_RES)
    shade = 1.0 - min(0.18 + 0.03 * t, 0.4) * m
    return tex * np.clip(shade, 0.3, 1)[..., None]


# ------------------------------------------------------------------ camera
def make_camera(theta_deg, D, azim_deg, roll_deg, target):
    th, az, ro = map(math.radians, (theta_deg, azim_deg, roll_deg))
    back = np.array([-math.sin(az) * math.sin(th), -math.cos(az) * math.sin(th), math.cos(th)])
    C = target + D * back
    f = -back
    xc = np.array([math.cos(az), -math.sin(az), 0.0])
    yc = np.cross(f, xc)
    xr = math.cos(ro) * xc + math.sin(ro) * yc
    yr = -math.sin(ro) * xc + math.cos(ro) * yc
    R = np.stack([xr, yr, f])
    fy = (OUT_H / 2) / math.tan(math.radians(FOV_V_DEG / 2))
    K = np.array([[fy, 0, OUT_W / 2], [0, fy, OUT_H / 2], [0, 0, 1.0]])
    return R, C, K


def project(R, C, K, pts):
    Xc = (np.asarray(pts, np.float64) - C) @ R.T
    uv = Xc[:, :2] / Xc[:, 2:3]
    return np.stack([K[0, 0] * uv[:, 0] + K[0, 2], K[1, 1] * uv[:, 1] + K[1, 2]], 1), Xc[:, 2]


def raycast_plane(R, C, K, tex):
    H, W = OUT_H * SS, OUT_W * SS
    u = (np.arange(W, dtype=np.float32) + 0.5) / SS
    v = (np.arange(H, dtype=np.float32) + 0.5) / SS
    uu, vv = np.meshgrid(u, v)
    d = np.stack([(uu - K[0, 2]) / K[0, 0], (vv - K[1, 2]) / K[1, 1], np.ones_like(uu)], -1)
    dw = d @ R.astype(np.float32)
    dz = dw[..., 2]
    hit = dz < -1e-6
    t = np.where(hit, -C[2] / np.where(hit, dz, -1), 0)
    X = C[0] + t * dw[..., 0]
    Y = C[1] + t * dw[..., 1]
    mx = ((X - TEX_X0) * TEX_RES).astype(np.float32)
    my = ((TEX_Y1 - Y) * TEX_RES).astype(np.float32)
    img = cv2.remap(tex.astype(np.float32), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    on_table = hit & (Y < TEX_Y1) & (Y > TEX_Y0) & (X > TEX_X0) & (X < TEX_X1)
    img[~on_table] = np.array([150, 165, 175], np.float32)
    return img


# ------------------------------------------------------------------ vat the
def footprint(hinh, L, W, n_arc=6):
    """Duong bien day vat trong he toa do cuc bo (truc dai = x)."""
    if hinh == 'tron':
        r = L / 2
        a = np.linspace(0, 2 * np.pi, 72, endpoint=False)
        return np.stack([r * np.cos(a), r * np.sin(a)], 1)
    r = min(3.0, W / 6)                       # bo goc nhe nhu the nhua
    pts = []
    for (sx, sy, a0) in [(1, 1, 0), (-1, 1, 90), (-1, -1, 180), (1, -1, 270)]:
        ox, oy = sx * (L / 2 - r), sy * (W / 2 - r)
        for k in range(n_arc + 1):
            a = math.radians(a0 + 90 * k / n_arc)
            pts.append((ox + r * math.cos(a), oy + r * math.sin(a)))
    return np.array(pts)


def to_world(local, center, yaw_deg):
    a = math.radians(yaw_deg)
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    return local @ R.T + center


def fill(img, uv, color):
    cv2.fillPoly(img, [np.round(uv * SS * 16).astype(np.int32)], [float(c) for c in color], cv2.LINE_AA, shift=4)


def draw_object(img, R, C, K, key, center, yaw, light, rng):
    hinh, L, W, t, color, kieu = VAT[key]
    foot = to_world(footprint(hinh, L, W), center, yaw)
    n = len(foot)
    bot = np.c_[foot, np.zeros(n)]
    top = np.c_[foot, np.full(n, t)]
    base = np.array(color, np.float64) * rng.uniform(0.93, 1.07)
    # mat ben (chi ve mat huong ve camera)
    if t > 0.15:
        cen = np.r_[center, t / 2]
        sides = []
        for i in range(n):
            j = (i + 1) % n
            mid = (bot[i] + bot[j]) / 2 + np.array([0, 0, t / 2])
            nrm = np.r_[mid[:2] - center, 0.0]
            nrm /= np.linalg.norm(nrm) + 1e-9
            if np.dot(nrm, C - mid) > 0:
                sides.append((np.linalg.norm(C - mid), i, j, nrm))
        for _, i, j, nrm in sorted(sides, reverse=True):
            ld = light - bot[i]; ld /= np.linalg.norm(ld)
            sh = 0.35 + 0.35 * max(0.0, float(np.dot(nrm, ld)))
            uv, _ = project(R, C, K, [bot[i], bot[j], top[j], top[i]])
            fill(img, uv, np.clip(base * sh, 0, 255))
    # mat tren
    sh_top = 0.80 + 0.2 * (light[2] / np.linalg.norm(light - np.r_[center, t]))
    uv, _ = project(R, C, K, top)
    fill(img, uv, np.clip(base * sh_top, 0, 255))
    # hoa tiet in tren mat (khong doi kich thuoc vat)
    def local_poly(poly2):
        w2 = to_world(np.asarray(poly2, np.float64), center, yaw)
        return project(R, C, K, np.c_[w2, np.full(len(w2), t + 0.01)])[0]
    light_col = np.clip(base * sh_top * 1.35 + 25, 0, 255)
    dark_col = np.clip(base * sh_top * 0.6, 0, 255)
    if kieu == 'the':
        fill(img, local_poly([(-L/2+2, W/2-14), (L/2-2, W/2-14), (L/2-2, W/2-22), (-L/2+2, W/2-22)]), dark_col)
        fill(img, local_poly([(-L/2+8, -2), (-L/2+20, -2), (-L/2+20, -11), (-L/2+8, -11)]), (60, 170, 200))
        for k in range(4):
            x0 = -L/2 + 8 + k * 14
            fill(img, local_poly([(x0, -W/2+10), (x0+11, -W/2+10), (x0+11, -W/2+7), (x0, -W/2+7)]), light_col)
    elif kieu == 'nhan':
        fill(img, local_poly([(-L/2+3, W/2-3), (L/2-3, W/2-3), (L/2-3, -W/2+3), (-L/2+3, -W/2+3)]), light_col)
        for k in range(3):
            y0 = W/2 - 10 - k * 8
            fill(img, local_poly([(-L/2+7, y0), (L/2-12, y0), (L/2-12, y0-3), (-L/2+7, y0-3)]), dark_col)
    elif kieu == 'xu':
        a = np.linspace(0, 2 * np.pi, 48, endpoint=False)
        ring = np.stack([(L/2-2.5) * np.cos(a), (L/2-2.5) * np.sin(a)], 1)
        fill(img, local_poly(ring), np.clip(base * sh_top * 1.15, 0, 255))
        inner = np.stack([(L/2-4.5) * np.cos(a), (L/2-4.5) * np.sin(a)], 1)
        fill(img, local_poly(inner), np.clip(base * sh_top * 0.95, 0, 255))
    return foot


# ------------------------------------------------------------------ hieu ung camera
def camera_effects(img, rng):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r2 = ((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2
    vign = 1.0 - 0.18 * r2 / 2
    grad = 1.0 + rng.uniform(-0.06, 0.06) * (yy / h - 0.5) + rng.uniform(-0.05, 0.05) * (xx / w - 0.5)
    img = img * (vign * grad)[..., None]
    wb = np.array([rng.uniform(0.95, 1.04), 1.0, rng.uniform(0.96, 1.05)], np.float32)
    img = img * wb * rng.uniform(0.94, 1.05)
    img = cv2.GaussianBlur(img, (0, 0), rng.uniform(0.45, 0.85))
    img = img + rng.normal(0, rng.uniform(1.2, 2.8), img.shape).astype(np.float32)
    return np.clip(img, 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ 1 anh
def render_one(key, theta, yaw, vi_tri, rng):
    hinh, L, W, t = VAT[key][:4]
    paper_rot = rng.uniform(-4, 4)
    paper_off = rng.uniform(-8, 8, 2)
    corners = paper_corners(paper_rot, paper_off)
    a = math.radians(paper_rot)
    ey = np.array([-math.sin(a), math.cos(a)])          # huong canh dai to giay
    lech = A4H / 2 - max(L, W) / 2 - 8.0                  # vat nam tron tren giay, cach mep 8 mm
    dy = {'giua': rng.uniform(-15, 15), 'gan': -lech, 'xa': lech}[vi_tri]
    center = paper_off + dy * ey + rng.uniform(-12, 12) * np.array([math.cos(a), math.sin(a)])
    light = np.array([rng.uniform(-300, 300), rng.uniform(-200, 300), rng.uniform(1500, 2000)])
    azim, roll = rng.uniform(-4, 4), rng.uniform(-3, 3)
    target = np.array([paper_off[0], paper_off[1] + rng.uniform(-10, 10), 0.0])
    D = rng.uniform(330, 380)
    foot_l = to_world(footprint(hinh, L, W), center, yaw)
    pts3 = np.vstack([np.c_[corners, np.zeros(4)], np.c_[foot_l, np.full(len(foot_l), t)]])
    for _ in range(80):
        R, C, K = make_camera(theta, D, azim, roll, target)
        uv, z = project(R, C, K, pts3)
        mx, my = 0.03 * OUT_W, 0.03 * OUT_H
        if (z > 0).all() and (uv[:, 0] > mx).all() and (uv[:, 0] < OUT_W - mx).all() \
                and (uv[:, 1] > my).all() and (uv[:, 1] < OUT_H - my).all():
            break
        D += 15
    tex = make_table(rng)
    tex = draw_paper(tex, corners, rng)
    tex = add_shadow(tex, foot_l, t, light)
    img = raycast_plane(R, C, K, tex)
    draw_object(img, R, C, K, key, center, yaw, light, rng)
    img = cv2.resize(img, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)
    img = camera_effects(img, rng)
    # 4 goc hinh chu nhat bao day vat (truc dai, truc rong) -> nhan tham chieu
    rect = to_world(np.array([[-L/2, -W/2], [L/2, -W/2], [L/2, W/2], [-L/2, W/2]]), center, yaw)
    meta = dict(D=D, azim=azim, roll=roll, paper_rot=paper_rot, center=center, K=K,
                a4_uv=project(R, C, K, np.c_[corners, np.zeros(4)])[0],
                vat_uv=project(R, C, K, np.c_[rect, np.zeros(4)])[0])
    return img, meta


# ------------------------------------------------------------------ ke hoach
def plan():
    jobs = []
    def add(folder, tier, keys, angles, huongs=('doc', 'ngang'), vi_tri='giua'):
        for a in angles:
            for key in keys:
                for h in huongs:
                    jobs.append((folder, tier, key, a, h, vi_tri))
    add('dev', 'dev', DEV, [0, 10, 25, 35, 45, 55])
    add('eval/tang1_nhe_0-15', 'nhe', EVAL, [5, 12])
    add('eval/tang2_trungbinh_15-35', 'trung_binh', EVAL, [22, 30])
    add('eval/tang3_nang_35-55', 'nang', EVAL, [40, 50])
    add('e4_cucnang_55-75', 'cuc_nang', EVAL, [60, 70])
    add('e4_vat_day', 'vat_day', DAY, [0, 15, 30, 45])
    for vt in ('gan', 'xa'):
        add('minh_hoa_vi_tri', 'minh_hoa', ['v01_the_ngan_hang', 'v03_bia_do_dai', 'v05_bia_tim'], [40],
            huongs=('doc',), vi_tri=vt)
    return jobs


def run_job(args):
    out, idx, seed, (folder, tier, key, a, huong, vi_tri) = args
    rng = np.random.default_rng(seed)
    theta = a + rng.uniform(-1.0, 1.0)
    yaw = (90.0 if huong == 'doc' else 0.0) + rng.uniform(-5, 5)   # 'doc': canh dai song song huong nghieng
    img, m = render_one(key, theta, yaw, vi_tri, rng)
    os.makedirs(os.path.join(out, folder), exist_ok=True)
    name = f"{key}_t{a:02d}_{huong}" + ('' if vi_tri == 'giua' else f"_{vi_tri}") + ".jpg"
    cv2.imwrite(os.path.join(out, folder, name), img, [cv2.IMWRITE_JPEG_QUALITY, int(rng.integers(88, 94))])
    hinh, L, W, t = VAT[key][:4]
    row = {'file': f"{folder}/{name}", 'bo': folder.split('/')[0], 'tang': tier, 'vat': key, 'hinh': hinh,
           'dai_mm': L, 'rong_mm': W, 'day_mm': t, 'theta_deg': round(theta, 2), 'huong': huong,
           'vi_tri': vi_tri, 'yaw_vat_deg': round(yaw, 2), 'khoang_cach_mm': round(m['D'], 1),
           'azim_deg': round(m['azim'], 2), 'roll_deg': round(m['roll'], 2),
           'xoay_giay_deg': round(m['paper_rot'], 2), 'fx': round(m['K'][0, 0], 2),
           'fy': round(m['K'][1, 1], 2), 'cx': m['K'][0, 2], 'cy': m['K'][1, 2]}
    for i in range(4):
        row[f'a4_g{i+1}_u'] = round(m['a4_uv'][i, 0], 2); row[f'a4_g{i+1}_v'] = round(m['a4_uv'][i, 1], 2)
    for i in range(4):
        row[f'vat_g{i+1}_u'] = round(m['vat_uv'][i, 0], 2); row[f'vat_g{i+1}_v'] = round(m['vat_uv'][i, 1], 2)
    return idx, row


def main():
    out = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 2026
    nproc = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    jobs = plan()
    seeds = np.random.default_rng(seed).integers(1 << 31, size=len(jobs))
    args = [(out, i, int(seeds[i]), j) for i, j in enumerate(jobs)]
    rows = [None] * len(jobs)
    if nproc > 1:
        from multiprocessing import Pool
        with Pool(nproc) as p:
            for k, (i, r) in enumerate(p.imap_unordered(run_job, args)):
                rows[i] = r
                if k % 25 == 0: print(k, len(jobs), flush=True)
    else:
        for k, a in enumerate(args):
            i, r = run_job(a); rows[i] = r
            if k % 25 == 0: print(k, len(jobs), flush=True)
    with open(os.path.join(out, 'labels.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    with open(os.path.join(out, 'danh_muc_vat.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['vat', 'bo', 'hinh', 'dai_mm', 'rong_mm', 'day_mm'])
        for k, v in VAT.items():
            bo = 'dev' if k in DEV else ('eval' if k in EVAL else 'e4_vat_day')
            w.writerow([k, bo, v[0], v[1], v[2], v[3]])


if __name__ == '__main__':
    main()
