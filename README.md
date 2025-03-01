
---

### **Tổng quan dự án: AutoSubtitle**
**Tên dự án:** AutoSubtitle  
**Mục tiêu:** Tự động hóa việc tạo và nhúng phụ đề cho các file video MP4 bằng cách sử dụng mô hình nhận diện giọng nói Whisper và công cụ nhúng phụ đề FFmpeg. Chương trình hỗ trợ xử lý hàng loạt file trong một thư mục, bao gồm cả các thư mục con, một cách hiệu quả và đáng tin cậy.

**Các tính năng chính:**
1. **Tạo phụ đề:** Sử dụng Whisper để tạo file phụ đề định dạng .srt từ video, với cài đặt mặc định là mô hình "small" và ngôn ngữ tiếng Anh.
2. **Nhúng phụ đề:** Sử dụng FFmpeg để tích hợp phụ đề vào video, đảm bảo chất lượng âm thanh và video gốc không bị ảnh hưởng.
3. **Xử lý hàng loạt:** Tự động tìm và xử lý tất cả file MP4 trong một thư mục và các thư mục con.
4. **Quản lý file duy nhất:** Tự động tạo tên file độc nhất (ví dụ: `video_subtitled.mp4`, `video_subtitled_1.mp4`, v.v.) để tránh ghi đè hoặc trùng lặp file.
5. **Ghi log chi tiết:** Sử dụng hệ thống logging để theo dõi tiến trình, lưu thông tin vào file `subtitle_processor.log` và hiển thị trên màn hình console.
6. **Xử lý lỗi:** Hỗ trợ xử lý các lỗi phổ biến như timeout, lỗi từ FFmpeg, lỗi từ Whisper, và ngắt chương trình bởi người dùng (Ctrl+C).

**Yêu cầu công cụ:**
- Python 3.x
- Thư viện Whisper (cài đặt qua lệnh: `pip install whisper`)
- FFmpeg (cài đặt qua trang chính thức hoặc package manager)
- Các thư viện Python: `os`, `subprocess`, `glob`, `logging`, `shutil`, `pathlib`, `signal`, `sys`

**Điểm nổi bật:**
- Xử lý đồng thời nhiều video với hiển thị tiến độ rõ ràng.
- Đảm bảo không ghi đè file gốc hoặc tạo file trùng lặp.
- Hỗ trợ ngắt chương trình an toàn bằng phím Ctrl+C.
- Cung cấp báo cáo chi tiết về số file thành công, thất bại, và bị bỏ qua.

---

### **Hướng dẫn sử dụng đoạn code**

#### **1. Cài đặt môi trường**
Trước khi chạy chương trình, bạn cần thực hiện các bước sau:

1. **Cài đặt Python 3.x** (nếu chưa có):
   - Tải và cài đặt Python từ [python.org](https://www.python.org/downloads/).

2. **Cài đặt Whisper**:
   - Mở terminal hoặc command prompt và chạy lệnh sau:
     ```bash
     pip install whisper
     ```

3. **Cài đặt FFmpeg**:
   - Tải FFmpeg từ [ffmpeg.org](https://ffmpeg.org/download.html) và cài đặt theo hướng dẫn dành cho hệ điều hành của bạn (Windows, macOS, hoặc Linux).
   - Đảm bảo FFmpeg có thể được gọi từ dòng lệnh bằng cách thêm đường dẫn của FFmpeg vào biến môi trường PATH (nếu cần).

4. **Lưu code vào file**:
   - Lưu đoạn code vào một file Python, ví dụ: `AutoSubtitle.py`.

#### **2. Chuẩn bị thư mục video**
- Đặt tất cả các file video MP4 cần xử lý vào một thư mục cụ thể, chẳng hạn: `C:\Users\Downloads\VideoFolder`.
- Đảm bảo bạn có quyền truy cập đọc và ghi trong thư mục đó.

#### **3. Khởi chạy chương trình**
- Mở terminal hoặc command prompt, truy cập thư mục chứa file `AutoSubtitle.py`, và chạy:
  ```bash
  python AutoSubtitle.py
  ```
- Khi được yêu cầu, nhập đường dẫn đến thư mục chứa video:
  ```
  Enter the video folder path: C:\Users\Downloads\VideoFolder
  ```

#### **4. Theo dõi tiến trình**
- Chương trình sẽ:
  - Tự động tìm kiếm tất cả file `.mp4` trong thư mục chỉ định và các thư mục con.
  - Tạo file phụ đề (.srt) cho từng video nếu chưa tồn tại, sử dụng Whisper.
  - Nhúng phụ đề vào video bằng FFmpeg, tạo ra file mới với hậu tố `_subtitled.mp4` (hoặc `_subtitled_X.mp4` nếu file đã tồn tại).
  - Hiển thị tiến độ trên console (ví dụ: "Processing video 1/5: Video1.mp4") và ghi log chi tiết vào file `subtitle_processor.log`.
- Khi hoàn tất, chương trình sẽ hiển thị tóm tắt kết quả:
  ```
  Processing Summary:
  Successfully processed: X
  Failed: Y
  Skipped: Z
  ```

#### **5. Kiểm tra kết quả**
- Kiểm tra thư mục video để xem các file đã được xử lý:
  - File gốc (ví dụ: `Video1.mp4`) có thể được thay thế bằng phiên bản có phụ đề, hoặc giữ nguyên nếu đã có phiên bản subtitled (tùy thuộc vào logic bảo toàn file gốc).
  - Các file phụ đề (.srt) sẽ được lưu trong thư mục con `subtitles` trong cùng thư mục video.
- Xem file `subtitle_processor.log` để kiểm tra chi tiết về tiến trình và bất kỳ lỗi nào (nếu có).

#### **6. Ngắt chương trình (nếu cần)**
- Nếu muốn dừng chương trình, nhấn `Ctrl+C`. Chương trình sẽ thoát an toàn và ghi thông báo vào log: "Process interrupted by user".

#### **7. Tùy chỉnh cấu hình (nếu cần)**
- Bạn có thể điều chỉnh các tham số trong class `SubtitleProcessor`:
  - `whisper_model`: Thay đổi mô hình Whisper (ví dụ: 'medium', 'large') trong phương thức `__init__`.
  - `language`: Thay đổi ngôn ngữ (ví dụ: 'Vietnamese', 'Spanish') trong phương thức `__init__`.
  - `timeout`: Điều chỉnh thời gian timeout cho Whisper (600 giây) hoặc FFmpeg (300 giây) trong các phương thức `generate_subtitles` và `embed_subtitles`.

---

### **Lưu ý quan trọng**
- Đảm bảo đường dẫn thư mục không chứa ký tự đặc biệt hoặc khoảng trắng không cần thiết để tránh lỗi đường dẫn.
- Nếu gặp lỗi liên quan đến Whisper hoặc FFmpeg, kiểm tra cài đặt và đảm bảo cả hai công cụ hoạt động chính xác từ dòng lệnh.
- Với các video lớn hoặc phức tạp, bạn có thể cần tăng giá trị `timeout` trong code để tránh lỗi timeout.

---

### **Ví dụ kết quả**
Giả sử bạn chạy chương trình với thư mục chứa file `Video1.mp4`:
- Ghi log sẽ hiển thị:
  ```
  2025-03-01 20:41:49,143 - INFO - Processing video 1/5: Video1.mp4
  2025-03-01 20:41:49,143 - INFO - Generating subtitles for: Video1.mp4
  2025-03-01 20:42:27,467 - INFO - Successfully generated subtitles for: Video1.mp4
  2025-03-01 20:42:27,467 - INFO - Embedding subtitles into: Video1.mp4
  2025-03-01 20:42:30,123 - INFO - Successfully embedded subtitles into: Video1.mp4
  ```
- Kết quả:
  - File `Video1.mp4` sẽ được thay thế bằng phiên bản có phụ đề (hoặc tạo `Video1_subtitled.mp4` nếu giữ file gốc).
  - File phụ đề `Video1.srt` sẽ được lưu trong thư mục `subtitles`.

---

