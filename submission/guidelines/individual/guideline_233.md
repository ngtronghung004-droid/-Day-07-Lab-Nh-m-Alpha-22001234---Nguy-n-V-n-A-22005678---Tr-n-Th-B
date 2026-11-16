# GUIDELINE CÁ NHÂN — GÁN NHÃN BOUNDING BOX

**Lab 07: Guideline, Taxonomy & Quality Control**

Nhóm: Alpha
Người thực hiện: Nguyễn Thị Hương Giang
Mã học viên: 2A202603233
Phiên bản: Individual Final v1.0
Phạm vi: 40 ảnh đường phố (data/images/img_001.jpg – img_040.jpg)
Công cụ: CVAT, xuất chuẩn COCO 1.0
Trạng thái: Guideline cá nhân (Pha 1 - Độc lập)

---

## 1. Mục tiêu và phạm vi

Nhãn dùng để huấn luyện mô hình phát hiện người và phương tiện thật đang có mặt ngoài đời trên ảnh đường phố (camera giao thông, xe tự lái).

**Nguyên tắc nền (đọc trước mọi quy tắc khác):**

1. Chỉ gán **vật thật**. Phương tiện thật là xe thật, có thể di chuyển bằng động cơ hoặc sức người. Tượng, ma-nơ-canh, đồ chơi/mô hình, hình in trên áp phích/biển quảng cáo/tranh tường, bia mộ hình xe, điêu khắc dáng xe ghép từ phụ tùng, bóng phản chiếu trên kính, gương hoặc mặt đường **không** phải vật thật → không gán, không dùng `ignore_region`. Ngoại lệ: xe thật trưng bày trong bảo tàng/showroom, xe cổ vẫn là xe thật → gán.
2. Mỗi vật thuộc đúng một lớp.
3. Box ôm sát **phần nhìn thấy** của vật, không đoán phần bị che.
4. Ảnh không có vật nào để gán là **ảnh hợp lệ không có box** (ảnh âm tính), không bỏ ảnh.
5. Không chắc → làm theo quy tắc gần nhất, rồi tick `can_review`.

---

## 2. Lớp

| Lớp | Định nghĩa | Ví dụ gán vào lớp này | KHÔNG gán vào lớp này |
|---|---|---|---|
| `car` | Ô tô con: sedan, hatchback, SUV, taxi con, xe thể thao, xe diễu hành chạy động cơ có hình dạng ô tô. | Mazda, Honda Civic, xe vàng diễu hành (img_019) | Xe bán tải (→ `truck`), xe 12–16 chỗ (→ `van`) |
| `truck` | Xe tải mọi cỡ **và xe bán tải (pickup)**, kể cả pickup gắn mui/thùng kín; xe đầu kéo kèm rơ-moóc; xe tải cổ. | Isuzu, Hilux, xe chở xe (img_002), pickup cổ (img_028), xe tải nhỏ mui bạt (img_036) | Xe van thùng liền khối, xe buýt |
| `van` | Xe thùng kín liền khối, thân cao, **tối đa khoảng 16 chỗ**: van chở hàng, minivan, xe 12–16 chỗ (Hiace, Transit), van taxi. | 51LD-70-65 (img_005), van taxi (img_016) | Xe khách trên 16 chỗ (→ `bus`) |
| `bus` | Xe buýt và xe khách **trên 16 chỗ**: nhiều cửa sổ dọc thân, thường có nhiều hàng ghế. | Xe buýt xanh (img_037), Coaster (img_009) | Van/minivan |
| `motorcycle` | Xe máy, mô tô, xe tay ga, xe máy điện; **kể cả xe có thùng bên hông (sidecar)**. Box bao cả sidecar. | Xe máy đỗ (img_008, 030), xe sidecar (img_022) | Xe đạp, xe ba bánh có cabin/ghế (→ `three_wheeler`) |
| `three_wheeler` | Xe ba bánh có động cơ chở khách/hàng: tuk-tuk, xe lam, xe ba gác máy. | Tuk-tuk (img_004, 016), auto-rickshaw (img_035) | Xích lô đạp (→ `bicycle`) |
| `bicycle` | Xe đạp, kể cả xe đạp ba bánh/xích lô đạp (không động cơ). Box bao toàn xe (gồm ghế khách), **không** gồm người. | Xích lô (img_023), xe đạp (img_039) | Xe đạp điện có động cơ mạnh dáng xe máy (→ `motorcycle`) |
| `person` | Người thật: đi bộ, đứng, ngồi, đang lái hoặc ngồi trên xe nhìn thấy được. | Tài xế xe máy, tài xế tuk-tuk, người đạp xích lô | Tượng, ma-nơ-canh, người trên áp phích, hình nộm/linh vật |
| `ignore_region` | Vùng mà vật thật có mặt nhưng quá dày/nhỏ/dính để gán từng vật (xem 4.6). | Bãi xe máy dày đặc, đám đông dính nhau | Vùng chỉ có vật không thật |

