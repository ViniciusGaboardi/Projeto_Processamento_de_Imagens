
import unittest

import numpy as np

from src.metrics import calculate_metrics


class TestCalculateMetrics(unittest.TestCase):

    def test_perfect_prediction(self):
        mask = np.array([
            [1, 0],
            [1, 1],
        ])

        result = calculate_metrics(mask, mask)

        self.assertEqual(result["precision"], 1.0)
        self.assertEqual(result["recall"], 1.0)
        self.assertEqual(result["iou"], 1.0)

    def test_partial_overlap(self):
        prediction = np.array([
            [1, 1],
            [0, 0],
        ])

        ground_truth = np.array([
            [1, 0],
            [0, 1],
        ])

        result = calculate_metrics(prediction, ground_truth)

        self.assertAlmostEqual(result["precision"], 0.5)
        self.assertAlmostEqual(result["recall"], 0.5)
        self.assertAlmostEqual(result["iou"], 1 / 3)

    def test_no_overlap(self):
        prediction = np.array([
            [1, 0],
            [0, 0],
        ])

        ground_truth = np.array([
            [0, 1],
            [0, 0],
        ])

        result = calculate_metrics(prediction, ground_truth)

        self.assertEqual(result["precision"], 0.0)
        self.assertEqual(result["recall"], 0.0)
        self.assertEqual(result["iou"], 0.0)

    def test_both_masks_empty(self):
        empty = np.zeros((2, 2), dtype=bool)

        result = calculate_metrics(empty, empty)

        self.assertEqual(result["precision"], 0.0)
        self.assertEqual(result["recall"], 0.0)
        self.assertEqual(result["iou"], 0.0)

    def test_different_shapes_raise_error(self):
        prediction = np.zeros((2, 2))
        ground_truth = np.zeros((3, 3))

        with self.assertRaises(ValueError):
            calculate_metrics(prediction, ground_truth)


if __name__ == "__main__":
    unittest.main()
