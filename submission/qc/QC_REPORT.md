# QC_REPORT — Báo cáo hiện trạng (HOLD, chưa nghiệm thu)

## Phạm vi và dữ liệu
- Nhóm Alpha: 5 thành viên, 40 ảnh, 3 người gán độc lập trên mỗi ảnh.
- Nguồn: `consensus_draft.json` và `calibration_candidates.csv` từ `qc_compare.py`, cùng kết quả IAA đã báo trong terminal.
- 360 box trong **bản đồng thuận nháp**, trong đó 312 box có `needs_calibration=true`.

## Kết quả IAA (chưa đạt)
- Mean IoU: **0.852** (ngưỡng **0.85**): đạt.
- Đồng thuận class: **94.6%** (ngưỡng **95%**): không đạt.
- 720 cặp box được ghép để so sánh.
- 929 ca bất thường trên **35/40 ảnh**:
  - Bỏ sót / thừa: **239**
  - IoU thấp: **241**
  - Sai thuộc tính: **402**
  - Sai lớp: **39**
  - Có cờ cần xem: **8**

## Calibration
Nhóm chọn **không chỉnh sửa annotation thêm** ở thời điểm lập báo cáo. Có danh sách ca cần xem và dữ liệu đồng thuận nháp, **chưa có chứng cứ rằng 35 ảnh và 929 ca đã được thảo luận, chốt hoặc sửa đúng guideline**.

`calibration_decisions.csv` đính kèm chỉ là **biểu mẫu chưa điền**, không phải quyết định đã được thông qua. Chưa tạo `labels_calibrated.json` hay `labels_calibrated.csv` vì chưa có bộ nhãn cuối được phê duyệt. Không có thay đổi quy tắc được chứng minh, nên chưa khẳng định có guideline v1.1.

## QC và kết luận
**Chưa có mẫu QC được reviewer chấm thực tế**, nên chưa có tỷ lệ lỗi sau hiệu chỉnh, không được khẳng định đạt điều kiện Release. Hai cảnh báo từ validator cần được ghi nhận: `img_013.jpg` (car, 17px), `img_002.jpg` (van, 16px), ngưỡng tối thiểu 20px.

**Quyết định hiện tại: HOLD** — giữ nguyên dữ liệu đã làm để nộp báo cáo kết quả hiện trạng nếu mentor cho phép, nhưng chưa đạt nghiệm thu đầy đủ theo pipeline của repo.