### 2.1 Vật không thuộc lớp nào → không gán

Nón giao thông, biển báo, xe đẩy tay, xe nôi, xe lăn, động vật, hàng hoá, tượng. Không tạo lớp mới cho chúng và không dùng `ignore_region`.

Dự phòng cho ảnh sau này: xe chuyên dụng cỡ tải (bồn, cẩu, ben, cứu hoả) → `truck`; xe công trình/máy cày/xe lu → không gán, tick `can_review`.

**Cây quyết định khi do dự giữa hai lớp:**

- Pickup / bán tải, dù gắn mui kín? → `truck`.
- 12–16 chỗ, thân liền khối? → `van`. Trên 16 chỗ hoặc dáng xe khách/xe buýt? → `bus`. Không đếm được chỗ: nhìn dáng. Còn do dự → `van` + `can_review`.
- Ba bánh có động cơ → `three_wheeler`. Ba bánh đạp → `bicycle`.
- Xe diễu hành/xe độ có dáng ô tô, chạy bằng động cơ → theo dáng (thường `car`), tick `can_review`.

---

## 3. Thuộc tính

| Thuộc tính | Giá trị | Định nghĩa (đã định lượng) |
|---|---|---|
| `occluded_level` | `0` | Thấy ≥ 90% vật (nếu vật không bị cắt mép). |
| | `1` | Thấy 60–90%. |
| | `2` | Thấy 30–60%. |
| | `3` | Thấy 10–30% nhưng vẫn nhận ra lớp nhờ đặc điểm rõ (đèn, bánh, mũ bảo hiểm…). **Bắt buộc tick `can_review`.** |
| `truncated` | `no` / `yes` | `yes` khi vật bị mép ảnh cắt. Mép ảnh chỉ gây `truncated`, **không** tính vào `occluded_level`. Bị vật khác che thì `occluded_level`, không phải `truncated`. |
| `can_review` | tick / không | Tick khi thuộc một trong các trường hợp ở mục 5.2. |

Ước lượng "thấy bao nhiêu %" theo hình dáng toàn vật mà bạn hình dung được. Không có vật nào bị che quá 90% còn được gán (xem 4.3).

---

## 4. Quy tắc vẽ box

### 4.1 Chung

1. Box ôm sát phần nhìn thấy của vật, gồm gương chiếu hậu, tay lái. Không gồm bóng đổ, phản chiếu, dây điện.
2. Cạnh box nằm sát biên vật, sai lệch tối đa 2–3 px khi zoom 100%.
3. Gán đủ vật; không gán vật không thật (nguyên tắc nền 1).
4. Hai vật có box chồng nhau là bình thường (xe máy và người ngồi trên nó, xe này che xe kia). Không cắt box để tránh chồng.

### 4.2 Ngưỡng nhỏ

- Gán khi cạnh dài của box ≥ **40 px** (đo ở ảnh gốc, zoom 100%) **và** còn nhận ra lớp.
- Dưới 40 px, hoặc không nhận ra lớp: không gán. Nếu nằm trong cụm dày (4.6): đưa vào `ignore_region`.

### 4.3 Bị che

- Vẽ box quanh phần **thấy được**, không vẽ phần đoán sau vật che.
- Thấy dưới **10%** vật, hoặc không nhận ra lớp: không gán.
- Thấy 10–30%: gán, `occluded_level=3`, tick `can_review`.
- **Vật che thưa/xuyên thấu** (hàng rào lưới, song sắt thưa, cành lá thưa): vẫn gán nếu nhận ra lớp. `occluded_level` tối thiểu `1`; từ `2` trở lên tick `can_review`. Kính trong suốt của máy ảnh/cửa sổ nơi người chụp đứng thì không tính là vật che.

### 4.4 Bị cắt mép ảnh

