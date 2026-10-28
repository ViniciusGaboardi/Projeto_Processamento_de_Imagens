
import numpy as np


def calculate_metrics(prediction, ground_truth):
    """Calcula precisão, revocação e IoU entre duas máscaras binárias."""
    prediction = np.asarray(prediction, dtype=bool)
    ground_truth = np.asarray(ground_truth, dtype=bool)

    if prediction.shape != ground_truth.shape:
        raise ValueError(
            "A previsão e a máscara de referência devem ter o mesmo formato."
        )

    tp = np.count_nonzero(prediction & ground_truth)
    fp = np.count_nonzero(prediction & ~ground_truth)
    fn = np.count_nonzero(~prediction & ground_truth)

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    iou = tp / (tp + fp + fn) if tp + fp + fn else 0.0

    return {
        "precision": precision,
        "recall": recall,
        "iou": iou,
    }
