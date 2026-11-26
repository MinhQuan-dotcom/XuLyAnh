import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

TEN_THAM_SO = {
    "canny_cao": ("Ngưỡng Canny cao", "Giá trị canny_cao"),
    "do_rong_dai_canh": ("Độ rộng vùng lấy điểm biên", "Giá trị do_rong_dai_canh"),
    "do_phan_giai_nan": ("Độ phân giải ảnh nắn", "Giá trị do_phan_giai_nan"),
    "kich_thuoc_lam_mo": ("Kích thước làm mờ (tìm giấy)", "Giá trị kich_thuoc_lam_mo"),
    "nguong_s": ("Ngưỡng bão hòa S (tách vật)", "Giá trị nguong_s"),
    "he_so_v": ("Hệ số độ sáng V (tách vật)", "Giá trị he_so_v"),
}

def main():
    parser = argparse.ArgumentParser(
        description="Vẽ 3 biểu đồ E2 từ tong_hop_e2.csv"
    )
    parser.add_argument(
        "--csv",
        default="results/e2/tong_hop_e2.csv",
        help="Đường dẫn tới CSV kết quả E2",
    )
    parser.add_argument(
        "--ra",
        default="results/e2/bieu_do",
        help="Thư mục lưu biểu đồ",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    output_dir = Path(args.ra)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy {csv_path}. Hãy chạy E2 trước hoặc kiểm tra lại --csv."
        )

    df = pd.read_csv(csv_path)
    required = {
        "tham_so", "gia_tri", "mae_dai_mm", "mae_rong_mm"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV thiếu các cột: {', '.join(sorted(missing))}")

    output_dir.mkdir(parents=True, exist_ok=True)

    for key, (title, xlabel) in TEN_THAM_SO.items():
        part = df[df["tham_so"] == key].copy()
        if part.empty:
            print(f"Bỏ qua {key}: không có dữ liệu trong CSV.")
            continue

        part["gia_tri"] = pd.to_numeric(part["gia_tri"])
        part = part.sort_values("gia_tri")

        plt.figure(figsize=(8, 5))
        plt.plot(
            part["gia_tri"], part["mae_dai_mm"],
            marker="o", linewidth=2, label="MAE chiều dài"
        )
        plt.plot(
            part["gia_tri"], part["mae_rong_mm"],
            marker="s", linewidth=2, label="MAE chiều rộng"
        )
        plt.title(f"{title} – E2")
        plt.xlabel(xlabel)
        plt.ylabel("MAE (mm)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()

        output_file = output_dir / f"bieu_do_{key}.png"
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Đã lưu: {output_file}")

if __name__ == "__main__":
    main()
