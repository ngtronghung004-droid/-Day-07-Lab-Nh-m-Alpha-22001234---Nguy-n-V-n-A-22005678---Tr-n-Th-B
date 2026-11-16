# Guideline gán nhãn cá nhân — Ngô Thị Minh Quang

- MSHV: 2A202603146.
- Mã thành viên: 146.
- Phiên bản: individual-v0.7.
- Ngày: 16/11/2026.
- Công cụ gán nhãn: CVAT; xuất COCO 1.0.

## 1. Mục tiêu

Tôi xây dựng quy tắc gán bounding box cho người và phương tiện trong bộ 40 ảnh đường phố. Nhãn được dùng để huấn luyện mô hình phát hiện đối tượng, chẳng hạn trong camera giao thông hoặc hệ thống hỗ trợ lái xe.

Tôi chú ý việc bỏ sót người, nhầm loại phương tiện và vẽ box không sát vật. Những lỗi này làm mô hình học sai đối tượng hoặc phạm vi cần phát hiện. Tôi chỉ gán các đối tượng thuộc taxonomy; không chọn một class gần giống để thay cho trường hợp chưa rõ.

Ở Pha 1, tôi sẽ xem đủ 40 ảnh và ghi những điểm v0 chưa giải thích, chưa vẽ box. Khi gán nhãn ở Pha 3, tôi sẽ dùng guideline v1.0 đã được nhóm thống nhất và khóa, làm độc lập theo ảnh được phân công.

## 2. Lớp và thuộc tính

### Lớp

Tôi sử dụng năm class đối tượng dưới đây và `ignore_region`. Mỗi đối tượng thuộc một class; vùng bỏ qua không phải một loại đối tượng. Các ví dụ trong bảng chỉ minh họa định nghĩa.

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con, SUV. | Ô tô con, SUV. | Xe tải hoặc van thùng kín cỡ nhỏ. |
| `truck` | Xe tải, xe có thùng hàng riêng. | Xe tải có thùng hàng riêng. | Xe con; không chọn truck chỉ vì xe lớn hoặc chở nhiều hàng. |
| `van` | Xe thùng kín cỡ nhỏ. | Van giao hàng thùng kín cỡ nhỏ. | Xe tải có thùng hàng riêng; không phải mọi xe thân kín đều là van. |
| `motorcycle` | Xe máy, mô tô. | Xe máy, mô tô. | Xe đạp; tuk-tuk chưa có quy tắc phân lớp riêng. |
| `person` | Người đi bộ hoặc người ngồi trên xe. | Người đi bộ, người ngồi trên phương tiện. | Tượng, ma-nơ-canh, hình người in hoặc phản chiếu. |
| `ignore_region` | Vùng bỏ qua (không phải vật): nơi không gán từng vật, bỏ sót ở đây không tính là lỗi. | Vùng chứa vật cao dưới 20 px theo quy tắc vật nhỏ. | Không thay cho class chưa biết hoặc ca khó chưa giải quyết. |

Tôi phân biệt `car`, `truck` và `van` bằng cấu trúc xe theo định nghĩa, không chỉ bằng kích thước. Tôi dùng `person` cho cả người đi bộ và người ngồi trên xe. Nếu không phân biệt chắc class, tôi ghi lại điểm chưa rõ để hỏi reviewer.

Với xe đạp, xích lô, tuk-tuk hoặc vật không thuộc lớp nào, tôi không tự thêm class và không gán ép. Tôi đề xuất không tạo box đối tượng cho vật rõ ràng ngoài phạm vi; ca chưa rõ sẽ được nhóm thảo luận. Tôi không mặc định biến vật ngoài taxonomy thành `ignore_region`.

### Thuộc tính

| Thuộc tính | Kiểu và giá trị hợp lệ | Ý nghĩa | Mặc định |
|---|---|---|---|
| `occluded_level` | `select`: chuỗi `0`, `1`, `2`, `3` | Theo v0: `0` thấy rõ; `1` bị che ít; `2` bị che nhiều; `3` không rõ. | `0` |
| `truncated` | `select`: `no`, `yes` | `no`: không bị cắt mép ảnh; `yes`: một phần vật bị khung ảnh cắt. | `no` |
| `can_review` | `checkbox`; `values: []` | Tôi tick khi còn phân vân về class, box, thuộc tính hoặc cách áp dụng quy tắc. | Taxonomy lưu chuỗi `"false"`. |

