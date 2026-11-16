# Guideline gán nhãn — v0.1 — Thành viên Nguyễn Tấn Dũng

- **Phiên bản:** v0.1 (bản guideline cá nhân, đề xuất để thảo luận)
- **Ngày:** 2026-11-16
- **Người viết / duyệt:** Thành viên Nguyễn Tấn Dũng / Duyệt

## 1. Mục tiêu

Thống nhất cách gán Bounding Box cho các đối tượng giao thông trong bộ dữ liệu đường phố, hạn chế việc các thành viên đưa ra kết quả khác nhau trên cùng một tình huống.

Nguyên tắc chung:
- Mỗi đối tượng thực tế được gán một Bounding Box riêng nếu thuộc taxonomy và có thể nhận diện.
- Không gộp người với phương tiện thành một Bounding Box.
- Không suy đoán class khi hình ảnh không đủ căn cứ.
- Khi chưa thể quyết định chắc chắn, đánh dấu `can_review` hoặc ghi vấn đề ở cấp ảnh để reviewer xử lý.
- Chỉ sử dụng class có sẵn trong taxonomy; không tự ý thêm class mới.

## 2. Lớp và thuộc tính

### 2.1. Lớp

Sử dụng các class có sẵn trong taxonomy của repository. Trong guideline cá nhân này, bổ sung quy tắc cho class `bus`; việc thêm class vào cấu hình taxonomy/CVAT chỉ thực hiện nếu nhóm và yêu cầu bài lab cho phép:

| Lớp | Định nghĩa / cách áp dụng | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô con; gán riêng từng xe nhìn thấy và nhận diện được | Ô tô đang lưu thông hoặc được chở trên xe chuyên dụng | Không gộp nhiều ô tô thành một box |
| `truck` | Xe tải hoặc xe đầu kéo vận chuyển | Xe đầu kéo trong tình huống xe chở xe | Không gộp các ô tô được chở vào box `truck` |
| `bus` | Xe buýt; gán một box riêng bao quanh phần xe buýt nhìn thấy trong ảnh | Xe buýt đang lưu thông hoặc dừng đón trả khách | Không gán xe buýt thành `truck` chỉ vì kích thước lớn |
| `van` | Xe van theo taxonomy hiện có | Xe van nhìn thấy rõ | Không tự đổi thành class khác |
| `motorcycle` | Xe máy / mô tô | Xe máy đang lưu thông | Không gộp người lái vào box xe |
| `person` | Người thật xuất hiện trong ảnh, gồm người lái và người ngồi sau xe | Người lái xe, người ngồi sau, người đi bộ | Không gán tượng, ma-nơ-canh hoặc hình người in/phản chiếu |
| `ignore_region` | Chỉ sử dụng theo đúng định nghĩa và quy tắc có sẵn của repository | Vùng được guideline quy định là vùng bỏ qua | Không tự tạo vùng ignore chỉ vì đối tượng nhỏ hoặc khó |

**Vật không thuộc class nào:** Không tự tạo class `other_vehicle` và không ép gán vào class gần giống. Nếu chắc chắn vật nằm ngoài taxonomy thì không gán nhãn đối tượng. Nếu không đủ thông tin để xác định vật có thuộc taxonomy hay không, đánh dấu `can_review` hoặc ghi vấn đề cấp ảnh.

### 2.2. Thuộc tính

#### `occluded_level`

Đánh giá theo **tỷ lệ phần đối tượng bị che khuất** trên toàn bộ đối tượng (ước lượng theo hình dạng thực tế của đối tượng):

| Mức | Tỷ lệ phần bị che khuất | Cách xử lý |
|---|---:|---|
| `0` | 0%–20% | Không hoặc chỉ bị che rất ít; gán box bình thường |
| `1` | Trên 20%–50% | Bị che khuất một phần; vẫn gán box nếu nhận diện được |
| `2` | Trên 50%–80% | Bị che khuất nhiều; vẫn gán nếu xác định chắc chắn class |
| `3` | Trên 80%–dưới 100%, nhưng phần còn nhìn thấy vẫn đủ để nhận diện | Vẫn gán box và đánh dấu mức occlusion cao nhất |

