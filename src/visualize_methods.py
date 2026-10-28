
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
RESULTS = ROOT / "results"

ORIGINALS = IMAGES / "orig_testing" / "testing"
MASKS = IMAGES / "masks_testing" / "testing"
EDITED = IMAGES / "sd2-sp_testing" / "testing"

def index_pngs(folder):
    return {p.stem: p for p in folder.rglob("*.png")}

def read_rgb(path):
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Erro ao ler {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def error_overlay(image, prediction, truth):
    result = image.astype(np.float32).copy()

    regions = [
        (prediction & truth, [0, 220, 0]),   # Acerto: verde
        (prediction & ~truth, [255, 0, 0]),  # Falso positivo: vermelho
        (~prediction & truth, [0, 80, 255]), # Falso negativo: azul
    ]

    for mask, color in regions:
        result[mask] = (
            0.45 * result[mask] + 0.55 * np.array(color)
        )

    return np.clip(result, 0, 255).astype(np.uint8)

def main():
    csv_path = RESULTS / "method_comparison.csv"
    df = pd.read_csv(csv_path)

    # Usa uma fotografia presente no experimento comparativo.
    sample = df.iloc[0]
    filename = sample["image"]
    coco_id = str(sample["coco_id"])

    originals = index_pngs(ORIGINALS)
    masks = index_pngs(MASKS)
    edited_files = index_pngs(EDITED)

    suffix = ".png_ps_mask.png_sd2_"
    if suffix not in filename:
        raise ValueError(f"Nome de arquivo inesperado: {filename}")

    mask_stem = filename.split(suffix, 1)[0]

    original_path = originals.get(f"{coco_id}_orig")
    edited_path = edited_files.get(filename)
    mask_path = masks.get(mask_stem)

    if not all([original_path, edited_path, mask_path]):
        raise FileNotFoundError(
            f"Arquivos ausentes para a fotografia {coco_id}"
        )

    original = read_rgb(original_path)
    edited = read_rgb(edited_path)

    truth_gray = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    if truth_gray is None:
        raise ValueError(f"Erro ao ler máscara: {mask_path}")

    truth = truth_gray > 127

    if original.shape != edited.shape or original.shape[:2] != truth.shape:
        raise ValueError("As dimensões dos arquivos não coincidem.")

    difference = np.abs(
        original.astype(np.int16) - edited.astype(np.int16)
    ).mean(axis=2).astype(np.float32)

    smoothed = cv2.GaussianBlur(
        difference, (5, 5), sigmaX=1.0
    )

    baseline15 = difference > 15
    gaussian15 = smoothed > 15
    baseline30 = difference > 30
    gaussian30 = smoothed > 30

    fig, axes = plt.subplots(3, 3, figsize=(15, 14))

    panels = [
        (original, "Imagem original", None),
        (edited, "Imagem adulterada", None),
        (truth, "Máscara de referência", "gray"),
        (baseline15, "Original — limiar 15", "gray"),
        (gaussian15, "Gaussiano — limiar 15", "gray"),
        (baseline30, "Original — limiar 30", "gray"),
        (gaussian30, "Gaussiano — limiar 30", "gray"),
        (
            error_overlay(edited, baseline15, truth),
            "Erros — original, limiar 15", None
        ),
        (
            error_overlay(edited, gaussian15, truth),
            "Erros — Gaussiano, limiar 15", None
        ),
    ]

    for ax, (image, title, cmap) in zip(axes.flat, panels):
        ax.imshow(image, cmap=cmap, vmin=0, vmax=1 if cmap else None)
        ax.set_title(title)
        ax.axis("off")

    fig.suptitle(f"Comparação dos métodos — fotografia {coco_id}")
    fig.tight_layout()

    output = RESULTS / f"method_comparison_{coco_id}.png"
    fig.savefig(output, dpi=150, bbox_inches="tight")
    print(f"Fotografia: {coco_id}")
    print(f"Figura salva em: {output}")

    plt.show()

if __name__ == "__main__":
    main()
