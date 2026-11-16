# Guideline gán nhãn — v0.1 — Thành viên 147

- **Phiên bản:** v0.1 (Bản guideline cá nhân độc lập — Pha 1)
- **Ngày lập:** 2026-11-16
- **Thành viên thực hiện:** Thành viên 147 (Mã sinh viên / MSHV: 2A202603147 / 147)
- **Nhóm:** Alpha
- **Bộ dữ liệu áp dụng:** 40 ảnh đường phố (`data/images/img_001.jpg` – `img_040.jpg`)
- **Công cụ gán nhãn:** CVAT, xuất định dạng chuẩn COCO 1.0

---

## 1. Mục tiêu và phạm vi

### 1.1. Mục đích sử dụng dữ liệu
Bộ nhãn Bounding Box này được xây dựng để huấn luyện và kiểm thử các mô hình học sâu phát hiện đối tượng (Object Detection — ví dụ YOLO, Faster R-CNN, Deformable DETR) phục vụ cho:
1. Hệ thống giám sát và điều hành camera giao thông đô thị thông minh (ITS).
2. Hệ thống hỗ trợ lái xe nâng cao (ADAS) và xe tự hành (Autonomous Vehicles) hoạt động trong môi trường giao thông hỗn hợp phức tạp đặc thù tại các đô thị châu Á.

### 1.2. Đánh giá mức độ rủi ro và các lỗi nguy hiểm
Trong bài toán nhận diện giao thông thời gian thực, sự mơ hồ trong guideline gán nhãn dẫn đến dữ liệu huấn luyện nhiễu loạn, gây ra những hệ quả nghiêm trọng:
- **Bỏ sót đối tượng thật (False Negative — Lỗi nghiêm trọng nhất):** Không phát hiện người đi bộ, người điều khiển xe máy hoặc xe cộ trên đường có thể dẫn đến việc hệ thống tự hành không kích hoạt phanh tự động khẩn cấp, gây ra tai nạn giao thông đe dọa trực tiếp tính mạng con người.
- **Gán thừa đối tượng (False Positive):** Nhận diện nhầm ma-nơ-canh, tượng điêu khắc, tranh quảng cáo 2D hoặc bóng phản chiếu qua gương/mặt đường ướt là chướng ngại vật thực thể sẽ làm xe phanh gấp bất ngờ giữa dòng lưu thông (phantom braking), tiềm ẩn nguy cơ bị các xe phía sau đâm dồn toa.
- **Phân loại sai (Classification Confusion):** Nhầm lẫn giữa `car` và `truck`, hoặc giữa `person` và `motorcycle` sẽ làm sai lệch mô hình dự đoán quỹ đạo và hành vi (xe máy và người đi bộ có gia tốc chuyển hướng đột ngột hơn ô tô con và xe tải nặng).
- **Vẽ box không chuẩn xác (Bounding Box Inaccuracy):** Box vẽ lỏng lẻo nuốt nền xung quanh sẽ làm mô hình học các đặc trưng rác của môi trường; box vẽ cắt cụt bánh xe/thân xe làm mô hình học sai tỷ lệ khung hình (aspect ratio); box kéo theo vệt sáng lóa hoặc bóng đổ khiến mô hình nhận diện sai kích thước thực tế của chướng ngại vật.

### 1.3. Phạm vi áp dụng
- Áp dụng độc lập cho 40 ảnh trong thư mục `data/images/` ở Pha 1.
- Không tự ý gán nhãn theo cảm tính; chỉ gán các đối tượng thực sự thuộc taxonomy hoặc các vùng quy định được hướng dẫn chi tiết bên dưới.

---

## 2. Lớp đối tượng và thuộc tính

### 2.1. Bảng định nghĩa các lớp (Classes)

Mỗi đối tượng hợp lệ trong ảnh chỉ thuộc đúng **MỘT** lớp duy nhất.

