import os
import re


def process_file(file_path):
    """
    Process a single SCSS file to wrap :hover occurrences with a media query.
    Tracks nested blocks to correctly identify the closing brace of :hover blocks
    and avoids re-wrapping blocks already inside a media query.
    """
    print(f"Inspecting file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    hover_start_pattern = re.compile(r"^\s*(&?:hover)\s*{")  # Matches :hover blocks
    media_query_pattern = re.compile(r"^\s*@media\s*\(hover:\s*hover\)\s*and\s*\(pointer:\s*fine\)\s*{$")  # Matches media query
    modified = False  # Tracks if the file was modified

    updated_content = []
    inside_hover = False
    inside_media_query = False
    hover_block_lines = []
    brace_depth = 0  # Tracks the current depth of braces

    for line_num, line in enumerate(content, start=1):
        stripped_line = line.strip()

        if inside_hover:
            hover_block_lines.append(line)

            # Update the brace depth
            brace_depth += stripped_line.count("{")
            brace_depth -= stripped_line.count("}")

            # Check if we're back to the same level as when :hover started
            if brace_depth == 0:
                inside_hover = False

                # If not already inside a media query, wrap the hover block
                if not inside_media_query:
                    modified = True
                    updated_content.append("  @media (hover: hover) and (pointer: fine) {\n")
                    updated_content.extend(hover_block_lines)
                    updated_content.append("  }\n")
                else:
                    # Already inside a media query, just add the hover block
                    updated_content.extend(hover_block_lines)

                hover_block_lines = []  # Reset for the next block
        elif hover_start_pattern.search(line):  # Detect the start of a :hover block
            inside_hover = True
            hover_block_lines.append(line)

            # Initialize the brace depth for this block
            brace_depth = stripped_line.count("{") - stripped_line.count("}")
        elif media_query_pattern.search(line):  # Detect the start of a media query
            inside_media_query = True
            updated_content.append(line)
        elif inside_media_query and stripped_line == "}":  # Detect the end of a media query
            inside_media_query = False
            updated_content.append(line)
        else:
            # Lines outside :hover blocks are directly added to the updated content
            updated_content.append(line)

    # Write back to the file if modifications were made
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
            if file.endswith('.scss'):  # Process only SCSS files
                process_file(os.path.join(root, file))

    print("Processing complete! All applicable :hover occurrences have been wrapped.")


if __name__ == "__main__":
    # Automatically determine the directory where the script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))
    process_directory(current_directory)
