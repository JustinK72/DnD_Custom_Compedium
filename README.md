# My Custom D&D Compendium

This is a central repository for all our campaign's custom rules, items, monsters, and the new 2024 One D&D updates. It works for both **Fight Club 5** (iOS/Android) and **RPG Companion App**.

## 🚀 How to Install

Choose the instructions for the app you use below.

### Option A: Fight Club 5 / Game Master 5 (Lion's Den)
*Best for: Managing full character sheets, leveling up, and DMs.*

1. **Download the File:**
   - Go to the file list above and click on `1_XML_Compendium.xml`.
   - Click the **Download** button (or "Raw" > Save Page As).
   - Save it to your phone (Files app, Google Drive, or Dropbox).

2. **Import into App:**
   - Open Fight Club 5.
   - Tap the **Compendium** icon (the book).
   - Tap the **Arrow Menu** at the bottom of the screen.
   - Tap **Import**.
   - Select **Local File** (or Cloud) and choose `1_XML_Compendium.xml`.
   - **IMPORTANT:** When asked, choose **"Keep Existing"** to add this to your current library (safest), or "Overwrite" if you want to replace everything.

---

### Option B: 5e Companion App (Blastervla)
*Best for: Quick references, simple character tracking, and players who prefer a modern UI.*

1. **Get the Link:**
   - [Click here to open the RAW JSON file](LINK_TO_YOUR_RAW_JSON_HERE) *(DM Note: You need to replace this link once you upload your file!)*
   - Copy the URL from your browser's address bar.

2. **Import into App:**
   - Open the 5e Companion App.
   - Go to the **Tools** section (or the Earl/Settings menu).
   - Tap **Homebrew** or **Repository**.
   - Select **Import from URL**.
   - Paste the link you copied.
   - Tap **Import**.

---

## 🛠 For the DM: How to Update
*If you are adding new content to this repo, follow these steps.*

1. **Add Content:**
   - Create your XML files inside the `Sources/` folders.
   - Use the templates provided in the repo.

2. **Build:**
   - Run the builder script:
     ```bash
     python builder.py
     ```

---

## For creating a RPG System
https://docs.rpg-companion.app/