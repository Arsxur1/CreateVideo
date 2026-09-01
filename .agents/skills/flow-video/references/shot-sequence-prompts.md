# Prompt chuẩn — series "Dưới tán hoa"

Chuẩn viết prompt ảnh và video cho một chuỗi cảnh **diễn ra ở cùng một chỗ**.
Rút ra từ bản dựng 2 (anime 9:16, Ngày 10) sau khi phải sinh lại 3 trong 8 cảnh.

Đây là **luật**, không phải kịch bản: các khối cụ thể của từng tập viết thẳng
trong script sinh ảnh của tập đó, không chép vào đây.

---

## 1. Chuyện gì đã hỏng

Ba lỗi, 39 credits, đều truy về được đúng một câu prompt:

| Cảnh | Câu prompt đã viết | Model dựng ra | Vì sao |
|---|---|---|---|
| 4 | "she kneels on **the dry grass** and digs a small hole" | đào hố giữa bãi cỏ khô | Prompt tự mâu thuẫn: cảnh 5 và 8 viết "dark soil… edged with brick". Không phải model sai — **bản thân bộ prompt viết hai chỗ khác nhau** |
| 6 | "she tips a watering can over **the patch of soil**" | một dải đất hẹp cạnh lối đi, đã có cây mọc | "the patch" là mạo từ xác định trỏ vào thứ model chưa từng thấy. Mỗi ảnh sinh độc lập, **không tồn tại "the patch"** — model tự bịa một cái |
| 7 | "she has stood up and looks back over the patch of freshly turned soil" | đứng giẫm lên chính luống vừa gieo | Câu này nói cô **nhìn gì**, không nói cô **đứng ở đâu**. Chỗ trống thì model tự điền |

Prompt video lặp lại đúng khoảng trống đó: "she tips the watering can" không cấm
đi lại, nên clip cho cô vừa đi vừa tưới.

## 2. Nguyên nhân gốc

Bản dựng 2 ghim **nhân vật** rất chặt — dài tóc, kiểu váy, tay lửng, giày vải —
và kết quả là qua 8 cảnh trang phục và tóc không lệch một lần nào. Kỹ thuật đó
đúng và đã chứng minh được.

Nhưng **bối cảnh** thì chỉ được tả như phông nền: "khu vườn rộng bỏ hoang, cỏ
vàng, viền gạch thấp". Trong khi với một chuỗi 8 cảnh cùng một chỗ, bối cảnh
chính là thứ duy nhất khiến người xem tin đây là **một sự việc liên tục**. Nó
phải được ghim chặt ngang nhân vật.

Không cần kỹ thuật mới. Chỉ cần đem kỷ luật đã dùng cho danh từ thứ nhất áp
sang danh từ thứ hai.

## 3. Năm khối (trước là ba)

`STYLE` → `CHARACTER` → **`STAGE`** → **`ACTION`** → **`KHÔNG-CÓ-GÌ`**

Ba khối đầu **dán nguyên văn vào mọi prompt**, không diễn đạt lại. Diễn đạt lại
là cách trôi bắt đầu.

### STYLE — khoá phong cách
Ghim medium, bảng màu, chất ánh sáng, khung hình. Đặt **đầu tiên** để render
không bao giờ trôi về photoreal.

### CHARACTER — khoá người
Chỉ dùng thuộc tính **đo được**: độ dài tóc, màu tóc, kiểu váy, độ dài tay áo,
loại giày. Bỏ tính từ cảm xúc ("thanh thoát", "dịu dàng") — không tái lập được.

### STAGE — khoá chỗ đứng  ← khối mới, khối gánh việc
Ba câu, không thiếu câu nào:

1. **Một mảnh địa hình, tả bằng thuộc tính đo được.**
   "a wide rectangular raised bed of bare dark tilled soil, edged with a low
   red-brick wall, an old white-framed glasshouse standing directly behind it,
   dry pale-gold grass all around."
