# Project Summary Generator

A simple Python utility that generates a comprehensive text file containing your project's directory structure and all source code files in one place.

## Overview

This tool walks through your project directory and creates a single text file that includes:
- A visual tree structure of your project
- Complete contents of all relevant source files (.py, .ts, .json, requirements.txt, .env)
- Automatic exclusion of common directories like virtual environments, git folders, and build artifacts

Perfect for:
- Sharing your entire codebase with AI assistants
- Creating project documentation
- Code reviews and audits
- Project backups and snapshots

## Features

- **Automatic Output Naming**: Generates output file based on your project name
- **Smart Filtering**: Automatically ignores virtual environments, build folders, and other irrelevant directories
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Clean Tree Structure**: Creates a beautiful visual representation of your project structure
- **Self-Aware**: Excludes its own output file from the generated summary

## Installation

No installation required! Just download `project_summary.py` and run it with Python 3.x.

### Requirements
- Python 3.6 or higher
- No external dependencies

## Usage

### Basic Usage

```bash
python project_summary.py <project_path>
```

### Examples

**Windows:**
```bash
python project_summary.py C:\abcd\xyz\my_project
```

**Linux/macOS:**
```bash
python project_summary.py /home/user/projects/my_project
```

**Paths with spaces (no quotes needed):**
```bash
python project_summary.py C:\My Projects\Web App
```

### Output

The script will create a file named `{project_name}_full_code.txt` in the same directory as your project.

**Example output file structure:**
```
# Project: my_project
# Generated on: 2025-10-28 07:30:36 UTC
# Source Path: C:\abcd\xyz\my_project
# ======================================================

## Project Structure
# ======================================================

my_project/
├── src/
│   ├── main.py
│   └── utils.py
└── requirements.txt

## File Contents
# ======================================================

### File: C:/abcd/xyz/my_project/src/main.py
# ======================================================

[File contents here...]
```

## Configuration

You can customize what gets ignored by editing these variables in `project_summary.py`:

### Ignored Directories
```python
ignore_dirs = [
    '.venv', 'venv', '.git', '.github', '__pycache__', 'site-packages',
    'dist', 'build', 'Include', 'Lib', 'Scripts', 'tcl', 'Tools', 'DLLs',
    'pyvenv.cfg', '.idea', 'share', 'bin', 'include', '.cfg', '.qodo'
]
```

### Ignored File Extensions
```python
ignore_file_extensions = ['.md', '.gitignore', '.png', '.jpg', '.jpeg', '.gif',
                          '.svg', '.ico', '.exe', '.dll', '.so', '.dylib',
                          '.zip', '.tar', '.gz', '.rar', '.7z', '.pdf',
                          '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                          '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv',
                          '.mkv', '.class', '.jar', '.pyc', '.pyo','LICENSE']
```

### Included File Types (for full content)
By default, the tool includes complete contents of:
- `.py` files (Python)
- `.ts` files (TypeScript)
- `.json` files (JSON)
- `requirements.txt`
- `.env` files

To add more file types, modify the condition in the `create_output_file()` function.

## How It Works

1. **Scans** your project directory recursively
2. **Filters** out common directories and files you don't need (virtual environments, git folders, etc.)
3. **Generates** a tree structure visualization
4. **Collects** contents of all relevant source files
5. **Creates** a single consolidated text file with everything

## Use Cases

### Share with AI Assistants
```bash
python project_summary.py /path/to/project
# Upload the generated .txt file to ChatGPT, Claude, etc.
```

### Code Review
```bash
python project_summary.py /path/to/project
# Share the output file with your team for review
```

### Project Documentation
```bash
python project_summary.py /path/to/project
# Use the output as a comprehensive project snapshot
```

## Troubleshooting

### "Error: Project directory does not exist"
- Check that the path is correct
- Make sure you have read permissions for the directory

### "Error reading file: [encoding error]"
- The tool automatically tries UTF-8 and Latin-1 encodings
- Binary files may show encoding errors but won't break the process

### Output file not created
- Ensure you have write permissions in the project directory
- Check that the disk has sufficient space

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Feel free to modify this script for your needs! Common customizations:
- Add more file extensions to include
- Change the output format
- Add file size information
- Include file modification dates
- Add syntax highlighting in output

## Author
Name: Aban Sikhar Mitra

Created for developers who need a quick way to consolidate their project files into a single document.

---

**Quick Start:**
```bash
python project_summary.py /path/to/your/project
```

That's it! Your complete project summary will be generated in seconds.