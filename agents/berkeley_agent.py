from playwright.sync_api import sync_playwright
import os
import time
import pdfkit
import pandas as pd

def save_pdf_from_html(page, save_path):
    html_content = page.content()
    pdfkit.from_string(html_content, save_path)

def create_folder(tms):
    folder_path = os.path.join("output", "Berkeley", tms)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def run_berkeley_agent(tms_number):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        folder = create_folder(tms_number)

        # Step 1-3: Property card
        page.goto("https://berkeleycountysc.gov/propcards/prop_card_search.php")
        page.fill("#tms", tms_number)
        page.click("text='Retrieve Property Card'")
        page.wait_for_timeout(3000)
        prop_card_path = os.path.join(folder, "Property Card.pdf")
        save_pdf_from_html(page, prop_card_path)

        # Step 5: Extract Book/Page from previous owner history
        text = page.content()
        book_pages = []
        for line in text.split("\n"):
            if "Book:" in line and "Page:" in line:
                try:
                    parts = line.split()
                    book = parts[parts.index("Book:") + 1]
                    page_num = parts[parts.index("Page:") + 1]
                    book_pages.append((book, page_num))
                except:
                    continue

        # Step 6-9: Tax bill and receipt
        page.goto("https://taxes.berkeleycountysc.gov/#/WildfireSearch")
        page.fill("input[name='search']", tms_number)
        page.keyboard.press("Enter")
        page.wait_for_timeout(4000)
        page.click("text='View'")
        page.wait_for_timeout(3000)

        try:
            page.click("text='View & Print Bill'")
            page.wait_for_timeout(2000)
            save_pdf_from_html(page, os.path.join(folder, "Tax Bill.pdf"))
        except:
            pass

        try:
            page.click("text='View & Print Receipt'")
            page.wait_for_timeout(2000)
            save_pdf_from_html(page, os.path.join(folder, "Tax Receipt.pdf"))
        except:
            pass

        # Step 10–13: Deeds lookup
        for book, page_num in book_pages:
            page.goto("https://search.berkeleydeeds.com/NameSearch.php?Accept=Accept")
            if int(book) < 9999:
                page.select_option("#bookcode", "ORP")  # Old Real Property for older dates
            else:
                page.select_option("#bookcode", "RB")
            page.fill("#booknum", book)
            page.fill("#pagenum", page_num.zfill(3))
            page.click("text='Search'")
            page.wait_for_timeout(3000)

            try:
                page.click("text='View'")
                page.wait_for_timeout(3000)
                deed_path = os.path.join(folder, f"DB {book} {page_num.zfill(3)}.pdf")
                save_pdf_from_html(page, deed_path)
            except:
                print(f"Deed not found: {book} {page_num}")

        browser.close()

if __name__ == "__main__":
    run_berkeley_agent("2590502005")
