
from pathlib import Path

# Raiz do projeto: pasta que contém images/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_ROOT = PROJECT_ROOT / "images"

FOLDERS = {
    "original": IMAGES_ROOT / "orig_testing" / "testing",
    "masks": IMAGES_ROOT / "masks_testing" / "testing",
    "manipulated": IMAGES_ROOT / "sd2-sp_testing" / "testing",
}


def list_png_files(root: Path, limit: int = 5) -> None:
    print(f"\n[{root.name}]")

    if not root.exists():
        print(f"Diretório não encontrado: {root}")
        return

    files = sorted(root.rglob("*.png"))

    print(f"Total de arquivos PNG: {len(files)}")

    for file in files[:limit]:
        print(f"  {file.relative_to(root)}")


def main() -> None:
    for name, root in FOLDERS.items():
        print(f"\n{'=' * 50}")
        print(f"Categoria: {name}")
        list_png_files(root)


if __name__ == "__main__":
    main()