Tôi phân biệt che bởi vật khác với cắt bởi cạnh ảnh. Một vật có thể gặp cả hai tình huống, nên tôi kiểm hai thuộc tính riêng. Tôi không chọn `truncated=yes` chỉ vì box chạm cạnh mà chưa có dấu hiệu vật bị cắt.

V0 và taxonomy chưa quy định phần trăm che khuất cho từng mức. Tôi không tự đổi mức `3` thành một khoảng phần trăm, cũng không dùng giá trị mặc định thay việc kiểm từng vật. Nếu chưa phân biệt được mức che, tôi dùng `can_review` và ghi câu hỏi.

**Đề xuất cần thảo luận:** tôi sẽ chọn các ca thật, ghi cách hiểu về che ít / che nhiều và thử trên ảnh khác để nhóm chốt cách phân mức đo được. Hiện chưa có ranh giới phần trăm được xác nhận trong bản này.

## 3. Quy tắc vẽ box

Tôi giữ các quy định đã có trong v0, template và tài liệu QC. Những cách diễn giải chưa được nguồn nói rõ được ghi riêng là đề xuất cần thảo luận.

| Rule ID | Cách tôi áp dụng | Căn cứ / điểm cần thống nhất |
|---|---|---|
| R-01 | Tôi vẽ box ôm sát phần nhìn thấy, nằm trong ảnh, có kích thước dương; không chủ ý thêm lề hoặc cắt mất phần vật nhìn thấy. | V0 và template. |
| R-02 | Với vật bị che, tôi dựa vào phần còn nhìn thấy, không dựng lại phần khuất; chọn `occluded_level` phù hợp. | Template. Đề xuất: một box bao các phần nhìn thấy của cùng vật khi chúng bị ngăn cách bởi vật che; cần nhóm chốt. |
| R-03 | Với vật bị cạnh ảnh cắt, tôi giới hạn box trong ảnh và chọn `truncated=yes`; vẫn kiểm điều kiện kích thước. | V0 và nguyên tắc phần nhìn thấy. |
| R-04 | Tôi không gán hình phản chiếu hoặc hình in trên quảng cáo như người hay phương tiện thật. | Tài liệu QC xếp box trên phản chiếu / hình in vào lỗi thừa. |
| R-05 | Tôi không gán tượng như đối tượng thật. Với ma-nơ-canh, đồ chơi và mô hình, tôi đề xuất áp dụng cùng nguyên tắc và hỏi lại ca chưa rõ. | Quy tắc tượng từ tài liệu QC; phần mở rộng cho đồ chơi / mô hình cần thảo luận. |
| R-06 | Với xe chủ (ego), tôi ghi phần xe xuất hiện và câu hỏi về phạm vi; chưa tự chốt khi guideline chưa giải thích. | Template yêu cầu xét xe chủ; v0 chưa có hướng dẫn chi tiết. |
| R-07 | Vật cao dưới 20 px được xử lý bằng `ignore_region`, không gán từng vật. Đúng 20 px không thuộc điều kiện dưới ngưỡng. | Taxonomy và tài liệu QC. Đề xuất: đo theo phần nhìn thấy ở độ phân giải gốc; cách đo và gom vùng cần chốt. |
| R-08 | Với đám đông hoặc vật chồng lấn, tôi đề xuất xét từng vật phân biệt được, không gộp nhiều vật thành một box đối tượng chỉ vì ở gần nhau. | Vùng không tách được cần thảo luận cách dùng `ignore_region`; chưa có ngưỡng mật độ hay độ mờ riêng. |
| R-09 | Với người và xe, tôi đề xuất xét riêng người và phương tiện. Tôi sẽ tự xác định số box, phần được bao và thử cùng quy tắc trên ảnh thứ hai. | Taxonomy có các class riêng; số box và chi tiết như mũ đang đội cần kiểm trên ảnh. |
| R-10 | Với xe chở xe, tôi đề xuất xét xe vận chuyển và từng xe được chở riêng nếu thuộc phạm vi và đủ điều kiện. | Cần chốt phạm vi đầu kéo / rơ-moóc và cách xử lý các xe bị giàn che. |
| R-11 | Với phương tiện ngoài taxonomy, tôi không chọn lớp gần giống hoặc tự thêm class; tôi ghi lại để nhóm thống nhất. | Giữ nguyên taxonomy trong bản cá nhân. |
| R-12 | Nếu có box nhưng chưa chắc, tôi tick `can_review`. Nếu chưa thể vẽ box, tôi ghi ảnh, vùng và lý do thay vì tạo một box giả để đánh dấu. | GUIDE gốc; tập hợp vấn đề với nhóm sau khi khóa lượt gán độc lập. |

