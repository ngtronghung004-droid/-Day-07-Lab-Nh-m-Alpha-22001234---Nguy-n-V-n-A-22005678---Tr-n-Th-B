# Guideline gán nhãn cá nhân — Ngô Thị Minh Quang

- MSHV: 2A202603146.
- Mã thành viên: 146.
- Phiên bản: Individual v0.1.
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

Tôi dùng hai ảnh dưới đây để minh họa phương án tách người và phương tiện theo R-09. Số box chỉ tính trong cụm được mô tả, không phải tổng nhãn toàn ảnh. Đây là phương án để tôi tự kiểm lại, chưa phải kết quả gán nhãn hoặc xác nhận quan sát cá nhân.

| Nội dung cần xác định | Ảnh thứ nhất | Ảnh thứ hai |
|---|---|---|
| Tên ảnh | `img_026.jpg` | `img_029.jpg` |
| Cụm đang xét | Hai người trên xe máy đỏ ở tiền cảnh. | Người điều khiển xe máy chở thanh dài ở giữa ảnh; chưa tính người và xe khác. |
| Số box trong cụm đang xét | Dự kiến 3 box: 2 `person` và 1 `motorcycle`. | Dự kiến 2 box: 1 `person` và 1 `motorcycle`. |
| Box dành cho người | Tôi tách mỗi người một box theo phần cơ thể nhìn thấy, không gộp hai người. | Tôi tạo box riêng cho người trên xe máy; người bên xe đạp được xét riêng ngoài cụm này. |
| Box dành cho phương tiện | Một box cho xe máy theo phần nhìn thấy; không lấy cả người làm phạm vi của xe. | Một box cho xe máy; không kéo box tới hai đầu thanh hàng dài. |
| Phần cơ thể và mũ được bao gồm | Tôi đề xuất bao đầu, mũ đang đội, thân và phần tay chân nhìn thấy của từng người; không nhập cơ thể người kia vào cùng đối tượng. | Tôi bao phần cơ thể nhìn thấy của người điều khiển; thanh hàng và xe đạp bên cạnh không thuộc cơ thể người đó. Không tự thêm mũ nếu không thấy. |
| Xử lý khi người bị xe hoặc người khác che | Tôi không dựng lại phần khuất. Tôi kiểm `occluded_level` riêng cho từng người; `truncated=yes` chỉ khi chính vật đó bị khung ảnh cắt. | Tôi dựa vào phần nhìn thấy, không suy thêm phần cơ thể sau xe hoặc hàng; kiểm mức che riêng, không tự quy đổi sang phần trăm. |
| Lý do và điểm cần hỏi lại | Người và xe thuộc class khác nhau. Tôi cần thống nhất phạm vi mũ, phần nhìn thấy rời nhau và mức che giữa hai người. | Tôi áp dụng cùng nguyên tắc tách người–xe; hàng nhô ra không phải thân xe. Xe đạp ngoài taxonomy, nhưng người đi xe đạp vẫn được xét theo `person` nếu đủ điều kiện. |

Tôi sẽ đối chiếu lại hai ảnh trước khi chốt số box và thuộc tính. Phương án này không bao gồm tọa độ, không xác nhận tổng số nhãn và không thay phần tự ghi nhận trong checklist.

Khi kiểm nhãn, tôi xem lại bỏ sót, box thừa / trùng, sai class, sai phạm vi và sai thuộc tính. Tôi không coi vật tối hoặc nhòe là vật nhỏ khi chưa kiểm kích thước. Script giúp kiểm định dạng và điều kiện kỹ thuật; độ ôm sát và đúng đối tượng vẫn cần kiểm bằng mắt.

## 4. Ca khó

