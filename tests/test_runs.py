"""A supplement change is a different protocol. A plot without a run id is refused."""

from __future__ import annotations

import unittest

from organoid_ops import OpsError, Run, accept_result, comparable


PLATE = {"A1": "line-1", "A2": "line-2"}


class RunTests(unittest.TestCase):
    def test_same_record_is_comparable(self) -> None:
        left = Run("run-14", "protocol-3", PLATE, 56, "10:30")
        right = Run("run-16", "protocol-3", PLATE, 56, "10:30")
        self.assertTrue(comparable(left, right)["comparable"])

    def test_new_protocol_version_is_named(self) -> None:
        left = Run("run-14", "protocol-3", PLATE, 56, "10:30")
        right = Run("run-15", "protocol-3.1", PLATE, 56, "11:00")
        check = comparable(left, right)
        self.assertFalse(check["comparable"])
        self.assertEqual(check["reasons"], ["protocol", "assay_window"])

    def test_result_must_name_the_run(self) -> None:
        run = Run("run-14", "protocol-3", PLATE, 56, "10:30")
        self.assertTrue(accept_result(run, {"run_id": "run-14"})["accepted"])
        with self.assertRaises(OpsError):
            accept_result(run, {"mean_spike_rate": 1.2})

    def test_empty_plate_raises(self) -> None:
        with self.assertRaises(OpsError):
            Run("run-1", "protocol-3", {}, 56, "10:30")


if __name__ == "__main__":
    unittest.main()
