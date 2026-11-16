# Nhóm Alpha — Pha 2: Bộ tài liệu Guideline v1.0 hoàn thiện

**Ngày cập nhật:** 2026-11-16  
**Trạng thái:** 10/10 quyết định Pha 2 đã được nhóm Alpha xác nhận.

## 1. Phạm vi quyết định

Bộ tài liệu phản ánh 10 quyết định nhóm:

1. Xe chở xe: gán riêng xe chuyên chở và từng ô tô được chở khi đủ điều kiện.
2. Ngưỡng vật nhỏ: giữ `min_box_height_px = 20`, đo chiều cao box trên ảnh gốc.
3. `occluded_level`: áp dụng dải phần trăm theo guideline 031.
4. Bổ sung `bus`, `three_wheeler`, `bicycle`; không thêm `other_vehicle`.
5. Box phương tiện không bao gồm hàng hóa nhô ra ngoài.
6. Mọi pickup, kể cả có nắp thùng/canopy, thuộc `truck`.
7. Không gán người chỉ nhìn thấy qua kính cabin kín; ngoại lệ khi người thò đầu/thân ra ngoài và nhìn rõ.
8. Không gán bộ phận của chính Ego Vehicle mang camera.
9. `ignore_region` chỉ bao cụm nhiều đối tượng thật không thể tách; đối tượng rõ vẫn phải gán riêng.
10. Xe máy gắn sidecar thuộc `motorcycle`, một box bao cả xe máy và sidecar.

## 2. Danh sách file

- `guideline_v1.0_agreed.md`: Guideline nhóm chính thức, gồm taxonomy, quy tắc, ca khó và checklist QC.
- `guideline_comparison.md`: Đối chiếu 5 guideline cá nhân và quyết định nhóm.
- `decision_log.md`: Nhật ký 10 quyết định D-01 đến D-10.
- `taxonomy_v1.0.json`: Taxonomy v1.0 đã đồng bộ định nghĩa class.
- `taxonomy_v0_reference.json`: Bản taxonomy gốc v0 để đối chiếu.

## 3. Trạng thái và lưu ý triển khai

- 5 quyết định bổ sung D-06 đến D-10 được nhóm Alpha xác nhận đồng ý toàn bộ ngày 2026-11-16; không có ý kiến sửa đổi.
- Không còn mục mở trong danh sách 5 vấn đề được đưa ra xác nhận lần này.
- Các thuộc tính `occluded_level`, `truncated`, `can_review` và các ngưỡng QC/IAA được giữ nguyên; đặc biệt `min_box_height_px = 20`.
- Trước khi annotation, dùng `taxonomy_v1.0.json` để đồng bộ danh sách nhãn CVAT và kiểm tra đúng tên class. Không tự ý thay đổi schema hoặc thêm class.
- Tình huống mới ngoài quy tắc đã chốt phải được ghi nhận và chuyển reviewer; không tự suy diễn thành quyết định nhóm.
