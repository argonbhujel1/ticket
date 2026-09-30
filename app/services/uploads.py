"""Simple secure image upload helper — optional clear background for logos."""
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def _clear_white_bg(path: Path):
    """Make near-white background transparent (cleaner crests on dark UI)."""
    try:
        from PIL import Image
        img = Image.open(path).convert('RGBA')
        pixels = img.getdata()
        new = []
        for r, g, b, a in pixels:
            # near-white / light gray → transparent
            if r > 240 and g > 240 and b > 240:
                new.append((255, 255, 255, 0))
            elif r > 230 and g > 230 and b > 230 and abs(r - g) < 12 and abs(g - b) < 12:
                new.append((r, g, b, max(0, 255 - int((r + g + b) / 3 - 200) * 8)))
            else:
                new.append((r, g, b, a))
        img.putdata(new)
        out = path.with_suffix('.png')
        img.save(out, 'PNG')
        if out != path and path.exists():
            path.unlink(missing_ok=True)
        return out
    except Exception:
        return path


def save_upload(file_storage, folder='general', clear_bg=False):
    if not file_storage or not file_storage.filename:
        return None
    ext = file_storage.filename.rsplit('.', 1)[-1].lower() if '.' in file_storage.filename else ''
    if ext not in ALLOWED:
        return None
    root = Path(current_app.config['UPLOAD_FOLDER'])
    dest_dir = root / folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    name = f'{uuid.uuid4().hex[:12]}.{ext}'
    path = dest_dir / name
    file_storage.save(str(path))
    if clear_bg or folder == 'logos':
        path = _clear_white_bg(path)
        name = path.name
    return f'{folder}/{name}'