| Tên lớp | Định nghĩa chuẩn xác | Ví dụ thực tế trong bộ ảnh | Phản ví dụ & Ca dễ nhầm lẫn |
|---|---|---|---|
| `car` | Ô tô con thiết kế chở người từ 4 đến 9 chỗ (sedan, hatchback, SUV, crossover, coupe, station wagon, taxi con). | Taxi sedan vàng (`img_040`), sedan đang lưu thông (`img_005`), xe cổ AMC Pacer wagon (`img_024`). | **Không gán:** Xe bán tải pickup (xem xét thuộc `truck`), xe van khoang kín, xe buýt lớn. |
| `truck` | Xe tải chở hàng, xe ben, xe đầu kéo, xe vận tải chuyên dụng có kết cấu cabin lái và thùng chở hàng/khung sàn tách biệt. | Xe chuyên chở ô tô 2 tầng Renault (`img_002`), xe tải giao hàng kho Pattaya (`img_007`), xe tải nhỏ mui bạt CMC Veryca (`img_036`). | **Không gán:** Xe van thân liền khối, ô tô con du lịch, xe ba gác máy. |
| `van` | Xe ô tô chở người hoặc hàng dạng khối hộp kín cỡ nhỏ/trung bình (thường từ 7 đến 16 chỗ), thân xe và khoang sau liền khối (monovolume). | Xe van trắng lưu thông giữa làn xe (`img_005`, biển 51LD-70-65), xe van taxi Bangkok (`img_016`). | **Không gán:** Xe buýt cỡ lớn (> 16 chỗ), xe tải thùng kín rời chassis, SUV 5 chỗ thông thường. |
| `motorcycle` | Xe hai bánh có động cơ (xe máy, mô tô phân khối lớn, xe gắn máy, xe tay ga scooter, xe máy điện). Kể cả xe máy có gắn thùng bên hông (sidecar). | Xe tay ga/xe số lưu thông tại TP.HCM (`img_005`), xe máy đỗ ban đêm (`img_008`, `img_030`), xe máy có sidecar (`img_022`). | **Không gán:** Xe đạp không động cơ, xe ba bánh tuk-tuk, xe xích lô đạp. Người ngồi trên xe gán lớp `person` riêng. |
| `person` | Con người thực thể sống (người đi bộ, người đứng, người ngồi, người điều khiển hoặc hành khách trên xe hở, người mặc trang phục hóa trang). | Người đi bộ băng qua đường (`img_014`), người lái xe máy (`img_005`, `img_026`), người mặc đồ cosplay Predator (`img_011`). | **Không gán:** Tượng người (`img_017`), người in trên billboard (`img_018`), ma-nơ-canh cửa hiệu (`img_033`), bóng người phản chiếu (`img_020`). |
| `ignore_region` | Vùng bỏ qua (không phải đối tượng nhận dạng): nơi tập trung nhiều đối tượng thật thuộc taxonomy nhưng quá nhỏ (< 20 px) hoặc quá dày đặc không thể phân tách từng box. | Hàng trăm xe máy đỗ dày đặc hoặc đám đông ở hậu cảnh xa tít (`img_005`, `img_008`, `img_025`). | **Tuyệt đối không dùng** `ignore_region` để che lấp các ca khó lẽ ra phải phân tích gán box hoặc đối tượng ngoài taxonomy. |

### 2.2. Xử lý các phương tiện ngoài taxonomy v0

Guideline khởi đầu v0 không quy định một số phương tiện xuất hiện trong ảnh đường phố châu Á. Đề xuất cá nhân của 147 trong Pha 1:
1. **Xe buýt cỡ lớn (`img_032`, `img_040`):** Không có lớp `bus` trong taxonomy v0. Tuyệt đối không ép vào `car` (vì kích thước và hành vi khác hẳn) và không ép vào `truck` (vì đây là xe chở khách công cộng). **Quyết định đề xuất:** Không gán box đối tượng, tick `can_review` hoặc ghi chú cấp ảnh để nhóm thống nhất ở Pha 2 xem có bổ sung lớp `bus` vào `taxonomy.json` hay không.
2. **Xe ba bánh (Tuk-tuk `img_004`, `img_016`, Auto-rickshaw `img_035`):** Phương tiện 3 bánh có động cơ. Không thuộc `motorcycle` (vốn là 2 bánh) và không phải `car` (ô tô con). **Quyết định đề xuất:** Tạm thời không gán box, ghi nhận ca khó để bàn ở Pha 2. Nếu nhìn thấy người lái/hành khách rõ ràng thì gán box `person` cho người.
3. **Xe xích lô đạp (`img_006`, `img_009`, `img_023`, `img_034`, `img_039`):** Phương tiện 3 bánh chạy bằng sức người đạp. Không thuộc taxonomy v0. Không gán khung xe xích lô; chỉ gán người đạp xích lô và khách du lịch ngồi trên xích lô bằng các box `person` riêng biệt.
4. **Xe đạp (`img_010`, `img_021`, `img_039`):** Không có lớp `bicycle` trong taxonomy v0. Không gán xe đạp; người đang điều khiển xe đạp vẫn gán box `person`.
5. **Xe bán tải (Pickup truck — `img_001`, `img_012`, `img_028`, `img_037`):**
   - Xe có cabin đơn/kép phía trước và thùng chở hàng hở lộ thiên phía sau: Xếp vào lớp `truck`.
   - Xe bán tải có gắn thêm nắp đậy thùng kín (truck cap/canopy như `img_037`): Bản chất khung gầm và tải trọng vẫn là bán tải chở hàng $\rightarrow$ Đề xuất xếp vào `truck`, tick `can_review` để thống nhất ở Pha 2.

