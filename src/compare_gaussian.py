
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from src.metrics import calculate_metrics

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_ROOT = PROJECT_ROOT / "images"
RESULTS_DIR = PROJECT_ROOT / "results"

PREVIOUS_RESULTS = RESULTS_DIR / "threshold_results.csv"
OUTPUT_FILE = RESULTS_DIR / "method_comparison.csv"

ORIGINALS = IMAGES_ROOT / "orig_testing" / "testing"
MASKS = IMAGES_ROOT / "masks_testing" / "testing"
MANIPULATED = IMAGES_ROOT / "sd2-sp_testing" / "testing"

THRESHOLDS = [15, 30]
GAUSSIAN_KERNEL = (5, 5)
GAUSSIAN_SIGMA = 1.0


def index_pngs(root: Path) -> dict[str, Path]:
    return {path.stem: path for path in root.rglob("*.png")}


def read_gray_mask(path: Path) -> np.ndarray:
    mask = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)

    if mask is None:
        raise ValueError(f"Não foi possível ler a máscara: {path}")

    return mask > 127

def main():
    if not PREVIOUS_RESULTS.exists():
        raise FileNotFoundError(
            "Execute primeiro src/compare_thresholds.py."
        )

    previous = pd.read_csv(PREVIOUS_RESULTS)

    # Reutiliza exatamente as imagens do experimento anterior.
    samples = previous.drop_duplicates(subset=["image"])

    originals = index_pngs(ORIGINALS)
    masks = index_pngs(MASKS)
    manipulated = index_pngs(MANIPULATED)

    rows = []
    skipped = 0

    suffix = ".png_ps_mask.png_sd2_"

    for _, sample in samples.iterrows():
        edited_name = sample["image"]
        coco_id = str(sample["coco_id"])

        if suffix not in edited_name:
            skipped += 1
            continue

        mask_stem = edited_name.split(suffix, 1)[0]

        original_path = originals.get(f"{coco_id}_orig")
        edited_path = manipulated.get(edited_name)
        mask_path = masks.get(mask_stem)

        if not all((original_path, edited_path, mask_path)):
            print(f"Arquivos ausentes; ignorando: {edited_name}")
            skipped += 1
            continue

        original = cv2.imread(
            str(original_path), cv2.IMREAD_COLOR
        )
        edited = cv2.imread(
            str(edited_path), cv2.IMREAD_COLOR
        )
        ground_truth = read_gray_mask(mask_path)

        if original is None or edited is None:
            print(f"Falha ao ler imagem: {edited_name}")
            skipped += 1
            continue

        if (
            original.shape != edited.shape
            or original.shape[:2] != ground_truth.shape
        ):
            print(f"Dimensões incompatíveis: {edited_name}")
            skipped += 1
            continue

        # Método A: diferença absoluta média dos canais BGR.
        difference = np.abs(
            original.astype(np.int16)
            - edited.astype(np.int16)
        ).mean(axis=2).astype(np.float32)

        # Método B: suaviza o mapa de diferença antes da
        # limiarização, sem modificar as imagens originais.
        smoothed_difference = cv2.GaussianBlur(
            difference,
            GAUSSIAN_KERNEL,
            sigmaX=GAUSSIAN_SIGMA,
        )

        difference_maps = {
            "baseline": difference,
            "gaussian": smoothed_difference,
        }

        for method, difference_map in difference_maps.items():
            for threshold in THRESHOLDS:
                prediction = difference_map > threshold

                metrics = calculate_metrics(
                    prediction,
                    ground_truth,
                )

                rows.append({
                    "image": edited_name,
                    "coco_id": coco_id,
                    "method": method,
                    "threshold": threshold,
                    **metrics,
                })

    if not rows:
        raise RuntimeError(
            "Nenhuma imagem foi avaliada. Confira os caminhos."
        )

    results = pd.DataFrame(rows)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_FILE, index=False)

    summary = (
        results.groupby(["method", "threshold"])[
            ["precision", "recall", "iou"]
        ]
        .agg(["mean", "std"])
        .round(4)
    )

    print(f"Fotografias avaliadas: {results['image'].nunique()}")
    print(f"Arquivos ignorados: {skipped}")
    print(f"\nKernel Gaussiano: {GAUSSIAN_KERNEL}")
    print(f"Sigma: {GAUSSIAN_SIGMA}")
    print("\n=== Médias e desvios-padrão ===")
    print(summary.to_string())

    # Comparação pareada: Gaussiano menos baseline,
    # para cada limiar e cada fotografia.
    print("\n=== Diferença média por fotografia (Gaussiano - baseline) ===")

    for threshold in THRESHOLDS:
        subset = results[results["threshold"] == threshold]

        paired = subset.pivot(
            index="image",
            columns="method",
            values=["precision", "recall", "iou"],
        )

        print(f"\nLimiar {threshold}:")

        for metric in ["precision", "recall", "iou"]:
            difference = (
                paired[metric]["gaussian"]
                - paired[metric]["baseline"]
            )

            print(
                f"{metric:10s}: "
                f"média = {difference.mean():.4f}; "
                f"desvio-padrão = {difference.std():.4f}; "
                f"melhora em {(difference > 0).sum()} de "
                f"{len(difference)} fotografias"
            )

    print(f"\nResultados completos salvos em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
