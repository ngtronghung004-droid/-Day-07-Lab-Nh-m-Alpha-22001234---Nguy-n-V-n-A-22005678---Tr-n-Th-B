# Guideline gán nhãn — individual-v0.4 — 146

- Phiên bản: individual-v0.4 (bản tham khảo do AI hỗ trợ, chờ thành viên tự kiểm).
- Ngày: 2026-11-16.
- Thành viên: Ngô Thị Minh Quang.
- Mã sinh viên: 2A202603146.
- Mã thành viên: 146.
- Người soạn bản tham khảo: Codex; người xác nhận cá nhân: chưa xác nhận.

Tài liệu giữ cấu trúc năm phần của template VinUni, class / attributes / rules theo taxonomy nhóm. Theo yêu cầu mới, Codex đã mở xem cả 40 ảnh và soạn nhận xét / đề xuất bên dưới; images.zip chứa đúng 40 ảnh trùng SHA256 với data/images/. Thành viên xác nhận chưa tự xem ảnh. Mọi quyết định do AI đề xuất đều chưa phải quyết định của 146, không chứng minh hoàn thành Pha 1. RULES yêu cầu người học tự quan sát và không dùng AI nhìn ảnh để quyết nhãn; vì vậy bản tham khảo này chưa đủ điều kiện thay cho bài cá nhân theo quy định. Thông tin họ tên và mã sinh viên được thêm theo yêu cầu trực tiếp mới nhất; tên file vẫn dùng mã 146.

## 1. Mục tiêu

Nhãn bounding box dùng để huấn luyện mô hình phát hiện người và phương tiện trên ảnh đường phố, chẳng hạn camera giao thông hoặc xe tự lái. Phạm vi gồm năm lớp đối tượng và vùng bỏ qua theo taxonomy trong bộ 40 ảnh. Công cụ dự kiến là CVAT, xuất COCO 1.0; Pha 1 chỉ quan sát và viết guideline, chưa vẽ box.

Mục tiêu là box chính xác, class đúng, thuộc tính nhất quán và quyết định có thể giải thích. Bỏ sót người có thể làm mô hình không phát hiện người; nhầm loại xe hoặc box quá rộng / hẹp làm sai mục tiêu huấn luyện. Không gán lên vật không thật và không ép vật ngoài taxonomy vào lớp gần giống. IAA cao không bảo đảm hai người đều đúng.

Giữ yêu cầu v0: gán mọi người và phương tiện thuộc phạm vi, box ôm sát, chọn đúng lớp và thuộc tính; áp dụng ngoại lệ vật nhỏ và vật không thật theo tài liệu chuẩn. Tôi phải tự xem đủ 40 ảnh, tự giải thích mỗi quyết định và gửi riêng bản cá nhân trước khi xem bản của người khác. Bản này chưa chứng minh đã hoàn thành Pha 1.

## 2. Lớp và thuộc tính

### Lớp

Mỗi đối tượng thuộc đúng một lớp. Định nghĩa giữ nguyên taxonomy; `ignore_region` là vùng bỏ qua, không phải đối tượng thứ sáu.

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con, SUV. | Ô tô con, SUV. | Xe tải; xe thùng kín cỡ nhỏ dễ nhầm với van. |
| `truck` | Xe tải, xe có thùng hàng riêng. | Xe tải có thùng hàng riêng. | Ô tô con; van cỡ nhỏ. |
| `van` | Xe thùng kín cỡ nhỏ. | Xe van giao hàng thùng kín cỡ nhỏ. | Không phải mọi xe kín đều là van; dễ nhầm car hoặc truck. |
| `motorcycle` | Xe máy, mô tô. | Xe máy, mô tô. | Xe đạp; người ngồi trên xe thuộc person; không tự ép tuk-tuk vào lớp này. |
| `person` | Người đi bộ hoặc người ngồi trên xe. | Người đi bộ, người ngồi trên xe. | Tượng, ma-nơ-canh, hình người in trên quảng cáo hoặc phản chiếu. |
| `ignore_region` | Vùng bỏ qua (không phải vật): nơi không gán từng vật, bỏ sót ở đây không tính là lỗi. | Vùng có vật cao dưới 20 px theo quy tắc vật nhỏ. | Không dùng để thay lớp chưa biết hoặc bỏ qua ca khó chưa được chốt. |