### 2.3. Hệ thống thuộc tính và ngưỡng đo lường định lượng

#### Thuộc tính 1: `occluded_level` (Mức độ che khuất do vật khác chắn trước)
Đo bằng **tỷ lệ phần trăm diện tích đối tượng bị che khuất** so với toàn bộ hình thể thực tế ước tính của đối tượng. Không chồng lấn dải giá trị:

| Mức giá trị | Ngưỡng định lượng | Định nghĩa & Hướng dẫn xử lý |
|:---:|:---:|---|
| `0` | Che từ 0% đến < 10% | Đối tượng nhìn thấy trọn vẹn hoặc gần như trọn vẹn, không bị vật cản đáng kể. Vẽ box bình thường. |
| `1` | Che từ 10% đến 35% | Đối tượng bị che nhẹ bởi cột đèn, cành cây, biển báo hoặc phương tiện đi trước. Vẫn nhìn rõ cấu trúc chính. |
| `2` | Che từ > 35% đến 70% | Đối tượng bị che khuất một phần lớn nhưng các đặc trưng nhận dạng cơ bản vẫn nhận biết chắc chắn lớp. |
| `3` | Che từ > 70% đến 90% | Đối tượng bị che khuất nghiêm trọng, chỉ còn thấy một phần nhỏ (ví dụ chỉ thấy mũ bảo hiểm và vai người lái xe, hoặc chỉ thấy góc đuôi xe). **Bắt buộc tick `can_review = true`.** |

> **Quy tắc ngưỡng sàn:** Nếu đối tượng bị che khuất trên 90% diện tích và phần còn lại không đủ đặc trưng nhận diện chắc chắn lớp $\rightarrow$ **KHÔNG gán box** (tránh đoán mò).  
> **Lưu ý quan trọng:** Hiện tượng mờ do thời tiết, tối ban đêm hoặc cắt bởi mép ảnh **KHÔNG** được tính vào `occluded_level`.

#### Thuộc tính 2: `truncated` (Mức độ bị cắt bởi biên khung ảnh)
- `no`: Toàn bộ ranh giới đối tượng hiển thị đầy đủ bên trong khung hình (hoặc đối tượng chỉ tiếp xúc sát mép ảnh mà không bị cắt mất chi tiết hình học nào).
- `yes`: Đối tượng bị cắt ngang bởi ít nhất một trong bốn mép ảnh (trái, phải, trên, dưới). Bounding box dừng lại ngay tại mép ảnh, tuyệt đối không suy đoán phần ngoài biên ảnh.
- **Quan hệ giữa hai thuộc tính:** `truncated` và `occluded_level` là hai thuộc tính hoàn toàn độc lập, có thể đồng thời xảy ra trên cùng một đối tượng (ví dụ: chiếc xe ở góc mép dưới vừa bị mép ảnh cắt `truncated=yes`, vừa bị xe bên cạnh che một phần `occluded_level=2`).

#### Thuộc tính 3: `can_review` (Đánh dấu cần xem lại)
Giá trị dạng checkbox (`true` / `false`). Bắt buộc tick `true` trong các tình huống:
1. Đối tượng bị che khuất nghiêm trọng (`occluded_level = 3`).
2. Phương tiện ở vùng ranh giới phân loại chưa được v0 làm rõ (xe bán tải pickup, xe chở hàng cồng kềnh, xe buýt).
3. Biên đối tượng bị nhòe mờ do mưa, phản xạ kính hoặc vệt sáng ban đêm mà mắt thường khó xác định ranh giới dứt khoát.
4. Tình huống có sự hoài nghi giữa đối tượng thật và mô hình/tượng giả.

---

## 3. Quy tắc vẽ Bounding Box (Rules)

Các quy tắc được chuẩn hóa bằng mã quy tắc từ R-01 đến R-12 để phục vụ đối chiếu và thảo luận nhóm:

