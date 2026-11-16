# Guideline gán nhãn — v0.1 — 176 - Bùi Kim Trại

- Phiên bản: v0.1 (bản guideline cá nhân đề xuất)
- Ngày: 2026-11-16
- Người thực hiện: Bùi Kim Trại (MSHV: 2A202603176)
- Nhóm: Alpha
- Công cụ: CVAT, xuất COCO 1.0

---

## 1. MỤC TIÊU VÀ PHẠM VI

### 1.1. Mục tiêu

Xây dựng hệ thống quy tắc gán nhãn Bounding Box có tính chính xác, nhất quán và dễ kiểm tra cho các đối tượng người và phương tiện xuất hiện trong ảnh đường phố châu Á.

Các quy tắc nhằm giải quyết triệt để sự mơ hồ của guideline v0, đặc biệt đối với những tình huống như phương tiện có hình dạng đặc biệt, đối tượng bị che khuất, bị cắt bởi mép ảnh, nhiều đối tượng chồng lấn, vệt sáng lóa ban đêm/mưa, và các hình ảnh không phải đối tượng thật (tượng, tranh quảng cáo, ma-nơ-canh).

Dữ liệu được sử dụng để huấn luyện và đánh giá mô hình Object Detection (phục vụ hệ thống hỗ trợ lái xe hoặc camera giao thông thông minh). Việc gán nhãn không chính xác có thể gây ra ba nhóm lỗi nguy hiểm:
- **Bỏ sót đối tượng (False Negative):** Phương tiện tự hành bỏ qua vật cản, dẫn đến nguy cơ va chạm.
- **Gán thừa đối tượng (False Positive):** Nhận nhầm hình in quảng cáo, tượng đá, bóng phản chiếu là người/xe thật khiến hệ thống phanh gấp bất ngờ.
- **Phân loại sai (Classification Error):** Nhầm lẫn giữa người và phương tiện, hoặc giữa xe con và xe tải làm sai lệch dự đoán hành vi.

### 1.2. Phạm vi

Bộ dữ liệu gồm 40 ảnh, từ `img_001.jpg` đến `img_040.jpg`.

Chỉ sử dụng các lớp được định nghĩa trong taxonomy đang áp dụng. Không tự ý tùy tiện bổ sung lớp trong quá trình gán nhãn nếu chưa có quyết định thống nhất của nhóm trong Pha 2.

Các vùng ngoài phạm vi nhận diện hoặc đám đông không thể tách instance cần được phân biệt rõ với vùng `ignore_region` để tránh nhầm lẫn giữa việc không yêu cầu gán một loại đối tượng và việc bỏ qua một vùng khó xử lý.

---

## 2. LỚP ĐỐI TƯỢNG VÀ THUỘC TÍNH

### 2.1. Định nghĩa lớp