Lưu ý:
- Các khoảng được viết không chồng lấn để tránh một đối tượng rơi vào hai mức.
- Nếu đối tượng bị che hoàn toàn (100%) hoặc phần còn nhìn thấy không đủ để nhận diện, không tạo box với class phỏng đoán; đánh dấu `can_review` hoặc ghi vấn đề cấp ảnh để reviewer xử lý.
- Các tỷ lệ là ước lượng nhất quán giữa các thành viên, không yêu cầu đo pixel tuyệt đối.
- Các ngưỡng trên là quy ước đề xuất của guideline cá nhân, cần được nhóm thống nhất ở Pha 2; không mặc định đây là ngưỡng chính thức của BDD100K.

#### `truncated`

`truncated` dùng để đánh dấu đối tượng **bị khung ảnh cắt mất một phần**. Nếu đối tượng bị cắt bởi bất kỳ mép nào của ảnh và vẫn được gán nhãn, đặt `truncated = true`, bất kể phần đối tượng nhìn thấy nhiều hay ít.

- Nếu đối tượng nằm sát mép ảnh nhưng vẫn hiển thị đầy đủ, đặt `truncated = false`.
- Bounding Box chỉ bao quanh phần đối tượng nhìn thấy bên trong ảnh; không ước lượng hoặc vẽ phần nằm ngoài khung ảnh.
- `truncated` và `occluded_level` là hai thuộc tính khác nhau: bị cắt bởi mép ảnh thì đánh dấu `truncated`; bị vật thể khác che khuất thì đánh giá `occluded_level`. Một đối tượng có thể đồng thời bị cắt mép và bị che khuất, khi đó áp dụng cả hai thuộc tính.

#### `can_review`

Đánh dấu khi:
- Không chắc chắn class của đối tượng.
- Không phân biệt được người thật với tượng / ma-nơ-canh / hình phản chiếu.
- Đối tượng quá nhỏ hoặc bị che đến mức không đủ căn cứ.
- Tình huống chưa có quy tắc thống nhất.

Nếu không có box phù hợp để gắn thuộc tính, ghi vấn đề ở cấp ảnh hoặc trong nhật ký ca khó để reviewer xem xét.

## 3. Quy tắc vẽ Bounding Box và xử lý tình huống

### R-01. Người đi xe máy

- Gán một box riêng cho xe máy với class `motorcycle`.
- Gán một box riêng cho người lái với class `person`.
- Box người bao gồm các phần cơ thể nhìn thấy như đầu, thân, tay và chân.
- Mũ bảo hiểm được tính trong box người vì mũ che phần đầu; không tách mũ thành đối tượng riêng.
- Người ngồi sau xe cũng được gán một box `person` riêng.
- Không gộp người và xe máy thành một box chung.

### R-02. Xe đầu kéo / xe chở xe

- Xe đầu kéo hoặc xe tải vận chuyển được gán class `truck`.
- Những chiếc ô tô được chở phía sau cũng được gán box riêng class `car` nếu nhìn thấy và nhận diện được.
- Không gộp các xe được chở vào box `truck`.
- Nếu một chiếc xe được chở bị che khuất, vẫn gán nếu nhận diện được và đánh dấu `occluded_level` phù hợp.
- Nếu không đủ căn cứ xác định class, đánh dấu `can_review`; không đoán class.

### R-03. Đối tượng bị che khuất (Occlusion)

- **Che khuất nhẹ:** vẫn gán box.
- **Che khuất một phần lớn:** vẫn gán nếu xác định được đối tượng.
- **Chỉ còn một phần nhỏ nhưng vẫn nhận diện chắc chắn:** vẫn gán box và đánh dấu mức occlusion cao phù hợp.
- **Không thể xác định đối tượng hoặc class:** không đoán class; chuyển review bằng `can_review` hoặc ghi vấn đề cấp ảnh.
- Box bao quanh phần đối tượng nhìn thấy theo quy ước của nhóm; không tự vẽ thêm phần bị che mà không có căn cứ.

### R-04. Vật thể nhỏ / ở rất xa

- Đối tượng ở xa vẫn được gán nếu có thể nhận diện chắc chắn class.
- Không bỏ qua chỉ vì đối tượng nhỏ.
- Nếu không nhận diện được đó là loại xe gì hoặc không đủ thông tin xác định class, đánh dấu `can_review` hoặc xử lý theo quy tắc vùng không chắc chắn của repository.
- Không tự đặt ngưỡng kích thước, ví dụ dưới 10 pixel thì bỏ qua, nếu nhóm chưa có quy định được thống nhất.

