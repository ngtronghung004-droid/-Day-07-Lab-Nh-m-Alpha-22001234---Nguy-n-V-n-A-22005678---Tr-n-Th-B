# Nhóm Alpha — Nhật ký quyết định Pha 2

- **Phiên bản:** 1.1
- **Ngày cập nhật:** 2026-11-16
- **Căn cứ:** 5 quyết định Pha 2 ban đầu và 5 quyết định bổ sung do
  nhóm Alpha xác nhận ngày 2026-11-16.
- **Trạng thái:** Đã chốt 10/10 quyết định đang theo dõi; 5 quyết định
  bổ sung được nhóm đồng ý toàn bộ, không có ý kiến sửa đổi.

## 1. Các quyết định đã chốt

| ID   | Nội dung                            | Quyết định cuối cùng của nhóm                                                                                                                                                            | Tác động                                              | Trạng thái  |
|------|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|-------------|
| D-01 | Xe chở xe — `img_002`               | Gán riêng từng ô tô được chở nếu nhìn thấy, nhận diện được và đạt ngưỡng kích thước. Xe chuyên chở có box `truck`; mỗi ô tô được chở có box `car` riêng.                                 | Guideline R-05; ca khó `img_002`.                     | **ĐÃ CHỐT** |
| D-02 | Ngưỡng kích thước tối thiểu         | Giữ `min_box_height_px = 20` theo taxonomy. Dùng chiều cao box trên ảnh gốc; không dùng cạnh dài 40 px.                                                                                  | Giữ nguyên `rules.min_box_height_px`; Guideline R-04. | **ĐÃ CHỐT** |
| D-03 | Ngưỡng `occluded_level`             | Dùng dải của 031, tính theo tỷ lệ phần đối tượng bị vật khác che: `0` = 0–20%; `1` = trên 20–50%; `2` = trên 50–80%; `3` = trên 80% nhưng dưới 100%, nếu phần còn thấy vẫn đủ nhận diện. | Guideline mục 3.1; giữ nguyên select `0`–`3`.         | **ĐÃ CHỐT** |
| D-04 | Bổ sung class phương tiện           | Thêm `bus`, `three_wheeler`, `bicycle`. Không thêm `other_vehicle`.                                                                                                                      | `taxonomy_v1.0.json`; Guideline mục 2.                | **ĐÃ CHỐT** |
| D-05 | Xe chở hàng cồng kềnh / hàng nhô ra | Box phương tiện chỉ bao thân/cấu trúc của phương tiện; không bao phần hàng hóa nhô ra ngoài.                                                                                             | Guideline R-06; ca khó `img_029`.                     | **ĐÃ CHỐT** |
| D-06 | Pickup có canopy/nắp thùng | Mọi xe bán tải pickup thuộc `truck`, bất kể thùng hở, có nắp đậy hay canopy. | Guideline R-13; taxonomy `truck`. | **ĐÃ CHỐT** |
| D-07 | Người trong cabin kín | Không gán `person` khi người chỉ nhìn thấy qua kính cabin kín; ngoại lệ khi người thò đầu/thân ra ngoài và nhìn rõ, đạt ngưỡng. | Guideline R-14; định nghĩa `person`. | **ĐÃ CHỐT** |
| D-08 | Ego Vehicle mang camera | Không gán các bộ phận của chính phương tiện mang camera; phương tiện khác trong cảnh vẫn gán bình thường. | Guideline R-15; xử lý ảnh chụp từ trong xe. | **ĐÃ CHỐT** |
| D-09 | Quy tắc `ignore_region` | Chỉ bao cụm nhiều đối tượng thật không thể tách; đối tượng rõ, tách được và đạt ngưỡng vẫn phải gán riêng, kể cả khi box chồng lên vùng ignore. | Guideline R-10; định nghĩa `ignore_region`. | **ĐÃ CHỐT** |
| D-10 | Xe máy gắn sidecar | Gán một box `motorcycle` bao cả xe máy và sidecar; người lái/hành khách là `person` riêng nếu đủ điều kiện. | Guideline R-16; taxonomy `motorcycle`; `img_022`. | **ĐÃ CHỐT** |

## 2. Quy ước triển khai

### D-01 — Xe chở xe

- Xe đầu kéo/xe chuyên chở: một box `truck`.
- Từng ô tô được chở: một box `car` riêng khi nhìn thấy và nhận diện
  được, đồng thời đạt chiều cao box tối thiểu 20 px.
- Nếu ô tô được chở bị che, vẫn gán nếu nhận diện được và đạt ngưỡng;
  đánh dấu `occluded_level` riêng.
- Không coi toàn bộ xe được chở là hàng hóa để bỏ nhãn.

### D-02 — Ngưỡng 20 px

- Đo **chiều cao Bounding Box** trên ảnh gốc, không dựa vào mức zoom
  CVAT.
- Chiều cao từ 20 px trở lên: đủ điều kiện xét gán box riêng nếu class
  nhận diện được.
- Chiều cao dưới 20 px: không gán instance riêng theo ngưỡng hiện tại;
  xử lý vùng nhỏ/dày theo quy tắc `ignore_region` và QC.
- Không thay ngưỡng này bằng cạnh dài 40 px.

