import os
import re

def update_references(directory):
    for root, _, files in os.walk(directory):
        for f in files:
            if not f.endswith(('.md', '.yml', '.yaml')): 
                continue
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            orig = content
            # Replace frontmatter/yaml paths: `key: images/...` -> `key: /images/...`
            content = re.sub(r'^(\s*[a-zA-Z0-9_]+Image|thumbnail|image):\s*images/', r'\1: /images/', content, flags=re.MULTILINE)
            
            # In shortcodes: src="images/...
            content = re.sub(r'src="images/', r'src="/images/', content)
            
            # In shortcodes: image="images/...
            content = re.sub(r'image="images/', r'image="/images/', content)
            
            if orig != content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f'Updated {path}')

if __name__ == '__main__':
    update_references('content')
    update_references('data')