| Lớp | Định nghĩa đề xuất | Ví dụ điển hình | Phản ví dụ / Dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con từ 4–9 chỗ, sedan, hatchback, SUV, coupe, crossover, wagon. | Xe taxi sedan (`img_040`), xe SUV gia đình, AMC wagon (`img_024`). | Xe bán tải (pickup), xe van thùng kín, xe buýt lớn. |
| `truck` | Xe vận tải chở hàng có kết cấu cabin và thùng chở hàng tách biệt, xe bồn, xe đầu kéo, xe chuyên dụng chở xe con. | Xe tải chở hàng (`img_007`), xe tải chuyên chở ô tô (`img_002`), xe tải nhẹ Veryca (`img_036`). | Xe van chở hàng thân liền khối, xe bán tải nhỏ không có thùng riêng biệt. |
| `van` | Xe dạng hộp kín cỡ nhỏ/trung bình, thân xe và khoang hành khách/hàng hóa tương đối liền khối. | Xe minivan chở khách, xe cứu thương cỡ nhỏ, xe chuyển phát bưu kiện dạng van. | Xe buýt lớn nhiều chỗ, xe SUV cỡ lớn, xe tải thùng kín rời cabin. |
| `motorcycle` | Xe máy hai bánh có động cơ, xe gắn máy, xe tay ga (scooter), xe phân khối lớn. | Xe tay ga, xe số của người dân trên đường (`img_005`, `img_026`, `img_030`). | Xe đạp không động cơ, xe ba bánh tuk-tuk, xe xích lô đạp. |
| `person` | Người thật (bất kể đang đi bộ, đứng, ngồi, lái xe hay người hóa trang). | Người đi bộ qua đường (`img_014`), người điều khiển xe máy (`img_005`), người hóa trang nhân vật (`img_011`). | Tượng người điêu khắc (`img_017`), người in trên biển quảng cáo (`img_018`), ma-nơ-canh (`img_033`), bóng phản chiếu trong gương (`img_020`). |
| `ignore_region` | Vùng không yêu cầu phân tách từng đối tượng riêng lẻ do quá nhỏ, quá xa, quá dày đặc hoặc thuộc đối tượng không gán. | Cụm đám đông người/xe ở hậu cảnh quá mờ hoặc chiều cao < 20 px. | Không dùng `ignore_region` để che lấp các ca khó lẽ ra phải gán box. |

### 2.2. Quy tắc phân biệt phương tiện

- **CLS-01 — Phân biệt Car và Truck:**
  Đề xuất sử dụng cấu tạo khung sườn và mục đích thiết kế, không chỉ dựa vào kích thước. Xe sedan, hatchback, wagon và SUV thuộc `car`. Xe tải có khoang chở hàng riêng biệt thuộc `truck`. Đối với xe bán tải (pickup) như trong `img_001`, `img_012`, `img_037`: đề xuất xếp vào `truck` nếu có thùng chở hàng hở lộ thiên nằm sau cabin độc lập; nếu có nắp đậy liền khối dạng SUV thì xem xét trong thảo luận Pha 2.
- **CLS-02 — Phân biệt Truck và Van:**
  Xe van có kết cấu thân hộp kín liền khối từ cabin ra sau. Xe tải có sự phân tách rõ giữa cabin lái và chassis/thùng hàng độc lập phía sau. Không phân loại chỉ bằng màu sơn hay số cửa.
- **CLS-03 — Phân biệt Motorcycle và phương tiện ba bánh (Tuk-tuk, Xích lô):**
  Chỉ gán `motorcycle` cho phương tiện hai bánh có động cơ. Tuk-tuk (`img_004`, `img_035`) và xích lô (`img_006`, `img_009`, `img_023`, `img_034`) có 3 bánh và kết cấu khác biệt, đề xuất coi là phương tiện ngoài taxonomy v0 hiện tại (tạm thời không gán hoặc ghi nhận họp Pha 2 để thống nhất có bổ sung lớp/quy ước riêng hay không).
- **CLS-04 — Phương tiện không có lớp tương ứng (Xe buýt, Xe đạp):**
  Xe buýt lớn (`img_032`, `img_040`) và xe đạp chở hàng rong (`img_010`) không có lớp trong taxonomy gốc. Tuyệt đối không ép xe buýt vào `car` hay ép xe đạp vào `motorcycle`. Cần giữ nguyên tắc "ngoài taxonomy thì không gán gượng ép", tick `can_review` để mang ra họp Pha 2.

### 2.3. Thuộc tính

**ATTR-01 — `occluded_level` (Mức độ che khuất):**
Xác định dựa trên tỷ lệ phần trăm diện tích đối tượng bị các vật thể khác (cột đèn, cây cối, xe khác, hàng hóa) che chắn trước tầm nhìn:
- `0`: Không bị che khuất (thấy rõ trọn vẹn 100% thân thể/phương tiện).
- `1`: Bị che nhẹ, tỷ lệ che từ 1% đến 25%.
- `2`: Bị che trung bình/nhiều, tỷ lệ che từ trên 25% đến 75%.
- `3`: Bị che khuất nghiêm trọng, tỷ lệ che trên 75% nhưng vẫn đủ đặc trưng nhận dạng rõ đối tượng.
*(Lưu ý: Ảnh mờ, tối do thiếu sáng hoặc lóa vệt sáng không tính là occlusion nếu không có vật thể che chắn phía trước).*