2. **Máy đặt đâu so với mảnh đó.** ("from behind her, looking across the bed
   toward the glasshouse")
3. **Chân nhân vật ở đâu.** ← câu bị quên, và là câu đắt nhất.
   "both feet on the grass outside the brick edge; she does not step on the soil."

Không bao giờ dùng "the patch", "the spot", "that area". Model không có trí
nhớ giữa các lần sinh — mạo từ xác định là một lời mời bịa.

### ACTION — một nhịp, cộng thứ đứng yên
Một hành động cho 6–10 giây. Rồi nói rõ **cái gì không đổi**:
"She does not walk. The bed stays empty — nothing is growing in it."

### KHÔNG-CÓ-GÌ — nói cái vắng mặt bằng câu khẳng định
Veo và gpt-image không có negative prompt. Nêu từng mâu thuẫn mà **riêng cảnh
này** có thể đẻ ra:
- cảnh 6: "The bed is empty — no plants, no seedlings, nothing growing in it yet."
- cảnh 8: "The soil is bare — there is NO seed lying on top of it."

## 4. Prompt ảnh — khung

```
{STYLE}{CHARACTER}{STAGE}
{ACTION: một nhịp + cái gì đứng yên}
{KHÔNG-CÓ-GÌ: mâu thuẫn riêng của cảnh này, viết khẳng định}
```

Với cảnh chỉ có bàn tay (3, 5, 8) thì bỏ CHARACTER, giữ STAGE — cận cảnh vẫn
phải cho thấy đúng nền đất và đúng viền gạch, nếu không cắt về cảnh rộng là lộ.

## 5. Prompt video — khung

Flow **sinh lại** chứ không phát ảnh, nên mọi ràng buộc phải nhắc lại. Prompt
video thêm ba thứ prompt ảnh không có:

```
{Máy: locked-off / slow push-in / pan left to right}
{ACTION: đúng một nhịp, viết lại từ prompt ảnh}
{ĐỨNG YÊN: cái gì không được đổi, viết thẳng}
{ambient: hai đến ba tiếng động hiện trường}
no dialogue, no music, no voices.
```

Ghi chú đã đo được:
- **"Locked-off"** dùng cho mọi cảnh có chữ hoặc logo trong khung. Cảnh 8 giữ
  nguyên được logo suốt 6 giây là nhờ câu "the sign itself stays perfectly
  still and unchanged — the lettering does not move, warp or alter".
- **Viết prompt bằng tiếng Anh** kể cả dự án tiếng Việt: bám thuật ngữ máy và
  ống kính chặt hơn hẳn.
- **Bắt buộc có `ambient:`** — thiếu thì Veo tự bịa lời thoại lẩm bẩm.
- Một nhịp một clip. Hai hành động đẻ ra một cú cắt mình không đặt và không sửa được.

## 6. Checklist trước khi tiêu credit

Chạy trên **toàn bộ** bảng prompt, trước cảnh đầu tiên:

- [ ] Mọi cảnh ngoại cảnh có khối `STAGE` giống nhau **từng chữ**?
- [ ] Có cảnh nào tả nền đất khác các cảnh còn lại không? (đây là lỗi cảnh 4)
- [ ] Có chữ "the patch" / "the spot" / "that area" nào còn sót? (lỗi cảnh 6)
- [ ] Mọi cảnh có người: đã nói **chân đứng ở đâu** chưa? (lỗi cảnh 7)
- [ ] Mỗi cảnh có đúng một hành động?
- [ ] Cảnh nào có thứ đã bị chôn/phủ ở cảnh trước — đã viết câu khẳng định là nó không lộ ra chưa?
- [ ] Prompt video có `ambient:` và `no dialogue` chưa?

Sau khi sinh xong: `python scripts/flow_continuity_check.py <clip-dir>`, rồi
quét bốn lượt theo `.agents/skills/flow-video/SKILL.md`. **Sửa xong một cảnh
phải quét lại cả tám** — sửa cảnh 4 mới lòi cảnh 6, sửa cảnh 6 mới lòi cảnh 7.
