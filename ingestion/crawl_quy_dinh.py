import asyncio
import hashlib
import json
import os
import requests
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime
from config import MAIN_URL, API_LOC_QUYDINH, PDF_DIR, METADATA_PATH

CLICK_WAIT = 2000

os.makedirs(PDF_DIR, exist_ok=True)

async def get_all_ids():
    ids = set()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        async def handle_response(response):
            if "w-locdsquydinh" in response.url:
                try:
                    data = await response.json()
                    item = data.get("data", {}).get("quy_dinh", {})
                    if item and "id" in item:
                        ids.add(item["id"])
                        print("📡 Bắt được ID:", item["id"])
                except:
                    pass

        page.on("response", handle_response)

        # Mở trang
        await page.goto(MAIN_URL)
        await page.wait_for_timeout(50000)
        try:
            await page.click("li.el-menu-item:has-text('Quy chế – Quy định')")
            await page.wait_for_timeout(CLICK_WAIT)
        except:
            pass

        # Lấy tất cả mục con
        items = await page.query_selector_all("li.el-menu-item")
        total = len(items)
        print(f"Tổng số mục con tìm được: {total}")

        for index in range(total):
            items = await page.query_selector_all("li.el-menu-item")
            print(f"➡ Click mục {index + 1}/{total}...")
            try:
                await items[index].click()
                await page.wait_for_timeout(CLICK_WAIT)
            except:
                print("Click lỗi mục", index + 1)

        await browser.close()

    return list(ids)

def download_pdfs(ids):
    headers = {"Content-Type": "application/json"}

    # Load metadata cũ
    metadata = {}
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

    for id_ in ids:
        payload = {"filter": {"id": id_}}
        try:
            res = requests.post(API_LOC_QUYDINH, headers=headers, json=payload, timeout=10)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            print(f" Lỗi lấy nội dung ID {id_}: {e}")
            continue

        html_content = data.get("data", {}).get("quy_dinh", {}).get("noi_dung", "")
        if not html_content:
            continue

        soup = BeautifulSoup(html_content, "html.parser")
        links = soup.find_all("a")

        for link in links:
            pdf_url = link.get("href")
            if not pdf_url:
                continue
            if not pdf_url.startswith("http"):
                pdf_url = "https://daotaodaihoc.humg.edu.vn" + pdf_url

            filename = pdf_url.split("/")[-1]
            filepath = os.path.join(PDF_DIR, filename)

            try:
                response = requests.get(pdf_url, timeout=15)
                response.raise_for_status()
                content = response.content
                current_hash = hashlib.md5(content).hexdigest()

                if filename in metadata and metadata[filename]['hash'] == current_hash:
                    print(f" Không thay đổi: {filename}")
                    continue

                with open(filepath, 'wb') as f:
                    f.write(content)
                metadata[filename] = {
                    'hash': current_hash,
                    'url': pdf_url,
                    'last_updated': str(datetime.now())
                }
                print(f"⬇ Đã tải/cập nhật: {filename}")

            except Exception as e:
                print(f"Lỗi tải {pdf_url}: {e}")

    # Lưu metadata
    with open(METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

async def main():
    print("BẮT ĐẦU QUÉT TẤT CẢ QUY CHẾ...\n")
    ids = await get_all_ids()
    if not ids:
        print("Không lấy được ID nào, kết thúc.")
        return
    print("\nID thu được:", ids)
    print("Tổng số ID:", len(ids))
    download_pdfs(ids)
    print("\nHOÀN TẤT!")

if __name__ == "__main__":
    asyncio.run(main())