### R-05. Tượng và ma-nơ-canh

- Tượng và ma-nơ-canh không được gán class `person`.
- Nếu không phân biệt chắc chắn được người thật với tượng / ma-nơ-canh, đánh dấu `can_review` để reviewer xử lý.
- Không tự đoán là người thật chỉ vì hình dáng giống người.

### R-06. Phản chiếu và hình ảnh in

- Xe xuất hiện dưới dạng phản chiếu không được gán thành một đối tượng xe mới.
- Người xuất hiện dưới dạng phản chiếu không được gán thành `person`.
- Hình người hoặc phương tiện được in trên biển quảng cáo, poster hay bề mặt khác không được tính là đối tượng thực tế.
- Nếu không xác định được hình ảnh là người thật hay phản chiếu / hình in, chuyển review bằng `can_review`.

### R-07. Vật ngoài taxonomy

- Vật chắc chắn không thuộc bất kỳ class nào trong taxonomy thì không gán.
- Không tự ý tạo class mới hoặc gán vào class gần giống.
- Nếu chưa chắc vật có thuộc taxonomy hay không, đánh dấu `can_review`.

### R-08. Xe chủ (Ego vehicle)

- Có gán phương tiện đang chụp ảnh nếu chính phương tiện đó xuất hiện nhìn thấy được trong khung hình và thuộc một class trong taxonomy.
- Nếu phương tiện chỉ là góc nhìn của camera và bản thân phương tiện không xuất hiện trong ảnh, không tạo box.

### R-09. Đám đông

- Gán từng người bằng một box `person` riêng khi từng người có thể nhận diện được.
- Không gộp cả đám đông thành một box chung.
- Nếu một người bị che bởi người khác, áp dụng R-03.

### R-10. Đối tượng bị cắt mép ảnh (Truncated)

- Nếu đối tượng bị khung ảnh cắt mất một phần và vẫn được gán nhãn, đặt `truncated = true`, bất kể tỷ lệ phần nhìn thấy.
- Nếu đối tượng chỉ nằm sát mép nhưng vẫn hiển thị đầy đủ, đặt `truncated = false`.
- Bounding Box chỉ bao quanh phần đối tượng nhìn thấy bên trong ảnh; không suy đoán hoặc vẽ phần nằm ngoài khung.
- `truncated` không thay thế `occluded_level`. Nếu đối tượng vừa bị mép ảnh cắt vừa bị vật khác che, đánh dấu `truncated = true` và đồng thời chọn `occluded_level` theo tỷ lệ bị che khuất bởi vật khác.

### R-11. Đồ chơi mô hình

- Phân biệt đồ chơi / mô hình với phương tiện thật.
- Đồ chơi hoặc mô hình không được gán thành `car`, `truck`, `van` hoặc `motorcycle`.
- Nếu không phân biệt chắc chắn được mô hình với phương tiện thật, đánh dấu `can_review`.

### R-12. Một vật có nhiều phần: người và xe

- Người và phương tiện là hai đối tượng độc lập.
- Gán box riêng cho người và box riêng cho xe.
- Áp dụng R-01 cho người lái và người ngồi sau xe máy.
- Không tạo một box bao trọn cả người lẫn phương tiện.

## 4. Ca khó

Bảng dưới đây được lập sau khi xem trực tiếp 40 ảnh trong `data/images/` (`img_001.jpg` đến `img_040.jpg`). Các mã ảnh là ví dụ thực tế để minh họa quy tắc; khi annotation, vẫn phải kiểm tra từng đối tượng cụ thể trong ảnh.

