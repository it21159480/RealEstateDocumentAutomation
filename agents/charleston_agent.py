from playwright.sync_api import sync_playwright
import os
import time
import pdfkit
import pandas as pd

def save_pdf_from_html(page, save_path):
    html_content = page.content()
    pdfkit.from_string(html_content, save_path)

def create_folder(tms):
    folder_path = os.path.join("output", "Charleston", tms)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def run_charleston_agent(tms_number):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Step 1-3: Navigate to the search page
        page.goto("https://sc-charleston.publicaccessnow.com/RealPropertyRecordSearch.aspx")
        page.wait_for_timeout(20000)

        # Step 4: Input TMS
        page.fill("#ctl00_ContentPlaceHolder1_txtParcelID", tms_number)
        page.keyboard.press("Enter")
        page.wait_for_timeout(30000)

        # Step 5: Click view details
        page.click("text='View Details'")
        page.wait_for_timeout(30000)

        folder = create_folder(tms_number)

        # Step 6: Save Property Card as PDF
        prop_card_path = os.path.join(folder, "Property Card.pdf")
        save_pdf_from_html(page, prop_card_path)

        # Step 7: Scrape Book and Page from Transactions section
        transactions = page.locator("#ctl00_ContentPlaceHolder1_dgSales tr")
        book_pages = []
        for row in range(transactions.count()):
            try:
                text = transactions.nth(row).inner_text()
                parts = text.split()
                if len(parts) >= 2:
                    book = parts[-2]
                    page_num = parts[-1]
                    book_pages.append((book, page_num))
            except:
                continue

        # Step 8: Click Tax Info and save as PDF
        page.click("text='Tax Info'")
        page.wait_for_timeout(30000)
        tax_info_path = os.path.join(folder, "Tax Info.pdf")
        save_pdf_from_html(page, tax_info_path)

        # Step 9–13: Navigate to ROD and save deeds by book/page
        for book, page_num in book_pages:
            page.goto("https://www.charlestoncounty.org/departments/rod/ds-DMBookandPage.php")
            page.fill("#book", book)
            page.fill("#page", page_num.zfill(3))
            page.check("#accept")
            page.click("#submit")
            page.wait_for_timeout(30000)

            try:
                page.click("text='View'")
                page.wait_for_timeout(30000)
                deed_path = os.path.join(folder, f"DB {book} {page_num.zfill(3)}.pdf")
                save_pdf_from_html(page, deed_path)
                page.go_back()
            except:
                print(f"Deed not found: {book} {page_num}")

        browser.close()

if __name__ == "__main__":
    # Example usage for one TMS number
    run_charleston_agent("5590200072")
