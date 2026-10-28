
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_ROOT = PROJECT_ROOT / "images"

ORIGINALS = IMAGES_ROOT / "orig_testing" / "testing"
MASKS = IMAGES_ROOT / "masks_testing" / "testing"
MANIPULATED = IMAGES_ROOT / "sd2-sp_testing" / "testing"


def find_file(root: Path, filename: str) -> Path | None:
    matches = list(root.rglob(filename))
    return matches[0] if matches else None


def read_image(path: Path, grayscale: bool = False):
    mode = cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR
    image = cv2.imread(str(path), mode)

    if image is None:
        raise ValueError(f"Não foi possível ler: {path}")

    if not grayscale:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


def main():
    # Exemplo confirmado pelo validador.
    original_path = find_file(ORIGINALS, "134886_orig.png")
    edited_name = "134886_mask_bbox.png_ps_mask.png_sd2_0.png"
    edited_path = find_file(MANIPULATED, edited_name)
    mask_path = find_file(MASKS, "134886_mask_bbox.png")

    if not all((original_path, edited_path, mask_path)):
        raise FileNotFoundError(
            "Não foi possível encontrar todos os arquivos da amostra."
        )

    original = read_image(original_path)
    edited = read_image(edited_path)
    mask = read_image(mask_path, grayscale=True)

    if original.shape != edited.shape or original.shape[:2] != mask.shape:
        raise ValueError("As dimensões dos arquivos não coincidem.")

    # Diferença absoluta média entre os canais de cor.
    difference = np.abs(
        original.astype(np.int16) - edited.astype(np.int16)
    ).mean(axis=2).astype(np.uint8)

    figure, axes = plt.subplots(1, 4, figsize=(18, 5))

    axes[0].imshow(original)
    axes[0].set_title("Original")

    axes[1].imshow(edited)
    axes[1].set_title("Adulterada (SD2)")

    axes[2].imshow(mask, cmap="gray", vmin=0, vmax=255)
    axes[2].set_title("Máscara de referência")

    axes[3].imshow(difference, cmap="inferno")
    axes[3].set_title("Diferença absoluta")

    for axis in axes:
        axis.axis("off")

    figure.tight_layout()

    output_dir = PROJECT_ROOT / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "sample_comparison.png"

    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Visualização salva em: {output_path}")

    plt.show()


if __name__ == "__main__":
    main()
