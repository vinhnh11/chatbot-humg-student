
import asyncio
from ingestion.crawl_quy_dinh import main as crawl_main
from ingestion.pdf_to_docx import main as pdf_to_docx_main

if __name__ == "__main__":
    print("1. Crawl & download PDF mới nhất")
    print("2. Chuyển PDF → DOCX (OCR)")
    print("3. Chạy chatbot")
    choice = input("Chọn chức năng (1/2/3): ")

    if choice == "1":
        asyncio.run(crawl_main())
    elif choice == "2":
        pdf_to_docx_main()
    elif choice == "3":
        from rag.chatbot_cli import main as chatbot_main
        chatbot_main()
    else:
        print("Lựa chọn không hợp lệ.")