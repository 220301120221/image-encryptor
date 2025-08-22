
# Image Encryptor (Simple, Reversible Pixel Manipulation)

A tiny command-line tool that **encrypts and decrypts images** using basic pixel manipulation:
- **XOR** every pixel value with a key derived from your password (reversible).
- **Shuffle** all pixel bytes using a deterministic permutation derived from your password (reversible).
- Or apply **both** (default): XOR first, then Shuffle.

> ⚠️ **Not for real security.** This is a learning project and **not** a replacement for cryptography libraries.

## Features
- Works with common image formats (PNG, JPG, etc.).
- Keeps the image dimensions and mode (L, RGB, RGBA).
- Deterministic password-based operations: encrypt → decrypt gives back the original (with the same password & mode).

---

## Quick Start

### 1) Create & activate a virtual environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux (bash):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Encrypt an image
```bash
python main.py encrypt -i input.jpg -o encrypted.png -p "myPassword" -m both
```

### 4) Decrypt it back
```bash
python main.py decrypt -i encrypted.png -o restored.jpg -p "myPassword" -m both
```

> If you used `-m xor` or `-m shuffle` while encrypting, use the **same** mode while decrypting.

---

## Command Help
```bash
python main.py -h
python main.py encrypt -h
python main.py decrypt -h
```

### Examples
```bash
# Only XOR (fastest)
python main.py encrypt -i photo.jpg -o photo.enc.png -p "pass123" -m xor
python main.py decrypt -i photo.enc.png -o photo.dec.jpg -p "pass123" -m xor

# Only Shuffle
python main.py encrypt -i photo.jpg -o photo.enc.png -p "pass123" -m shuffle
python main.py decrypt -i photo.enc.png -o photo.dec.jpg -p "pass123" -m shuffle

# Both (default)
python main.py encrypt -i photo.jpg -o photo.enc.png -p "pass123" -m both
python main.py decrypt -i photo.enc.png -o photo.dec.jpg -p "pass123" -m both
```

---

## How it works (short version)

- **XOR**: derive one byte from your password and XOR it with every pixel value (byte-wise). XOR is its own inverse: `x ^ k ^ k == x`.
- **Shuffle**: derive a random seed from your password, create a permutation for all bytes, and
  - **encrypt**: apply the permutation
  - **decrypt**: apply the inverse permutation
- **Both**: XOR first, then Shuffle. Decryption reverses: Unshuffle, then XOR.

> We convert uncommon modes to `RGBA` when needed to ensure consistent byte handling and lossless round-trip output.

---

## VS Code: Run Locally

1. **Open Folder**: `File → Open Folder…` and select this project folder.
2. **Create venv** and **activate** it (see Quick Start).
3. `pip install -r requirements.txt`.
4. Put a test image (e.g., `input.jpg`) in the folder.
5. Use the integrated terminal to run the examples above.
6. Check the output images in the Explorer panel.

---

## Upload to GitHub — Step-by-Step (VS Code)

### One-time setup (install Git)
- **Windows**: install Git from the official site and restart VS Code.
- **macOS**: Git is usually preinstalled; otherwise use Xcode CLT or Homebrew.
- **Linux**: `sudo apt install git` (Debian/Ubuntu) or your distro's package manager.

### Publish from VS Code
1. Open this project in VS Code.
2. Click **Source Control** icon → click **Initialize Repository**.
3. Enter a commit message like "Initial commit" → **Commit**.
4. Click **Publish to GitHub** (or **Publish Branch**) and follow the prompts.
   - If prompted: sign in to GitHub and choose **Public** or **Private**.
5. Done! Your repo is live at `https://github.com/<your-username>/image-encryptor`.

### (Alternative) Command line push
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/image-encryptor.git
git push -u origin main
```

---

## Limitations / Notes
- **This is educational**; it does **not** offer real cryptographic security.
- Always keep a backup of originals until you verify your decrypt works.
- For lossy formats (e.g., JPEG), prefer saving encrypted output as **PNG** to avoid extra artifacts.

---

## License
MIT
