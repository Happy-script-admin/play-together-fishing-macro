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