- Vẽ box tới sát mép ảnh, `truncated=yes`.
- Dùng cùng ngưỡng 10% với 4.3: chỉ còn một góc bánh, mẩu gương, ngón tay → không gán.
- Ví dụ: xe đỏ ở mép trái và xe bạc ở mép phải của img_015 đều gán, `truncated=yes`.

### 4.5 Người trên/trong xe, vật bị chở

| Tình huống | Quy tắc |
|---|---|
| Người ngồi/lái xe máy, xe đạp, xích lô, xe ba bánh hở | **Mỗi người một box `person`** + một box cho xe (xe không bao người). Hai box chồng nhau là đúng. |
| Một xe máy chở 2–3 người | Mỗi người một box `person`. Người bị che nhiều thì theo 4.3. |
| Người trong **cabin kín** (ô tô, xe tải, van, xe buýt) sau kính | **Không gán** (kính phản chiếu, nhận dạng không ổn định). Ngoại lệ: người thò đầu/thân ra ngoài, nhìn rõ. |
| Người trong khoang hở hoặc xe **không có cửa kính hai bên** (tuk-tuk, auto-rickshaw, xe diễu hành mui trần), kể cả khi nhìn qua kính chắn gió | Gán `person` nếu thấy rõ từ đầu tới ngực trở lên. Chỉ thấy lờ mờ → không gán. |
| Người đạp xích lô và khách ngồi trên đó | Mỗi người một box `person`; xích lô là một box `bicycle`. |
| Hàng hoá trong thùng pickup/xe tải | Không gán (không thuộc lớp nào). |
| **Ô tô được chở trên xe chở xe** | Không gán từng xe: coi là hàng hoá. Chỉ gán box `truck` cho cả xe đầu kéo + giàn/rơ-moóc (một box liền). |
| Xe đầu kéo + rơ-moóc | Một box `truck` bao cả đầu kéo và rơ-moóc nếu đang nối. |
| Tượng/hình nộm/linh vật hình nộm ngồi trên xe | Không gán. Người thật mặc đồ hoá trang nhìn rõ có người bên trong → gán `person`, tick `can_review`. |
| Xe máy đỗ có người thật ngồi hoặc đứng cạnh | Người gán `person` nếu đạt 4.2, xe gán `motorcycle`. Người ngồi trên xe đỗ (không lái) vẫn là `person`. |
| Người dắt xe đạp/xe máy | `person` + xe riêng (`bicycle`/`motorcycle`), hai box chồng nhau. |
| Xe đạp thồ, xe đạp gắn sạp/giỏ bán rong | `bicycle`, box ôm xe đạp. Hàng, sạp, thúng không gán. Xe đẩy tay thuần tuý không có yên/bàn đạp: không gán. |
| Hàng **nhô ra ngoài** xe/người (ống dài vắt qua hai xe, hàng chất cao trên nóc xe ba bánh, đòn gánh + thúng) | Box chỉ ôm thân xe/người, **không** gồm phần hàng nhô ra. Balo, túi đeo sát người thì gồm trong box `person`. |

### 4.6 Dày đặc, nhoè, tối

**`ignore_region`**: dùng khi trong một vùng có nhiều vật thật mà không thể gán hết từng vật theo 4.1–4.4:

- Bãi xe máy đỗ dày, xe chồng chéo, chỉ thấy lờ mờ.
- Đám đông dính nhau, không tách được từng người.
- Cụm vật nhỏ ở xa dưới 40 px.

Quy tắc đi kèm:

1. Vẽ một box bao quanh toàn cụm.
2. Vật nào trong cụm **thấy rõ, tách được, đạt ngưỡng** thì vẫn gán riêng (box chồng lên vùng ignore là bình thường).
3. Vật nào ở ngoài vùng ignore mà tách được thì gán bình thường, đừng đẩy cả ảnh vào một `ignore_region`.
4. Không dùng `ignore_region` để "né" vật khó chỉ vì lười: vật lớn, rõ, riêng lẻ luôn phải gán.
5. **Cảnh đông theo chiều sâu** (giờ cao điểm, hàng xe máy dài): gán từ gần ra xa, vật nào đạt 4.2–4.3 thì gán đủ. Khi quá nửa vật ở một khoảng xa không còn đạt ngưỡng hoặc không tách được, dừng gán và bao phần còn lại bằng `ignore_region`.