- **R-01 — Bounding Box ôm sát ranh giới nhìn thấy (Tight Bounding Box):**
  Box là hình chữ nhật có các cạnh song song với các trục tọa độ ảnh $(x, y)$. Box phải ôm vừa khít đường viền vật lý nhìn thấy của đối tượng, sai số biên không vượt quá 2–3 pixel ở mức phóng đại 100%. Tuyệt đối không vẽ box rộng nuốt nền đường và không bao gồm bóng đổ (shadow), quầng sáng đèn xe hoặc vệt sáng phản chiếu.
- **R-02 — Đối tượng bị che khuất (Visible Bounding Box):**
  Box chỉ bao quanh phần nhìn thấy của đối tượng, không mở rộng box đoán phần bị che khuất sau vật cản. Nếu một đối tượng bị một vật chắn mỏng (như cột biển báo, dây điện, thanh chắn) cắt ngang làm đôi, vẫn vẽ **MỘT BOX DUY NHẤT** trùm qua cả hai phần nhìn thấy đó (miễn là xác định chúng cùng thuộc một thực thể).
- **R-03 — Đối tượng bị cắt bởi mép ảnh (Truncation):**
  Box kết thúc ngay tại đường biên mép ảnh, không vẽ tọa độ âm hoặc tràn ra ngoài ảnh; gán thuộc tính `truncated = yes`. Đối tượng bị cắt mép chỉ được gán nhãn nếu phần nhìn thấy trong ảnh đạt chiều cao tối thiểu 20 px và còn đủ đặc trưng nhận biết lớp.
- **R-04 — Tách độc lập người và phương tiện (Instance Separation):**
  Tuyệt đối không gộp chung người và phương tiện vào một box:
  - Gán một box `motorcycle` cho xe máy: Box bao gồm khung xe, bánh xe, tay lái, gương chiếu hậu.
  - Gán một box `person` riêng cho từng người ngồi trên xe: Box người bao gồm đầu (kể cả mũ bảo hiểm đang đội), thân mình, tay và chân nhìn thấy.
  - Hai box của người và xe được phép chồng đè tự nhiên lên nhau theo đúng hình thể thực tế.
- **R-05 — Xe chuyên dụng chở ô tô (Car Carrier — `img_002`):**
  - Gán 1 box `truck` bao toàn bộ xe tải đầu kéo và dàn khung rơ-moóc chuyên dụng.
  - Gán từng box `car` riêng biệt cho từng chiếc ô tô con được xếp trên giá chở (nếu ô tô con đó nhìn thấy rõ và chiều cao $\ge 20$ px). Việc ô tô đang được vận chuyển không làm mất đi tính chất thực thể của nó.
- **R-06 — Xe máy chở hàng hóa cồng kềnh, quá khổ (`img_029`):**
  - Box `motorcycle` chỉ ôm sát kết cấu xe máy thực tế và kiện hàng nhỏ gắn liền sát yên; **KHÔNG mở rộng box** để nuốt các thanh sắt, ống kim loại dài hàng mét nhô ra phía trước và phía sau. Lý do: việc kéo box theo hàng dài nhô xa sẽ làm tỷ lệ khung hình (aspect ratio) bị méo mó nghiêm trọng, phá hỏng đặc trưng học của mô hình cho lớp xe máy.
  - Người lái xe bị hàng che: Vẽ box `person` cho phần cơ thể nhìn thấy, đặt `occluded_level = 3`, tick `can_review = true`.
- **R-07 — Loại trừ triệt để vật thể không thật (False Positive Suppression):**
  Tuyệt đối **KHÔNG gán nhãn** cho các trường hợp:
  - Tượng điêu khắc bằng đá, kim loại, thạch cao (`img_017`, `img_027`).
  - Hình người, xe in trên biển quảng cáo, poster, áp phích, tranh vẽ tường (`img_018`, `img_026`).
  - Ma-nơ-canh trưng bày quần áo trong tủ kính cửa hàng (`img_033`).
  - Đồ chơi, mô hình xe, búp bê trong tủ kính (`img_038`).
  - Hình ảnh phản chiếu qua gương chiếu hậu (`img_020`) hoặc mặt nước/mặt đường ướt (`img_013`).
- **R-08 — Người mặc trang phục hóa trang / Cosplay (`img_011`):**
  Vẫn gán box `person` ôm sát người mặc đồ hóa trang (như nhân vật Predator). Căn cứ: Đây là một con người thực thể sống đang di chuyển trong không gian công cộng; hệ thống tự hành bắt buộc phải nhận diện để đảm bảo an toàn va chạm.
