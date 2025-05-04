```markdown
# META-GUARD 🔍🛡️

![META-GUARD Banner](https://i.ibb.co/ccmc0ygm/foto-no-exif-1.png)

**META-GUARD** is a powerful Python tool for extracting metadata, analyzing security headers, and detecting sensitive data from web pages.  
Developed by [Cipher Squid](https://github.com/ciphersquid666) — use it responsibly! ☠️

---

## ✨ Features

- 📄 **Extracts metadata**: title, description, Open Graph, Twitter Cards, etc.  
- ⚡ **Checks SSL certificate and HTTP status**.  
- 🔐 **Analyzes security headers** (CSP, HSTS, etc.).  
- 🧠 **Detects structured data** (`ld+json`).  
- 🕵️ **Scans for sensitive data**: API keys, tokens, secrets.  
- 🖼️ **Collects headings, links, images**.  
- 📁 **Saves everything** to a `metadata.json` file.  
- 🛠️ **Verbose mode** for detailed inspection.  

---

## ▶️ Demo

```bash
=====================================
[×] META-GUARD Tool by 𝘾𝙞𝙥𝙝𝙚𝙧 𝙎𝙦𝙪𝙞𝙙
[×] Use responsibly!
=====================================
Enter the URLs of the web pages (comma separated): https://example.com
Enable verbose mode? (yes/no): yes
```

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ciphersquid666/META-GUARD.git
   cd META-GUARD
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

Run the tool:
```bash
python MetaGuard.py
```

You'll be prompted to input URLs and whether to enable verbose mode.

---

## 📤 Output

- **`metadata.json`**: Full structured metadata output.  
- **CLI summary**: Concise or verbose report with extracted data.

---

## 🧰 Requirements

The following Python libraries are required:
- `requests`
- `beautifulsoup4`
- `tabulate`
- `termcolor`

Install them all with:
```bash
pip install -r requirements.txt
```

---

## ⚠️ Disclaimer

This tool is intended for **educational and ethical use only**.  
Do not use it on websites you do not own or have permission to scan. ⚖️

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Cipher Squid**  
GitHub: [@ciphersquid666](https://github.com/ciphersquid666)
```

---
