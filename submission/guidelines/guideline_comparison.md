# Nhóm Alpha — Bảng đối chiếu Guideline cá nhân và kết quả Pha 2

- **Nhóm:** Alpha
- **Thành viên có tài liệu:** 031, 146, 147, 176, 233
- **Nguồn:** 5 guideline cá nhân và `taxonomy.json` v0 do nhóm cung cấp.
- **Phiên bản đối chiếu:** 1.1
- **Ngày cập nhật:** 2026-11-16
- **Trạng thái:** Đã đối chiếu 5 guideline cá nhân và cập nhật đủ 10
  quyết định Pha 2; 5 vấn đề bổ sung đã được nhóm Alpha xác nhận.

> **Lưu ý về thành viên 146:** Guideline 146 tự ghi là bản tham khảo do
> AI hỗ trợ và chưa được thành viên tự xác nhận. Tài liệu này được đưa
> vào đối chiếu tham khảo, không xem là ý kiến cá nhân đã xác nhận hoặc
> một phiếu biểu quyết.

## 1. Bảng so sánh và kết quả đã chốt

| Chủ đề                                             | Khác biệt trong guideline cá nhân                                                                                                                   | Quyết định nhóm                                                                                                                                                                                        | Trạng thái  |
|----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Xe chở xe — `img_002`                              | 031 và 176 đề xuất gán `truck` cùng từng `car` được chở; 233 xem xe được chở là hàng hóa và chỉ gán `truck`.                                        | Gán một box `truck` cho xe chuyên chở và một box `car` riêng cho từng ô tô được chở nếu nhìn thấy, nhận diện được và đạt ngưỡng kích thước. Không gộp ô tô vào box `truck`.                            | **ĐÃ CHỐT** |
| Ngưỡng vật nhỏ                                     | 031 không muốn tự đặt ngưỡng; 146, 147, 176 theo chiều cao tối thiểu 20 px của taxonomy; 233 đề xuất cạnh dài 40 px.                                | Giữ `min_box_height_px = 20` theo taxonomy. Đo chiều cao box trên ảnh gốc; không thay bằng cạnh dài 40 px.                                                                                             | **ĐÃ CHỐT** |
| `occluded_level`                                   | Các cá nhân đưa ra các dải phần trăm khác nhau hoặc chưa định lượng.                                                                                | Dùng dải của 031 theo **tỷ lệ phần đối tượng bị vật khác che**: level 0 = 0–20%; level 1 = trên 20–50%; level 2 = trên 50–80%; level 3 = trên 80% nhưng dưới 100%, khi phần còn thấy vẫn đủ nhận diện. | **ĐÃ CHỐT** |
| Class phương tiện bổ sung                          | 031 đề xuất `bus`; 233 đề xuất `bus`, `three_wheeler`, `bicycle`; các bản khác yêu cầu không ép phương tiện ngoài taxonomy vào class không phù hợp. | Bổ sung `bus`, `three_wheeler`, `bicycle` vào taxonomy nhóm. Không thêm `other_vehicle`.                                                                                                               | **ĐÃ CHỐT** |
| Hàng hóa nhô ra — `img_029` và tình huống tương tự | 176 đề xuất box phương tiện bao cả khối hàng gắn liền; 147 và 233 đề xuất chỉ bao thân xe, không bao phần hàng nhô ra.                              | Box phương tiện chỉ bao thân/cấu trúc của chính phương tiện; không bao phần hàng hóa nhô ra.                                                                                                           | **ĐÃ CHỐT** |

## 2. Những điểm tương đối thống nhất trong các bản cá nhân

| Chủ đề               | Nội dung chung rút ra                                                                         | Ghi chú                                                            |
|----------------------|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| Người và phương tiện | Người và phương tiện là các instance độc lập; không gộp người lái/người ngồi sau với xe.      | Mỗi người đủ điều kiện một box `person`; phương tiện có box riêng. |
| Box khi bị che       | Box chỉ bao phần nhìn thấy; không tự vẽ phần bị che khuất.                                    | `occluded_level` đánh giá phần bị vật khác che.                    |
| `truncated`          | Đánh dấu khi khung ảnh cắt mất một phần đối tượng đã được gán.                                | Đặt `truncated = yes`; box nằm trong biên ảnh.                     |
| Vật không thật       | Tượng, ma-nơ-canh, hình in/quảng cáo và phản chiếu không được gán như người/phương tiện thật. | Đồ chơi/mô hình cũng không gán thành phương tiện thật.             |
| Vệt sáng và bóng     | Không kéo box theo bóng đổ, phản chiếu hoặc vệt sáng lóa.                                     | Chỉ gán nếu thân phương tiện còn nhận diện được.                   |

## 3. Đối chiếu 5 vấn đề bổ sung và quyết định nhóm ngày 2026-11-16

