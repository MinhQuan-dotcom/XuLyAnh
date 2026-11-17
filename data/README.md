# Dữ liệu

- `data/mau/`: 25 ảnh mẫu lấy từ bộ tổng hợp, có sẵn trong repo, dùng để chạy thử.
- `data/dataset_vat_phang/`: bộ tổng hợp đầy đủ 286 ảnh. Tải ở đây:
  https://drive.google.com/file/d/1pOIU3mLZHTwnr4KlKRzSgF9a8CKbkRxD/view?usp=sharing
  rồi giải nén vào thư mục `data/` (sau khi giải nén phải có `data/dataset_vat_phang/labels.csv`).
- `data/dataset_that/`: ảnh nhóm tự chụp, sẽ bổ sung sau.

Có thể tải bằng lệnh thay vì tải tay:

```
pip install gdown
gdown 1pOIU3mLZHTwnr4KlKRzSgF9a8CKbkRxD -O data/dataset_vat_phang.zip
```

Ảnh và file zip trong `data/` không đưa lên GitHub (đã có trong .gitignore), trừ `data/mau`.

## Lưu ý về ảnh tự chụp

Ảnh thật xếp thư mục giống bộ tổng hợp (`dev/`, `eval/tang1_nhe_0-15/`, ...) và file `labels.csv`
dùng cùng tên cột. Các cột tọa độ góc (`a4_g...`, `vat_g...`) và thông số camera thì để trống.

Bộ tổng hợp được tạo bằng `tools/render_vat_phang.py`, chạy lại với seed 2026 sẽ ra đúng bộ ảnh này:

```
python tools/render_vat_phang.py data/dataset_vat_phang 2026
```