**Nhoè chuyển động:**

- Còn nhận ra lớp và biên vật ước lượng được (sai lệch dưới khoảng 20% kích thước) → gán, tick `can_review` nếu biên mơ hồ.
- Chỉ còn vệt mờ không nhận ra lớp → không gán, không ignore (ví dụ phần xe/người bị nhoè ở nền img_014).

**Tối, ngược sáng, đêm:**

- Gán khi nhận ra lớp. Nếu chỉ thấy đèn sáng mà không thấy thân xe → không gán.
- Người ngược sáng/dạng bóng đen: gán nếu còn nhận ra dáng người và đạt 4.2; biên mơ hồ → tick `can_review`.

### 4.7 Phản chiếu và vật "giả"

- Bóng xe trên mặt đường ướt, hình xe/quần áo trong kính, ảnh phản chiếu qua gương xe: không gán.
- Hình người trên áp phích, biển quảng cáo, tranh: không gán.
- Tượng người/động vật, ma-nơ-canh, đồ chơi, xe mô hình, bia mộ hình xe: không gán.
- Xe cổ, xe độ nhưng **là xe thật** → gán theo lớp.
- Điêu khắc dáng xe ghép từ phụ tùng, xe chỉ để trang trí không chạy được: không gán, tick `can_review`.
- Xe thật trưng bày trong nhà (bảo tàng, showroom) → gán theo lớp. Xe đặt trên nóc xe khác như vật trưng bày: xử lý như hàng chở (4.5), không gán, tick `can_review`.
- Tranh tường, biển quảng cáo in cảnh/xe/người: không gán.

### 4.8 Ảnh chụp từ trong xe hoặc qua kính

- Phần xe của người chụp (nội thất, bảng điều khiển, nắp capo, gương) không gán.
- Xe/cảnh nhìn thấy **trong gương chiếu hậu** là phản chiếu → không gán (có thể làm ảnh trở thành ảnh âm tính).
- Ảnh chụp qua kính cửa sổ/kính xe: gán bình thường nếu vật còn rõ; kính bẩn làm biên mơ hồ thì tick `can_review`.

---

## 5. QC

### 5.1 Kiểm tra trước khi nộp một ảnh

- [ ] Mọi vật gán đều là vật thật (không phải tượng/áp phích/phản chiếu).
- [ ] Mọi box đạt ngưỡng 4.2 và 4.3.
- [ ] Người trên xe có box `person` riêng; xe không bao người.
- [ ] Hàng hoá/ô tô bị chở không bị gán.
- [ ] Vùng đông đúc có `ignore_region`, không để sót cả mảng lẫn không gán.
- [ ] `occluded_level` và `truncated` điền cho mọi box.
- [ ] `occluded_level=3` đã tick `can_review`.
- [ ] Hàng nhô ra khỏi xe/người không nằm trong box.
- [ ] Xe/người trong gương, trên tranh, trên điêu khắc không bị gán.

### 5.2 Khi nào bắt buộc tick `can_review`

1. Lưỡng lự giữa hai lớp theo cây quyết định (mục 2).
2. `occluded_level=3`.
3. Vật nhoè mà biên mơ hồ.
4. Xe diễu hành/xe độ/người hoá trang không chắc có phải vật thật.
5. Ranh giới ignore/gán của đám đông hoặc bãi xe không rõ ràng.
6. Mọi trường hợp bạn tự mình phải suy đoán thêm ngoài guideline này.
7. Xe đặt trên xe khác để trưng bày, điêu khắc/xe trang trí không chắc có chạy được.
8. Vật bị che bởi vật thưa ở mức `occluded_level` từ 2 trở lên.

### 5.3 Phiên bản

- Mọi thay đổi làm đổi nhãn (đổi định nghĩa lớp, ngưỡng, thêm/bớt lớp) đều tăng phiên bản guideline và ghi vào mục 7.
- Ca mơ hồ: tick `can_review` và ghi ghi chú để bổ sung vào mục 6 ở phiên bản sau.

---

## 6. Ca khó (tình huống từ 40 ảnh)

Mức `occluded_level` cụ thể do người gán ước lượng theo mục 3.

