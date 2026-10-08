"""Two runs compare only when protocol, plate, and assay window agree.

A result that does not name its run id is not entered.
"""

from __future__ import annotations

from typing import Mapping


class OpsError(ValueError):
    """A run or a result file is missing the field the record requires."""


class Run:
    def __init__(
        self,
        run_id: str,
        protocol_version: str,
        plate: Mapping[str, str],
        assay_day: int,
        assay_clock: str,
    ) -> None:
        if not run_id.strip() or not protocol_version.strip():
            raise OpsError("run id and protocol version are required")
        if not plate:
            raise OpsError("plate map is required")
        if assay_day < 0:
            raise OpsError("assay day cannot be negative")
        if len(assay_clock) != 5 or assay_clock[2] != ":":
            raise OpsError("assay clock is HH:MM")
        self.run_id = run_id.strip()
        self.protocol_version = protocol_version.strip()
        self.plate = dict(plate)
        self.assay_day = assay_day
        self.assay_clock = assay_clock

    def as_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "protocol_version": self.protocol_version,
            "plate": self.plate,
            "assay_day": self.assay_day,
            "assay_clock": self.assay_clock,
        }


def comparable(left: Run, right: Run) -> dict[str, object]:
    reasons: list[str] = []
    if left.protocol_version != right.protocol_version:
        reasons.append("protocol")
    if left.plate != right.plate:
        reasons.append("plate")
    if left.assay_day != right.assay_day or left.assay_clock != right.assay_clock:
        reasons.append("assay_window")
    return {"comparable": not reasons, "reasons": reasons}


def accept_result(run: Run, result: Mapping[str, object]) -> dict[str, object]:
    named = str(result.get("run_id", "")).strip()
    if named != run.run_id:
        raise OpsError("result does not name its run")
    return {"accepted": True, "run_id": run.run_id}


def format_report(left: Run, right: Run, orphan_rejected: bool) -> str:
    check = comparable(left, right)
    lines = [
        "organoid-ops",
        "",
        f"run {left.run_id}  {left.protocol_version}  day {left.assay_day} {left.assay_clock}",
        f"run {right.run_id}  {right.protocol_version}  day {right.assay_day} {right.assay_clock}",
        f"comparable: {str(check['comparable']).lower()}",
    ]
    reasons = check["reasons"]
    assert isinstance(reasons, list)
    lines.append("disagreement: " + (", ".join(reasons) if reasons else "none"))
    lines.append(f"result without a run id rejected: {str(orphan_rejected).lower()}")
    lines.append("")
    lines.append("no organoid measurements are stored here")
    return "\n".join(lines)
