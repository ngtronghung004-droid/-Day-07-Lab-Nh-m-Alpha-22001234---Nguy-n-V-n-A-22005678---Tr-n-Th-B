# Ghi chú cá nhân — 176 - Bùi Kim Trại

> Ghi chú cá nhân phục vụ theo dõi tiến trình làm lab qua từng pha (từ Pha 1 đến Pha 6).

## 1. Pha 1: ba ca khó tôi tìm ra trong 40 ảnh

| Ảnh | v0 không trả lời được gì | Quyết định ban đầu của tôi |
|---|---|---|
| `img_029.jpg` | Xe máy chở một kiện hàng cồng kềnh khổng lồ cao quá đầu người, che khuất gần hết xe và thân người. v0 không quy định box có bao gồm hàng hóa cồng kềnh không, và người lái bị che khuất gần hết thì gán ra sao. | - Box `motorcycle` vẽ ôm trọn cả khung xe và kiện hàng gắn liền trên xe (vì hàng hóa gắn chặt vào phương tiện khi tham gia giao thông).<br>- Box `person` vẽ ôm phần đầu/tay nhìn thấy của người lái, gán thuộc tính `occluded_level = 3` (bị che $>75\%$). |
| `img_015.jpg` | Ảnh chụp qua kính chắn gió ô tô ướt mưa, đèn hậu xe phía trước bị nhòe và khúc xạ tạo vệt sáng đỏ lóa kéo dài. v0 không hướng dẫn cách xử lý vệt sáng nhòe/motion blur. | - Box `car` chỉ ôm vừa khít kết cấu thân xe thực tế nhìn thấy được, tuyệt đối không kéo dài box để nuốt vệt sáng lóa.<br>- Đặt `occluded_level = 0` (vì không bị vật khác che chắn, chỉ do thời tiết/kính mờ), tick `can_review = true` để nhóm cùng xem lại ranh giới thân xe. |
| `img_017.jpg` / `img_018.jpg` / `img_033.jpg` | Xuất hiện các đối tượng mang hình dáng người nhưng không phải người thật: tượng đài đá/đồng (`img_017`), người in trên biển quảng cáo 2D (`img_018`), ma-nơ-canh trong tủ kính cửa hàng thời trang (`img_033`). v0 chỉ ghi chung chung "person là người", dễ khiến người gán nhầm lẫn tạo box. | - Tuyệt đối **KHÔNG gán** nhãn `person` cho cả 3 trường hợp này.<br>- Chỉ gán `person` cho thực thể người thật đang chuyển động/tồn tại trong không gian 3D thực tế để tránh làm mô hình tự hành nhận diện nhầm (false positive). |

## 2. Pha 2: chỗ tôi bất đồng với nhóm
*(Sẽ điền sau buổi họp thống nhất Pha 2)*
- Chỗ nào bản của tôi khác bản của bạn? Cuối cùng nhóm chốt gì, tôi đồng ý / chưa đồng ý vì sao?

## 3. Pha 3: ảnh tôi đã gán
*(Sẽ điền sau khi hoàn thành gán nhãn Pha 3)*
- Số ảnh được giao: … Số box đã vẽ: … Số lần tôi tick `can_review`: …
- Ca nào tôi lưỡng lự nhất khi gán (ảnh, vì sao)?

## 4. Pha 4–5: tôi lệch ở đâu
*(Sẽ điền sau khi có kết quả đo IAA và buổi họp calibration)*
- Trong `calibration_candidates.csv`, các ca có tên tôi: tôi lệch vì guideline mơ hồ hay vì tôi chưa nắm quy tắc?
- Quyết định calibration nào tôi thấy quan trọng nhất?

## 5. Dùng AI
- Không dùng (tự quan sát 40 ảnh trong `data/images/` và tự viết guideline theo template).

## 6. Bài học
*(Sẽ điền tổng kết sau khi hoàn thành toàn bộ bài lab)*
- Một điều tôi sẽ làm khác khi viết guideline lần sau:
