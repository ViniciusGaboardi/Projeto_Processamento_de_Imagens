
from pathlib import Path
import random

import cv2
import numpy as np
import pandas as pd
from src.metrics import calculate_metrics

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_ROOT = PROJECT_ROOT / "images"

ORIGINALS = IMAGES_ROOT / "orig_testing" / "testing"
MASKS = IMAGES_ROOT / "masks_testing" / "testing"
MANIPULATED = IMAGES_ROOT / "sd2-sp_testing" / "testing"

THRESHOLDS = [15, 30]
MAX_SAMPLES = 50
RANDOM_SEED = 42


def index_pngs(root: Path) -> dict[str, Path]:
    return {path.stem: path for path in root.rglob("*.png")}


def load_rgb(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Falha ao ler {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def load_mask(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Falha ao ler {path}")
    return image > 127


def main():
    originals = index_pngs(ORIGINALS)
    masks = index_pngs(MASKS)
    manipulated = index_pngs(MANIPULATED)

    # Monta a lista de trios válidos.
    candidates = []
    skipped = 0

    for edited_name, edited_path in manipulated.items():
        marker = "_mask_"
        suffix = ".png_ps_mask.png_sd2_"

        if marker not in edited_name or suffix not in edited_name:
            skipped += 1
            continue

        coco_id = edited_name.split(marker, 1)[0]
        mask_stem = edited_name.split(suffix, 1)[0]

        original_path = originals.get(f"{coco_id}_orig")
        mask_path = masks.get(mask_stem)

        if original_path is None or mask_path is None:
            skipped += 1
            continue

        candidates.append(
            (coco_id, edited_name, edited_path, original_path, mask_path)
        )

    # Embaralha de forma reproduzível.
    rng = random.Random(RANDOM_SEED)
    rng.shuffle(candidates)

    # Mantém apenas uma amostra por fotografia original.
    selected = []
    seen_ids = set()

    for candidate in candidates:
        coco_id = candidate[0]

        if coco_id in seen_ids:
            continue

        selected.append(candidate)
        seen_ids.add(coco_id)

        if len(selected) >= MAX_SAMPLES:
            break

    rows = []

    for coco_id, edited_name, edited_path, original_path, mask_path in selected:
        original = load_rgb(original_path)
        edited = load_rgb(edited_path)
        ground_truth = load_mask(mask_path)

        if (
            original.shape != edited.shape
            or original.shape[:2] != ground_truth.shape
        ):
            skipped += 1
            continue

        difference = np.abs(
            original.astype(np.int16) - edited.astype(np.int16)
        ).mean(axis=2)

        for threshold in THRESHOLDS:
            prediction = difference > threshold

            metrics = calculate_metrics(
                prediction, ground_truth
            )

            rows.append({
                "coco_id": coco_id,
                "image": edited_name,
                "threshold": threshold,
                **metrics,
            })

    if not rows:
        raise RuntimeError("Nenhuma amostra válida foi encontrada.")

    results = pd.DataFrame(rows)

    output_dir = PROJECT_ROOT / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    results.to_csv(output_dir / "threshold_results.csv", index=False)

    summary = (
        results.groupby("threshold")[["precision", "recall", "iou"]]
        .mean()
        .round(4)
    )

    print(f"Fotografias originais selecionadas: {len(selected)}")
    print(f"Fotografias originais avaliadas: {results['coco_id'].nunique()}")
    print(f"Imagens adulteradas avaliadas: {results['image'].nunique()}")
    print(f"Arquivos ignorados: {skipped}")
    print("\nMédias por limiar:")
    print(summary)
    print(f"\nResultados salvos em: {output_dir / 'threshold_results.csv'}")


if __name__ == "__main__":
    main()
