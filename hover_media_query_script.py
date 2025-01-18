import os
import re


def process_file(file_path):
    """
    Process a single SCSS file to wrap :hover occurrences with a media query.
    Ensures only :hover blocks are wrapped, leaving the rest of the file intact.
    Logs any modifications made.
    """
    print(f"Inspecting file: {file_path}")

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Patterns to match the start and end of a :hover block
    hover_start_pattern = re.compile(r"^\s*(&?:hover)\s*{")  # Matches :hover blocks
    block_end_pattern = re.compile(r"^\s*}")  # Matches the end of a CSS block

    modified = False  # Tracks whether the file was modified
    updated_content = []
    inside_hover = False
    hover_block_lines = []

    for line_num, line in enumerate(content, start=1):
        if inside_hover:
            # If inside a :hover block, append the line to the hover block
            hover_block_lines.append(line)
            if block_end_pattern.match(line):  # Detect the end of the :hover block
                inside_hover = False
                modified = True
                # Wrap the collected :hover block in a media query
                updated_content.append("  @media (hover: hover) and (pointer: fine) {\n")
                updated_content.extend(hover_block_lines)
                updated_content.append("  }\n")
                hover_block_lines = []  # Reset the hover block
        elif hover_start_pattern.search(line):  # Detect the start of a :hover block
            inside_hover = True
            hover_block_lines.append(line)
        else:
            # Lines outside of :hover blocks are directly appended to the updated content
            updated_content.append(line)

    # Write back to the file if it was modified
    if modified:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(updated_content)
        print(f"Modified file: {file_path}")


def process_directory(directory_path):
    """
    Recursively process all SCSS files in the directory and its subdirectories.
    """
    print(f"Starting processing in directory: {directory_path}")

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.scss'):  # Only process SCSS files
                process_file(os.path.join(root, file))

    print("Processing complete! All applicable :hover occurrences have been wrapped.")


if __name__ == "__main__":
    # Automatically determine the directory where the script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))
    process_directory(current_directory)