**ATTR-02 — `truncated` (Cắt mép ảnh):**
- `no`: Toàn bộ ranh giới đối tượng nằm trọn vẹn trong khung hình.
- `yes`: Một phần đối tượng bị cắt ngang bởi 1 trong 4 biên ảnh (trên, dưới, trái, phải).

**ATTR-03 — `can_review` (Đánh dấu cần xem lại):**
- Tick `true`: Khi gặp tình huống chưa có tiền lệ trong guideline, phương tiện nằm ở ranh giới giữa 2 lớp (như xe bán tải, xe xích lô, xe buýt), hoặc mức độ che quá khó xác định.

---

## 3. QUY TẮC VẼ BOUNDING BOX

- **BOX-01 — Nguyên tắc bao sát hình học (Tight Bounding Box):**
  Box là hình chữ nhật có các cạnh song song trục toạ độ ảnh. Box phải ôm sát ranh giới vật lý nhìn thấy của đối tượng, không chừa khoảng trống nền thừa thãi. Không vẽ box trùm theo bóng đổ trên mặt đường, quầng sáng đèn xe hay vệt sáng lóe.
- **BOX-02 — Đối tượng bị che khuất (Visible Bounding Box):**
  Vẽ box bao trọn phần nhìn thấy của đối tượng. Nếu đối tượng bị một vật mỏng (như cột đèn, dây điện) chắn ngang chia cắt thành 2 vùng nhìn thấy, vẫn chỉ vẽ **DUY NHẤT 1 Bounding Box** bao trọn cả hai phần đó nếu xác định chúng thuộc cùng một instance vật lý. Không kéo box suy đoán vào vùng bị che khuất hoàn toàn.
- **BOX-03 — Đối tượng bị cắt bởi mép ảnh:**
  Box dừng ngay sát mép ảnh, không vẽ tràn ra ngoài hoặc suy đoán phần nằm ngoài màn hình; đặt `truncated = yes`.
- **BOX-04 — Người điều khiển và phương tiện (Chồng lấn instance):**
  Người lái và xe là hai đối tượng độc lập. Vẽ 1 box `motorcycle` cho xe máy và 1 box `person` riêng biệt cho từng người ngồi trên xe. Hai box này được phép chồng đè tự nhiên lên nhau theo đúng hình thể thực tế.
- **BOX-05 — Xe chuyên dụng chở phương tiện khác (Car carrier):**
  Trong trường hợp xe tải chở nhiều xe con (`img_002`), vẽ 1 box `truck` cho xe tải lớn bên dưới, và vẽ các box `car` độc lập cho từng chiếc ô tô con đặt trên giá chở (nếu ô tô con đó nhìn thấy rõ và đạt kích thước tối thiểu).
- **BOX-06 — Ngưỡng kích thước tối thiểu (Min Box Height):**
  Chiều cao tối thiểu của bounding box là **20 pixel** trên độ phân giải gốc của ảnh. Đối tượng nhỏ hơn 20 px không gán box riêng lẻ; nếu tụ tập thành cụm thì khoanh `ignore_region`.
- **BOX-07 — Đám đông xe máy và người đi lại:**
  Nếu các phương tiện chen chúc nhau ở ngã tư (`img_005`, `img_030`) nhưng còn phân biệt rõ từng đầu xe, thân xe $\rightarrow$ gán box riêng từng xe và người, đặt `occluded_level = 2` hoặc `3`. Nếu ở quá xa và dính chùm không thể tách rời $\rightarrow$ vẽ một vùng `ignore_region`.