- **R-09 — Hiện tượng lóa sáng, nhòe mưa và vệt sáng ban đêm (`img_013`, `img_015`, `img_031`):**
  - Box phương tiện chỉ ôm khít khối thân vỏ kim loại nhìn thấy. Tuyệt đối không kéo dài box theo các vệt đèn nhòe (light streaks), quầng lóa trên kính chắn gió ướt mưa hoặc ánh đèn phản chiếu dưới mặt đường.
  - Nếu phương tiện bị nhòe hoàn toàn chỉ còn lại đốm sáng vô định hình $\rightarrow$ **KHÔNG gán box**.
- **R-10 — Xe chủ mang camera (Ego Vehicle):**
  Các bộ phận của chính chiếc xe chở thiết bị chụp ảnh (như nắp ca-pô, cần gạt nước, khung gương chiếu hậu, bảng điều khiển nội thất) xuất hiện ở góc ảnh: **KHÔNG gán nhãn**, vì mục tiêu của mô hình là phát hiện chướng ngại vật ngoài môi trường lưu thông, không nhận diện chính phương tiện mang cảm biến.
- **R-11 — Ngưỡng kích thước tối thiểu và vùng bỏ qua (`ignore_region`):**
  - Đối tượng có chiều cao box nhỏ hơn 20 pixel trên độ phân giải gốc của ảnh: Không gán box đơn lẻ.
  - Nếu ở hậu cảnh xa xuất hiện hàng loạt đối tượng nhỏ dính chùm hoặc đám đông xe máy quá dày đặc không thể tách rời từng xe (`img_005`, `img_008`, `img_025`): Vẽ một vùng `ignore_region` bao quanh toàn cụm để tránh bị tính lỗi bỏ sót khi kiểm tra chất lượng.
- **R-12 — Người bên trong khoang cabin kín:**
  - Người ngồi bên trong ô tô con, xe tải, xe buýt có kính đóng kín: **KHÔNG gán box `person`**, do bị khúc xạ, phản chiếu kính và che khuất hầu hết cơ thể.
  - Người ngồi trên phương tiện khoang hở (xe máy, xe ba bánh hở, xích lô, xe diễu hành mui trần) hoặc thò người ra ngoài cửa sổ nhìn thấy rõ từ ngực trở lên: Gán box `person` bình thường.

---

## 4. Danh mục ca khó (Edge Cases) từ 40 ảnh thực tế

Dưới đây là 16 ca khó tiêu biểu được phát hiện trực tiếp khi khảo sát chi tiết bộ 40 ảnh trong `data/images/`, kèm quyết định của Thành viên 147 và lý giải kỹ thuật cụ thể:

