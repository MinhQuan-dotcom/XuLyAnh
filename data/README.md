# Dữ liệu

| Thư mục | Nội dung | Ở đâu |
|---|---|---|
| `data/mau/` | 20 ảnh mẫu lấy từ bộ tổng hợp, để chạy thử code | Có sẵn trong repo |
| `data/dataset_vat_phang/` | 286 ảnh tổng hợp đầy đủ | Tải từ Google Drive: `<dán link Drive vào đây>` rồi giải nén vào `data/` |
| `data/dataset_that/` | Ảnh tự chụp (từ 09/11) | Google Drive: `<dán link>` |

Ảnh thật phải có **cùng cấu trúc thư mục** (`dev/`, `eval/tang1_nhe_0-15/`, …) và **cùng tên cột** trong `labels.csv` như bộ tổng hợp. Các cột tọa độ góc (`a4_g…`, `vat_g…`) và thông số camera để trống với ảnh thật.

Bộ ảnh tổng hợp được sinh bằng `tools/render_vat_phang.py` (chạy lại ra đúng bộ ảnh):
```
python tools/render_vat_phang.py data/dataset_vat_phang 2026
```
