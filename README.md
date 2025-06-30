
# 🏡 Real Estate Document Automation – Charleston County

This project automates the process of navigating the Charleston County property record website, extracting property and deed information, and saving the associated documents as PDFs.

## ✅ Features

- Navigates Charleston County's official records portal using Playwright
- Searches by TMS number to access property records
- Saves:
  - 🧾 Property Card PDF
  - 💰 Tax Info PDF
  - 📄 Deeds from Register of Deeds as PDFs
- Automatically names files by TMS and deed `Book`/`Page` number
- Organizes files by TMS inside a structured `/output/Charleston/` folder

---

## 🔁 Steps Automated

1. Navigate to Charleston County Online Services
2. Click “Pay Taxes & View Records”
3. Click “Real Property Record Search”
4. Enter the TMS number (no dashes)
5. Click “View Details” to access the property record
6. Save the Property Card as a PDF
7. Extract all Book and Page numbers from the Sales History
8. Click “Tax Info” and save it as a PDF
9. For each Book/Page:
   - Open Register of Deeds search
   - Enter Book and Page
   - Agree to legal disclaimer
   - Click “View”
   - Save the opened deed document as a PDF
10. Repeat for all listed transactions
11. Save files under `output/Charleston/<TMS>/` folder

---


## 📂 Project Structure

```
.
├── agents/
│   └── charleston_agent.py     # Core automation script
├── data/
│   └── tms_table.csv           # Input: list of TMS numbers
├── output/
│   └── Charleston/             # Output folder structure
├── main.py                     # Entry point to run batch TMS processing
├── README.md                   # You're here
├── requirements.txt            # Python dependencies
```

---

## ⚙️ Requirements

- Python 3.9+
- Google Chrome or Chromium
- wkhtmltopdf (for PDF rendering of HTML content)

---

## 📦 Installation

```bash
git clone https://github.com/it21159480/RealEstateDocumentAutomation.git
cd RealEstateDocumentAutomation

python -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows

pip install -r requirements.txt
```

Ensure `wkhtmltopdf` is installed and accessible in your system PATH.  
Download it from: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)

---

## 🏁 How to Run

1. Add your TMS numbers to `data/tms_table.csv` under the column `Charleston County`

2. Run the script:

```bash
python main.py
```

---

## 🗃 Output

Files will be saved like:

```
output/
└── Charleston/
    └── 5590200072/
        ├── Property Card.pdf
        ├── Tax Info.pdf
        ├── DB 1247 453.pdf
        ├── DB 0799 591.pdf
        └── ...
```

---

## 🚦 Notes

- The code handles session navigation and waits for content loads before scraping.
- Deeds are rendered to PDF using Playwright’s `page.pdf()` to avoid reCAPTCHA and fetch issues.
- Headless mode is required for accurate `page.pdf()` rendering.

---

## ⏱ Time Spent

> Approx. 2 - 3 days including testing, debugging, and optimization

---

## 📈 Future Improvements

- Support for Berkeley County
- Integrate full LLM-based instruction parsing
- Add download retry logic or reCAPTCHA challenge bypass

---


