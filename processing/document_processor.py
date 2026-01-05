import os
import re
import logging
from docx import Document as DocxDocument
from langchain_core.documents import Document

from config import DOCX_DIR

logger = logging.getLogger(__name__)


class DocumentProcessor:
    def __init__(self, verbose: bool = False):
        """
        verbose = True  -> in log khi debug / crawl
        verbose = False -> im lặng khi chạy chatbot
        """
        self.verbose = verbose

    def lam_sach_ocr(self, van_ban: str) -> str:
        if not van_ban:
            return ""

        thay_the = {
            'Mó': 'Mỏ', 'chât': 'chất', 'QĐÐ': 'QĐ',
            'đục': 'dục', 'đồi': 'đổi', 'bồ': 'bổ',
            'bồ sung': 'bổ sung', 'sửa đỏi': 'sửa đổi',
            'sửa đồi': 'sửa đổi', 'phề`^1n': 'phần',
            'học phe`^1n': 'học phần',
            'HƯMG': 'HUMG', 'CTCT-SV': 'CTCT-SV',
            'Ô': '0', 'ø': '0', 'Ó': '0', 'ƒ': '2',
            't/hiện': 'thực hiện', 'p/hợp': 'phối hợp',
            'Địa chât': 'Địa chất', 'Mó - Địa chât': 'Mỏ - Địa chất',
        }

        for sai, dung in thay_the.items():
            van_ban = van_ban.replace(sai, dung)

        van_ban = re.sub(r'\s+', ' ', van_ban)
        van_ban = re.sub(
            r'[^\w\s\.,;:!?\-\(\)/đĐáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ]',
            ' ',
            van_ban
        )
        return van_ban.strip()

    def read_word(self, path: str):
        docs = []
        try:
            doc = DocxDocument(path)
            name = os.path.basename(path)

            # Paragraphs
            for p in doc.paragraphs:
                text_raw = p.text.strip()
                if text_raw:
                    text_clean = self.lam_sach_ocr(text_raw)
                    if text_clean:
                        docs.append(
                            Document(
                                page_content=f"[Word:{name}] {text_clean}",
                                metadata={"source": name, "type": "paragraph"}
                            )
                        )

            # Tables
            for i, t in enumerate(doc.tables):
                rows = []
                for r in t.rows:
                    cells = [c.text.strip() for c in r.cells if c.text.strip()]
                    if cells:
                        cleaned = [self.lam_sach_ocr(c) for c in cells]
                        rows.append(" | ".join(cleaned))

                if rows:
                    docs.append(
                        Document(
                            page_content=f"[Table {i+1}:{name}]\n" + "\n".join(rows),
                            metadata={
                                "source": name,
                                "type": "table",
                                "table_index": i + 1
                            }
                        )
                    )

        except Exception as e:
            logger.exception(f"Lỗi đọc file {path}: {e}")

        return docs

    def read_word_folder(self, folder_path: str):
        docs = []

        docx_files = sorted(
            f for f in os.listdir(folder_path)
            if f.lower().endswith(".docx")
        )

        if self.verbose:
            logger.info(
                f"Tìm thấy {len(docx_files)} file .docx trong thư mục {folder_path}"
            )

        for file in docx_files:
            if self.verbose:
                logger.info(f"Đang xử lý: {file}")

            path = os.path.join(folder_path, file)
            docs.extend(self.read_word(path))

        return docs


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    processor = DocumentProcessor(verbose=True)
    all_docs = processor.read_word_folder(DOCX_DIR)

    print(f"\nTổng số đoạn văn bản sau khi đọc và làm sạch: {len(all_docs)}")
    if all_docs:
        print("Test doc:")
        print(all_docs[0].page_content)
        print("Metadata:", all_docs[0].metadata)
