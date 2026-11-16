# Guideline gán nhãn Bounding Box — Nhóm Alpha

- **Lab:** Day 07 — Guideline, Taxonomy & Quality Control
- **Phiên bản:** v1.0
- **Ngày cập nhật:** 2026-11-16
- **Phạm vi dữ liệu:** 40 ảnh đường phố (`img_001.jpg` đến
  `img_040.jpg`)
- **Công cụ:** CVAT
- **Định dạng xuất:** COCO 1.0
- **Trạng thái:** Bản v1.0 hoàn thiện; 10 quyết định Pha 2 đã được
  nhóm Alpha xác nhận, không còn mục mở trong danh sách theo dõi này.

## 1. Mục tiêu và nguyên tắc chung

Mục tiêu là tạo Bounding Box nhất quán cho người và phương tiện thật
xuất hiện trong ảnh đường phố, phục vụ bài toán Object Detection.

Nguyên tắc bắt buộc:

1.  Chỉ gán các đối tượng thật thuộc taxonomy nhóm.
2.  Mỗi đối tượng là một instance riêng; không gộp người với phương tiện
    hoặc nhiều phương tiện khác nhau vào cùng một box.
3.  Box ôm sát phần nhìn thấy của đối tượng, nằm trong khung ảnh.
4.  Không suy đoán phần bị che khuất hoặc phần nằm ngoài mép ảnh.
5.  Không gán tượng, ma-nơ-canh, đồ chơi/mô hình, hình in hoặc hình phản
    chiếu thành đối tượng thật.
6.  Không tự tạo class ngoài taxonomy đã chốt.
7.  Khi không đủ căn cứ phân loại hoặc vẽ box, không đoán; ghi nhận để
    reviewer xử lý bằng `can_review` hoặc ghi chú cấp ảnh.

## 2. Taxonomy nhóm v1.0

Mỗi đối tượng được gán vào đúng một class phù hợp nhất. `ignore_region`
là vùng bỏ qua, không phải một đối tượng giao thông.

| Class           | Định nghĩa áp dụng                                                                               | Ví dụ / lưu ý                                                                       |
|-----------------|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| `car`           | Ô tô con chở người: sedan, hatchback, SUV, crossover, coupe, wagon và taxi con. | Không dùng cho xe buýt hoặc xe bán tải pickup. |
| `truck`         | Xe tải, xe có thùng hàng riêng, xe đầu kéo, xe chuyên dụng vận tải và mọi xe bán tải pickup. | Pickup thuộc `truck` dù thùng hở, có nắp đậy hay gắn canopy. |
| `van`           | Xe dạng hộp kín cỡ nhỏ/trung bình, khoang lái và khoang sau tương đối liền khối. | Không tự động gán mọi xe thân kín vào `van`; phân biệt cấu trúc với `truck`. |
| `bus`           | Xe buýt và xe khách chở nhiều hành khách. | Không gán xe buýt vào `truck` chỉ vì kích thước lớn. |
| `motorcycle`    | Xe máy, mô tô và phương tiện hai bánh có động cơ, bao gồm xe gắn sidecar. | Một box bao cả xe máy và sidecar gắn liền. |
| `three_wheeler` | Phương tiện ba bánh có động cơ dùng chở người hoặc hàng. | Bao gồm tuk-tuk và auto-rickshaw; không dùng cho sidecar. |
| `bicycle`       | Xe đạp và phương tiện ba bánh chạy bằng sức người. | Bao gồm xích lô đạp; box bao phương tiện, không gộp người đạp/ngồi trên xe. |
| `person`        | Người thật: người đi bộ, người lái xe và hành khách nhìn thấy đủ rõ. | Người chỉ nhìn thấy qua kính cabin kín không gán; ngoại lệ khi thò đầu/thân ra ngoài và nhìn rõ. |
| `ignore_region` | Vùng bỏ qua bao một cụm đối tượng thật thuộc phạm vi nhưng quá nhỏ, quá dày hoặc chồng lấn đến mức không thể tách từng instance. | Đối tượng rõ, tách được và đạt ngưỡng vẫn phải gán box riêng, kể cả khi box chồng lên vùng ignore. |

**Không có class `other_vehicle`.** Nếu xác định chắc chắn là phương
tiện nhưng chưa rõ thuộc class nào, không tự tạo nhãn khác; đánh dấu
review để nhóm/reviewer xử lý.