### D-03 — Occlusion

| `occluded_level` | Tỷ lệ bị che bởi vật khác | Cách xử lý                                           |
|------------------|--------------------------:|------------------------------------------------------|
| `0`              |                     0–20% | Không hoặc chỉ bị che rất ít                         |
| `1`              |               Trên 20–50% | Bị che một phần; vẫn gán nếu nhận diện được          |
| `2`              |               Trên 50–80% | Bị che nhiều; vẫn gán nếu nhận diện được             |
| `3`              |  Trên 80% nhưng dưới 100% | Chỉ gán khi phần còn thấy vẫn đủ nhận diện chắc chắn |

- Các khoảng không chồng lấn; 20%, 50%, 80% thuộc mức kết thúc tại mốc
  đó.
- Không tính phần bị khung ảnh cắt vào tỷ lệ occlusion.
- Nếu bị che hoàn toàn hoặc không đủ căn cứ nhận diện class, không đoán
  nhãn; ghi `can_review`/vấn đề cấp ảnh.

### D-04 — Class bổ sung

- `bus`: xe buýt/xe khách.
- `three_wheeler`: phương tiện ba bánh có động cơ như tuk-tuk,
  auto-rickshaw.
- `bicycle`: xe đạp và phương tiện ba bánh chạy bằng sức người như xích
  lô đạp.
- Không tạo class `other_vehicle`.
- Sidecar gắn liền với xe máy thuộc `motorcycle`; một box bao cả xe và
  sidecar theo D-10.

### D-05 — Hàng hóa nhô ra

- Box phương tiện chỉ bao phần thân/cấu trúc của chính phương tiện.
- Không kéo box theo ống, thanh dài, bó hàng hoặc kiện hàng nhô ra ngoài
  thân xe.
- Nếu hàng hóa che một phần xe hoặc người, đánh giá occlusion cho đối
  tượng bị che; không đưa hàng vào box phương tiện.
- Người lái/người vận chuyển là instance `person` riêng nếu nhìn thấy và
  đủ điều kiện gán.

## 3. Quy ước triển khai bổ sung cho D-06 đến D-10

### D-06 — Pickup có canopy/nắp thùng

- Mọi pickup thuộc `truck`, dù thùng hở, có nắp đậy hoặc gắn canopy.
- Canopy không làm thay đổi class; không chuyển pickup thành `car`/`van`
  chỉ vì khoang hàng được che.
- Nếu không đủ căn cứ nhận diện pickup, đánh dấu `can_review`.

### D-07 — Người trong cabin kín

- Không gán `person` khi người chỉ nhìn thấy qua kính cabin kín của ô tô,
  pickup, truck, van hoặc bus.
- Nếu người thò đầu/thân ra ngoài và phần nhìn thấy đủ rõ, đạt ngưỡng,
  gán một box `person` riêng quanh phần cơ thể nhìn thấy.
- Người trên phương tiện khoang hở vẫn được gán riêng nếu đủ điều kiện.

### D-08 — Ego Vehicle

- Không gán nắp capo, cần gạt nước, gương, bảng điều khiển, nội thất và
  các bộ phận khác của chính phương tiện mang camera.
- Không gán hình ảnh phương tiện chỉ xuất hiện trong gương thành
  instance mới vì đó là phản chiếu.
- Các phương tiện giao thông khác trong cảnh vẫn gán theo taxonomy.

### D-09 — `ignore_region`

- Chỉ dùng cho cụm nhiều đối tượng thật thuộc taxonomy quá nhỏ, quá dày,
  chồng lấn hoặc dính nhau đến mức không thể tách và gán đầy đủ.
- Đối tượng rõ, tách được và có chiều cao box từ 20 px trở lên vẫn phải
  có box instance riêng, kể cả khi box chồng lên vùng ignore.
- Không tạo `ignore_region` cho một đối tượng riêng lẻ chỉ vì nó nhỏ;
  không dùng cho vật giả hoặc vật ngoài taxonomy.

### D-10 — Sidecar

- Xe máy và sidecar gắn liền: một box `motorcycle` bao toàn bộ cụm.
- Không tạo box riêng cho sidecar và không xếp thành `three_wheeler`.
- Người lái/hành khách trong sidecar là box `person` riêng nếu nhìn rõ
  và đạt ngưỡng.

## 4. Thông tin buổi họp và phê duyệt

- Thời gian họp: Chưa được cung cấp.
- Người tham dự: Chưa được cung cấp.
- Người điều phối: Chưa được cung cấp.
- Người phê duyệt cuối cùng: Chưa được cung cấp.
- Căn cứ cập nhật: Nhóm Alpha xác nhận đồng ý cả 5 quyết định bổ sung
  D-06 đến D-10 trong trao đổi ngày 2026-11-16; ý kiến sửa đổi: không có.
- Phạm vi xác nhận: 5/5 quyết định bổ sung được chấp thuận. Đây là căn
  cứ nội dung để cập nhật tài liệu; không suy diễn thành biên bản họp có
  chữ ký hoặc danh sách người tham dự.

> Không tự điền tên người biểu quyết, chữ ký hoặc thời gian họp khi nhóm
> chưa cung cấp.