| Ảnh | Tình huống thực tế quan sát được | Rule ID | Quyết định gán nhãn | Lý do / lưu ý |
|---|---|---|---|---|
| `img_002` | Xe đầu kéo chở nhiều ô tô | R-02 | Gán một box `truck` cho xe đầu kéo; gán box `car` riêng cho từng ô tô nhìn thấy và nhận diện được | Không gộp các ô tô được chở vào box `truck` |
| `img_005`, `img_006`, `img_010`, `img_026`, `img_035`, `img_040` | Người lái / người ngồi sau xe máy | R-01, R-12 | Gán box `person` riêng cho từng người và box `motorcycle` riêng cho xe; người ngồi sau cũng có box riêng | Không gộp người và xe; box người bao gồm phần đầu có mũ bảo hiểm cùng tay, chân và thân thể nhìn thấy |
| `img_005`, `img_008`, `img_021`, `img_040` | Người hoặc phương tiện bị che khuất / chồng lấn | R-03 | Vẫn gán nếu nhận diện được; đánh dấu `occluded_level` theo tỷ lệ bị che khuất | Không bỏ đối tượng chỉ vì bị che; không đoán class nếu không đủ căn cứ |
| `img_013`, `img_025`, `img_031`, `img_039` | Phương tiện hoặc người ở xa, kích thước nhỏ; một số ảnh có điều kiện ánh sáng khó | R-04 | Gán nếu nhận diện chắc chắn class; nếu không đủ thông tin thì đánh dấu `can_review` hoặc ghi vấn đề cấp ảnh | Không đặt ngưỡng pixel tùy ý và không đoán loại phương tiện |
| `img_017` | Tượng người cưỡi ngựa | R-05 | Không gán tượng thành `person`; không gán các phần tượng thành phương tiện thật | Đây là tượng, không phải người tham gia giao thông |
| `img_033` | Ma-nơ-canh trưng bày trong cửa hàng | R-05 | Không gán `person`; nếu không phân biệt chắc chắn với người thật thì chuyển review | Tránh nhầm ma-nơ-canh với người thật |
| `img_028` | Xe bán tải chở tượng ngựa | R-05, R-07 | Gán xe thật theo class phù hợp trong taxonomy; không gán tượng ngựa thành `person` hoặc phương tiện | Chỉ gán đối tượng thật thuộc taxonomy |
| `img_018` | Hình chân dung người in trên biển quảng cáo | R-06 | Không gán hình người trên biển quảng cáo thành `person` | Hình in không phải người thật trong cảnh |
| `img_015`, `img_020` | Hình phản chiếu phương tiện trên mặt đường ướt hoặc trong gương chiếu hậu | R-06 | Chỉ gán phương tiện thật nhìn thấy trực tiếp; không tạo box riêng cho hình phản chiếu | Tránh gán trùng một phương tiện do phản chiếu |
| `img_004`, `img_016`, `img_035`, `img_040` | Xe tuk-tuk / xe ba bánh có động cơ | R-07 | Không tự ép vào `motorcycle`, `car` hoặc `truck`; nếu nhóm xác nhận không thuộc taxonomy thì không gán, nếu chưa thống nhất thì đánh dấu review | Taxonomy hiện tại không có class `tuk-tuk`; cần nhóm thống nhất cách xử lý |
| `img_023`, `img_029` | Xe đạp / xe ba bánh đạp hoặc phương tiện dạng xích lô | R-07 | Không tự gán vào class xe máy; nếu ngoài taxonomy thì không gán, trường hợp chưa rõ thì review | Không có class `bicycle` trong danh sách class đang dùng |
| `img_006`, `img_021`, `img_032` | Nhiều người và phương tiện xuất hiện thành đám đông | R-09 | Gán từng người `person` riêng khi nhận diện được; gán từng phương tiện thuộc taxonomy riêng | Không gộp cả đám đông thành một box |
| `img_001`, `img_008`, `img_034` | Một số đối tượng nằm sát và bị khung ảnh cắt ở mép ảnh | R-10 | Nếu đối tượng bị mép ảnh cắt và vẫn được gán thì đặt `truncated = true`; box chỉ bao phần nhìn thấy trong ảnh | Không phụ thuộc tỷ lệ phần đối tượng còn nhìn thấy |
| `img_024`, `img_027`, `img_038` | Xe mô hình / xe trưng bày / mô hình xe dạng tượng | R-11 | Không gán mô hình thành `car` hoặc `truck`; nếu không phân biệt chắc chắn với xe thật thì chuyển review | Tránh nhầm đồ chơi, mô hình hoặc vật trưng bày với phương tiện thật |

### 4.1. Những tình huống chưa có ví dụ rõ ràng trong 40 ảnh