| Ảnh | Tình huống | Quyết định (quy tắc) |
|---|---|---|
| img_002 | Xe chở xe, ô tô trên giàn, người nhỏ sau rơ-moóc | 1 box `truck` bao đầu kéo + giàn (4.5). Ô tô trên giàn: không gán. Người sau rơ-moóc: gán `person` nếu còn ≥ 10% và ≥ 24 px, kèm `can_review`. |
| img_004 | 2 tuk-tuk ban đêm, nón giao thông | 2 box `three_wheeler`. Tài xế nhìn thấy trong khoang hở: `person` mỗi người. Nón giao thông: không gán. |
| img_005 | Van bị xe máy che, nhiều người cận cảnh bị cắt mép, xe ở mép trái | `van` (occluded theo ước lượng). Mỗi người một `person`, `truncated=yes` nếu bị cắt. `motorcycle` phần thấy được. Xe ở mép trái thấy ít: theo 4.3/4.4 (có thể `occluded_level=3` + `can_review`). |
| img_007 | Pickup trắng, xe tải bị cắt mép, sàn ướt phản chiếu | Pickup → `truck`. Xe tải Isuzu → `truck`, `truncated=yes`. Phản chiếu: không gán. |
| img_008 | Bãi xe máy đỗ, người áo cam ngồi xe, người và xe ở xa, xe buýt xa | `motorcycle` + `person` cho xe và người rõ. Dãy xe phía trong chồng chéo → `ignore_region`. Cụm người xa → ignore hoặc bỏ nếu < 24 px. Xe buýt xa: `bus` nếu ≥ 24 px. |
| img_009 | Xe khách cỡ nhỏ (Coaster), vật nhỏ ở xa | Xe khách → `bus` (trên 16 chỗ). Xe máy, người xa gán nếu ≥ 24 px, còn lại bỏ. |
| img_012 | Pickup cận cảnh có hàng, xe Mazda, xe tải mờ phía sau | Pickup cận cảnh `truck`, `truncated=yes`; hàng trong thùng không gán. Mazda → `car`. Xe tải mờ phía sau: `truck` theo 4.3. |
| img_014 | 2 người rõ, nền nhoè | 2 `person`. Người/xe nhoè ở nền: không gán (4.6). |
| img_015 | Xe bị cắt mép, xe nhoè, bóng xe trên đường ướt | 2 box `car` cận cảnh (`truncated=yes`). Xe nền thấy rõ: `car`. Xe nhoè chuyển động: gán nếu nhận ra lớp, kèm `can_review`. Bóng phản chiếu trên đường: không gán (4.7). |
| img_016 | 2 tuk-tuk (1 cắt mép), van taxi, xe máy + người, người cận cảnh cắt mép, xe đen bị che | `three_wheeler` ×2; `van`; `motorcycle` + `person`; `person` cận cảnh (`truncated=yes`); xe đen bị che theo 4.3. |
| img_017 | Tượng người cưỡi ngựa, nón giao thông | Ảnh âm tính: tượng không phải vật thật, không gán. |
| img_019 | Xe diễu hành vàng, tài xế, linh vật chuột, đám đông sau rào | Xe vàng → `car`, `can_review`. Tài xế → `person`. Linh vật hình nộm: không gán. Người rõ hàng đầu gán `person`; phần đông dính nhau sau rào → `ignore_region`. |
| img_022 | Ảnh đen trắng tư liệu, xe sidecar nhỏ | `motorcycle` (box bao cả sidecar). Người ngồi: `person` nếu ≥ 24 px. Ảnh đen trắng vẫn gán bình thường. |
| img_023 | Ô tô, xích lô có người đạp, xe máy xa, dãy xe đỗ | `car`; `bicycle` (box bao xích lô) + `person` người đạp; xe máy rõ gán, dãy xe đỗ dày → `ignore_region`. |
| img_025 | Người đi bộ, xe ở xa, người nằm ghế trên bãi biển nhỏ, thân cọ che | `person` đi bộ rõ. Taxi/xe xa: gán nếu ≥ 24 px. Xe máy kéo thùng xa: `motorcycle` hoặc `three_wheeler` theo dáng, `can_review`. Cụm người trên bãi biển nhỏ → `ignore_region`. Thân cọ che: theo 4.3. |
| img_027 | Bia mộ đá hình xe bán tải, người xa | Ảnh âm tính: bia mộ không phải xe thật (4.7). Người rất xa < 24 px: bỏ. |
| img_028 | Xe bán tải cổ, tượng ngựa trên thùng, xe đỏ bị che | Xe cổ → `truck` (là xe thật). Tượng ngựa: không gán. Xe đỏ phía sau → `car`, theo 4.3. |
| img_030 | Bãi xe máy dày đặc, người áo xanh, áp phích có mặt người | `motorcycle` gán các xe rõ, khối còn lại → `ignore_region`. Người áo xanh → `person`. Mặt trên áp phích: không gán. |
| img_032 | Đám đông chờ xe, xe xanh cắt mép, nón giao thông | `car` xanh `truncated=yes`. Người đứng tách được gán `person`; nhóm dính nhau → `ignore_region`. Nón: không gán. Xe trắng sau đám đông: theo 4.3. |
| img_033 | Ma-nơ-canh, ảnh phản chiếu qua kính, gương xe | Ảnh âm tính: ma-nơ-canh và phản chiếu không phải vật thật. |
| img_034 | Người đi bộ, xe đen, xe máy + người, người lái cận cảnh cắt mép, ngược sáng | `person` đi bộ; `car`; `motorcycle` + `person`; người lái cận cảnh `truncated=yes`. Xe nhỏ xa: gán nếu ≥ 24 px. |
| img_037 | Pickup gắn mui kín, xe buýt xanh (một xe bị che), người đi xa | Pickup mui kín → `truck`. Xe buýt → `bus`. Người ở xa: gán nếu ≥ 24 px. |
| img_038 | Xe mô hình, vịt cao su, đồ chơi sau kính | Ảnh âm tính: toàn đồ chơi/mô hình (4.7). |
| img_039 | Xe máy đỗ bị che, người nhỏ, xe đạp xa, hình trên biển quảng cáo | `motorcycle` đỗ; `person`/`bicycle`/`motorcycle` xa gán nếu ≥ 24 px. Hình người trên biển: không gán. |
| img_001 | Pickup nhỏ nhìn từ phía sau, ống thép trong thùng; nhiều người ngồi quán bị xe che; người đứng cắt mép dưới; áp phích hình đồ ăn | `truck` (ống/hàng không gán). Mỗi người ngồi quán là `person` (bị xe che theo 4.3). Người đứng bên trái `truncated=yes`. Áp phích: không gán. |
| img_003 | Người dắt xe đạp, người gánh hàng bằng đòn gánh, xe máy đỗ xa, người cắt mép trên | Mỗi người `person`, người dắt có `bicycle` riêng. Box người gánh không gồm thúng/đòn gánh (4.5). Người cắt mép trên `truncated=yes`. Xe máy xa: gán xe rõ, còn lại `ignore_region`. |
| img_006 | Giờ cao điểm, nhiều xe máy nhìn từ phía sau, xe đạp, taxi cắt mép trái | Mỗi xe máy một `motorcycle`, mỗi người (kể cả người ngồi sau) một `person`. Xe đạp + người đạp. Taxi `car`, `truncated=yes`. Vật xa < 24 px: bỏ hoặc `ignore_region`. |
| img_010 | Chợ, xe đạp thồ có rau, người ngồi trên xe máy đỗ, hàng treo (mũ, túi, búp bê) | Mỗi người `person` (kể cả người ngồi xe đỗ), mỗi xe máy `motorcycle`. Xe đạp thồ → `bicycle` (rau không gán). Hàng treo, búp bê: không gán. |
| img_011 | Lễ hội: tượng đầu báo khổng lồ cận cảnh, điêu khắc dáng xe máy bằng kim loại, người xa, SUV bị che | Tượng và điêu khắc dáng xe: không gán (4.7), `can_review`. Người xa gán nếu ≥ 24 px, nhóm dính → `ignore_region`. SUV bị che: `car` theo 4.3. |
| img_013 | Đêm, đường ướt, xe nhỏ ở xa, xe máy + người, 2 người đi bộ, nhiều nón giao thông, tượng vàng | `car`, `motorcycle` + `person`, `person` đi bộ nếu ≥ 24 px. Nón, tượng, vệt sáng phản chiếu: không gán. Xe chỉ thấy đèn: bỏ. |
| img_018 | Chụp qua kính, biển quảng cáo có mặt người, xe đỗ sau hàng rào lưới | Mặt trên biển: không gán. Xe sau rào: `car`, `occluded_level` tối thiểu 1 (vật che thưa, 4.3). |
| img_020 | Chụp từ trong xe: gương chiếu hậu ướt, nội thất | Ảnh âm tính (4.8): xe trong gương là phản chiếu, nội thất/xe người chụp không gán. |
| img_021 | Giờ cao điểm, hàng chục xe máy + người dày đặc, ô tô bên trái cắt mép, xe buýt xa | Theo 4.6 mục 5: gán xe máy + người từ gần ra xa; phần xa dính nhau → `ignore_region`. `car` `truncated=yes`. `bus` xa nếu ≥ 24 px. |
| img_024 | Bảo tàng xe cổ trong nhà, ô tô vàng đặt trên nóc ô tô đen, xe cam cắt mép | Xe cổ thật → `car`. Xe vàng trên nóc: vật trưng bày, không gán, `can_review` (4.7). Xe cam cắt mép `truncated=yes`. Dãy xe xa: gán xe rõ, còn lại `ignore_region`. |
| img_026 | Đêm, 2 người trên xe máy đỏ cắt mép, tranh tường in cảnh cảng biển | `motorcycle` + 2 `person` (người sau bị che), `truncated=yes`. Tranh tường: không gán. |
| img_029 | Ảnh gần đen trắng: người đi xe máy và người đạp xe đạp cùng chở một ống dài vắt qua hai xe | `motorcycle` + `person`; `bicycle` + `person`. Ống dài không gồm trong box (4.5). Người/xe xa gán nếu ≥ 24 px. |
| img_031 | Đêm mưa, đường ướt phản chiếu đèn, xe con, xe buýt, người dạng bóng đen, xe máy xa | `car`, `bus`, `motorcycle`, `person` nếu nhận ra và ≥ 24 px. Vệt đèn và phản chiếu: không gán. Vật bị cột che: 4.3. Biên mơ hồ: `can_review`. |
| img_035 | Auto-rickshaw chở hàng chất cao quá khổ, xe máy, ô tô, auto khác | `three_wheeler`, hàng chất trên nóc không gồm (4.5). Tài xế qua kính chắn gió: `person` nếu thấy rõ (xe không có cửa kính hai bên). `motorcycle` + `person`; `car`. |
| img_036 | Xe tải nhỏ mui bạt xanh, biển số bị làm mờ, dãy xe máy đỗ bên trái | `truck`, box bao cả thùng bạt. Biển số bị làm mờ không ảnh hưởng nhãn. Dãy xe máy: gán xe rõ, còn lại `ignore_region`. |
| img_040 | Người đội mũ bảo hiểm cận cảnh cắt mép, chỉ thấy hai gương xe máy, taxi xanh-đỏ bị người che, tuk-tuk taxi, SUV, xe buýt xa | `person` cận cảnh `truncated=yes`. Xe máy chỉ thấy hai gương (< 10%): không gán (4.4). Taxi xanh-đỏ `car` bị che. Tuk-tuk `three_wheeler`. SUV `car`. Xe buýt xa `bus`. |