Phân biệt phương tiện bằng cấu trúc theo định nghĩa, không chỉ kích thước. Xe con / SUV thuộc `car`, xe tải hoặc xe có thùng hàng riêng thuộc `truck`, xe thùng kín cỡ nhỏ thuộc `van`. Nếu không đủ căn cứ phân biệt, dùng `can_review` trên box có thể vẽ hoặc ghi vấn đề cấp ảnh khi chưa vẽ được. Vật không thuộc lớp nào không được gán ép và không tự thêm class. **Đề xuất cá nhân cần thảo luận:** không tạo box đối tượng cho vật rõ ràng ngoài phạm vi; ghi ca chưa rõ để nhóm chốt. Không tự chuyển mọi vật ngoài taxonomy sang `ignore_region`.

### Thuộc tính

| Tên | Kiểu / các mức cố định | Ý nghĩa từng mức | Mặc định / ngưỡng |
|---|---|---|---|
| `occluded_level` | `select`: chuỗi `0`, `1`, `2`, `3` | Theo v0: `0` thấy rõ; `1` bị che ít; `2` bị che nhiều; `3` không rõ. | Mặc định `0`; chưa có ngưỡng phần trăm chính thức trong v0 hoặc taxonomy. |
| `truncated` | `select`: `no`, `yes` | `no`: không bị cắt mép ảnh; `yes`: bị cắt ở mép ảnh. | Mặc định `no`; kiểm dấu hiệu bị khung ảnh cắt, không chỉ chạm cạnh. |
| `can_review` | `checkbox`, `values: []` | Tick khi chưa chắc class, box, mức che hoặc cách áp dụng quy tắc; bỏ tick khi không cần đề nghị xem lại. | Taxonomy lưu mặc định là chuỗi `"false"`; không thêm mức select cho checkbox. |

Che bởi vật khác và cắt bởi khung ảnh là hai hiện tượng riêng, có thể đồng thời xảy ra. Không suy từ `truncated=yes` sang một mức occlusion. Không dùng mặc định thay việc kiểm từng vật. Không tự hiểu mức `3` thành một khoảng phần trăm mới.

#### Đề xuất cá nhân cần 146 xác nhận và thảo luận nhóm

Không có ngưỡng phần trăm occlusion chính thức trong v0 hoặc taxonomy. Giữ nguyên `occluded_level` với các giá trị `0`, `1`, `2`, `3` và nghĩa v0 ở bảng trên. Không áp dụng tỷ lệ ở bản nháp trước như quy định; không tự thay nghĩa mức `3`.

| Nội dung | Đề xuất của 146 / căn cứ | Trạng thái |
|---|---|---|
| Cách ước lượng và phân biệt các mức che khuất | TODO 146 tự đề xuất sau khi xem ảnh | Chưa xác nhận, cần thảo luận Pha 2 |
| Ngưỡng cụ thể nếu 146 đề xuất | TODO; ghi rõ là đề xuất cá nhân, không phải ngưỡng chính thức | Chưa chốt |
| Ảnh thực tế và phép thử trên ảnh thứ hai | TODO | Chưa thực hiện |
| Kết quả thảo luận nhóm / Calibration nếu còn bất đồng | TODO | Chưa có quyết định |

Phần mức thuộc tính đo được của rubric chưa hoàn tất; không bổ sung số phần trăm thay cho việc tự quan sát và thống nhất.

## 3. Quy tắc vẽ box

