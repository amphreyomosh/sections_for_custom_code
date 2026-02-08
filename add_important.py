import os

file_path = r'c:\Users\GLAD\Desktop\testing\murecar.html'
output_path = r'c:\Users\GLAD\Desktop\testing\murecar_updated.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_style = False
new_lines = []

for line in lines:
    original_line = line
    stripped = line.strip()

    if '<style>' in line:
        in_style = True
        new_lines.append(line)
        continue
    if '</style>' in line:
        in_style = False
        new_lines.append(line)
        continue

    if in_style:
        # Check if line ends with a semicolon
        if stripped.endswith(';'):
            # It might be a property definition
            # Avoid lines that start with @media, comments, or containing braces (selectors)
            # However, some properties are inside media queries, so indentation differs.
            # We want to exclude lines that define the selector, e.g. "body {"
            # We want to include lines that are "prop: value;" or "  prop: value;"
            # We also check for closing parenthesis lines of multi-line values i.e. "        );"
            
            # Cases to skip:
            # 1. "}" (closing brace for rule) - but these usually don't end with ;
            # 2. "@import ..." (ends with ;) - maybe should add important? Usually not.
            # 3. "@charset ..."
            
            # Check if it has a colon - usually properties do, but multi-line values ending line might not.
            # E.g.
            #   background:
            #      ...
            #   ); <-- This line has no colon.
            
            should_add = False
            
            if ':' in stripped:
                # Likely "prop: val;"
                # Check it's not a selector pseudo-element like "a:hover;" (invalid css usually has braces)
                # But "filter: progid:DXImage...;" has colons.
                
                # Exclude if it has "{" or "}" on the same line, just in case
                if '{' not in stripped and '}' not in stripped:
                    should_add = True
            elif stripped.startswith(')') or stripped.endswith(');'):
                 # End of multi-line function like gradient
                 should_add = True
            
            # Special case avoidance
            if '@import' in stripped or '@charset' in stripped:
                should_add = False

            if should_add:
                if '!important' not in stripped:
                    # Replace the last semicolon
                    # Find the last semicolon index in the original line (to preserve whitespace)
                    parts = line.rsplit(';', 1)
                    if len(parts) == 2:
                        # Append !important before the semicolon
                        # But wait, we want " !important;"
                        line = parts[0] + ' !important;' + parts[1]

    new_lines.append(line)

with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Created {output_path}")
