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

            # Handle {{ $asset := resources.Get SOMETHING }}
            # {{ $img := $asset... }}
            # <img ... src="{{ $img.RelPermalink }}" ... />
            
            # This can be tricky due to newlines and attributes before/after src.
            # Let's do string replacement for the specific files.
            
            # layouts/blog/list.html
            content = re.sub(
                r'\{\{\s*\$asset\s*:=\s*resources\.Get\s*(.+?)\s*\}\}\s*\{\{\s*\$img\s*:=\s*\$asset\.(?:Resize|Fit|Fill)\s*".+?"\s*\}\}\s*<img(.*?)src="\{\{\s*\$img\.RelPermalink\s*\}\}"(.*?)>',
                r'<img\2src="{{ \1 | relURL }}"\3>',
                content,
                flags=re.DOTALL
            )
            
            # layouts/partials/header/navbar.html
            content = re.sub(
                r'\{\{\s*\$asset\s*:=\s*resources\.Get\s*(.+?)\s*\}\}\s*\{\{\s*\$img\s*:=\s*\$asset\.(?:Resize|Fit|Fill)\s*".+?"\s*\}\}\s*<img(.*?)src="\{\{\s*\$img\.RelPermalink\s*\}\}"(.*?)/>',
                r'<img\2src="{{ \1 | relURL }}"\3/>',
                content,
                flags=re.DOTALL
            )

            # Let's check for any other pattern where resources.Get is used for images and then RelPermalink
            # The general pattern:
            # {{ $asset := resources.Get (VAR) }}
            # {{ $img := $asset.Method (PARAMS) }}
            # <img ... src="{{ $img.RelPermalink }}" ... />

            if content != original_content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated {path}")

if __name__ == '__main__':
    refactor_html('layouts')