| STT | Ảnh | Tình huống thực tế quan sát được | Mã quy tắc | Quyết định cá nhân của 147 | Căn cứ & Lập luận kỹ thuật |
|:---:|---|---|:---:|---|---|
| 1 | `img_001.jpg` | Xe bán tải cũ đỗ trước quán ăn lề đường lúc chạng vạng; người phụ nữ có hình xăm đứng cạnh xe; khách ngồi trong quán. | R-01, R-04 | - Gán 1 box `truck` cho xe bán tải.<br>- Gán 1 box `person` cho người phụ nữ đứng cạnh xe.<br>- Gán box `person` cho các thực khách nếu chiều cao $\ge 20$ px. | Xe bán tải có kết cấu thùng hàng hở phía sau xếp vào `truck`. Người đứng cạnh xe có thân thể tách biệt, gán box `person` riêng. |
| 2 | `img_002.jpg` | Xe tải chuyên dụng Renault chở nhiều tầng ô tô con trên khung giá rơ-moóc; người đứng ở góc phải. | R-04, R-05 | - Gán 1 box `truck` bao toàn bộ đầu kéo và rơ-moóc.<br>- Gán từng box `car` riêng biệt cho mỗi chiếc ô tô con trên giá.<br>- Gán 1 box `person` cho người bên phải. | Tách bạch giữa phương tiện chuyên chở và các ô tô là hàng hóa nhưng vẫn giữ nguyên hình thái ô tô con hoàn chỉnh; người đứng độc lập gán riêng. |
| 3 | `img_004.jpg` | Hai xe Tuk-tuk màu xanh đỗ cạnh nhau trên vỉa hè ban đêm ở Pattaya; có người ngồi bên trong khoang lái. | R-04, R-12 | - Tạm thời **KHÔNG gán box phương tiện** cho xe tuk-tuk, tick `can_review`.<br>- Gán box `person` cho người ngồi trong khoang hở nhìn thấy rõ. | Tuk-tuk là xe 3 bánh, không khớp `car` hay `motorcycle` trong taxonomy v0. Người ngồi trong khoang hở vẫn là đối tượng nhận diện thật. |
| 4 | `img_005.jpg` | Ngã tư TP.HCM đông đúc, hàng chục xe máy và người điều khiển ken đặc; xe van trắng 51LD-70-65 phía sau; các xe ở xa bị cắt mép. | R-01, R-04, R-11 | - Gán từng cặp box `motorcycle` và `person` cho các xe ở cự ly gần và trung bình.<br>- Gán box `van` cho xe 51LD-70-65.<br>- Dùng `ignore_region` bao cụm xe máy quá xa ở hậu cảnh. | Phải tách biệt người và xe máy để mô hình học đúng đặc trưng; cụm xe quá xa và mờ nhạt gom vào ignore để tránh gán sót. |
| 5 | `img_011.jpg` | Người mặc trang phục hóa trang Predator đứng trên bục cạnh hàng xe mô tô độ tại lễ hội. | R-04, R-08 | - Gán box `person` cho người mặc đồ Predator.<br>- Gán từng box `motorcycle` cho các xe mô tô nhìn thấy rõ bên cạnh. | Dù mặc trang phục giả tưởng nhưng thực thể bên trong là con người đang di chuyển, hệ thống lái xe tự hành bắt buộc phải nhận diện để phòng tránh va chạm. |
| 6 | `img_012.jpg` | Xe bán tải đỗ trong ngõ hẹp, thùng chở hàng chất đầy các hộp và túi hàng hóa nhô cao. | R-01, R-06 | Gán 1 box `truck` bao quanh cabin xe và khung thùng xe; hàng hóa chất trong thùng được coi là tải trọng gắn liền trên xe. | Bản chất là xe bán tải chở hàng xếp vào `truck`. Khối hàng nằm gọn trong phạm vi lòng thùng sau. |
| 7 | `img_013.jpg` | Đường phố đêm ướt mưa, ánh đèn phản chiếu trên mặt đường và đèn xe chạy tạo vệt sáng nhòe. | R-01, R-09 | - Chỉ gán box cho các phương tiện đỗ hoặc đi chậm có thân vỏ kim loại nhìn thấy rõ.<br>- Bỏ qua các vệt sáng nhòe kéo dài trên mặt đường. | Vệt sáng đèn nhòe do tốc độ màn trập máy ảnh không phải là thực thể xe vật lý; vẽ box theo vệt sáng sẽ làm sai kích thước xe. |
| 8 | `img_015.jpg` | Ảnh chụp qua kính chắn gió ô tô ướt mưa, đèn hậu xe phía trước bị nhòe và khúc xạ tạo vệt sáng đỏ kéo dài. | R-01, R-09 | - Vẽ box `car` ôm sát khối thân xe mờ phía trước.<br>- Tuyệt đối không kéo dài box theo vệt sáng đèn.<br>- Đặt `occluded_level = 0`, tick `can_review = true`. | Ánh sáng phản xạ và vệt lóe trên kính lái không phải bộ phận vật lý của xe; xe không bị vật khác che nên occlusion là 0; tick review để nhóm thống nhất ranh giới mờ. |
| 9 | `img_017.jpg` | Tượng đài Công tước Wellington cưỡi ngựa đội nón giao thông ở Glasgow, đặt trên bệ đá lớn. | R-07 | **Tuyệt đối KHÔNG gán box** (không gán `person` cho tượng người). | Đây là tác phẩm điêu khắc bằng kim loại/đá tĩnh, không phải con người thật tham gia giao thông. Gán box sẽ gây lỗi báo động giả (false positive). |
| 10 | `img_018.jpg` | Biển quảng cáo (Billboard) in hình chân dung chính khách rất lớn; phía dưới có các xe thật sau hàng rào. | R-03, R-07 | - **KHÔNG gán** `person` cho hình chân dung in trên biển quảng cáo.<br>- Gán từng box `car`/`truck` cho các xe thật phía dưới, đặt `occluded_level = 1` hoặc `2` do hàng rào che. | Hình in 2D trên biển bạt không phải con người thật; các xe thật bên dưới vẫn phải được gán theo đúng nguyên tắc che khuất. |
| 11 | `img_019.jpg` | Xe ô tô vàng tạo hình hoạt hình Danger Mouse trong lễ diễu hành Hamleys; có người thật lái bên trong và mô hình đầu chuột lớn. | R-01, R-04 | - Gán box `car` cho chiếc xe diễu hành màu vàng.<br>- Gán box `person` cho người thật ngồi điều khiển.<br>- Không gán `person` cho phần đầu chuột mô hình. | Xe diễu hành có động cơ và bánh xe di chuyển trên đường công cộng được xếp vào `car`; tách người thật điều khiển với đầu thú bông trang trí. |
| 12 | `img_020.jpg` | Gương chiếu hậu ô tô phản chiếu cầu vồng và các xe phía sau; một phần khung cửa và gương xe chủ. | R-07, R-10 | **KHÔNG gán box** nào cho ảnh này (ảnh âm tính hợp lệ không có nhãn). | Ảnh xe trong gương là phản chiếu quang học 2D, không phải xe thật đang ở vị trí đó; khung gương và cửa xe thuộc về xe chủ (ego vehicle) không gán. |
| 13 | `img_022.jpg` | Xe máy cổ có gắn thùng bên hông (Sidecar) chở người chạy trên đường. | R-01, R-04 | - Gán 1 box `motorcycle` bao trọn cả xe máy và kết cấu thùng sidecar gắn liền.<br>- Gán các box `person` riêng cho người lái và người ngồi trong thùng sidecar. | Sidecar là bộ phận gắn cố định vào xe máy tạo thành một phương tiện duy nhất; hành khách và người lái được gán nhãn `person` độc lập. |
| 14 | `img_026.jpg` | Hai người đội mũ bảo hiểm ngồi trên một xe máy đỏ trong hầm Thủ Thiêm; mép dưới bị cắt; hậu cảnh có tranh tường vẽ cảnh sông nước. | R-01, R-03, R-04, R-07 | - Cụm chính: Gán 1 box `motorcycle` và 2 box `person` riêng cho người lái và người ngồi sau.<br>- Đặt `truncated = yes` cho box bị mép dưới cắt.<br>- Không gán người/thuyền trên tranh tường. | Hai người có thân thể riêng biệt; xe máy là phương tiện riêng; chân người và bánh xe chạm đáy ảnh đặt truncated; loại trừ tranh tường nghệ thuật. |
| 15 | `img_027.jpg` | Khối đá hoa cương tạc hình xe bán tải pickup đặt trên bệ trong nghĩa trang Oak Hill Memorial Park. | R-07 | **Tuyệt đối KHÔNG gán box** (không gán `truck` hay `car`). | Đây là bia mộ điêu khắc bằng đá tĩnh, không có động cơ và không bao giờ tham gia giao thông. |
| 16 | `img_029.jpg` | Xe máy chở một bó thanh kim loại dài quá khổ chạy chéo qua ảnh; người đạp xe đạp bên cạnh. | R-01, R-04, R-06 | - Box `motorcycle` chỉ ôm vừa khít thân xe máy, không kéo theo hai đầu thanh sắt dài nhô ra ngoài.<br>- Box `person` ôm phần đầu và tay nhìn thấy của người lái, đặt `occluded_level = 3`, tick `can_review`.<br>- Gán `person` cho người đi xe đạp bên cạnh. | Tránh làm méo mó aspect ratio của lớp xe máy; người lái bị che gần hết nhưng vẫn nhận biết được người điều khiển. |

