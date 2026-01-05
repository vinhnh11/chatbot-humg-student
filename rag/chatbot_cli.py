
from rag.chain import create_conversation_chain


def main():
    print("Xin chào! Tôi là trợ lý tư vấn quy định Trường Đại học Mỏ - Địa chất.")
    print("Gõ 'tạm biệt' để thoát.\n")

    chain = create_conversation_chain()
    lich_su_tro_chuyen = []

    while True:
        cau_hoi = input("Bạn: ").strip()

        if cau_hoi.lower() in ["tạm biệt", "bye", "thoát", "exit"]:
            print("Cảm ơn bạn đã sử dụng! Hẹn gặp lại nhé.")
            break

        if not cau_hoi:
            continue

        try:
            ket_qua = chain.invoke({
                "question": cau_hoi,
                "chat_history": lich_su_tro_chuyen
            })

            print(f"Trợ lý: {ket_qua['answer']}\n")

            lich_su_tro_chuyen.append((cau_hoi, ket_qua["answer"]))
            if len(lich_su_tro_chuyen) > 10:
                lich_su_tro_chuyen = lich_su_tro_chuyen[-10:]

        except Exception as e:
            print("Hệ thống gặp lỗi tạm thời:", e)


if __name__ == "__main__":
    main()
