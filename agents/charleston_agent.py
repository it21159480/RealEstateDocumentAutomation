from playwright.sync_api import sync_playwright
import os
import time
import pdfkit
import pandas as pd
import requests
from io import BytesIO

def download_binary_pdf(url, save_path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/pdf"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"[✓] Successfully downloaded PDF: {save_path}")
        else:
            print(f"[!] Failed to download PDF: {response.status_code}, {response.headers.get('Content-Type')}")
    except Exception as e:
        print(f"[!] Error downloading PDF: {e}")


def save_pdf_from_html(page, save_path):
    try:
        html_content = page.content()
        pdfkit.from_string(html_content, save_path)
        print(f"Saved PDF: {save_path}")
    except Exception as e:
        print(f"[Error] Failed to save PDF at {save_path}: {e}")


def save_pdf_from_url(url, save_path):
    try:
        pdfkit.from_url(url, save_path)
        print(f"[✓] Saved PDF: {save_path}")
    except Exception as e:
        print(f"[!] Failed to save PDF at {save_path}: {e}")

def create_folder(tms):
    folder_path = os.path.join("output", "Charleston", tms)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def run_charleston_agent(tms_number):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,)
        context = browser.new_context()
        page = context.new_page()



        # Step 1: Go to Charleston County Online Services page
        # page.goto("https://www.charlestoncounty.org/online-services.php")
        # print("Navigated to Charleston County Online Services page.")
        # page.wait_for_timeout(20000)
        # # Step 2: Click on “Pay Taxes & View Records”
        # page.click("h3:text('Pay Taxes & View Records')")
        # print("Clicked on 'Pay Taxes & View Records'.")
        # page.wait_for_timeout(120000)
        # # Step 3: Click on “Real Property Record Search”
        # page.click("a:text('Real Property Record Search')")
        # print("Clicked on 'Real Property Record Search'.")
        # page.wait_for_timeout(20000)
        
        # page.wait_for_load_state("load")

        # # Step 4: Input TMS
        # page.fill("input[aria-label='PIN']", tms_number)
        # page.keyboard.press("Enter")
        # print(f"Entered TMS number: {tms_number}")
        # page.wait_for_timeout(10000)
        

        # # Step 5: Click view details
        # page.wait_for_selector("a[title^='View Details']")
        # page.click("a[title^='View Details']")
        # print("Clicked on 'View Details'.")
        # page.wait_for_timeout(20000)
        

        folder = create_folder(tms_number)
        print(f"Created folder: {folder}")

        # # Step 6: Save current Property Card URL and use pdfkit
        # property_url = page.url
        # save_pdf_from_url(property_url, os.path.join(folder, "Property Card.pdf"))
        # print(f"Saved Property Card PDF at {os.path.join(folder, 'Property Card.pdf')}")

      

        # # Step 7: Scrape Book and Page from updated sales table
        # # Wait until the correct module and table are loaded
        # page.wait_for_selector("div.DnnModule-ProValSalesHistory table.ui-widget-content.ui-table > tbody > tr td")

        # # Scope to the correct module only
        # sales_history_module = page.locator("div.DnnModule-ProValSalesHistory")
        # sales_rows = sales_history_module.locator("table.ui-widget-content.ui-table > tbody > tr")
        # print(f"Found {sales_rows.count()} rows in the sales table.")
        # book_pages = []
        # for i in range(sales_rows.count()):
        #     row = sales_rows.nth(i)
        #     try:
        #         book = row.locator("td").nth(0).inner_text().strip()
        #         page.wait_for_timeout(5000)
        #         page_num = row.locator("td").nth(1).inner_text().strip()
        #         page.wait_for_timeout(5000)
        #         if (book[0].isalpha() or (book[0].isdigit() and int(book) >= 280)):
        #             book_pages.append((book, page_num))
        #             print(f"Row {i}: Book {book}, Page {page_num}")
        #     except Exception as e:
        #         print(f"Skipping row {i} due to error: {e}")

        # # Step 8: Click Tax Info and save as PDF
        # page.click("a[title='Tax Info']")
        # print("Clicked on 'Tax Info', waiting for redirect...")

        # # Wait for navigation to the final /AccountSummary.aspx URL
        # page.wait_for_url("**/AccountSummary.aspx**")
        # page.wait_for_timeout(20000)
        # tax_url = page.url
        # save_pdf_from_url(tax_url, os.path.join(folder, "Tax Info.pdf"))
        # print(f"Saved Tax Info PDF from {tax_url}")

        book_pages = [("1247","453"),("0799","591"),("0310","940")]
        browser_second = p.chromium.launch(headless=True,)
        new_context = browser_second.new_context()
        # Step 9-15: Go to Register of Deeds and download deeds
        for book, page_num in book_pages:
            try:

                newTab = new_context.new_page()
                newTab.goto("https://www.charlestoncounty.org/departments/rod/ds-DMBookandPage.php")
                newTab.wait_for_timeout(20000)
                print("Navigated to Register of Deeds newTab.")
                newTab.wait_for_selector("#booknumber")


                newTab.fill("#booknumber", book)
                newTab.fill("#pagenumber", page_num.zfill(3))

                # Check the "agreelegal" checkbox if it exists
                try:
                    if newTab.is_visible("input[name='agreelegal']"):
                        newTab.check("input[name='agreelegal']")
                        print("Checked 'agreelegal' checkbox.")
                except Exception as e:
                    print(f"'agreelegal' checkbox not found or could not be checked: {e}")
                newTab.click("input[name='send_button']")
                newTab.wait_for_timeout(40000)

                # page.wait_for_selector("text='View'")
                # page.click("text='View'")
                # page.wait_for_timeout(60000)
                # deed_url = page.url
                with context.expect_page() as new_tab_info:
                    newTab.click("text='View'")

                new_page = new_tab_info.value
                new_page.wait_for_load_state("load")
                print("Clicked 'View' to open deed in new tab.")
                new_page.wait_for_url("**/ViewDocument?param1=**", timeout=15000)
                new_page.wait_for_timeout(20000)
                deed_url = new_page.url
                print(f"Deed URL: {deed_url}")
                deed_path = os.path.join(folder, f"DB {book} {page_num.zfill(3)}.pdf")
                pdf_url = new_page.evaluate("() => window.PDFViewerApplication?.url")
                if pdf_url:
                    print(f"[→] Attempting to fetch actual PDF from viewer URL: {pdf_url}")
                    download_binary_pdf(pdf_url, deed_path)
                else:
                    print("[⚠] PDF URL not found in viewer. Falling back to page.pdf().")
                    new_page.pdf(path=deed_path, format="A4")
                    print(f"[✓] Saved deed via rendered PDF: {deed_path}")
                # # Save the full visible page as a PDF (headless mode required)
                # new_page.pdf(path=deed_path, format="A4", print_background=True)
                # print(f"[✓] Saved deed PDF via page.pdf(): {deed_path}")
                # path = os.path.join(folder, f"DB {book}.pdf")
                # save_pdf_from_html(new_page, path)
                # print(f"[✓] Saved deed PDF via save_pdf_from_html(): {path}")


                # Extract PDF bytes directly from browser context
                # pdf_bytes = new_page.evaluate("""async () => {
                #     const response = await fetch(window.location.href);
                #     const blob = await response.blob();
                #     const arrayBuffer = await blob.arrayBuffer();
                #     return Array.from(new Uint8Array(arrayBuffer));
                # }""")

                # # Save the file to disk
                # with open(deed_path, "wb") as f:
                #     f.write(bytes(pdf_bytes))
                # print(f"[✓] Saved deed PDF via browser context: {deed_path}")

                # download_binary_pdf(deed_url, deed_path)

                # new_page.screenshot(path=deed_path, full_page=True)
                # print(f"Saved deed screenshot at {deed_path}")
                # save_pdf_from_url(deed_url, deed_path)
                # print(f"Saved deed PDF at {deed_path}")
                new_page.close()
                print("Closed deed tab.")
                newTab.close()
            


                # page.go_back()
            except Exception as e:
                print(f"[Warning] Could not retrieve deed: Book {book}, Page {page_num} — {e}")

        browser.close()

# if __name__ == "__main__":
#     run_charleston_agent("5590200072")
