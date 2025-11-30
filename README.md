# LLM Code Context Generator

A simple and effective tool to help you package your entire project's structure and code into a single, clean Markdown file. This is perfect for pasting into Large Language Models (LLMs) like Gemini, ChatGPT, or Claude when you need to ask for help with debugging, refactoring, or understanding your code.

This repository provides two versions of the tool:

1. A standalone **Python GUI Application** for desktop use.
2. A static **Web Application** that runs directly in your browser.

## Key Features

- **Directory Tree Generation**: Automatically creates a visual tree of your project's directory structure.
- **Code Inclusion**: Copies the full content of relevant code files into the final output.
- **Intelligent Filtering**: Automatically ignores common development folders like `node_modules`, `.venv`, and `.git` to keep the output clean and focused.
- **Visible Output & Copy Function**: The web version displays the generated markdown directly on the page and includes a one-click "Copy Results" button.
- **Single File Output**: Consolidates everything into one `.md` file for easy copying or downloading.

## Version 1: Python GUI Application

A desktop application built with Python and its native Tkinter library.

### Requirements

- Python 3.x
- Tkinter library. This is usually included with Python installations on Windows and macOS. On Debian-based Linux (like Ubuntu), you may need to install it manually:
  ```
  sudo apt-get install python3-tk
  ```

### Setup & Usage (Windows)

1. Ensure you have `llm_context_generator.py` and `run.bat` in the same folder.
2. Create a Python virtual environment in that folder:
   ```
   python -m venv .venv
   ```
3. Double-click the **`run.bat`** file. This will activate the virtual environment and launch the application.
4. In the application window, click **"Select Folder"** and choose your project directory.
5. Click **"Generate Context File"**.
6. The output file will be automatically saved in a new `output/` folder.

## Version 2: Web Application

A static HTML file that runs entirely in your browser. No installation is required.

### Requirements

- A modern web browser (e.g., Chrome, Firefox, Edge) that supports folder selection.

### Usage

1. Open the **`index.html`** file in your web browser.
2. Click the **"Select Project Folder"** button.
3. Your browser will open a dialog. Choose your project folder and approve the browser's request to access the files.
4. The application will process the files and display the generated Markdown content in a text box on the page.
5. You have two options:
   - Click the **"Copy Results"** button to copy the entire content to your clipboard.
   - Click the **"Download .md File"** button to save the content as a Markdown file on your computer.
