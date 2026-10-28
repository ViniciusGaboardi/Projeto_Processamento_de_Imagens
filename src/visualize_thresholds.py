
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_ROOT = PROJECT_ROOT / "images"
RESULTS_FILE = PROJECT_ROOT / "results" / "threshold_results.csv"

ORIGINALS = IMAGES_ROOT / "orig_testing" / "testing"
MASKS = IMAGES_ROOT / "masks_testing" / "testing"
MANIPULATED = IMAGES_ROOT / "sd2-sp_testing" / "testing"

THRESHOLDS = [15, 30]


def index_pngs(root: Path) -> dict[str, Path]:
    return {path.stem: path for path in root.rglob("*.png")}


def read_rgb(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Não foi possível ler: {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def read_mask(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Não foi possível ler: {path}")
    return image > 127


def create_error_overlay(
    image: np.ndarray,
    prediction: np.ndarray,
    ground_truth: np.ndarray,
) -> np.ndarray:
    """Verde = acerto; vermelho = falso positivo; azul = falso negativo."""
    overlay = image.astype(np.float32).copy()

    true_positive = prediction & ground_truth
    false_positive = prediction & ~ground_truth
    false_negative = ~prediction & ground_truth

    colors = {
        "tp": np.array([0, 220, 0], dtype=np.float32),
        "fp": np.array([255, 0, 0], dtype=np.float32),
        "fn": np.array([0, 80, 255], dtype=np.float32),
    }

    alpha = 0.55

    for region, color in [
        (true_positive, colors["tp"]),
        (false_positive, colors["fp"]),
        (false_negative, colors["fn"]),
    ]:
        overlay[region] = (
            (1 - alpha) * overlay[region] + alpha * color
        )

    return np.clip(overlay, 0, 255).astype(np.uint8)


def main():
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(
            "Resultados não encontrados. Execute primeiro "
            "src/compare_thresholds.py."
        )

    results = pd.read_csv(RESULTS_FILE)

    if results.empty:
        raise ValueError("O arquivo de resultados está vazio.")

    # Escolhe a primeira amostra registrada no experimento.
    sample = results.iloc[0]
    edited_name = sample["image"]
    coco_id = str(sample["coco_id"])

    originals = index_pngs(ORIGINALS)
    masks = index_pngs(MASKS)
    manipulated = index_pngs(MANIPULATED)

    edited_path = manipulated.get(edited_name)
    original_path = originals.get(f"{coco_id}_orig")

    suffix = ".png_ps_mask.png_sd2_"
    if suffix not in edited_name:
        raise ValueError(
            f"Formato de nome inesperado: {edited_name}"
        )

    mask_stem = edited_name.split(suffix, 1)[0]
    mask_path = masks.get(mask_stem)

    if not all((edited_path, original_path, mask_path)):
        raise FileNotFoundError(
            "Não foi possível encontrar todos os arquivos "
            f"da amostra {edited_name}."
        )

    original = read_rgb(original_path)
    edited = read_rgb(edited_path)
    ground_truth = read_mask(mask_path)

    if (
        original.shape != edited.shape
        or original.shape[:2] != ground_truth.shape
    ):
        raise ValueError("As dimensões dos arquivos não coincidem.")

    difference = np.abs(
        original.astype(np.int16) - edited.astype(np.int16)
    ).mean(axis=2)

    predictions = {
        threshold: difference > threshold
        for threshold in THRESHOLDS
    }

    overlay = create_error_overlay(
        edited,
        predictions[15],
        ground_truth,
    )

    figure, axes = plt.subplots(2, 3, figsize=(16, 10))

    panels = [
        (original, "Imagem original", None),
        (edited, "Imagem adulterada (SD2)", None),
        (ground_truth, "Máscara de referência", "gray"),
        (predictions[15], "Detecção — limiar 15", "gray"),
        (predictions[30], "Detecção — limiar 30", "gray"),
        (overlay, "Erros — limiar 15", None),
    ]

    for axis, (image, title, cmap) in zip(axes.flat, panels):
        if cmap:
            axis.imshow(image, cmap=cmap, vmin=0, vmax=1)
        else:
            axis.imshow(image)

        axis.set_title(title)
        axis.axis("off")

    figure.suptitle(
        f"Comparação de limiares — fotografia COCO {coco_id}",
        fontsize=14,
    )
    figure.tight_layout()

    output_dir = PROJECT_ROOT / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"sample_errors_{coco_id}.png"
    figure.savefig(output_path, dpi=150, bbox_inches="tight")

    print(f"Fotografia original: {coco_id}")
    print(f"Imagem adulterada: {edited_path.name}")
    print(f"Máscara: {mask_path.name}")
    print(f"Figura salva em: {output_path}")

    plt.show()


if __name__ == "__main__":
    main()