---

## 5. Kiểm soát chất lượng (QC) và Quản lý phiên bản

### 5.1. Các ngưỡng kỹ thuật áp dụng
Tuân thủ đầy đủ và nghiêm ngặt 8 ngưỡng kỹ thuật quy định tại `submission/taxonomy.json` và `docs/QC_CHEATSHEET.md`:

| Chỉ số / Đại lượng | Ngưỡng bắt buộc | Mục đích & Ý nghĩa kỹ thuật |
|---|:---:|---|
| Chiều cao box tối thiểu (`min_box_height_px`) | $\ge 20\text{ px}$ | Loại bỏ các đối tượng quá nhỏ hoặc quá xa gây nhiễu tín hiệu mô hình. |
| Ngưỡng IoU cho box lớn (`iou_thr_large`) | $\ge 0.85$ | Áp dụng cho các box có chiều cao $\ge 50\text{ px}$, yêu cầu độ ôm sát rất cao. |
| Ngưỡng IoU cho box nhỏ (`iou_thr_small`) | $\ge 0.70$ | Áp dụng cho các box có chiều cao từ 20 đến dưới 50 px (nới lỏng dung sai). |
| Ngưỡng phân chia kích thước (`large_px`) | $50\text{ px}$ | Ranh giới phân chia giữa đối tượng lớn và đối tượng nhỏ. |
| Độ đồng thuận IoU trung bình (`iaa_iou`) | $\ge 0.85$ | Đo lường độ trùng khớp vị trí hình học giữa 2 người gán nhãn độc lập. |
| Độ đồng thuận gán lớp (`iaa_class`) | $\ge 95\%$ | Đảm bảo tính nhất quán cao về phân loại ngữ nghĩa giữa các thành viên. |
| Tỷ lệ lỗi tối đa theo ảnh (`error_rate_img_max`) | $\le 2.0\%$ | Ngưỡng trần tối đa để ra quyết định Release cho lô dữ liệu. |
| Ngưỡng ghép cặp box (`match_iou`) | $0.50$ | Ngưỡng IoU tối thiểu để thuật toán so khớp xem hai box có cùng trỏ vào một vật thể hay không. |