> Ý kiến dưới đây được tóm tắt từ nội dung guideline cá nhân. Việc một
> thành viên không đề cập một vấn đề không được hiểu là đồng ý hoặc phản
> đối. Guideline 146 là bản tham khảo AI hỗ trợ, chưa được thành viên tự
> xác nhận nên không xem là phiếu biểu quyết.

| Chủ đề | Ý kiến trong tài liệu cá nhân | Quyết định cuối cùng của nhóm | Trạng thái |
|---|---|---|---|
| Pickup/canopy | 176: pickup thùng hở đề xuất `truck`, pickup có canopy để thảo luận. 147: pickup thùng hở là `truck`; canopy cũng đề xuất `truck` nhưng tick `can_review`. 233: mọi pickup, kể cả canopy, thuộc `truck`. 031 không nêu quy tắc riêng. 146 có ghi ca pickup nhưng nội dung do AI đề xuất, chưa được xác nhận. | Tất cả pickup thuộc `truck`, bất kể thùng hở, có nắp hay canopy. | **ĐÃ CHỐT — D-06** |
| Người trong cabin kín | 147 và 233 đề xuất không gán người chỉ nhìn qua kính cabin kín; ngoại lệ khi người thò đầu/thân ra ngoài và nhìn rõ. 031 và 176 không nêu quy tắc riêng. 146 không có ý kiến cá nhân được xác nhận về điểm này. | Không gán `person` qua kính cabin kín; ngoại lệ khi người thò đầu/thân ra ngoài, nhìn rõ và đạt ngưỡng. | **ĐÃ CHỐT — D-07** |
| Ego Vehicle | 031 đề xuất gán phương tiện mang camera nếu chính phương tiện xuất hiện rõ trong khung hình và thuộc taxonomy. 147 và 233 đề xuất không gán bộ phận của xe mang camera như nắp capo, gương, cần gạt nước và nội thất. 176 không nêu quy tắc riêng. 146 ghi đây là vấn đề mở, chưa có ý kiến cá nhân được xác nhận. | Không gán các bộ phận của chính phương tiện mang camera; phương tiện khác trong cảnh vẫn gán bình thường. | **ĐÃ CHỐT — D-08** |
| `ignore_region` | 031 yêu cầu tuân thủ schema/repository, không tự tạo ignore chỉ vì vật nhỏ hoặc khó. 176 phân biệt vùng ngoài phạm vi với cụm không thể tách. 147 đề xuất dùng cho cụm nhỏ/dày, không che đối tượng khó nhưng còn gán được. 233 mô tả cụm nhiều vật thật không thể phân tách; vật rõ vẫn gán riêng. 146 ghi cần nhóm xác nhận cách gom vùng. | Chỉ bao cụm nhiều đối tượng thật không thể tách; đối tượng rõ, tách được và đạt ngưỡng vẫn có box riêng, kể cả khi chồng lên vùng ignore. | **ĐÃ CHỐT — D-09** |
| Sidecar | 147 và 233 xếp xe máy gắn sidecar vào `motorcycle`, box bao cả sidecar và người gán riêng. 031 và 176 không nêu quy tắc riêng. 146 đề xuất xem là một cụm phương tiện nhưng chưa được thành viên xác nhận. | Một box `motorcycle` bao cả xe máy và sidecar; người lái/hành khách là `person` riêng nếu đủ điều kiện. | **ĐÃ CHỐT — D-10** |

## 4. Trạng thái các vấn đề được rà soát

- 5 quyết định ban đầu D-01 đến D-05 vẫn giữ nguyên.
- 5 vấn đề bổ sung D-06 đến D-10 đã được nhóm Alpha xác nhận đồng ý
  toàn bộ, không có ý kiến sửa đổi.
- Không còn mục mở trong danh sách 5 vấn đề được đưa ra xác nhận lần này.
- Các tình huống mới ngoài phạm vi đã có quy tắc vẫn phải ghi nhận và
  chuyển reviewer; không tự thêm class hoặc tự sửa taxonomy.

## 5. Các thay đổi bắt buộc đồng bộ

1.  Guideline nhóm phản ánh đầy đủ 10 quyết định D-01 đến D-10.
2.  `taxonomy_v1.0.json` có `bus`, `three_wheeler`, `bicycle`; không có
    `other_vehicle`; `truck` bao gồm pickup/canopy và `motorcycle` bao
    gồm sidecar.
3.  Định nghĩa `person` và `ignore_region` phải khớp với các quyết định
    D-07 và D-09.
4.  Giữ nguyên các thuộc tính `occluded_level`, `truncated`,
    `can_review` và toàn bộ giá trị trong `rules`, đặc biệt
    `min_box_height_px = 20` cùng các ngưỡng QC/IAA.
5.  Cập nhật/sinh lại danh sách nhãn CVAT từ taxonomy v1.0 trước khi
    annotation; không tự thay đổi schema thuộc tính.