---

## 7. Lịch sử thay đổi

| Phiên bản | Thay đổi |
|---|---|
| v0 | Bản khởi đầu của giảng viên. |
| v1 | Thêm lớp: bus, three_wheeler, bicycle (đã cân nhắc và loại: xe đẩy/xe thồ, nón giao thông, động vật, gánh hàng). Định nghĩa lại: truck gồm pickup; van ≤ 16 chỗ; motorcycle gồm sidecar. Thêm nguyên tắc chỉ gán vật thật có thể di chuyển (loại tượng, ma-nơ-canh, đồ chơi, áp phích, tranh tường, điêu khắc/xe trang trí, phản chiếu; giữ xe trưng bày thật). Định lượng: ngưỡng 24 px, ngưỡng thấy 10%, 4 mức occluded_level. Thêm quy tắc người/vật bị chở, người dắt xe, xe đạp thồ, hàng nhô ra khỏi xe/người không tính vào box, vật che thưa (rào lưới), phân biệt cabin kín và xe không có cửa kính, ignore_region (gồm cảnh đông theo chiều sâu), nhoè, người ngược sáng, ảnh âm tính, ảnh chụp từ trong xe/qua kính/gương chiếu hậu (mục 4.8). Thêm mục 2.1 vật không thuộc lớp nào và mục QC có danh sách kiểm tra và 8 điều kiện bắt buộc tick can_review. Điền mục 6 "Ca khó" bằng 40 ảnh. |
