import os
import re

def refactor_html(directory):
    for root, _, files in os.walk(directory):
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()

            original_content = content

            # This regex looks for:
            # {{ $asset := resources.Get (SOMETHING) }}
            # optionally followed by {{ $img := $asset... }}
            # optionally followed by <img ... src="... $img.RelPermalink ..." ... >
            # We want to catch the whole block up to the > or /> of the img tag.

            # Find all resources.Get assignments
            matches = re.finditer(r'\{\{\s*\$asset\s*:=\s*resources\.Get\s*(.+?)\s*\}\}', content)
            
            for match in reversed(list(matches)): # Reverse so replacements don't mess up indices
                var_expr = match.group(1) # e.g. `.image` or `.Params.thumbnail` or `"js/alert-init.js"`
                start_idx = match.start()
                
                # Check if it's followed by Resize/Fit/Fill
                # Let's search from start_idx to a bit further
                img_block_pattern = r'\{\{\s*\$asset\s*:=\s*resources\.Get\s*(.+?)\s*\}\}\s*\{\{\s*\$img\s*:=\s*\$asset\.(?:Resize|Fit|Fill)\s*".+?"\s*\}\}\s*<img(.*?)src="\s*\{\{\s*\$img\.RelPermalink\s*\}\}\s*"(.*?)>'
                
                block_match = re.match(img_block_pattern, content[start_idx:], re.DOTALL)
                
                if block_match:
                    full_match_text = block_match.group(0)
                    var_name = block_match.group(1)
                    attrs_before = block_match.group(2)
                    attrs_after = block_match.group(3)
                    
                    replacement = f'<img{attrs_before}src="{{{{ {var_name} | relURL }}}}"{attrs_after}>'
                    
                    content = content[:start_idx] + replacement + content[start_idx + len(full_match_text):]

            if content != original_content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated {path}")

if __name__ == '__main__':
    refactor_html('layouts')
