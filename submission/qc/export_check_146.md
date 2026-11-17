# Kiểm tra bản xuất COCO — mã 146

- Ngày kiểm tra: 17/11/2026.
- Nguồn: `Day07_146.zip`, mục `annotations/instances_default.json`.
- File lưu: `submission/labels/146.json`; giữ nguyên toàn bộ byte của JSON trong ZIP.
- SHA-256 JSON: `d44829d43f91ae466d608d3af4dd7ca4e371ecd905f3124f64fb8bf12c654130`.
- Ảnh: 24/24 theo phân công; không thiếu, không thừa.
- Tổng box: 189, gồm 179 box đối tượng và 10 vùng bỏ qua.
- `can_review=true`: 0; đây là số đếm từ bản xuất, không xác nhận rằng không có ca mơ hồ.
- Ảnh không có annotation: 4: img_017.jpg, img_020.jpg, img_024.jpg, img_027.jpg
- Kết quả kiểm kỹ thuật: 0 lỗi, 0 cảnh báo.

## Số box theo lớp

| Lớp | Số box |
|---|---:|
| bicycle | 11 |
| bus | 5 |
| car | 31 |
| ignore_region | 10 |
| motorcycle | 23 |
| person | 99 |
| three_wheeler | 6 |
| truck | 3 |
| van | 1 |

## Cách kiểm và giới hạn

Dùng hàm validate của scripts/validate_labels.py với taxonomy hiện có. Trong tiến trình kiểm tra, áp dụng mẫu tên ba chữ số và đối chiếu mã 146 với 2A202603146 trong bảng phân công. Mã của cả năm thành viên được ánh xạ bằng ba chữ số cuối và đã kiểm không trùng. Không sửa script, bảng phân công hay nội dung nhãn.

Script CLI tại máy vẫn là phiên bản cũ, yêu cầu tên <MSHV>_<HoTen>.json và không chấp nhận 146.json. Vì vậy kết quả trên là kiểm tra bằng hàm với lớp tương thích trong bộ nhớ, không phải xác nhận lệnh CLI nguyên bản đã chạy thành công. Cần thống nhất phiên bản công cụ và định dạng mã trước khi chạy IAA toàn nhóm.

Kiểm thêm tính duy nhất của ID ảnh/annotation và liên kết image_id/category_id. Chưa kiểm trực quan độ sát box, tính đúng của lớp hoặc vật bị bỏ sót. Không tự sửa box hoặc ghi nhận quyết định QC của người review.

## Lỗi

Không có.

## Cảnh báo

Không có.

## Việc tiếp theo

- Chờ nhãn độc lập của các mã: `031.json`, `147.json`, `176.json`, `233.json`.
- Khi đủ đầu vào và thống nhất phiên bản công cụ: kiểm toàn nhóm, đo IAA, họp calibration, sửa nhãn, duyệt QC và lập báo cáo.
- Chưa tính IAA; chưa có calibration hoặc quyết định Release/Hold/Rework được reviewer xác nhận.