### 2.1. Quy tắc phân biệt class

- Phân biệt `car`, `truck`, `van` dựa trên kiểu phương tiện và cấu trúc
  thân xe, không chỉ dựa vào kích thước.
- Mọi xe bán tải pickup thuộc `truck`, bất kể thùng hở, có nắp đậy hay
  gắn canopy; không chuyển thành `car` hoặc `van` vì có nắp che.
- Xe buýt/xe khách thuộc `bus`.
- Tuk-tuk và auto-rickshaw ba bánh có động cơ thuộc `three_wheeler`.
- Xe đạp và xích lô đạp thuộc `bicycle`.
- Xe máy gắn sidecar thuộc `motorcycle`; box bao cả xe máy và sidecar.
- Nếu phương tiện nằm ở ranh giới giữa hai class mà quy tắc hiện tại
  chưa đủ rõ, đánh dấu `can_review`; không tự ép vào class gần giống.

## 3. Thuộc tính

### 3.1. `occluded_level`

Đánh giá theo **tỷ lệ phần đối tượng bị vật khác che khuất**, ước lượng
so với toàn bộ hình thể thực tế. Không tính phần bị mép ảnh cắt, bóng
đổ, tối, mờ hoặc lóa là occlusion.

| Mức |       Tỷ lệ bị che khuất | Cách áp dụng                                               |
|-----|-------------------------:|------------------------------------------------------------|
| `0` |                   0%–20% | Không hoặc chỉ bị che rất ít.                              |
| `1` |             Trên 20%–50% | Bị che một phần; vẫn gán nếu nhận diện được.               |
| `2` |             Trên 50%–80% | Bị che nhiều; vẫn gán nếu nhận diện chắc chắn.             |
| `3` | Trên 80% nhưng dưới 100% | Chỉ gán nếu phần còn nhìn thấy vẫn đủ nhận diện chắc chắn. |

Quy tắc: - Các khoảng không chồng lấn; 20%, 50%, 80% thuộc mức kết thúc
tại mốc đó. - Nếu bị che hoàn toàn hoặc phần còn thấy không đủ căn cứ
xác định class, không đoán nhãn; ghi `can_review` hoặc vấn đề cấp ảnh. -
Nếu vừa bị vật khác che vừa bị mép ảnh cắt, áp dụng cả `occluded_level`
và `truncated` độc lập.

### 3.2. `truncated`

- `yes`: đối tượng bị một trong bốn mép ảnh cắt mất một phần và vẫn được
  gán nhãn.
- `no`: đối tượng nằm trọn trong ảnh; chỉ chạm sát mép nhưng không bị
  cắt thì vẫn là `no`.
- Box chỉ bao quanh phần đối tượng nhìn thấy bên trong ảnh; không vẽ ra
  ngoài hoặc suy đoán phần bị cắt.
- Nếu đối tượng bị mép ảnh cắt và vẫn đủ điều kiện gán, đặt
  `truncated = yes` bất kể tỷ lệ phần nhìn thấy.

### 3.3. `can_review`

Tick checkbox khi: - Không chắc class hoặc đối tượng nằm ở ranh giới
giữa các class. - Không chắc ranh giới box do mờ, lóa, che khuất hoặc
chất lượng ảnh. - Không phân biệt chắc chắn vật thật với tượng,
ma-nơ-canh, mô hình hoặc phản chiếu. - Gặp trường hợp chưa có quy tắc
nhóm. - Áp dụng `ignore_region` theo đúng R-10; không tự mở rộng vùng bỏ qua.

Nếu không thể tạo box hợp lệ thì không tạo box giả chỉ để tick thuộc
tính; ghi mã ảnh, vị trí và lý do trong ghi chú QC.

## 4. Quy tắc Bounding Box

### R-01. Box ôm sát đối tượng

- Dùng hình chữ nhật song song trục ảnh.
- Box ôm sát ranh giới phần đối tượng nhìn thấy.
- Không bao gồm nền thừa, bóng đổ, phản chiếu, quầng sáng hoặc vệt sáng
  kéo dài.
- Không kéo box ra ngoài khung ảnh.

### R-02. Người và phương tiện là hai instance độc lập