Bảng dưới đây ghi phương án áp dụng quy tắc cho 15 ảnh cần kiểm tra. Các phương án chưa phải quyết định đã được tôi xác nhận sau khi tự quan sát. Tôi sẽ đối chiếu lại từng ảnh; ca thiếu căn cứ được ghi là chưa chốt và đưa ra thảo luận, không ép vào một class để điền cho đủ bảng.

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002.jpg` | Xe vận chuyển ô tô trên giàn. | R-02, R-10 | Tôi dự kiến gán xe vận chuyển theo `truck`, xét riêng từng ô tô được chở nếu nhận diện được và đủ điều kiện. Phạm vi đầu kéo / giàn chở cần nhóm chốt; không gộp toàn cụm thành một box. | Xe được chở vẫn có thể là đối tượng riêng. Việc nằm trên xe vận chuyển không tự loại chúng khỏi taxonomy; phần bị giàn che phải xét theo quy tắc che khuất. |
| `img_004.jpg` | Tuk-tuk và người trong khoang. | R-02, R-09, R-11 | Tôi chưa chốt class tuk-tuk, không tự gọi là `car` hoặc `motorcycle`. Người thật trong khoang được xét riêng theo `person` nếu đủ căn cứ; phần bị khung xe che chỉ bao phần nhìn thấy. | Taxonomy chưa có lớp riêng cho xe ba bánh. Người ngồi trên phương tiện vẫn thuộc phạm vi người; không gộp người với xe vì cùng nằm trong một khoang. |
| `img_005.jpg` | Nhiều người và xe máy che nhau, có vật cắt mép. | R-02, R-03, R-09 | Tôi dự kiến tách từng người và xe máy phân biệt được. Box ôm phần nhìn thấy; vật thực sự bị cạnh ảnh cắt dùng `truncated=yes`. Tôi kiểm mức che riêng, chưa chốt tổng số box. | Người và xe là các đối tượng khác lớp. Che bởi vật bên cạnh và cắt bởi cạnh ảnh là hai hiện tượng khác nhau, không dùng chung một mức thuộc tính cho cả cụm. |
| `img_006.jpg` | Giao thông đông, nhiều loại phương tiện. | R-07, R-08, R-09, R-11 | Tôi xét từng người và xe thuộc phạm vi, đo vật xa trước khi dùng `ignore_region` cho chiều cao dưới 20 px. Xe đạp / xích lô không tự nhập vào `motorcycle`; vùng không thể tách cần hỏi lại. | Đông hoặc chồng lấn không có nghĩa bỏ qua toàn ảnh. Tôi cần kiểm class, khả năng phân biệt và kích thước trước khi quyết định gán hoặc dùng vùng bỏ qua. |
| `img_017.jpg` | Tượng người cưỡi ngựa. | R-05 | Tôi không gán `person` cho phần người thuộc tượng, không dùng `ignore_region` chỉ để bao tượng. Các đối tượng thật khác, nếu có, vẫn xét riêng. | Class người dành cho người thật, không phải hình dáng người trong tác phẩm điêu khắc. Loại tượng không tự đồng nghĩa toàn ảnh không có nhãn. |
| `img_018.jpg` | Billboard và các xe sau hàng rào. | R-02, R-04 | Tôi không gán `person` cho chân dung in trên biển. Xe thật phía dưới được xét riêng theo phần nhìn thấy; mức che bởi hàng rào cần kiểm, không tự đặt mức tối thiểu. | Hình in khác người thật. Quy tắc loại hình in không loại các xe thật trong cùng ảnh; có rào không đủ để suy một mức occlusion cố định. |
| `img_019.jpg` | Xe diễu hành tạo hình và hình nhân. | R-05, R-08, R-11, R-12 | Tôi chưa chốt class xe vàng và ghi câu hỏi về phạm vi xe diễu hành. Theo phương án R-05, hình nhân không gán như người thật; người thật được xét riêng. Tôi chỉ dùng `can_review` khi đã có box có căn cứ. | Chữ Toy trong tên gốc không chứng minh chiếc xe là đồ chơi. Cần phân biệt xe tạo hình, hình nhân và người thật, không chọn lớp chỉ theo vẻ ngoài hoặc tên nguồn. |
| `img_020.jpg` | Phản chiếu trong gương và phần xe chủ. | R-04, R-06 | Tôi không gán xe chỉ xuất hiện dưới dạng phản chiếu trong gương. Với bộ phận xe chủ nhìn trực tiếp ngoài gương, tôi ghi vấn đề và chờ nhóm thống nhất phạm vi. | Phản chiếu không phải một xe trực tiếp khác trong cảnh. V0 chưa quy định rõ xe chủ nên tôi không tự kết luận toàn ảnh phải bỏ qua. |
| `img_022.jpg` | Xe máy gắn thùng bên (sidecar). | R-09, R-11, R-12 | Tôi đề xuất một box `motorcycle` bao phần nhìn thấy của xe máy và thùng bên gắn liền; cần nhóm chốt cách tính một đối tượng. Chỉ xét thêm người khi có dấu hiệu đủ rõ. | Thùng bên gắn với xe khác một xe độc lập được chở trên xe. Ảnh đen trắng không đổi taxonomy; vùng mờ chưa đủ để suy thêm người hoặc số box. |
| `img_026.jpg` | Hai người trên xe máy đỏ, vật cắt mép và hình in nền. | R-02, R-03, R-04, R-09 | Với cụm chính, tôi dự kiến 2 box `person` và 1 box `motorcycle` như bảng trên. Tôi kiểm cắt mép trên từng vật, không gán nội dung tranh in như đối tượng thật. | Mỗi người là một đối tượng, xe thuộc class khác. Tôi không gộp hai người với xe hoặc suy phần cơ thể ngoài khung ảnh; ba box chỉ nói cụm chính. |
| `img_027.jpg` | Công trình tưởng niệm hình pickup. | R-05 | Tôi không gán `truck` cho phần tạo hình xe thuộc công trình tưởng niệm. Nếu có đối tượng thật khác, tôi kiểm riêng theo taxonomy. | Giống hình dáng xe bán tải chưa đủ để là phương tiện thật. Cần phân biệt công trình tạo hình với xe mục tiêu, không quyết định chỉ theo hình dáng pickup. |
| `img_029.jpg` | Xe máy và người chở thanh hàng dài. | R-01, R-02, R-09, R-11 | Tôi dự kiến tách người và xe máy thành hai box cho cụm chính; không mở box tới hai đầu thanh hàng. Người bên xe đạp xét riêng; xe đạp không tự chuyển thành `motorcycle`. | Hàng chở không phải thân xe hoặc cơ thể người. Tiếp xúc với nhau không làm các vật thành một đối tượng; phương tiện ngoài taxonomy không được gán ép. |
| `img_033.jpg` | Ma-nơ-canh và ảnh phản chiếu qua kính. | R-04, R-05 | Theo phương án R-05, tôi không gán `person` cho ma-nơ-canh; không gán phương tiện chỉ xuất hiện trong phản chiếu. Chi tiết chưa phân biệt được sẽ ghi để hỏi reviewer. | Dáng người hoặc xe không đủ để chọn class: cần phân biệt vật thật trực tiếp với mô hình, hình in và phản chiếu. |
| `img_035.jpg` | Auto rickshaw chở kiện hàng cao. | R-01, R-09, R-11, R-12 | Tôi chưa chốt class auto rickshaw, không gọi là `truck` chỉ vì có nhiều hàng. Các người / xe thuộc phạm vi được xét riêng; cách bao thân xe và hàng cần thống nhất. | Lượng hàng không thay đổi định nghĩa class. Taxonomy chưa có lớp xe ba bánh; hàng nhô lên không phải căn cứ để thêm class hoặc gộp người–xe. |
| `img_038.jpg` | Đồ chơi và mô hình xe sau kính. | R-04, R-05 | Theo phương án R-05, tôi không gán mô hình xe thành ô tô thật hoặc hình nhân thành người thật. Tôi kiểm riêng phản chiếu và đối tượng thật khác nếu có. | Tôi xét phạm vi đối tượng trước kích thước. Mô hình nhìn rõ hoặc cao hơn 20 px vẫn không tự trở thành xe thật; không mặc định dùng vùng bỏ qua cho cả tủ. |

Các mục chưa chốt vẫn được giữ để thảo luận, không phải quyết định Calibration. Tôi chưa xác nhận mức occlusion, tọa độ hoặc tổng số nhãn cho các ảnh trên. Checklist đủ 40 ảnh và phần ghi nhận cá nhân nằm trong [ghi chú cá nhân](../../individual_notes/146.md).

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
| Individual v0.1 | Bổ sung ví dụ người–xe trên hai ảnh và phương án xử lý / lý do cho 15 ca khó. | Giữ nguyên taxonomy và ngưỡng; các phương án chưa được xác nhận thành quyết định cá nhân hoặc Calibration. |