Các quy tắc diễn giải từ bản cá nhân trước được giữ là phương án ban đầu để 146 tự kiểm qua ảnh, không phải quyết định nhóm hoặc quyết định cho ảnh cụ thể. Với vật thật đủ điều kiện gán, phải đồng thời áp dụng phạm vi lớp, kích thước tối thiểu và các thuộc tính.

| Rule ID | Quy tắc | Căn cứ / phần cần xác nhận |
|---|---|---|
| R-01 | Box chữ nhật ôm sát phần nhìn thấy, nằm trong ảnh, kích thước dương; không chủ ý lấy thừa nền. | V0, template và kiểm hợp lệ kỹ thuật. Không hiểu “không bao gồm vật khác” là cắt mất phần của vật mục tiêu khi chúng chồng lấn. |
| R-02 | Vật bị che: bao phần nhìn thấy, không đoán phần bị che; ghi `occluded_level`. | Template. **Đề xuất cá nhân cần thảo luận:** một box bao các phần nhìn thấy thuộc cùng một vật, không tách vật chỉ vì có phần che giữa. |
| R-03 | Vật bị cắt mép: box giới hạn trong ảnh, ôm phần nhìn thấy, `truncated=yes`. | V0 và nguyên tắc phần nhìn thấy; vẫn kiểm ngưỡng vật nhỏ. |
| R-04 | Phản chiếu và hình in / quảng cáo không được gán như đối tượng thật. | Cheatsheet xếp box trên phản chiếu / hình in vào lỗi `thua`. |
| R-05 | Tượng không được gán như người hoặc phương tiện thật. | Cheatsheet. **Đề xuất cá nhân cần thảo luận:** áp dụng cùng nguyên tắc cho ma-nơ-canh và đồ chơi; tự tìm căn cứ ở ảnh trước khi xác nhận. |
| R-06 | Xe chủ (ego): chưa có quy tắc chi tiết trong v0 / taxonomy, không tự chốt phạm vi. | TODO 146: tự ghi ca nếu gặp, đề xuất phần có / không gán và lý do, hỏi nhóm / reviewer. Không khẳng định ảnh nào có xe chủ. |
| R-07 | Vật cao dưới 20 px: dùng `ignore_region`, không gán từng vật; đúng 20 px không thuộc điều kiện dưới ngưỡng. | `min_box_height_px=20` và cheatsheet. **Đề xuất cá nhân cần thảo luận:** đo trên box phần nhìn thấy ở độ phân giải gốc; chốt cách gom vùng bỏ qua. |
| R-08 | Đám đông / chồng lấn: không tự gộp nhiều instance thành một box đối tượng. | Phương án cá nhân từ bản trước: phân biệt từng vật đủ điều kiện; nếu không thể tách thì ghi vấn đề, chờ nhóm thống nhất vùng bỏ qua. Không tự đặt ngưỡng mật độ. |
| R-09 | Người và xe: 146 tự quyết định số box, box dành cho người / phương tiện, phần cơ thể được bao và cách xử lý khi người bị xe che; thử quy tắc trên ảnh thứ hai. | Yêu cầu Pha 1 của GUIDE gốc; chưa có quyết định cá nhân. Điền mục riêng bên dưới sau khi tự xem, không dùng kết luận do AI đưa ra. |
| R-10 | Xe chở xe: phương án cá nhân là xét xe vận chuyển và từng xe được chở như các vật riêng, nếu trong phạm vi và đủ điều kiện. | Chưa xác nhận trên ảnh; không gộp cả cụm thành một box. Ranh giới chưa rõ thì ghi reviewer xem lại. |
| R-11 | Vật ngoài taxonomy: không thêm class, không ép vào lớp gần giống. | Taxonomy; phương án xử lý và ca chưa rõ ở mục 2 cần nhóm chốt. |
| R-12 | Box chưa chắc: tick `can_review`; chưa thể vẽ box: ghi ảnh, vùng và lý do, không tạo box / class giả chỉ để tick. | GUIDE gốc. Chỉ tập hợp vấn đề với nhóm sau khi khóa bản gán độc lập. |