### 5.2. Quy trình 5 bước tự kiểm tra (Self-Check Checklist) của 147
Trước khi xuất file COCO JSON và commit bản gán nhãn cá nhân, 147 sẽ thực hiện rà soát tuần tự:
1. **Kiểm tra tính có thật của đối tượng (Reality Check):** Đảm bảo 100% box đã vẽ là vật thể thật đang tham gia lưu thông. Không có box nào rơi vào tranh in (`img_018`), tượng đá (`img_017`, `img_027`), ma-nơ-canh (`img_033`), đồ chơi (`img_038`) hoặc bóng phản chiếu (`img_020`).
2. **Kiểm tra độ phân tách người – phương tiện (Separation Check):** Xe máy và người điều khiển/người ngồi sau phải là các box riêng biệt (`motorcycle` và `person`), không được gộp chung.
3. **Kiểm tra độ ôm sát hình học (Tightness Check):** Phóng to ảnh ở mức 100%, kiểm tra các cạnh box không được thừa lề quá 2-3 pixel; không kéo box theo vệt sáng lóa (`img_015`), bóng đổ hoặc thanh hàng quá khổ (`img_029`).
4. **Kiểm tra tính nhất quán thuộc tính (Attributes Consistency):** Mọi box đều phải có `occluded_level` (0, 1, 2, 3) khớp đúng ngưỡng định lượng %; các box chạm biên ảnh phải có `truncated = yes`; các ca nghi ngờ phải được tick `can_review = true`.
5. **Kiểm tra kỹ thuật tự động bằng script:** Chạy lệnh kiểm tra cấu trúc dữ liệu `python scripts/validate_labels.py` để bảo đảm file JSON không vi phạm schema kỹ thuật.

### 5.3. Các vấn đề kiến nghị mang ra thảo luận tại buổi họp Pha 2
1. **Thống nhất phân loại xe bán tải (Pickup truck):** Đề xuất nhóm xếp pickup vào `truck` nếu có thùng hàng hở, và thảo luận tình huống pickup có nắp thùng kín dạng canopy (`img_037`).
2. **Xử lý xe buýt (`img_032`, `img_040`):** Đề xuất nhóm bổ sung lớp `bus` vào `taxonomy.json` ở Pha 2 thay vì bỏ qua, vì xe buýt là phương tiện giao thông trọng yếu.
3. **Quy ước cho xe 3 bánh (Tuk-tuk, Xích lô):** Đề xuất giữ nguyên tắc không gán ép vào `car` hay `motorcycle`; nếu không bổ sung lớp mới thì chỉ gán box cho người ngồi trên xe (`person`).
4. **Quy tắc vẽ box xe chở hàng dài cồng kềnh (`img_029`):** Thống nhất xem box xe máy có bao thanh hàng dài hay chỉ ôm sát thân xe máy để tránh phá hỏng tỷ lệ khung hình chuẩn.

### 5.4. Lịch sử thay đổi phiên bản

| Phiên bản | Ngày | Người thực hiện | Nội dung thay đổi chính | Căn cứ & Lý do thực hiện |
|:---:|:---:|:---:|---|---|
| `v0` | 2026-11-16 | Giảng viên | Bản khởi đầu sơ sài do giảng viên cung cấp. | Tài liệu khung khởi tạo lab, chưa có quy tắc chi tiết. |
| `v0.1` | 2026-11-16 | Thành viên 147 | Xây dựng guideline cá nhân hoàn chỉnh gồm đủ 5 phần theo chuẩn rubric: định nghĩa chi tiết 6 lớp; lượng hóa 4 mức `occluded_level` theo % diện tích; chuẩn hóa 12 quy tắc vẽ box (R-01 đến R-12); phân tích 16 ca khó thực tế từ 40 ảnh; thiết lập 8 ngưỡng QC và quy trình tự kiểm tra 5 bước. | Hoàn thành Pha 1 (nghiên cứu độc lập 40 ảnh, không sao chép của người khác, phát hiện các ca mâu thuẫn để chuẩn bị họp Pha 2). |