- **BOX-08 — Hình in, tranh ảnh, tượng điêu khắc và ma-nơ-canh:**
  **Tuyệt đối không gán nhãn** cho tranh ảnh in trên poster, billboard, biển quảng cáo (`img_018`), tượng đài người/xe bằng đá hay kim loại (`img_017`, `img_027`), ma-nơ-canh trong cửa hàng thời trang (`img_033`), và ô tô/búp bê đồ chơi trong tủ kính (`img_038`).
- **BOX-09 — Vệt sáng lóe đèn xe, vệt mờ chuyển động (Motion Blur / Glare):**
  Khi chụp ảnh đêm hoặc trời mưa (`img_013`, `img_015`, `img_031`), đèn xe di chuyển nhanh tạo ra các vệt sáng kéo dài (light streaks) hoặc quầng lóa trên kính ướt. Box của phương tiện chỉ ôm sát kết cấu thân xe thực tế nhìn thấy được, **tuyệt đối không kéo dài box để nuốt các vệt sáng lóe**. Nếu xe bị nhòe hoàn toàn chỉ còn lại vệt sáng không rõ thân xe thì không gán box.
- **BOX-10 — Xe chở hàng cồng kềnh, quá khổ:**
  Đối với xe máy chở bó hàng cồng kềnh khổng lồ (`img_029`) hoặc xe bán tải chở đầy hàng (`img_012`):
  - Box phương tiện (`motorcycle`/`truck`) phải ôm trọn cả phần thân xe và khối hàng hóa gắn liền trên xe, vì khối hàng lúc này trở thành một phần chiếm dụng không gian của phương tiện khi tham gia giao thông.
  - Người lái bị khối hàng che khuất: vẽ box `person` cho phần cơ thể nhìn thấy, đặt `occluded_level = 2` hoặc `3`.

---

## 4. DANH MỤC CA KHÓ (EDGE CASES) ĐỐI CHIẾU THỰC TẾ TRÊN 40 ẢNH

Dưới đây là các ca khó thực tế được phát hiện trực tiếp khi khảo sát 40 ảnh trong thư mục `data/images/`, kèm quyết định xử lý và căn cứ cụ thể:

| STT | Ảnh | Tình huống thực tế quan sát được | Mã quy tắc | Quyết định cá nhân | Căn cứ & Lý do |
|---|---|---|---|---|---|
| 1 | `img_029.jpg` | **Xe máy chở hàng cồng kềnh khổng lồ**: Người lái xe máy chở kiện hàng khổng lồ cao vượt đầu, che kín gần như toàn bộ xe và thân sau của người lái. | BOX-10, ATTR-01 | - Gán `motorcycle` ôm trọn cả xe và khối hàng gắn liền.<br>- Gán `person` ôm phần đầu và tay nhìn thấy của người lái, đặt `occluded_level = 3`. | Khối hàng gắn liền tham gia giao thông cùng xe, cần cảnh báo khoảng không gian chiếm dụng; người lái bị che $>75\%$ nhưng vẫn nhận dạng rõ là người điều khiển. |
| 2 | `img_015.jpg` | **Phương tiện bị lóa vệt sáng, mưa nhòe kính lái**: Ảnh chụp qua kính ô tô ướt mưa, đèn hậu xe phía trước bị nhòe tạo vệt sáng đỏ lóa kéo dài. | BOX-01, BOX-09 | - Vẽ box `car` ôm sát khối thân xe mờ nhìn thấy.<br>- Không kéo dãn box theo vệt sáng đèn kéo dài.<br>- Đặt `occluded_level = 0`, tick `can_review = true`. | Ánh sáng phản xạ và vệt lóe trên kính không phải bộ phận vật lý của xe. Không bị vật khác che chắn nên occlusion là 0; đánh dấu review để nhóm xem lại ranh giới thân xe mờ. |
| 3 | `img_013.jpg` | **Vệt đèn xe chạy nhanh ban đêm trên đường ướt**: Phố đêm ướt mưa có vệt đèn xe chuyển động nhòe (motion blur) và ánh đèn phản chiếu trên vũng nước. | BOX-09 | - Chỉ gán box cho các phương tiện đỗ hoặc đi chậm có thân xe rõ ràng.<br>- Bỏ qua vệt sáng đèn nhòe kéo dài không xác định được thân xe vật lý. | Tránh làm mô hình học sai rằng vệt sáng trên mặt đường là phương tiện giao thông. |
| 4 | `img_017.jpg` | **Tượng đài người cưỡi ngựa (Duke of Wellington)**: Bức tượng điêu khắc người đội nón giao thông cưỡi ngựa trên bệ đá lớn. | BOX-08 | **Không gán box** (không gán `person`). | Đây là tác phẩm điêu khắc bằng kim loại/đá, không phải thực thể người thật tham gia giao thông. |
| 5 | `img_018.jpg` | **Hình người in trên biển quảng cáo (Billboard)**: Biển quảng cáo chính trị bên đường có in hình ảnh một người đàn ông rất lớn. | BOX-08 | **Không gán box** (không gán `person`). | Đây là mặt phẳng tranh in 2D, nếu gán sẽ gây lỗi nhận diện nhầm (false positive) nghiêm trọng cho xe tự lái. |
| 6 | `img_033.jpg` | **Ma-nơ-canh trong tủ kính thời trang**: Ma-nơ-canh mặc áo quần đứng sau vách kính cửa hàng. | BOX-08 | **Không gán box** (không gán `person`). | Ma-nơ-canh là vật thể trưng bày tĩnh, không phải con người. |
| 7 | `img_027.jpg` | **Tượng đài xe bán tải bằng đá hoa cương**: Khối đá tạc hình dáng chiếc xe pickup trong nghĩa trang tưởng niệm. | BOX-08 | **Không gán box** (không gán `truck` hay `car`). | Đây là khối đá điêu khắc tĩnh, không có động cơ và không tham gia giao thông. |
| 8 | `img_002.jpg` | **Xe chuyên dụng chở nhiều ô tô (Car carrier)**: Xe tải Renault chở nhiều tầng ô tô con trên khung giá. | BOX-05, CLS-01 | - Gán 1 box `truck` cho xe tải chuyên dụng lớn.<br>- Gán từng box `car` độc lập cho các xe con trên giá chở nếu nhìn thấy rõ thân xe $\ge 20\text{px}$. | Tách bạch giữa phương tiện vận tải và hàng hóa là các phương tiện độc lập có hình thái nhận dạng rõ ràng. |
| 9 | `img_004.jpg` | **Hai xe Tuk-tuk đỗ bên lề đường**: Phương tiện 3 bánh chở khách đặc trưng ở Thái Lan. | CLS-03 | Tạm thời **không gán box**, tick `can_review` để mang ra họp Pha 2. | Không thuộc định nghĩa `car` (4 bánh) cũng không phải `motorcycle` (2 bánh). Chờ nhóm thống nhất có bổ sung lớp `tuktuk` hay không. |
| 10 | `img_011.jpg` | **Người mặc trang phục cosplay Predator**: Người thật mặc bộ đồ hóa trang quái vật cồng kềnh đứng cạnh hàng xe mô tô. | CLS-01 | **Vẫn gán box `person`** ôm sát người hóa trang. | Dù mặc trang phục kỳ dị nhưng đây là một con người thực thể sống đang di chuyển, hệ thống lái xe bắt buộc phải phát hiện để phòng tránh va chạm. |

---

## 5. KIỂM SOÁT CHẤT LƯỢNG VÀ QUẢN LÝ PHIÊN BẢN

### 5.1. Ngưỡng QC áp dụng

