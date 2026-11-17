# Dữ liệu

- `data/mau/`: 25 ảnh mẫu lấy từ bộ tổng hợp, có sẵn trong repo, dùng để chạy thử.
- `data/dataset_vat_phang/`: bộ tổng hợp đầy đủ 286 ảnh. Tải ở đây:
  https://drive.google.com/file/d/1QYRKUxnb0PcF7RHkw_yJgH5MzCJtojsO/view?usp=sharing
  rồi giải nén vào thư mục `data/` (sau khi giải nén phải có `data/dataset_vat_phang/labels.csv`).
- `data/dataset_that/`: 48 ảnh nhóm tự chụp (iPhone 14, ngày 06/11/2026), đã đổi tên, có `labels.csv`. Tải ở đây:
  https://drive.google.com/file/d/1yZcRoDBUvKD8GD8LYIl8-KJgZhs0yW5S/view?usp=sharing
  rồi giải nén vào `data/` (sau khi giải nén phải có `data/dataset_that/labels.csv`).

Có thể tải bằng lệnh thay vì tải tay:

```
pip install gdown
gdown 1QYRKUxnb0PcF7RHkw_yJgH5MzCJtojsO -O data/dataset_vat_phang.zip
gdown 1yZcRoDBUvKD8GD8LYIl8-KJgZhs0yW5S -O data/dataset_that.zip
python -c "import zipfile; zipfile.ZipFile('data/dataset_vat_phang.zip').extractall('data')"
python -c "import zipfile; zipfile.ZipFile('data/dataset_that.zip').extractall('data')"
```

Giải nén xong kiểm tra: `ls data/dataset_vat_phang data/dataset_that` phải thấy `labels.csv` trong cả hai.
Nếu file zip của ảnh thật khi giải nén ra thư mục có tên khác (ví dụ lồng thêm một cấp), đổi lại cho
đúng thành `data/dataset_that/`.

Ảnh và file zip trong `data/` không đưa lên GitHub (đã có trong .gitignore), trừ `data/mau`.

## Lưu ý về ảnh tự chụp

Ảnh thật xếp thư mục giống bộ tổng hợp (`dev/`, `eval/tang1_nhe_0-15/`, ...) và file `labels.csv`
dùng cùng tên cột. Các cột tọa độ góc (`a4_g...`, `vat_g...`) và thông số camera thì để trống.

Bộ tổng hợp được tạo bằng `tools/render_vat_phang.py`, chạy lại với seed 2026 sẽ ra đúng bộ ảnh này:

```
python tools/render_vat_phang.py data/dataset_vat_phang 2026
```
