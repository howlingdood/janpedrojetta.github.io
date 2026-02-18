import re
from pathlib import Path

# Pages to update and the image folder they should display (relative to site root)
GALLERIES = {
    "illustrations.html": "images/illustrations",
    "sketchbook.html": "images/sketchbook",
}


# Supported image extensions (case-insensitive)
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

START = "<!-- AUTO-GALLERY:START -->"
END = "<!-- AUTO-GALLERY:END -->"

def nice_alt(filename: str) -> str:
    name = Path(filename).stem
    name = re.sub(r"[_\-]+", " ", name)
    name = re.sub(r"[()]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def build_img_tags(root: Path, folder: Path) -> str:
    if not folder.exists():
        return f'  <!-- Folder not found: {folder.as_posix()} -->\n'

    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in EXTS]
    files.sort(key=lambda p: p.name.lower())  # alphabetical

    if not files:
        return f'  <!-- No images found in: {folder.as_posix()} -->\n'

    lines = []
    for p in files:
        # IMPORTANT: make src relative to site root (not absolute Windows path)
        rel = p.relative_to(root).as_posix()  # e.g. images/characters/char1.jpg
        alt = nice_alt(p.name)
        lines.append(f'  <img src="{rel}" alt="{alt}" loading="lazy">')
    return "\n".join(lines) + "\n"

def replace_between_markers(html: str, new_block: str) -> str:
    if START not in html or END not in html:
        raise ValueError("Missing AUTO-GALLERY markers. Add START/END markers inside your .grid div.")

    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    replacement = START + "\n" + new_block + "  " + END
    return pattern.sub(replacement, html, count=1)

def main():
    root = Path(__file__).resolve().parent

    for page, folder_rel in GALLERIES.items():
        page_path = root / page
        folder_path = root / folder_rel

        if not page_path.exists():
            print(f"[skip] {page} not found")
            continue

        html = page_path.read_text(encoding="utf-8")
        new_imgs = build_img_tags(root, folder_path)
        updated = replace_between_markers(html, new_imgs)

        page_path.write_text(updated, encoding="utf-8")
        print(f"[ok] updated {page} from {folder_rel}")

    print("Done.")

if __name__ == "__main__":
    main()
