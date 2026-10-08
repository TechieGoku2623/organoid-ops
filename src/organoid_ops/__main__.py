"""Compare two designed runs. One changed the supplement."""

from __future__ import annotations

from .engine import OpsError, Run, accept_result, format_report

PLATE = {"A1": "line-1", "A2": "line-2"}


def main() -> int:
    left = Run("run-14", "protocol-3", PLATE, 56, "10:30")
    right = Run("run-15", "protocol-3.1", PLATE, 56, "10:30")
    accept_result(left, {"run_id": "run-14", "mean_spike_rate": 1.2})
    rejected = False
    try:
        accept_result(left, {"mean_spike_rate": 1.2})
    except OpsError:
        rejected = True
    print(format_report(left, right, rejected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