- Người lái xe máy và xe máy có hai box riêng: `person` và `motorcycle`.
- Người ngồi sau cũng có box `person` riêng nếu nhìn thấy và đạt ngưỡng.
- Box người bao phần cơ thể nhìn thấy, gồm đầu/mũ bảo hiểm, thân, tay và
  chân.
- Không gộp người và xe thành một box; hai box được phép chồng lấn tự
  nhiên.

### R-03. Đối tượng bị che khuất

- Box chỉ bao quanh phần nhìn thấy của đối tượng.
- Không vẽ phần bị che bằng suy đoán.
- Nếu vẫn nhận diện chắc chắn và đạt ngưỡng kích thước, vẫn gán box và
  chọn `occluded_level` theo mục 3.1.
- Nếu không đủ căn cứ nhận diện, không đoán class; chuyển review.

### R-04. Ngưỡng kích thước tối thiểu — 20 px

- Giữ nguyên `min_box_height_px = 20` theo taxonomy nhóm.
- Đo **chiều cao Bounding Box** trên ảnh gốc, không dựa vào mức zoom
  CVAT và không dùng cạnh dài thay thế.
- Box cao từ 20 px trở lên: đủ điều kiện xét gán instance riêng nếu
  class nhận diện được.
- Box cao dưới 20 px: không gán instance riêng theo ngưỡng hiện tại; nếu
  nằm trong cụm nhỏ/dày, xử lý vùng theo quy tắc `ignore_region` và QC.
  Không tự tạo ngưỡng 40 px.

### R-05. Xe chở xe — `img_002`

- Xe đầu kéo/xe chuyên chở được gán một box `truck`.
- Mỗi ô tô được chở được gán một box `car` riêng nếu nhìn thấy, nhận
  diện được và đạt chiều cao tối thiểu 20 px.
- Không gộp các ô tô được chở vào box `truck`, không xem toàn bộ ô tô
  được chở là hàng hóa để bỏ nhãn.
- Nếu ô tô được chở bị che, vẫn gán nếu nhận diện được và đạt ngưỡng;
  đánh dấu `occluded_level` riêng.

### R-06. Xe chở hàng cồng kềnh — `img_029` và tình huống tương tự

- Box phương tiện chỉ bao thân và cấu trúc của chính phương tiện.
- **Không bao phần hàng hóa nhô ra ngoài thân xe**, ví dụ ống dài, thanh
  dài hoặc bó hàng quá khổ.
- Không kéo box xe theo chiều dài hoặc chiều cao của hàng nhô ra.
- Người điều khiển/người vận chuyển là instance `person` riêng nếu nhìn
  thấy và đủ điều kiện gán.
- Nếu hàng hóa che một phần xe hoặc người, đánh giá occlusion cho đối
  tượng bị che; không đưa hàng vào box phương tiện.

### R-07. Phương tiện bổ sung

- Xe buýt/xe khách: `bus`.
- Tuk-tuk/auto-rickshaw ba bánh có động cơ: `three_wheeler`.
- Xe đạp và xích lô đạp: `bicycle`.
- Không gán các phương tiện này vào `car`, `truck` hoặc `motorcycle` chỉ
  để khớp taxonomy cũ.

### R-08. Đối tượng bị cắt mép ảnh

- Nếu đối tượng bị mép ảnh cắt nhưng vẫn đủ điều kiện gán theo ngưỡng và
  nhận diện, vẽ box phần nhìn thấy và đặt `truncated = yes`.
- Không suy đoán phần nằm ngoài ảnh.
- `truncated` không thay thế `occluded_level`.

### R-09. Tượng, ma-nơ-canh, đồ chơi, hình in và phản chiếu

Không gán thành người hoặc phương tiện thật: - Tượng người/tượng phương
tiện. - Ma-nơ-canh, hình nộm và đồ chơi/mô hình. - Người hoặc xe in trên
poster, billboard, biển quảng cáo, tranh tường. - Người hoặc xe chỉ xuất
hiện trong gương, kính hoặc phản chiếu trên mặt đường.

Nếu không chắc đó là đối tượng thật hay hình giả/phản chiếu, đánh dấu
review; không đoán.

### R-10. Đám đông và vùng bỏ qua (`ignore_region`)

