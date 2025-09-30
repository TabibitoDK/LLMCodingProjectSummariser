import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

# --- Constants ---
# A set of common code file extensions to include in the output.
# You can add or remove extensions as needed.
CODE_EXTENSIONS = {
    '.py', '.pyw', '.java', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', 
    '.scss', '.less', '.json', '.xml', '.yaml', '.yml', '.md', '.rst', 
    '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.rs', '.php', '.rb', '.swift', 
    '.kt', '.kts', '.sh', '.bat', '.ps1', 'Dockerfile', '.env', '.sql'
}

# --- Core Logic ---

def generate_llm_context(root_dir, output_file_path):
    """
    Traverses a directory, creates a tree view, and appends the content
    of specified code files to a single output file.
    """
    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            # 1. Write the main title
            outfile.write(f"# Project Context for: {os.path.basename(root_dir)}\n\n")

            # 2. Generate and write the directory tree structure
            outfile.write("## Directory Structure\n\n")
            outfile.write("```\n")
            files_to_include = []
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # Exclude common virtual environment and cache directories
                dirnames[:] = [d for d in dirnames if d not in ['__pycache__', 'node_modules', '.git', '.vscode', 'venv', '.venv', '.idea']]
                
                relative_path = os.path.relpath(dirpath, root_dir)
                if relative_path == ".":
                    level = 0
                    outfile.write(f"{os.path.basename(root_dir)}/\n")
                else:
                    level = len(relative_path.split(os.sep))
                    indent = '    ' * (level - 1) + '└── '
                    outfile.write(f"{indent}{os.path.basename(dirpath)}/\n")

                sub_indent = '    ' * level + '├── '
                for filename in sorted(filenames):
                    outfile.write(f"{sub_indent}{filename}\n")
                    # Check if the file should be included based on its extension
                    if any(filename.endswith(ext) for ext in CODE_EXTENSIONS) or os.path.splitext(filename)[1] == '':
                        files_to_include.append(os.path.join(dirpath, filename))
            outfile.write("```\n\n")

            # 3. Append the content of each identified code file
            outfile.write("---\n\n## File Contents\n\n")
            for filepath in sorted(files_to_include):
                relative_filepath = os.path.relpath(filepath, root_dir)
                # Normalize path separators for consistent output
                normalized_path = relative_filepath.replace('\\', '/')
                
                outfile.write(f"### 📄 **File:** `{normalized_path}`\n\n")
                
                # Determine language for markdown code block
                _, extension = os.path.splitext(filepath)
                language = extension.lstrip('.').lower()
                if not language:
                    language = 'text' # Default for files with no extension

                outfile.write(f"```{language}\n")
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"Error reading file: {e}")
                outfile.write("\n```\n\n---\n\n")
        return True, None
    except Exception as e:
        return False, str(e)


# --- GUI Application ---

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LLM Code Context Generator")
        self.geometry("600x300")
        self.minsize(500, 250)

        # --- Style Configuration ---
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", padding=5, font=("Helvetica", 10))
        style.configure("TButton", padding=6, font=("Helvetica", 10, "bold"))
        style.configure("TEntry", padding=5)
        style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Widgets ---
        header_label = ttk.Label(
            main_frame, 
            text="Generate Code Context for LLMs", 
            style="Header.TLabel"
        )
        header_label.pack(pady=(0, 15))

        # Directory Selection
        dir_frame = ttk.Frame(main_frame)
        dir_frame.pack(fill=tk.X, expand=True)
        
        dir_label = ttk.Label(dir_frame, text="Project Directory:")
        dir_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.dir_path_var = tk.StringVar()
        dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_path_var, state="readonly")
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(dir_frame, text="Browse...", command=self.browse_directory)
        browse_button.pack(side=tk.LEFT, padx=(10, 0))

        # Generate Button
        generate_button = ttk.Button(main_frame, text="Generate Context File", command=self.start_generation)
        generate_button.pack(pady=20, fill=tk.X)

        # Status Label
        self.status_var = tk.StringVar()
        status_label = ttk.Label(main_frame, textvariable=self.status_var, wraplength=550)
        status_label.pack(pady=(10, 0))

    def browse_directory(self):
        """Opens a dialog to select a directory and updates the entry field."""
        directory = filedialog.askdirectory(title="Select Project Folder")
        if directory:
            self.dir_path_var.set(directory)
            self.status_var.set(f"Selected: {directory}")

    def start_generation(self):
        """Handles the logic for generating the context file with automatic naming."""
        input_dir = self.dir_path_var.get()
        if not input_dir or not os.path.isdir(input_dir):
            messagebox.showerror("Error", "Please select a valid directory first.")
            return

        try:
            # Create an 'output' directory in the script's location if it doesn't exist
            output_folder = "output"
            os.makedirs(output_folder, exist_ok=True)

            # Generate the automatic filename
            dir_name = os.path.basename(input_dir)
            date_str = datetime.now().strftime("%Y%m%d")
            count = 1
            while True:
                # Format: directoryName_YYYYMMDD-count.md
                output_filename = f"{dir_name}_{date_str}-{count}.md"
                output_path = os.path.join(output_folder, output_filename)
                if not os.path.exists(output_path):
                    break
                count += 1
            
            self.status_var.set(f"Generating file: {output_path}")
            self.update_idletasks() # Refresh the UI to show the message

            success, error_msg = generate_llm_context(input_dir, output_path)

            if success:
                messagebox.showinfo("Success", f"Context file saved successfully to:\n{output_path}")
                self.status_var.set("Generation complete!")
            else:
                messagebox.showerror("Error", f"An error occurred:\n{error_msg}")
                self.status_var.set("Generation failed.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred during file generation:\n{e}")
            self.status_var.set("Generation failed with an unexpected error.")


if __name__ == "__main__":
    app = App()
    app.mainloop()


