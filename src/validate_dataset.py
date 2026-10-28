
from pathlib import Path
from collections import Counter

import cv2

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_ROOT = PROJECT_ROOT / "images"

ORIGINALS = IMAGES_ROOT / "orig_testing" / "testing"
MASKS = IMAGES_ROOT / "masks_testing" / "testing"
MANIPULATED = IMAGES_ROOT / "sd2-sp_testing" / "testing"


def index_pngs(root: Path) -> dict[str, Path]:
    """Indexa PNGs pelo nome completo, sem a extensão."""
    return {
        path.stem: path
        for path in root.rglob("*.png")
    }


def image_shape(path: Path):
    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None:
        return None
    return image.shape[:2]


def main():
    originals = index_pngs(ORIGINALS)
    masks = index_pngs(MASKS)
    manipulated = index_pngs(MANIPULATED)

    print(f"Originais indexados: {len(originals)}")
    print(f"Máscaras indexadas: {len(masks)}")
    print(f"Adulteradas indexadas: {len(manipulated)}")

    counts = Counter()
    examples = []

    for name, edited_path in manipulated.items():
        # Exemplo:
        # 134886_mask_bbox.png_ps_mask.png_sd2_0
        marker = "_mask_"
        if marker not in name:
            counts["nome_inesperado"] += 1
            continue

        coco_id = name.split(marker, 1)[0]

        # Primeiro tentamos a máscara com o mesmo nome-base,
        # removendo o sufixo de geração.
        suffix = ".png_ps_mask.png_sd2_"
        if suffix not in name:
            counts["sufixo_inesperado"] += 1
            continue

        mask_stem = name.split(suffix, 1)[0]
        mask_path = masks.get(mask_stem)

        # O nome-base original pode existir em diferentes resoluções.
        original_path = originals.get(f"{coco_id}_orig")

        if original_path is None:
            counts["original_ausente"] += 1
            continue

        if mask_path is None:
            counts["mascara_ausente"] += 1
            continue

        original_shape = image_shape(original_path)
        edited_shape = image_shape(edited_path)
        mask_shape = image_shape(mask_path)

        if None in (original_shape, edited_shape, mask_shape):
            counts["falha_leitura"] += 1
            continue

        counts["trio_encontrado"] += 1

        if original_shape == edited_shape == mask_shape:
            counts["tres_dimensoes_iguais"] += 1
        else:
            counts["dimensoes_diferentes"] += 1

        if len(examples) < 10:
            examples.append(
                (
                    edited_path.name,
                    original_path.name,
                    mask_path.name,
                    original_shape,
                    edited_shape,
                    mask_shape,
                )
            )

    print("\nResumo:")
    for key, value in counts.most_common():
        print(f"  {key}: {value}")

    print("\nExemplos de correspondências:")
    for edited, original, mask, osize, esize, msize in examples:
        print(f"\nAdulterada: {edited}")
        print(f"Original:   {original} {osize}")
        print(f"Máscara:    {mask} {msize}")
        print(f"Adulterada: {esize}")


if __name__ == "__main__":
    main()