- Chỉ dùng `ignore_region` để bao một **cụm gồm nhiều đối tượng thật
  thuộc taxonomy** khi chúng quá nhỏ, quá dày, chồng lấn hoặc dính nhau
  đến mức không thể tách và gán đầy đủ từng instance.
- Vẽ một vùng bao quanh phần cụm không thể phân tách; không dùng một
  vùng ignore để bao trùm toàn bộ ảnh hoặc khu vực không liên quan.
- Đối tượng trong cụm vẫn nhìn rõ, nhận diện được, tách được và có chiều
  cao box từ 20 px trở lên **vẫn phải được gán box riêng**. Box instance
  được phép chồng lên vùng `ignore_region`.
- Đối tượng riêng lẻ dưới 20 px không được tự động biến thành một
  `ignore_region`; chỉ đưa vào vùng ignore khi thuộc một cụm nhiều đối
  tượng thật không thể phân tách.
- Không dùng `ignore_region` cho tượng, ma-nơ-canh, đồ chơi/mô hình,
  hình in, phản chiếu hoặc vật ngoài taxonomy.
- Không dùng `ignore_region` để né một đối tượng lớn, rõ, có thể gán
  hoặc để thay thế class chưa biết.

### R-11. Vệt sáng, mờ chuyển động và điều kiện ban đêm/mưa

- Box chỉ bao phần thân phương tiện thực tế còn nhìn thấy; không bao
  quầng sáng đèn, vệt sáng kéo dài hoặc phản chiếu trên mặt đường.
- Mờ/tối/lóa không tự động được tính là occlusion.
- Nếu thân phương tiện không đủ rõ để nhận diện class, không đoán nhãn;
  ghi `can_review`/ghi chú QC.

### R-12. Vật ngoài taxonomy

- Không tự tạo class ngoài danh sách ở mục 2.
- Không ép vật ngoài taxonomy vào class gần giống.
- Nếu vật chắc chắn không thuộc phạm vi gán nhãn, không gán.
- Nếu chưa chắc vật thuộc class nào hoặc chưa rõ có nằm trong phạm vi
  không, chuyển review.

### R-13. Xe bán tải pickup, kể cả canopy

- Tất cả xe bán tải pickup thuộc class `truck`, không phụ thuộc thùng
  hàng đang hở, có nắp đậy, mui cứng hay canopy.
- Canopy/nắp thùng là phần che phủ khoang hàng, không làm thay đổi class
  của chiếc pickup.
- Không chuyển pickup sang `car` hoặc `van` chỉ vì thùng hàng được che
  kín. Nếu không đủ căn cứ nhận diện đó là pickup, đánh dấu `can_review`
  thay vì đoán.

### R-14. Người bên trong cabin kín

- Không gán box `person` cho người chỉ nhìn thấy qua kính của cabin kín
  trên ô tô, pickup, xe tải, van hoặc bus.
- Ngoại lệ: người thò đầu hoặc thân ra ngoài cabin và phần nhìn thấy đủ
  rõ để nhận diện, đồng thời đạt ngưỡng kích thước; khi đó gán một box
  `person` riêng quanh phần cơ thể nhìn thấy.
- Người trên xe máy, sidecar, tuk-tuk, auto-rickshaw hoặc phương tiện
  khoang hở vẫn được gán riêng nếu nhìn thấy rõ và đạt ngưỡng.
- Không gộp người vào box phương tiện.

### R-15. Ego Vehicle — phương tiện mang camera

- Không gán các bộ phận của chính phương tiện mang camera xuất hiện ở
  mép hoặc góc ảnh, gồm nắp capo, cần gạt nước, khung gương, bảng điều
  khiển và nội thất.
- Không gán hình ảnh phương tiện xuất hiện trong gương chiếu hậu như
  một instance mới vì đó là phản chiếu.
- Các phương tiện giao thông thật khác trong cảnh vẫn được gán bình
  thường theo taxonomy.
- Quy tắc này áp dụng cho phương tiện đang mang camera, không áp dụng
  để loại bỏ một phương tiện khác chỉ vì nó gần camera.

### R-16. Xe máy gắn sidecar

- Phương tiện gồm một xe máy và sidecar gắn liền được gán **một box
  `motorcycle` duy nhất**.
- Box `motorcycle` bao toàn bộ phần xe máy và kết cấu sidecar gắn liền;
  không tạo box riêng cho sidecar và không xếp thành `three_wheeler`.