### Người và xe máy

Tôi sẽ ghi rõ những nội dung sau trên hai ảnh do mình chọn sau khi xem. Tôi không suy số người, số xe hoặc phạm vi box chỉ từ tên ảnh.

| Nội dung cần xác định | Ảnh thứ nhất | Ảnh thứ hai |
|---|---|---|
| Tên ảnh | | |
| Số box trong cụm đang xét | | |
| Box dành cho người | | |
| Box dành cho phương tiện | | |
| Phần cơ thể và mũ được bao gồm | | |
| Xử lý khi người bị xe hoặc người khác che | | |
| Lý do và điểm cần hỏi lại | | |

Khi kiểm nhãn, tôi xem lại bỏ sót, box thừa / trùng, sai class, sai phạm vi và sai thuộc tính. Tôi không coi vật tối hoặc nhòe là vật nhỏ khi chưa kiểm kích thước. Script giúp kiểm định dạng và điều kiện kỹ thuật; độ ôm sát và đúng đối tượng vẫn cần kiểm bằng mắt.

## 4. Ca khó

Tôi giữ các ảnh dưới đây làm danh sách cần kiểm tra theo tên gốc trong `data/ATTRIBUTION.csv`. Đây chưa phải các ca do tôi tự quan sát và chốt quyết định. Rule ID chỉ dẫn chủ đề cần đối chiếu; Quyết định và Lý do để trống để tôi ghi sau khi xem.

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002.jpg` | Xe chở ô tô — Renault 380 car carrier. | R-02, R-10 | | |
| `img_004.jpg` | Hai tuk-tuk theo tên gốc. | R-09, R-11 | | |
| `img_005.jpg` | Người đi xe máy — Motorbike riders. | R-02, R-03, R-09 | | |
| `img_006.jpg` | Traffic Jam, Cyclo Tour — phạm vi phương tiện và vật trong cảnh đông. | R-07, R-08, R-11 | | |
| `img_017.jpg` | Tượng Duke of Wellington. | R-05 | | |
| `img_018.jpg` | Billboard — phân biệt hình in với đối tượng thật. | R-04 | | |
| `img_019.jpg` | Xe Dangermouse trong Toy Parade — cần làm rõ tính chất vật. | R-05, R-11, R-12 | | |
| `img_020.jpg` | Rainbow in a Car Mirror — phản chiếu và xe chủ. | R-04, R-06 | | |
| `img_022.jpg` | Motorcycle with sidecar — phạm vi xe có thùng bên. | R-09, R-11, R-12 | | |
| `img_026.jpg` | Couple on a motorbike — người và xe. | R-02, R-03, R-09 | | |
| `img_027.jpg` | Pickup Truck Monument — công trình tạo hình xe. | R-05 | | |
| `img_029.jpg` | Dangerous load on a motorbike — xe và hàng chở. | R-01, R-02, R-09 | | |
| `img_033.jpg` | Mannequin — ma-nơ-canh. | R-04, R-05 | | |
| `img_035.jpg` | Overloaded Auto Rickshaw — phương tiện và hàng chở. | R-01, R-11 | | |
| `img_038.jpg` | Shop window with toys and car models — đồ chơi, mô hình. | R-04, R-05 | | |

Tôi sẽ xem cả 40 ảnh theo [checklist trong ghi chú cá nhân](../../individual_notes/2A202603146_NgoThiMinhQuang.md), chọn ba ca thật cùng quyết định và lý do. Ca đã loại được bằng quy tắc cần phân biệt với ca chưa rõ phải hỏi reviewer.

## 5. QC và phiên bản

### Ngưỡng QC

Tôi giữ nguyên mục `rules` trong taxonomy, không đổi ngưỡng để làm kết quả đạt yêu cầu.

| Khóa | Giá trị | Cách áp dụng |
|---|---|---|
| `min_box_height_px` | 20 | Dưới 20 px: vùng bỏ qua, không gán từng vật. |
| `iou_thr_large` | 0.85 | Box cao từ 50 px: IoU ít nhất 0.85. |
| `iou_thr_small` | 0.7 | Box nhỏ hơn 50 px: IoU ít nhất 0.7; dưới 20 px áp dụng R-07. |
| `large_px` | 50 | Đúng 50 px thuộc nhóm lớn. |
| `iaa_iou` | 0.85 | IoU trung bình trên cặp ghép được ít nhất 0.85. |
| `iaa_class` | 0.95 | Đồng thuận class trên cặp ghép được ít nhất 95%. |
| `error_rate_img_max` | 0.02 | Tỷ lệ ảnh có lỗi không quá 2%. |
| `match_iou` | 0.5 | Ngưỡng ghép box 1–1 không phân biệt class, không phải ngưỡng chấp nhận box. |

Tôi chỉ đọc IAA khi đủ 100% lượt gán theo phân công. Mỗi ảnh được ít nhất hai người gán độc lập; nhóm năm người thì ba. IoU và đồng thuận class tính trên các cặp ghép được; box chưa ghép báo riêng, không có cặp thì ghi N/A. Tôi giữ IAA trước Calibration và đối chiếu ca tham chiếu để phát hiện trường hợp cùng đồng thuận nhưng cùng sai.

Tôi báo tỷ lệ lỗi theo ảnh và theo đối tượng, kèm tử số / mẫu số. Theo QC gốc, Release cần duyệt toàn bộ lô: 1/40 ảnh lỗi = 2,5%, đã vượt 2%. Vòng chỉ lấy mẫu là demo và giữ Hold khi bàn giao.

- **Hold:** thiếu bằng chứng, guideline / dữ liệu còn vấn đề, review lệch phiên bản hoặc chỉ lấy mẫu.
- **Rework:** trên 2% ảnh lỗi hoặc có lỗi lặp; cần sửa và kiểm lại. IoU / IAA chưa đạt phải được phân tích và xử lý trước khi báo đạt.
- **Release:** người kiểm xác nhận đủ bằng chứng và đạt yêu cầu toàn lô.

Các lỗi tôi dùng là `bo_sot`, `thua`, `sai_lop`, `sai_vi_tri_kich_thuoc`, `sai_thuoc_tinh`; `khong` dành cho ảnh đã kiểm và không phát hiện lỗi. Script không thay việc kiểm ảnh bằng mắt.

### Bất đồng và người chốt

Tôi ghi ảnh, vấn đề và Rule ID cho ca mơ hồ. Người chốt do nhóm phân công; hiện chưa có mã reviewer được xác nhận trong bản này. Cả hai lệch cùng loại ca thì cần xem lại guideline; một người lệch thì cần kiểm cách hiểu quy tắc; làm giống nhau nhưng cùng sai thì cần đối chiếu tham chiếu.

Tôi sẽ dùng v1.0 đã khóa trong Pha 3, giữ bản cá nhân để so với bản nhóm. Mỗi ca Calibration được ghi một dòng có quyết định, Rule ID, phiên bản, người chốt và dấu vết sửa / kiểm lại. Quy tắc đổi nghĩa cần xác định phạm vi rà lại cả lô. Người kiểm nên khác người sửa; nhóm hai người đổi vai và ghi rõ.

### Lịch sử phiên bản

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| individual-v0.6 | Ghi phương án dự kiến cho các ca cần kiểm tra. | Chưa có quyết định từ quan sát cá nhân. |
| individual-v0.7 | Viết lại toàn bộ nội dung, giữ bảng ca cần xem và để trống quyết định / lý do. | Tách quy tắc chung khỏi phần ghi nhận sau khi tự xem ảnh; chưa có kết quả họp hoặc Calibration. |
