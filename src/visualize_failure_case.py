
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
RESULTS = ROOT / "results"

CSV_FILE = RESULTS / "method_comparison.csv"
ORIGINALS = IMAGES / "orig_testing" / "testing"
MASKS = IMAGES / "masks_testing" / "testing"
EDITED = IMAGES / "sd2-sp_testing" / "testing"


def index_pngs(folder):
    return {p.stem: p for p in folder.rglob("*.png")}


def read_rgb(path):
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Não foi possível ler: {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def error_overlay(image, prediction, truth):
    result = image.astype(np.float32).copy()

    regions = [
        (prediction & truth, [0, 220, 0]),    # Acerto: verde
        (prediction & ~truth, [255, 0, 0]),   # Falso positivo: vermelho
        (~prediction & truth, [0, 80, 255]),  # Falso negativo: azul
    ]

    for region, color in regions:
        result[region] = (
            0.45 * result[region] + 0.55 * np.array(color)
        )

    return np.clip(result, 0, 255).astype(np.uint8)


def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            "Execute primeiro src/compare_gaussian.py."
        )

    df = pd.read_csv(CSV_FILE)

    baseline = (
        df[df["method"] == "baseline"]
        .set_index(["image", "coco_id", "threshold"])
    )
    gaussian = (
        df[df["method"] == "gaussian"]
        .set_index(["image", "coco_id", "threshold"])
    )

    paired = baseline[
        ["precision", "recall", "iou"]
    ].join(
        gaussian[["precision", "recall", "iou"]],
        how="inner",
        lsuffix="_baseline",
        rsuffix="_gaussian",
    )

    paired["iou_delta"] = (
        paired["iou_gaussian"] - paired["iou_baseline"]
    )

    # Prioriza o caso em que o Gaussiano mais reduziu a IoU.
    worst = paired.sort_values("iou_delta").iloc[0]
    image_name, coco_id, threshold = paired.sort_values(
        "iou_delta"
    ).index[0]

    print("=== Caso selecionado ===")
    print(f"Fotografia: {coco_id}")
    print(f"Imagem adulterada: {image_name}")
    print(f"Limiar: {threshold}")
    print(
        f"IoU original: {worst['iou_baseline']:.4f}\n"
        f"IoU Gaussiano: {worst['iou_gaussian']:.4f}\n"
        f"Diferença: {worst['iou_delta']:+.4f}"
    )
    print(
        f"Precisão: {worst['precision_baseline']:.4f} → "
        f"{worst['precision_gaussian']:.4f}"
    )
    print(
        f"Revocação: {worst['recall_baseline']:.4f} → "
        f"{worst['recall_gaussian']:.4f}"
    )

    originals = index_pngs(ORIGINALS)
    masks = index_pngs(MASKS)
    edited_files = index_pngs(EDITED)

    suffix = ".png_ps_mask.png_sd2_"
    if suffix not in image_name:
        raise ValueError(f"Formato de nome inesperado: {image_name}")

    mask_stem = image_name.split(suffix, 1)[0]

    original_path = originals.get(f"{coco_id}_orig")
    edited_path = edited_files.get(image_name)
    mask_path = masks.get(mask_stem)

    if not all([original_path, edited_path, mask_path]):
        raise FileNotFoundError(
            f"Não foi possível localizar todos os arquivos de {coco_id}."
        )

    original = read_rgb(original_path)
    edited = read_rgb(edited_path)

    truth_gray = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    if truth_gray is None:
        raise ValueError(f"Não foi possível ler a máscara: {mask_path}")

    truth = truth_gray > 127

    if original.shape != edited.shape or original.shape[:2] != truth.shape:
        raise ValueError("As dimensões dos arquivos não coincidem.")

    difference = np.abs(
        original.astype(np.int16) - edited.astype(np.int16)
    ).mean(axis=2).astype(np.float32)

    smoothed = cv2.GaussianBlur(
        difference, (5, 5), sigmaX=1.0
    )

    prediction_baseline = difference > threshold
    prediction_gaussian = smoothed > threshold

    panels = [
        (original, "Imagem original", None),
        (edited, "Imagem adulterada", None),
        (truth, "Máscara de referência", "gray"),
        (prediction_baseline, f"Original — limiar {threshold}", "gray"),
        (prediction_gaussian, f"Gaussiano — limiar {threshold}", "gray"),
        (
            np.logical_xor(prediction_baseline, prediction_gaussian),
            "Pixels em que os métodos divergem",
            "gray",
        ),
        (
            error_overlay(edited, prediction_baseline, truth),
            "Erros — método original", None,
        ),
        (
            error_overlay(edited, prediction_gaussian, truth),
            "Erros — método Gaussiano", None,
        ),
    ]

    fig, axes = plt.subplots(3, 3, figsize=(16, 14))

    for ax, (image, title, cmap) in zip(axes.flat, panels):
        if cmap:
            ax.imshow(image, cmap=cmap, vmin=0, vmax=1)
        else:
            ax.imshow(image)
        ax.set_title(title)
        ax.axis("off")

    # Nono painel: resumo numérico do caso.
    axes.flat[8].axis("off")
    axes.flat[8].text(
        0.05, 0.9,
        f"Fotografia: {coco_id}\n"
        f"Limiar: {threshold}\n\n"
        f"IoU original: {worst['iou_baseline']:.4f}\n"
        f"IoU Gaussiano: {worst['iou_gaussian']:.4f}\n"
        f"Diferença: {worst['iou_delta']:+.4f}\n\n"
        f"Precisão: {worst['precision_baseline']:.4f} → "
        f"{worst['precision_gaussian']:.4f}\n"
        f"Revocação: {worst['recall_baseline']:.4f} → "
        f"{worst['recall_gaussian']:.4f}\n\n"
        "Erros:\nVerde = verdadeiro positivo\n"
        "Vermelho = falso positivo\nAzul = falso negativo",
        va="top",
        fontsize=12,
        wrap=True,
    )

    fig.suptitle(
        f"Análise do pior caso do filtro Gaussiano — {coco_id}",
        fontsize=15,
    )
    fig.tight_layout()

    output = RESULTS / f"failure_case_{coco_id}_t{threshold}.png"
    fig.savefig(output, dpi=150, bbox_inches="tight")

    print(f"\nFigura salva em: {output}")
    plt.show()


if __name__ == "__main__":
    main()
