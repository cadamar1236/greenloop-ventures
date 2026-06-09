import base64
import os

with open('frontend/src/App.jsx', 'r') as f:
    app = f.read()

with open('frontend/src/index.css', 'r') as f:
    css = f.read()

with open('frontend/src/main.jsx', 'r') as f:
    main = f.read()

# Create vite_src directory structure
os.makedirs('vite_src/src', exist_ok=True)

# Write all files
for path, content in [
    ('vite_src/src/App.jsx', app),
    ('vite_src/src/index.css', css),
    ('vite_src/src/main.jsx', main),
]:
    with open(path, 'w') as f:
        f.write(content)
    print(f"✓ Written {path} ({len(content)} chars)")

# Copy the config files too
import shutil
for f in ['index.html', 'vite.config.js']:
    shutil.copy2(f'frontend/{f}', f'vite_src/{f}')
    print(f"✓ Copied {f}")