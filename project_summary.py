import os
import sys
from datetime import datetime, timezone

# List of directories to ignore
ignore_dirs = [
    '.venv', 'venv', '.git', '.github', '__pycache__', 'site-packages',
    'dist', 'build', 'Include', 'Lib', 'Scripts', 'tcl', 'Tools', 'DLLs',
    'pyvenv.cfg', '.idea', 'share', 'bin', 'include', '.cfg', '.qodo'
]

# List of file extensions to ignore
ignore_file_extensions = ['.md']


def normalize_path(path):
    """Normalize path to work with both Windows and Unix systems."""
    return os.path.normpath(os.path.expanduser(path))


def should_ignore_file(filename, output_filename=None):
    """Check if a file should be ignored based on extension or if it's the output file."""
    if filename == output_filename:
        return True

    # Check if file has an ignored extension
    for ext in ignore_file_extensions:
        if filename.lower().endswith(ext.lower()):
            return True

    return False


def get_project_name(project_path):
    """Extract project name from the project path."""
    # Get the last directory name from the path
    project_name = os.path.basename(os.path.abspath(project_path))

    # Clean the project name to be file-system safe
    # Remove or replace characters that are not allowed in filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        project_name = project_name.replace(char, '_')

    # Remove extra spaces and replace with underscores
    project_name = '_'.join(project_name.split())

    return project_name


def generate_output_filename(project_path):
    """Generate the output filename based on project path."""
    project_name = get_project_name(project_path)
    output_filename = f"{project_name}_full_code.txt"

    # Create the full output path (same directory as the project)
    output_path = os.path.join(project_path, output_filename)

    return normalize_path(output_path)


def get_directory_structure(rootdir, output_file=None):
    """Generates a proper tree structure representation of the directory."""
    output_filename = os.path.basename(output_file) if output_file else None
    root_name = os.path.basename(rootdir)

    # Collect all paths and organize them
    all_paths = []

    for root, dirs, files in os.walk(rootdir):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        # Get relative path
        rel_path = os.path.relpath(root, rootdir)
        if rel_path == '.':
            rel_path = ''

        # Add directories
        for dirname in sorted(dirs):
            dir_rel_path = os.path.join(rel_path, dirname) if rel_path else dirname
            all_paths.append((dir_rel_path.replace('\\', '/'), 'dir', dirname))

        # Add files (excluding ignored files)
        for filename in sorted(files):
            if not should_ignore_file(filename, output_filename):
                file_rel_path = os.path.join(rel_path, filename) if rel_path else filename
                all_paths.append((file_rel_path.replace('\\', '/'), 'file', filename))

    # Sort paths to ensure proper tree order
    all_paths.sort(key=lambda x: (x[0].count('/'), x[0], x[1] == 'file'))

    # Build tree structure
    result = [f"{root_name}/"]

    # Group items by their parent directory
    tree_dict = {}
    for path, item_type, name in all_paths:
        if '/' in path:
            parent = '/'.join(path.split('/')[:-1])
        else:
            parent = ''

        if parent not in tree_dict:
            tree_dict[parent] = []
        tree_dict[parent].append((path, item_type, name))

    def add_items_to_tree(parent_path, prefix):
        if parent_path not in tree_dict:
            return

        items = tree_dict[parent_path]

        for i, (path, item_type, name) in enumerate(items):
            is_last = (i == len(items) - 1)

            if item_type == 'dir':
                if is_last:
                    result.append(f"{prefix}└── {name}/")
                    new_prefix = prefix + "    "
                else:
                    result.append(f"{prefix}├── {name}/")
                    new_prefix = prefix + "│   "

                # Add subdirectory contents
                add_items_to_tree(path, new_prefix)
            else:
                if is_last:
                    result.append(f"{prefix}└── {name}")
                else:
                    result.append(f"{prefix}├── {name}")

    # Start with root level items
    add_items_to_tree('', '')

    return '\n'.join(result)


def copy_file_contents(filepath):
    """Reads and returns the content of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            with open(filepath, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def create_output_file(rootdir, output_file):
    """Creates the output file with directory structure and file contents."""
    # Normalize paths
    rootdir = normalize_path(rootdir)
    output_file = normalize_path(output_file)
    output_filename = os.path.basename(output_file)

    # Get current timestamp using timezone-aware datetime (fixes deprecation warning)
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    project_name = get_project_name(rootdir)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write header information
        outfile.write(f"# Project: {project_name}\n")
        outfile.write(f"# Generated on: {current_time}\n")
        outfile.write(f"# Source Path: {rootdir}\n")
        outfile.write("# ======================================================\n\n")

        # Write the directory structure (excluding the output file)
        outfile.write("## Project Structure\n")
        outfile.write("# ======================================================\n\n")
        outfile.write(get_directory_structure(rootdir, output_file))
        outfile.write("\n\n")

        # Write file contents section header
        outfile.write("## File Contents\n")
        outfile.write("# ======================================================\n\n")

        # Traverse the directory and write contents of specified files
        file_count = 0
        for root, dirs, files in os.walk(rootdir):
            # Remove ignored directories from the list
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file in files:
                # Skip ignored files
                if should_ignore_file(file, output_filename):
                    continue

                filepath = os.path.join(root, file)
                # Only include .py files (not .py.something) and requirements.txt for content details
                if ((file.endswith('.py') or file.endswith('.ts') or file.endswith(
                        '.json')) and not '.py.' or '.ts' or '.json' in file) or file == 'requirements.txt' or file == '.env':
                    # Use forward slashes for consistency in output, regardless of OS
                    display_path = filepath.replace(os.sep, '/')
                    outfile.write(f"### File: {display_path}\n")
                    outfile.write("# ======================================================\n\n")
                    outfile.write(copy_file_contents(filepath))
                    outfile.write("\n\n")
                    file_count += 1


def parse_single_argument():
    """Parse the single project path argument, handling spaces without quotes."""
    args = sys.argv[1:]  # Get all arguments except script name

    if len(args) == 0:
        print("Error: Missing project path argument.")
        print("Usage: python project_summary.py <project_path>")
        print(
            "Example: python project_summary.py D:\\work\\GenAI\\project_summary")
        sys.exit(1)

    # Join all arguments to handle spaces in path
    project_path = ' '.join(args).strip()

    return project_path


def main():
    try:
        # Parse the single project path argument
        project_path = parse_single_argument()

        print(f"Project Path: {project_path}")

        # Validate input directory exists
        normalized_path = normalize_path(project_path)
        if not os.path.exists(normalized_path):
            print(f"Error: Project directory '{normalized_path}' does not exist.")
            sys.exit(1)

        if not os.path.isdir(normalized_path):
            print(f"Error: '{normalized_path}' is not a directory.")
            sys.exit(1)

        # Generate output filename automatically
        output_file = generate_output_filename(normalized_path)
        project_name = get_project_name(normalized_path)

        print(f"Project Name: {project_name}")
        print(f"Output File: {output_file}")

        # Create the output file
        create_output_file(normalized_path, output_file)
        print(f"✓ Output successfully written to: {output_file}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
