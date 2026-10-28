
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = PROJECT_ROOT / "results" / "threshold_results.csv"
OUTPUT_FILE = PROJECT_ROOT / "results" / "threshold_summary.csv"

METRICS = ["precision", "recall", "iou"]


def main():
    df = pd.read_csv(RESULTS_FILE)

    # Estatísticas por limiar, considerando cada fotografia.
    summary = df.groupby("threshold")[METRICS].agg(["mean", "std"])

    print("\n=== Médias e desvios-padrão por limiar ===")
    print(summary.round(4).to_string())

    # Compara os dois limiares fotografia por fotografia.
    paired = df.pivot(
        index="image",
        columns="threshold",
        values=METRICS,
    )

    print("\n=== Diferença média por fotografia (15 - 30) ===")

    for metric in METRICS:
        difference = paired[metric][15] - paired[metric][30]

        print(
            f"{metric:10s}: "
            f"média = {difference.mean():.4f}; "
            f"desvio-padrão = {difference.std():.4f}; "
            f"melhora em {int((difference > 0).sum())} de "
            f"{len(difference)} fotografias"
        )

    summary.to_csv(OUTPUT_FILE)

    print(f"\nResumo salvo em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
