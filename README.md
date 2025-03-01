---
**Tên dự án:** AutoSubtitle  
**Mục đích:** Tự động tạo phụ đề cho video MP4 bằng Whisper (mô hình nhận diện giọng nói) và nhúng phụ đề vào video sử dụng FFmpeg, đảm bảo xử lý hàng loạt file trong một thư mục và các thư mục con.  

**Tính năng chính:**
1. **Tạo phụ đề:** Sử dụng Whisper để tạo file phụ đề (.srt) từ video, với cấu hình mặc định sử dụng mô hình "small" và ngôn ngữ tiếng Anh.
2. **Nhúng phụ đề:** Sử dụng FFmpeg để nhúng phụ đề vào video, tạo ra các file video có phụ đề mà không làm mất chất lượng âm thanh hoặc video gốc.
3. **Xử lý hàng loạt:** Tìm và xử lý tất cả file MP4 trong một thư mục và các thư mục con.
4. **Quản lý file duy nhất:** Tự động tạo tên file duy nhất (ví dụ: `video_subtitled.mp4`, `video_subtitled_1.mp4`, v.v.) để tránh ghi đè hoặc trùng lặp file.
5. **Ghi log chi tiết:** Sử dụng logging để theo dõi tiến trình, lưu thông tin vào file `subtitle_processor.log` và hiển thị trên console.
6. **Xử lý lỗi:** Bao gồm xử lý các lỗi phổ biến như timeout, lỗi FFmpeg, lỗi Whisper, và ngắt chương trình bởi người dùng (Ctrl+C).

**Công cụ yêu cầu:**
- Python 3.x
- Thư viện Whisper (cài đặt qua pip: `pip install whisper`)
- FFmpeg (cài đặt qua hệ thống hoặc package manager)
- Các thư viện Python: `os`, `subprocess`, `glob`, `logging`, `shutil`, `pathlib`, `signal`, `sys`

**Đặc điểm nổi bật:**
- Hỗ trợ xử lý nhiều video cùng lúc với tiến độ hiển thị.
- Đảm bảo không ghi đè file gốc hoặc tạo file trùng lặp.
- Có thể ngắt chương trình an toàn bằng Ctrl+C.
- Ghi lại thông tin chi tiết về thành công, thất bại, và các file bị bỏ qua.

---

### **Cách sử dụng đoạn code**

#### **1. Cài đặt môi trường**
Trước khi chạy code, bạn cần:

1. **Cài đặt Python 3.x** (nếu chưa có):
   - Tải và cài đặt từ [python.org](https://www.python.org/downloads/).

2. **Cài đặt Whisper**:
   - Mở terminal/command prompt và chạy:
     ```bash
     pip install whisper
     ```

3. **Cài đặt FFmpeg**:
   - Tải FFmpeg từ [ffmpeg.org](https://ffmpeg.org/download.html) và cài đặt theo hướng dẫn cho hệ điều hành của bạn (Windows, macOS, hoặc Linux).
   - Đảm bảo FFmpeg có thể được gọi từ dòng lệnh (thêm đường dẫn FFmpeg vào biến môi trường PATH nếu cần).

4. **Lưu code vào file**:
   - Lưu code vào một file Python, ví dụ: `AutoSubtitle.py`.

#### **2. Chuẩn bị thư mục video**
- Đặt các file video MP4 cần xử lý vào một thư mục cụ thể, ví dụ: `C:\Users\Downloads\VideoFolder`.
- Đảm bảo bạn có quyền đọc/ghi trong thư mục đó.

#### **3. Chạy chương trình**
- Mở terminal/command prompt, điều hướng đến thư mục chứa file `AutoSubtitle.py`, và chạy:
  ```bash
  python AutoSubtitle.py
  ```
- Khi được yêu cầu, nhập đường dẫn thư mục chứa video:
  ``` 
  Enter the video folder path: C:\Users\Downloads\VideoFolder
  ```

#### **4. Theo dõi tiến trình**
- Chương trình sẽ:
  - Tìm tất cả file `.mp4` trong thư mục và các thư mục con.
  - Tạo phụ đề (.srt) cho từng video nếu chưa có, sử dụng Whisper.
  - Nhúng phụ đề vào video sử dụng FFmpeg, tạo file mới với hậu tố `_subtitled.mp4` (hoặc `_subtitled_X.mp4` nếu file đã tồn tại).
  - Hiển thị tiến độ (ví dụ: "Processing video 1/5: Video1.mp4") và ghi log chi tiết vào file `subtitle_processor.log`.
- Khi hoàn tất, chương trình sẽ hiển thị tóm tắt:
  ``` 
  Processing Summary:
  Successfully processed: X
  Failed: Y
  Skipped: Z
  ```

#### **5. Kiểm tra kết quả**
- Kiểm tra thư mục video để xem các file đã được xử lý:
  - File gốc (ví dụ: `Video1.mp4`) có thể được thay thế bằng phiên bản có phụ đề, hoặc giữ nguyên nếu đã có phiên bản subtitled (tuỳ thuộc vào logic giữ file gốc).
  - Các file phụ đề (.srt) được lưu trong thư mục con `subtitles` trong cùng thư mục video.
- Xem file `subtitle_processor.log` để kiểm tra chi tiết tiến trình và bất kỳ lỗi nào (nếu có).

#### **6. Ngắt chương trình (nếu cần)**
- Nếu muốn dừng chương trình, nhấn `Ctrl+C`. Chương trình sẽ thoát một cách an toàn và ghi lại thông báo trong log: "Process interrupted by user".

#### **7. Cấu hình tùy chỉnh (nếu cần)**
- Bạn có thể chỉnh sửa các tham số trong class `SubtitleProcessor`:
  - `whisper_model`: Thay đổi mô hình Whisper (ví dụ: 'medium', 'large') trong `__init__`.
  - `language`: Thay đổi ngôn ngữ (ví dụ: 'Vietnamese', 'Spanish') trong `__init__`.
  - `timeout`: Điều chỉnh thời gian timeout cho Whisper (600 giây) hoặc FFmpeg (300 giây) trong các phương thức `generate_subtitles` và `embed_subtitles`.

---

### **Lưu ý quan trọng**
- Đảm bảo đường dẫn thư mục không chứa ký tự đặc biệt hoặc khoảng trắng không cần thiết để tránh lỗi đường dẫn.
- Nếu gặp lỗi liên quan đến Whisper hoặc FFmpeg, kiểm tra cài đặt và đảm bảo cả hai công cụ hoạt động đúng từ dòng lệnh.
- Nếu video lớn hoặc phức tạp, có thể cần tăng `timeout` trong code để tránh lỗi timeout.

---

### **Ví dụ đầu ra**
Giả sử bạn chạy với thư mục chứa `Video1.mp4`:
- Log sẽ hiển thị:
  ``` 
  2025-03-01 20:41:49,143 - INFO - Processing video 1/5: Video1.mp4
  2025-03-01 20:41:49,143 - INFO - Generating subtitles for: Video1.mp4
  2025-03-01 20:42:27,467 - INFO - Successfully generated subtitles for: Video1.mp4
  2025-03-01 20:42:27,467 - INFO - Embedding subtitles into: Video1.mp4
  2025-03-01 20:42:30,123 - INFO - Successfully embedded subtitles into: Video1.mp4
  ```
- Kết quả:
  - File `Video1.mp4` sẽ được thay thế bằng phiên bản có phụ đề (hoặc tạo `Video1_subtitled.mp4` nếu giữ file gốc).
  - File phụ đề `Video1.srt` được lưu trong `subtitles` folder.

---