Tuân thủ nghiêm ngặt các ngưỡng kỹ thuật quy định trong `submission/taxonomy.json` và `docs/QC_CHEATSHEET.md`:

| Đại lượng / Chỉ số | Ngưỡng bắt buộc | Mục đích kiểm soát |
|---|---|---|
| Chiều cao box tối thiểu (`min_box_height_px`) | $\ge 20\text{ px}$ | Loại bỏ các đối tượng quá nhỏ gây nhiễu mô hình |
| Ngưỡng IoU box lớn ($\ge 50\text{ px}$) | $\ge 0.85$ | Đảm bảo box ôm sát đối tượng ở cự ly gần và trung bình |
| Ngưỡng IoU box nhỏ ($20 - 50\text{ px}$) | $\ge 0.70$ | Nới lỏng dung sai hợp lý cho đối tượng ở cự ly xa |
| Độ đồng thuận IoU trung bình IAA (`iaa_iou`) | $\ge 0.85$ | Đảm bảo hai người gán độc lập vẽ box đồng đều |
| Độ đồng thuận gán lớp IAA (`iaa_class`) | $\ge 95\%$ | Đảm bảo hai người thống nhất cao về phân loại |
| Tỷ lệ lỗi tối đa theo ảnh để Release | $\le 2.0\%$ | Ngưỡng chấp nhận bàn giao lô dữ liệu gán nhãn |

### 5.2. Quy trình tự kiểm tra annotation cá nhân

Trước khi xuất file COCO JSON và commit lên GitHub:
1. **Kiểm tra độ đầy đủ:** Đảm bảo tất cả người và xe hợp lệ trong các ảnh được phân công đều đã có box.
2. **Kiểm tra độ chính xác nhãn:** Phân biệt đúng `car`, `truck`, `motorcycle`, `person`. Tuyệt đối không gán tượng, ma-nơ-canh, tranh quảng cáo.
3. **Kiểm tra độ ôm sát:** Box ôm vừa khít thân xe/người, không thừa lề và không bao gồm vệt sáng lóa hoặc bóng đổ.
4. **Kiểm tra thuộc tính:** `occluded_level` đúng định lượng % (0, 1, 2, 3); `truncated` đúng với các vật chạm biên ảnh.
5. **Chạy script kiểm tra:** Chạy lệnh `python scripts/validate_labels.py --all` và khắc phục 100% lỗi trước khi push.

### 5.3. Xử lý các ca bất đồng trong Pha 2 và Pha 5

- **Trong Pha 2 (Họp thống nhất nhóm):** Mang các ca khó chưa chốt (như Tuk-tuk trong `img_004`, Xe buýt trong `img_032`, Xe bán tải Pickup trong `img_001`/`img_012`) ra thảo luận với nhóm để thống nhất bổ sung quy tắc vào `guideline_v1.0_agreed.md` và cập nhật `taxonomy.json`.
- **Trong Pha 5 (Calibration):** Đối chiếu các ca lệch trong `calibration_candidates.csv` sau khi đo IAA, phân tích nguyên nhân (do guideline mơ hồ hay do cá nhân gán sót/sai) để hoàn thiện `guideline_v1.1_calibrated.md`.

### 5.4. Lịch sử thay đổi

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của đề bài | Chưa có quy tắc ca khó và ngưỡng đo lường |
| v0.1 | Bổ sung định nghĩa chi tiết các lớp, phân biệt car/truck/van, định lượng 4 mức `occluded_level`, bổ sung 10 quy tắc vẽ box và 10 ca khó thực tế từ 40 ảnh | Khảo sát 40 ảnh thực tế: xử lý xe chở hàng cồng kềnh (`img_029`), vệt sáng lóa (`img_013`/`img_015`), loại trừ tượng đài (`img_017`/`img_027`), tranh in (`img_018`), ma-nơ-canh (`img_033`), đề xuất phân tách xe chở xe (`img_002`), tuk-tuk (`img_004`) |