- **Ego vehicle:** Chưa xác định được ảnh nào thể hiện rõ phương tiện đang chụp ảnh xuất hiện như một đối tượng trong khung hình. Không tự ghi đây là ca đã quan sát; vẫn giữ quy tắc R-08 để áp dụng nếu gặp ở dữ liệu khác.
- **Trường hợp bị che hoàn toàn:** Bộ ảnh có các trường hợp che khuất và chồng lấn, nhưng không nên tự kết luận có một đối tượng bị che hoàn toàn mà vẫn xác định được danh tính. Nếu không nhận diện được thì không đoán class, chuyển review.
- **Đồ vật ngoài taxonomy khác:** Chỉ ghi thành ca thực tế khi xác định được đối tượng cụ thể trong ảnh; không tự bổ sung class mới.

**Lưu ý khi sử dụng bảng:**
1. Bảng này ghi nhận tình huống có thể quan sát trong ảnh, không phải danh sách box đã được annotation.
2. Một ảnh có thể minh họa nhiều Rule ID; khi gán nhãn phải áp dụng đồng thời các quy tắc liên quan.
3. Với tuk-tuk, xe đạp / xích lô và các phương tiện chưa có class tương ứng, cần ghi nhận để nhóm thống nhất ở Pha 2; không tự ý đổi taxonomy.
4. Nếu một ảnh không có tình huống tương ứng hoặc đối tượng không đủ rõ, không ép đưa vào một quyết định chắc chắn; sử dụng `can_review` theo quy định.

## 5. QC và phiên bản

### 5.1. Checklist QC cá nhân

- [ ] Người và phương tiện được gán bằng các box riêng.
- [ ] Người lái và người ngồi sau xe máy được gán riêng nếu nhìn thấy và nhận diện được.
- [ ] Xe đầu kéo được gán `truck`; từng ô tô được chở được gán `car` riêng nếu nhận diện được.
- [ ] Xe buýt được gán class `bus`, không nhầm với `truck`.
- [ ] Đối tượng bị che khuất được xử lý theo R-03 và `occluded_level`.
- [ ] Đối tượng nhỏ / ở xa không bị bỏ qua chỉ vì kích thước.
- [ ] Tượng, ma-nơ-canh, phản chiếu và hình in không bị gán nhầm thành đối tượng thực tế.
- [ ] Vật ngoài taxonomy không bị ép vào class có sẵn.
- [ ] Ca không chắc chắn được đánh dấu `can_review` hoặc ghi vấn đề cấp ảnh.
- [ ] Đối tượng bị cắt bởi mép ảnh được đánh dấu `truncated = true`, không phụ thuộc tỷ lệ phần nhìn thấy.
- [ ] `occluded_level` phản ánh tỷ lệ bị che bởi đối tượng khác, không nhầm với `truncated`.

### 5.2. Ca cần nhóm thống nhất ở Pha 2

1. Xác nhận cách ước lượng nhất quán các ngưỡng `occluded_level` và cách xử lý đối tượng bị che hoàn toàn / không thể nhận diện.
2. Cách sử dụng `ignore_region` theo đúng schema / hướng dẫn của repository.
3. Cách ghi nhận trường hợp không thể nhận diện class khi không có box để gắn `can_review`.
4. Xác nhận quy tắc ego vehicle và đồ chơi mô hình với ví dụ thực tế trong dataset.

### 5.3. Lịch sử thay đổi

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0.1 | Bổ sung quy tắc cá nhân R-01 đến R-12; đề xuất ngưỡng `occluded_level` và quy tắc `truncated` | Các tình huống edge case cần thống nhất trước khi annotation |
| v0.2 | Đổi ngưỡng `occluded_level` sang tỷ lệ bị che khuất; quy định `truncated = true` khi đối tượng bị mép ảnh cắt và vẫn được gán nhãn | Phân biệt rõ che khuất bởi vật khác và bị khung ảnh cắt |
| v0.3 | Bổ sung định nghĩa và checklist cho class `bus`; không thêm class `other_vehicle` | Thống nhất cách gán nhãn xe buýt mà không mở rộng sang class phương tiện chung |
| v1.0 | Chưa cập nhật | Chờ nhóm thảo luận và duyệt ở Pha 2 |
