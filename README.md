# 🎣 Auto Fishing Macro (Play Together)

Ứng dụng tự động hóa câu cá (Auto Fishing Bot) dành cho tựa game **Play Together** (phiên bản PC/Steam), được xây dựng bằng **Python** kết hợp với thư viện xử lý ảnh **OpenCV**.

---

## 🚀 Tính Năng Nổi Bật

* **Giao diện hiện đại (Dark Theme):** Tích hợp bảng điều khiển trực quan với CustomTkinter, hỗ trợ thanh tiến trình (Progress Bar) theo từng giai đoạn câu cá.
* **Theo dõi thống kê thời gian thực:** Hiển thị trực quan số lượng cá đã câu thành công (`🐟 Cá câu được`) và số lần phải kiểm tra/lỗi nhịp (`⚠️ Check lại`).
* **Nhận diện thông minh qua thị giác máy tính:** 
  * Quét và đối chiếu trạng thái nhân vật thông qua thuật toán lọc cạnh Canny Edge & Template Matching (`cv2.matchTemplate`).
  * Phát hiện cá cắn câu bằng cách phân tích sự thay đổi pixel khác biệt (`cv2.absdiff`) tại vùng phao.
* **Phím tắt nhanh:** Hỗ trợ phím **`F4`** để Bật/Tắt (Toggle) bot nhanh chóng ngay cả khi đang trong game.

---

## ⚙️ Hướng Dẫn Cài Đặt & Sử Dụng

### 1. Dành cho người dùng thông thường (Chạy file `.exe`)
* Bạn chỉ cần tải file `.exe` đã được đóng gói sẵn về máy.
* Mở game **Play Together** trên Steam ở chế độ cửa sổ hoặc toàn màn hình phù hợp.
* Khởi chạy ứng dụng `Auto Fishing Macro.exe`.

### 2. Dành cho lập trình viên (Chạy mã nguồn `.py` / `.pyw`)
Đảm bảo máy tính đã cài đặt Python, sau đó cài đặt các thư viện phụ thuộc bằng lệnh:
```bash
pip install customtkinter mss keyboard opencv-python numpy pillow
```

### 3. Các bước thiết lập trong ứng dụng
1. **Vùng Check Cá:** Ban đầu thả cần trước rồi bấm nút `1. Vùng Check Cá`, sau đó kéo chuột quét vùng ở trên đầu nhân vật, đúng vị trí mà dấu chấm than (`!`) sẽ xuất hiện khi cá cắn câu (frame quét càng nhỏ thì càng chuẩn vì frame chỉ quét thay đổi pixel trên 20%) sau khi chọn xong thì rút cần lại và không được di chuyển camera tránh lệch frame đã tạo.
2. **Vùng Avatar:** Bấm nút `2. Vùng Avatar`, khoét ô ôm sát vào trong khu vực Avatar của nhân vật (tránh quét tràn ra ngoài hoặc trúng nền động).
3. **Chạy Bot:** Bấm nút `START` hoặc nhấn phím **`F4`** để bắt đầu quá trình tự động hóa (yêu cầu cầm sẵn cần câu và ở thế chưa thả cần).

<p align="center">
  <video src="https://github.com/user-attachments/assets/34673f04-47de-401f-a3bf-44d64ae156cb" width="100%" controls></video>
</p>
---

## ⚠️ Lưu Ý Cực Kỳ Quan Trọng Khi Vận Hành (Rất Quan Trọng)

Để bot hoạt động chính xác và không bị lỗi nhịp, bạn bắt buộc phải tuân thủ các nguyên tắc sau trong suốt quá trình chạy (running):

* **Thiết lập Vùng Chọn (Selection):**
  * **Vùng Avatar (2. Vùng Avatar):** Yêu cầu quét ôm sát vào trong khu vực Avatar của nhân vật, tuyệt đối không quét tràn ra ngoài hoặc trúng các phần nền/chi tiết có thể thay đổi pixel động (như hiệu ứng xung quanh, chuyển động nền) dẫn đến sai lệch nhận diện.  
  * **Vùng Check Cá (1. Vùng Check Cá):** Yêu cầu quét vùng ở trên đầu nhân vật (ở trên phần tên của mình), đúng vị trí mà dấu chấm than (`!`) sẽ xuất hiện khi cá cắn câu.
* **Không di chuyển Camera:** Trong suốt quá trình bot chạy, tuyệt đối không xoay hay di chuyển góc nhìn camera nếu chưa hiểu rõ logic hoạt động của macro, tránh việc hệ thống nhận diện nhầm trạng thái cá cắn câu.
* **Cố định cửa sổ game:** Không kéo dịch chuyển hoặc thu nhỏ/phóng to cửa sổ game Play Together để tránh làm lệch khung hình (frame) quét tọa độ đã thiết lập.
* **Giữ tập trung ở cửa sổ game:** Bot sẽ tự động giả lập phím bấm (`Space` và phím `F`) để thực hiện toàn bộ quy trình thả cần, đợi cá và giật cần. Do đó, bạn phải giữ con trỏ/cửa sổ game ở trạng thái hoạt động trong suốt quá trình bot chạy.

---

## ⌨️ Phím Tắt Hệ Thống
* **`F4`**: Bật (`START`) hoặc Tắt (`STOP`) nhanh bot.

---

## 📄 License
Dự án này được phân phối dưới giấy phép mã nguồn mở phục vụ cho mục đích học tập và nghiên cứu kỹ thuật (afk farm là chính😉).

## 📥 Downloads

**Python file (.zip):**
[![Download .py](https://img.shields.io/badge/Download-.py-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://raw.githubusercontent.com/Happy-script-admin/play-together-fishing-macro/main/AutoFishingPy.zip)

**Raw:**
[![View .raw](https://img.shields.io/badge/View-raw-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://raw.githubusercontent.com/Happy-script-admin/play-together-fishing-macro/main/AutoFishing.py)

**EXE file (.zip):**
[![Download .exe](https://img.shields.io/badge/Download-.exe-Red?style=for-the-badge&logo=mega&logoColor=white)](https://mega.nz/file/CYkCyTBJ#G5E7nKKcMnPYxKaEcmDcs5DqwPs_vwnEoM_MTgYtcxk)
