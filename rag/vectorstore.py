
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from processing.document_processor import DocumentProcessor
from config import DOCX_DIR
def build_vectorstore(verbose: bool = False):
    processor = DocumentProcessor()
    tai_lieu_tho = processor.read_word_folder(DOCX_DIR)

    bo_chia_chunk = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        separators=["\n\n", "\n", "Điều ", "Khoản ", "TIÊU ĐỀ:", "BẢNG DỮ LIỆU:", ". ", " "]
    )

    cac_chunk = bo_chia_chunk.split_documents(tai_lieu_tho)

    embeddings = HuggingFaceEmbeddings(
        model_name="bkai-foundation-models/vietnamese-bi-encoder"
    )

    kho_vector = FAISS.from_documents(cac_chunk, embeddings)
    return kho_vector