### Người và xe máy — đề xuất AI cho R-09, chưa được 146 xác nhận

Phương án tham khảo: coi người và phương tiện là các đối tượng riêng; box ôm phần nhìn thấy, không gộp cả cụm người–xe. Đề xuất bao mũ đang đội cùng người, không bao cả xe hay hàng chở trong box người; chi tiết này cần 146 tự xác nhận và nhóm chốt. Khi người bị xe che, không tự khôi phục phần cơ thể khuất; `occluded_level` giữ nghĩa v0, không tự gán phần trăm.

| Nội dung | img_026.jpg — AI đề xuất | img_029.jpg — thử trên cụm chính |
|---|---|---|
| Phạm vi ví dụ | Hai người ngồi trên xe máy đỏ ở tiền cảnh. | Người điều khiển xe máy chở thanh dài ở giữa ảnh. |
| Có bao nhiêu box cho cụm nêu trên? | Đề xuất 3: hai người và một xe máy. Không phải số nhãn cuối đã xác nhận. | Đề xuất 2: người điều khiển và xe máy. Không tính người / xe khác trong ảnh vào con số này. |
| Box dành cho người | Mỗi người một box phần nhìn thấy; không gộp hai người thành một. | Một box riêng cho người trên xe máy; người đi xe đạp bên phải là đối tượng khác cần xét riêng. |
| Box dành cho phương tiện | Một box xe máy, phần bị người che không được suy thành đường bao toàn thân xe bị khuất. | Một box xe máy; không mở rộng tới hai đầu thanh hàng dài. |
| Phần nào của người được bao gồm? | Đầu / mũ, thân và phần tay chân nhìn thấy của từng người; tránh nhập cơ thể người kia. | Đầu, thân và tay chân nhìn thấy của người điều khiển; thanh hàng không thuộc cơ thể. |
| Khi người bị xe / người khác che? | Giữ box theo phần nhìn thấy, kiểm che khuất; phần bị khung ảnh cắt kiểm truncated riêng. | Không suy phần khuất sau xe / hàng; kiểm thuộc tính riêng cho từng vật. |
| Lý do / điều cần kiểm lại | Người và xe có lớp riêng; xe và chân người cắt mép dưới cần kiểm trên từng box. | Áp dụng cùng nguyên tắc tách người–xe; hàng nhô xa không phải thân phương tiện. |
| Xác nhận của 146 | Chưa tự xem, chưa xác nhận. | Chưa tự xem, chưa xác nhận. |

Đây là phép thử do AI thực hiện để giải thích phương án, không thay yêu cầu thành viên tự quan sát và tự giải thích trong Pha 1. Chưa xác nhận mức occlusion, tọa độ hoặc tổng số box của hai ảnh.

Trước khi lưu nhãn ở Pha 3: tự kiểm toàn ảnh, bỏ sót / thừa / trùng, đúng lớp, độ ôm sát, kích thước và vị trí, `occluded_level`, `truncated`, `can_review`. Script không thay thế việc kiểm nội dung và ranh giới bằng mắt. Pha 3 dùng v1.0 nhóm đã khóa, không tự sửa quy tắc giữa lượt gán.

## 4. Ca khó