- Người lái và từng hành khách trong sidecar là các box `person` riêng
  nếu nhìn thấy rõ và đạt ngưỡng; không gộp người vào box phương tiện.

## 5. Ca khó thực tế trong bộ 40 ảnh

| Ảnh                                                   | Tình huống                                                | Quyết định áp dụng                                                                                     |
|-------------------------------------------------------|-----------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| `img_002`                                             | Xe đầu kéo chở nhiều ô tô                                 | Một box `truck`; từng ô tô được chở có box `car` riêng nếu nhận diện được và cao ≥20 px.               |
| `img_004`, `img_016`, `img_035`, `img_040`            | Tuk-tuk/auto-rickshaw                                     | Gán phương tiện bằng `three_wheeler`; người nhìn thấy đủ điều kiện gán `person` riêng.                 |
| `img_006`, `img_009`, `img_023`, `img_034`, `img_039` | Xích lô/xe đạp ba bánh chạy bằng sức người                | Gán phương tiện bằng `bicycle`; người đạp và hành khách là `person` riêng nếu nhìn thấy và đạt ngưỡng. |
| `img_029`                                             | Người đi xe máy và người đạp xe chở ống dài               | Gán riêng người và phương tiện; box xe chỉ bao thân xe, không bao ống/hàng nhô ra.                     |
| `img_032`, `img_040`                                  | Xe buýt/xe khách                                          | Gán `bus`, không ép thành `car` hoặc `truck`.                                                          |
| `img_005`, `img_006`, `img_026`                       | Người lái/người ngồi sau xe máy                           | Mỗi người một box `person`, xe một box `motorcycle`; không gộp.                                        |
| `img_017`                                             | Tượng người                                               | Không gán `person`.                                                                                    |
| `img_018`                                             | Hình người in trên biển quảng cáo                         | Không gán `person`.                                                                                    |
| `img_020`                                             | Xe/người trong gương chiếu hậu                            | Không gán hình phản chiếu thành instance mới.                                                          |
| `img_020`                                             | Một phần xe mang camera (Ego Vehicle) và hình phản chiếu trong gương | Không gán nắp capo, gương, nội thất hoặc các bộ phận của xe mang camera; không gán phương tiện chỉ xuất hiện trong gương. |
| `img_022`                                             | Xe máy gắn sidecar                                        | Một box `motorcycle` bao cả xe máy và sidecar; người lái/hành khách nhìn rõ có box `person` riêng.      |
| `img_028`, `img_037`                                  | Xe bán tải pickup, gồm pickup có canopy                   | Gán `truck` trong mọi trường hợp; canopy không làm thay đổi class.                                     |
| `img_033`                                             | Ma-nơ-canh                                                | Không gán `person`.                                                                                    |
| `img_038`                                             | Đồ chơi/mô hình xe                                        | Không gán thành phương tiện thật.                                                                      |
| `img_015`, `img_031`                                  | Vệt sáng, phản chiếu và xe mờ trong điều kiện mưa/ban đêm | Không bao vệt sáng/phản chiếu; chỉ gán nếu thân xe còn nhận diện được.                                 |
| `img_001`, `img_008`, `img_034`                       | Đối tượng bị cắt mép                                      | Nếu đối tượng vẫn đủ điều kiện gán, box phần nhìn thấy và đặt `truncated = yes`.                       |

## 6. Quy trình xử lý ca chưa chắc chắn

1.  Kiểm tra đối tượng có phải vật thật hay không.
2.  Xác định đối tượng có thuộc một class trong taxonomy không.
3.  Kiểm tra chiều cao box trên ảnh gốc có đạt 20 px không.
4.  Vẽ box phần nhìn thấy; không suy đoán phần khuất hoặc ngoài ảnh.
5.  Điền `occluded_level` và `truncated` độc lập.
6.  Nếu còn bất định về class/box/rule, tick `can_review` hoặc ghi mã
    ảnh, vị trí và lý do để reviewer xem xét.
7.  Không tự thêm class hoặc tự sửa taxonomy trong lúc annotation.

## 7. Checklist QC

