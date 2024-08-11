#!/usr/bin/python3

"""
markdown2html module
Converts Markdown files to HTML
"""

import sys
import os
import hashlib


def convert_md_to_html(md_line):
    """
    Converts a single line of Markdown to HTML.
    """
    # Convert headings
    for i in range(6, 0, -1):
        if md_line.startswith('#' * i + ' '):
            return f"<h{i}>{md_line[i+1:].strip()}</h{i}>"
    
    # Convert unordered lists
    if md_line.startswith('- '):
        return f"<li>{md_line[2:].strip()}</li>", 'ul'
    
    # Convert ordered lists
    if md_line.startswith('* '):
        return f"<li>{md_line[2:].strip()}</li>", 'ol'
    
    # Convert bold and emphasis
    md_line = md_line.replace('**', '<b>').replace('__', '<em>')
    md_line = md_line.replace('<b>', '</b>', 1).replace('<em>', '</em>', 1)
    
    # Convert custom syntax
    if '[[' in md_line and ']]' in md_line:
        start = md_line.index('[[') + 2
        end = md_line.index(']]')
        content = md_line[start:end]
        md5_hash = hashlib.md5(content.encode()).hexdigest()
        md_line = md_line.replace(f"[[{content}]]", md5_hash)
    
    if '((' in md_line and '))' in md_line:
        start = md_line.index('((') + 2
        end = md_line.index('))')
        content = md_line[start:end]
        modified_content = content.replace('c', '').replace('C', '')
        md_line = md_line.replace(f"(({content}))", modified_content)

    return f"<p>{md_line.strip()}</p>"


def main():
    """
    Main function to handle file input/output and conversion.
    """
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)

    md_filename = sys.argv[1]
    html_filename = sys.argv[2]

    if not os.path.exists(md_filename):
        print(f"Missing {md_filename}", file=sys.stderr)
        exit(1)

    with open(md_filename, 'r') as md_file, open(html_filename, 'w') as html_file:
        content = md_file.readlines()

        in_list = False
        list_type = None

        for line in content:
            stripped_line = line.strip()
            if not stripped_line:
                if in_list:
                    html_file.write(f"</{list_type}>\n")
                    in_list = False
                continue

            html_line, current_list_type = convert_md_to_html(stripped_line), None

            if isinstance(html_line, tuple):
                html_line, current_list_type = html_line

            if current_list_type and not in_list:
                html_file.write(f"<{current_list_type}>\n")
                in_list = True
                list_type = current_list_type
            elif not current_list_type and in_list:
                html_file.write(f"</{list_type}>\n")
                in_list = False

            html_file.write(html_line + "\n")

        if in_list:
            html_file.write(f"</{list_type}>\n")

    exit(0)


if __name__ == "__main__":
    main()