**Bản phân tích tham khảo của AI, chưa được 146 tự quan sát hoặc xác nhận.** Bảng giữ 15 ứng viên đã chọn. Tình huống gồm tên gốc trong ATTRIBUTION.csv và nhận xét thị giác của AI; tên gốc không tự quyết định nhãn. Các cột Quyết định và Lý do là đề xuất của AI, chưa phải quyết định cá nhân. Chưa có box CVAT, tọa độ hoặc số liệu QC được tạo.

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002.jpg` | Tên gốc: Renault 380 car carrier (17688579282).jpg — AI nhận xét: Xe vận chuyển có nhiều ô tô trên hai tầng; khung giá che một phần các xe; có người đứng bên phải. | R-01, R-02, R-10 | Đề xuất AI, 146 chưa xác nhận: Xét xe vận chuyển và từng xe được chở độc lập, không gộp toàn bộ cụm; người đứng bên phải xét riêng. | Lập luận AI: Các xe có thân riêng, việc đang được chở không tự làm mất tư cách đối tượng; cần chốt phạm vi xe kéo / rơ-moóc. |
| `img_004.jpg` | Tên gốc: DFC 2465 Two brightly painted blue tuk-tuks parked side by side on a city sidewalk at night ready to ferry passengers.jpg — AI nhận xét: Hai xe ba bánh có mái; người ngồi trong bị khung xe che. | R-02, R-09, R-11, R-12 | Đề xuất AI, 146 chưa xác nhận: Không tự ép tuk-tuk vào car / motorcycle; hỏi nhóm về phạm vi xe ba bánh, xét người theo phần nhìn thấy. | Lập luận AI: Taxonomy không có định nghĩa tuk-tuk; người thật và phương tiện cần được xét riêng. |
| `img_005.jpg` | Tên gốc: Ho Chi Minh City, Vietnam, Motorbike riders.jpg — AI nhận xét: Nhiều người đội mũ ngồi trên các xe máy sát nhau; phía sau là xe thân kín; người và xe che lẫn nhau, một số phần bị cắt mép. | R-01, R-02, R-03, R-09 | Đề xuất AI, 146 chưa xác nhận: Tách đối tượng người và phương tiện, box theo phần nhìn thấy; không gộp cả hàng người–xe. Chưa chốt tổng số box hoặc mức occlusion. | Lập luận AI: Một box cho cả người lẫn xe sẽ trộn hai lớp; giao nhau không đủ để biết phần bị che chiếm bao nhiêu phần trăm. |
| `img_006.jpg` | Tên gốc: Traffic Jam, Cyclo Tour, Hue, Vietnam (7073456573).jpg — AI nhận xét: Xe máy, xe đạp và người đi đường đông; người trên xe ở tiền cảnh và nhiều vật xa phía sau. | R-02, R-07, R-08, R-09, R-11 | Đề xuất AI, 146 chưa xác nhận: Phân biệt người với xe; không gọi xe đạp là motorcycle; đo chiều cao trước khi dùng ignore_region cho vật xa. | Lập luận AI: Phương tiện không cùng loại; đông không tự có nghĩa mọi vật đều được bỏ qua. |
| `img_017.jpg` | Tên gốc: Duke of Wellington statue, Glasgow - traffic cone hat and gull, 2025.jpg — AI nhận xét: Tượng người cưỡi ngựa trên bệ, bề mặt điêu khắc, đặt trước tòa nhà. | R-05, R-11 | Đề xuất AI, 146 chưa xác nhận: Không gán person cho phần người bằng tượng; không dùng ignore_region chỉ vì đây là tượng. | Lập luận AI: Đây là biểu diễn điêu khắc, không phải người thật thuộc phạm vi phát hiện. |
| `img_018.jpg` | Tên gốc: Předvolební billboard na Praze 4 (Lukáš Zicha – Starostové).jpg — AI nhận xét: Chân dung in trên billboard; phía dưới có xe sau hàng rào. | R-02, R-04 | Đề xuất AI, 146 chưa xác nhận: Không gán person cho chân dung; xét từng xe thật phía dưới riêng theo phần nhìn thấy. | Lập luận AI: Hình in không phải người thật; loại chân dung không có nghĩa bỏ các xe thật trong cùng ảnh. |
| `img_019.jpg` | Tên gốc: View of the Dangermouse car in the Hamley's Toy Parade - geograph.org.uk - 5200140.jpg — AI nhận xét: Xe vàng tạo hình hoạt hình trong đoàn diễu hành, hình nhân lớn bên trong; có người thật ngồi cạnh và đám đông sau rào. | R-02, R-05, R-08, R-11, R-12 | Đề xuất AI, 146 chưa xác nhận: Chưa chốt class xe vàng; không coi hình nhân là người; xét người thật riêng, hỏi reviewer về phạm vi xe tạo hình. | Lập luận AI: Ảnh cho thấy vật có bánh và người ngồi nhưng chưa chứng minh là đồ chơi hoặc ô tô mục tiêu; không thể kết luận chỉ từ chữ Toy trong tên nguồn. |
| `img_020.jpg` | Tên gốc: Rainbow in a Car Mirror.jpg — AI nhận xét: Gương chiếu hậu phản chiếu thân xe và xe phía sau; có khung gương và một phần cửa xe sát người chụp. | R-04, R-06, R-12 | Đề xuất AI, 146 chưa xác nhận: Không gán xe chỉ xuất hiện trong phản chiếu; phần xe chủ thật ngoài gương chờ nhóm chốt phạm vi. | Lập luận AI: Phản chiếu khác vật trực tiếp trong cảnh; quy tắc ego chưa rõ trong v0. |
| `img_022.jpg` | Tên gốc: Motorcycle with sidecar, sunshine Fortepan 4915.jpg — AI nhận xét: Ảnh đen trắng có xe máy gắn thùng bên; vùng phía sau kính thùng bên chưa rõ có người hay không. | R-01, R-11, R-12 | Đề xuất AI, 146 chưa xác nhận: Đề xuất xem xe máy và thùng bên gắn liền là một cụm phương tiện, cần nhóm xác nhận; không suy thêm người từ vùng mờ. | Lập luận AI: Sidecar khác xe được chở độc lập; chưa đủ căn cứ chốt người hoặc số box toàn ảnh. |
| `img_026.jpg` | Tên gốc: Couple on a motorbike, in a tunnel in Saigon.jpg — AI nhận xét: Hai người đội mũ ngồi trên một xe máy đỏ; xe và chân người bị cắt ở mép dưới; nền là tranh in lớn. | R-02, R-03, R-04, R-09 | Đề xuất AI, 146 chưa xác nhận: Đề xuất 3 box cho cụm chính: 2 person và 1 motorcycle; không gán các hình in nền; kiểm truncated trên từng box bị cắt. | Lập luận AI: Hai người có đầu / thân riêng; xe là đối tượng khác lớp; số 3 chỉ nói cụm chính, chưa phải tổng nhãn được xác nhận. |
| `img_027.jpg` | Tên gốc: Pickup Truck Monument, Oak Hill Memorial Park, San Jose, Calif.jpg — AI nhận xét: Vật tạo hình xe bán tải trên bệ trong khu có các bia mộ; hình dạng như công trình tưởng niệm. | R-05, R-11 | Đề xuất AI, 146 chưa xác nhận: Không gán truck chỉ dựa vào hình dạng pickup; đối chiếu quy tắc tượng và xác nhận với nhóm. | Lập luận AI: Bệ và kết cấu tạo hình cho thấy cần phân biệt tượng xe với phương tiện thật. |
| `img_029.jpg` | Tên gốc: Dangerous load on a motorbike.jpg — AI nhận xét: Người trên xe máy chở thanh dài chạy chéo qua ảnh; bên phải có người cùng xe đạp, nền có người đi đường. | R-01, R-02, R-09, R-11 | Đề xuất AI, 146 chưa xác nhận: Đề xuất tách người và xe máy ở cụm chở hàng; không kéo box tới hai đầu thanh hàng, xét người và xe đạp bên cạnh riêng. | Lập luận AI: Thanh hàng không phải thân người hoặc xe; xe đạp không phải motorcycle theo taxonomy hiện tại. |
| `img_033.jpg` | Tên gốc: Glasgow. Buchanan Street. 'Mannequin'.jpg — AI nhận xét: Ma-nơ-canh trong cửa kính, phần hình người bên trái và ảnh phản chiếu thân xe / gương trên kính. | R-04, R-05 | Đề xuất AI, 146 chưa xác nhận: Không gán person cho ma-nơ-canh; không gán phương tiện từ phần phản chiếu trên kính. | Lập luận AI: Dáng người hoặc dáng xe chưa đủ: phải phân biệt vật thật trực tiếp với mô hình, hình in và phản chiếu. |
| `img_035.jpg` | Tên gốc: Overloaded Auto Rickshaw Hyderabad 2006.jpg — AI nhận xét: Xe ba bánh chở kiện hàng cao; xe máy với người ở tiền cảnh; ô tô và xe ba bánh phía sau. | R-01, R-02, R-09, R-11 | Đề xuất AI, 146 chưa xác nhận: Không tự gọi xe ba bánh là truck vì chở nhiều hàng; hỏi nhóm phạm vi rickshaw; xét người / xe máy rõ riêng. | Lập luận AI: Lượng hàng không làm thay đổi định nghĩa class; hàng nhô lên cần tách khỏi thân phương tiện theo quy tắc chốt. |
| `img_038.jpg` | Tên gốc: Shop window with collection of toys, dolls, car models etc. in Munich, Germany (2023) (cropped).jpg — AI nhận xét: Tủ kính có nhiều mô hình ô tô, đồ chơi và hình nhân; có phản chiếu trên mặt kính. | R-04, R-05, R-11 | Đề xuất AI, 146 chưa xác nhận: Đề xuất không gán các mô hình thành car / truck thật; không dùng ngưỡng vật nhỏ để hợp thức hóa nhãn trên đồ chơi. | Lập luận AI: Cần xét thuộc phạm vi trước khi xét kích thước; mô hình không thành xe thật chỉ vì nhìn rõ. |

146 cần tự kiểm lại từng ảnh, ghi quyết định riêng và lý do, có thể bác bỏ các đề xuất. Các trường hợp chưa rõ phải mang ra thảo luận, không coi nhận xét AI là kết luận Calibration. Checklist đủ 40 ảnh nằm tại `../../individual_notes/146.md`; trạng thái người học vẫn là Chưa xem.

## 5. QC và phiên bản

Giữ nguyên tám ngưỡng `rules` của taxonomy nhóm, không sửa để đạt số đo.

| Khóa | Giá trị | Áp dụng |
|---|---|---|
| `min_box_height_px` | 20 | Vật dưới 20 px dùng vùng bỏ qua, không gán từng vật. |
| `iou_thr_large` | 0.85 | Box cao từ 50 px: IoU ít nhất 0.85. |
| `iou_thr_small` | 0.7 | Box nhỏ hơn 50 px: IoU ít nhất 0.7; vật dưới 20 px áp dụng R-07. |
| `large_px` | 50 | Đúng 50 px thuộc nhóm lớn. |
| `iaa_iou` | 0.85 | IoU trung bình trên cặp ghép được ít nhất 0.85. |
| `iaa_class` | 0.95 | Đồng thuận class trên cặp ghép được ít nhất 95%. |
| `error_rate_img_max` | 0.02 | Tỉ lệ ảnh có lỗi không quá 2%. |
| `match_iou` | 0.5 | Ngưỡng ghép box 1–1, không phân biệt lớp; không phải ngưỡng chấp nhận box. |

Theo QC gốc, đủ 100% lượt gán trong phân công mới đo IAA; mỗi ảnh ít nhất hai người gán độc lập (nhóm năm người: ba). Báo tử số / mẫu số, cặp chưa ghép và ca bất đồng vùng bỏ qua riêng; không có cặp ghi N/A. Giữ IAA trước Calibration, đối chiếu tham chiếu coach sau khi khóa bản độc lập để tìm ca cùng sai.

QC báo cả ảnh có ít nhất một lỗi / ảnh đã duyệt và annotation đối tượng lỗi / annotation đã duyệt. Các lỗi: `bo_sot`, `thua`, `sai_lop`, `sai_vi_tri_kich_thuoc`, `sai_thuoc_tinh`; `khong` dành cho ảnh đã duyệt sạch. Chưa có số liệu hay quyết định QC trong Pha 1 này.

Theo đề gốc hiện hành: Release cần duyệt toàn bộ lô; 1/40 ảnh lỗi = 2,5%, vượt 2%. Hold khi thiếu bằng chứng, guideline / dữ liệu có vấn đề, review sai phiên bản hoặc chỉ lấy mẫu demo; Rework khi trên 2% ảnh lỗi hoặc lỗi lặp; Release khi reviewer xác nhận đầy đủ bằng chứng đạt yêu cầu. IoU / IAA chưa đạt phải phân tích và xử lý, không tự báo đạt. Cách lấy mẫu cũ trong Alpha chưa đủ căn cứ Release theo đề gốc.

Người quyết ca mơ hồ: TODO mã reviewer / người chốt do nhóm phân công, chưa có quyết định họp. Pha 2 thảo luận bất đồng, chốt v1.0 và khóa cho Pha 3. Cả hai lệch cùng loại ca có thể do guideline mơ hồ; chỉ một người lệch thì kiểm việc hiểu quy tắc; đồng thuận nhưng cùng sai thì đối chiếu ca tham chiếu. Pha 5 ghi mỗi ca bất thường một dòng, Rule ID, lý do, người chốt, phiên bản, dấu vết sửa / kiểm lại và phạm vi ảnh / lô. Thay đổi làm đổi nhãn phải tăng phiên bản; thay đổi ngữ nghĩa cần rà cả lô theo đề gốc. Người kiểm nên khác người sửa, nhóm hai người đổi vai và ghi rõ.

Giữ bản cá nhân sau Pha 1 để so với bản nhóm, không viết lại theo cuộc họp. V1.0 / v1.1 thuộc hồ sơ nhóm ở các pha sau, chưa được tạo trong lần này.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Starter của chương trình được giữ nguyên. | Nguồn khởi đầu, chưa đủ quy tắc chi tiết. |
| individual-v0.1 | Bản cá nhân 146 cung cấp ở phiên trước. | Có phương án ban đầu, chưa điền ảnh quan sát. |
| individual-v0.2 | Dựng lại theo template VinUni, đủ bảng class / ca khó / lịch sử; ngưỡng theo taxonomy, 40 tên ảnh thật. | Yêu cầu chuẩn bị mới; chưa có ca quan sát thực tế hay quyết định Calibration. |
| individual-v0.3 | Thay bảng 40 dòng bằng 15 ứng viên theo tên gốc ATTRIBUTION; chuyển checklist đủ 40 ảnh sang ghi chú, thêm câu hỏi người–xe và mục đề xuất thuộc tính. | Chỉnh bố cục theo yêu cầu 146; chưa có quyết định quan sát mới và không đổi ngưỡng. |
| individual-v0.4 | AI xem 40 ảnh và soạn phân tích có ghi nguồn AI; thêm thông tin thành viên theo yêu cầu mới. | Chưa có xác nhận quan sát của 146; không đổi taxonomy, ngưỡng hoặc tạo nhãn CVAT. |

Đối chiếu rubric Pha 1: cấu trúc và định nghĩa lớp / ví dụ / phản ví dụ đã điền; ngưỡng QC khớp taxonomy. **Chưa hoàn tất** tiêu chí ca thật có quyết định và lập luận, mức occlusion đo được, kiểm thử quy tắc qua ảnh. Không tự chấm điểm hoặc đánh dấu hoàn thành Pha 1. TODO 146: tự xem đủ 40 ảnh, chọn ít nhất ba ca thật theo mẫu ghi chú, ghi lý do, thử quy tắc người–xe trên ảnh khác, tự xác nhận các đề xuất trước khi gửi riêng.