- [ ] Đã dùng đúng class theo taxonomy v1.0.
- [ ] Không gán tượng, ma-nơ-canh, mô hình, hình in hoặc phản chiếu.
- [ ] Người và phương tiện được gán thành các box độc lập.
- [ ] Người ngồi sau xe được gán riêng nếu nhìn thấy và đạt ngưỡng.
- [ ] Xe chở xe: mỗi ô tô được chở có box `car` riêng nếu đủ điều kiện.
- [ ] Chiều cao box được kiểm tra trên ảnh gốc; ngưỡng là 20 px.
- [ ] `occluded_level` được chọn theo tỷ lệ bị vật khác che, không tính
  phần bị cắt mép.
- [ ] `truncated = yes` khi đối tượng được gán bị mép ảnh cắt.
- [ ] Box phương tiện không bao phần hàng hóa nhô ra.
- [ ] Box không bao bóng đổ, phản chiếu, quầng sáng hoặc vệt sáng.
- [ ] Ca không chắc chắn được đánh dấu `can_review`/ghi chú QC.
- [ ] `ignore_region` chỉ bao cụm nhiều đối tượng thật không thể tách;
  đối tượng rõ và đạt ngưỡng vẫn có box riêng, kể cả khi chồng lên vùng ignore.
- [ ] Pickup, kể cả có canopy/nắp thùng, được gán `truck`.
- [ ] Người chỉ nhìn thấy qua kính cabin kín không được gán `person`;
  ngoại lệ người thò đầu/thân ra ngoài và nhìn rõ.
- [ ] Không gán bộ phận của Ego Vehicle mang camera.
- [ ] Sidecar gắn liền được bao chung trong một box `motorcycle`;
  người trên xe được gán `person` riêng nếu đủ điều kiện.

## 8. Thông số QC/IAA giữ nguyên từ taxonomy

| Tham số              | Giá trị |
|----------------------|--------:|
| `min_box_height_px`  |      20 |
| `iou_thr_large`      |    0.85 |
| `iou_thr_small`      |    0.70 |
| `large_px`           |      50 |
| `iaa_iou`            |    0.85 |
| `iaa_class`          |    0.95 |
| `error_rate_img_max` |    0.02 |
| `match_iou`          |    0.50 |

Không thay đổi các tham số trên nếu chưa có quyết định nhóm riêng.

## 9. Các quyết định nhóm đã xác nhận bổ sung ngày 2026-11-16

Nhóm Alpha đã xác nhận đồng ý cả 5 nội dung sau, không có ý kiến sửa
đổi. Các quy tắc được áp dụng chính thức trong Guideline v1.0:

1. **Pickup/canopy:** mọi xe bán tải pickup thuộc `truck`, kể cả có
   nắp thùng hoặc canopy (D-06; R-13).
2. **Người trong cabin kín:** không gán `person` khi chỉ nhìn qua kính;
   ngoại lệ người thò đầu/thân ra ngoài và nhìn rõ (D-07; R-14).
3. **Ego Vehicle:** không gán các bộ phận của chính phương tiện mang
   camera; phương tiện khác trong cảnh vẫn gán bình thường (D-08; R-15).
4. **`ignore_region`:** chỉ bao cụm đối tượng thật không thể tách;
   đối tượng rõ, tách được và đạt ngưỡng vẫn phải gán box riêng (D-09; R-10).
5. **Sidecar:** xe máy gắn sidecar là một `motorcycle`, box bao cả hai;
   người trên xe được gán riêng nếu đủ điều kiện (D-10; R-16).

Không còn mục mở trong danh sách 5 vấn đề được đưa ra để nhóm Alpha
xác nhận. Tình huống mới ngoài các quy tắc trên vẫn phải ghi nhận và
chuyển reviewer; không tự ý sửa taxonomy.

## 10. Lịch sử phiên bản

| Phiên bản | Nội dung                                                                                                                                                                                                                                          |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| v0        | Taxonomy ban đầu gồm `car`, `truck`, `van`, `motorcycle`, `person`, `ignore_region`.                                                                                                                                                              |
| v1.0      | Tổng hợp 5 guideline cá nhân và 10 quyết định Pha 2 của nhóm Alpha; bổ sung `bus`/`three_wheeler`/`bicycle`, quy tắc pickup/canopy, cabin kín, Ego Vehicle, `ignore_region` và sidecar; giữ nguyên ngưỡng 20 px và các thông số QC/IAA. |
