import os
from pdf2image import convert_from_path
import pytesseract
from docx import Document

from config import PDF_DIR, DOCX_DIR, TESSERACT_CMD

# Cấu hình Tesseract ngay đầu file
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# Tạo thư mục nếu chưa có (an toàn)
os.makedirs(DOCX_DIR, exist_ok=True)


def main():
    print("Bắt đầu chuyển đổi PDF → DOCX (chỉ xử lý file chưa có DOCX)...\n")

    count_new = 0
    count_skip = 0

    for filename in os.listdir(PDF_DIR):
        if filename.lower().endswith((".pdf", ".PDF")):  # hỗ trợ cả .pdf và .PDF
            pdf_path = os.path.join(PDF_DIR, filename)

            # Tạo tên file DOCX tương ứng (xử lý cả .pdf và .PDF)
            docx_filename = filename.replace(".pdf", ".docx").replace(".PDF", ".docx")
            docx_path = os.path.join(DOCX_DIR, docx_filename)

            # Kiểm tra nếu file DOCX đã tồn tại thì bỏ qua
            if os.path.exists(docx_path):
                print(f"Bỏ qua (đã có): {filename} → {docx_filename}")
                count_skip += 1
                continue

            try:
                print(f"Đang OCR: {filename}...")
                images = convert_from_path(pdf_path, dpi=300)
                doc = Document()

                for img in images:
                    text = pytesseract.image_to_string(img, lang="vie")
                    doc.add_paragraph(text)

                doc.save(docx_path)
                print(f"OCR xong: {filename} → {docx_path}")
                count_new += 1

            except Exception as e:
                print(f"Lỗi xử lý {filename}: {e}")

    print(f"\nHoàn tất!")
    print(f"- Mới OCR: {count_new} file")
    print(f"- Bỏ qua (đã có): {count_skip} file")


if __name__ == "__main__":
    main()