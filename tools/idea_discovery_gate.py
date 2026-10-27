#!/usr/bin/env python3
"""Deterministically gate Idea Discovery reports on recorded stage evidence."""

from __future__ import annotations

import argparse
import re
import sys
from evidence import snapshot
from dataclasses import dataclass
from pathlib import Path

try:
    import run_state
except ImportError:  # package import: ``from tools import idea_discovery_gate``
    from tools import run_state


GATE_NAME = "idea-discovery-evidence"
# sec-paper vendored edition: defaults are the sec-* pipeline stage names.
# Override both lists from the CLI (--phases / --review-phases) if a project
# runs a differently-named chain.
REQUIRED_PHASES = (
    "sec-research-lit",
    "sec-idea-creator",
    "sec-novelty-check",
    "sec-research-review",
    "sec-research-refine-pipeline",
)
# These phases promise a model review, not merely executor-produced prose.  A
# heading and a ``done`` self-report therefore cannot satisfy their evidence
# obligation: the run state must contain the receipt written by ``accept`` or
# ``mark-provisional``.
REVIEW_REQUIRED_PHASES = frozenset({"sec-idea-creator", "sec-novelty-check", "sec-research-review", "sec-research-refine-pipeline"})
START_MARKER = "<!-- ARIS_IDEA_DISCOVERY_EVIDENCE_GATE:START -->"
END_MARKER = "<!-- ARIS_IDEA_DISCOVERY_EVIDENCE_GATE:END -->"


@dataclass(frozen=True)
class GateResult:
    verdict: str
    reasons: tuple[str, ...]


def _artifact_target(root: Path, artifact: str) -> tuple[Path, str | None]:
    path_text, separator, anchor = artifact.partition("#")
    if not path_text:
        raise ValueError("artifact path is empty")
    if separator and not anchor.strip():
        raise ValueError(f"artifact anchor is empty: {artifact}")
    candidate = (root / path_text).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"artifact escapes project root: {artifact}") from exc
    return candidate, anchor if separator else None


def _heading_slug(line: str) -> str | None:
    match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
    if not match:
        return None
    text = match.group(1).strip().lower()
    slug = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"[\s-]+", "-", slug).strip("-")


def _section_has_content(path: Path, anchor: str) -> tuple[bool, bool]:
    """Return whether the first matching section exists and has a non-empty body."""
    found = False
    level = 0
    fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        heading = _heading_slug(line)
        if not found:
            if heading == anchor:
                found = True
                level = len(line) - len(line.lstrip("#"))
            continue
        if heading is not None:
            if len(line) - len(line.lstrip("#")) <= level:
                return True, False
            continue
        if line.strip() and not line.strip().startswith("<!--"):
            return True, True
    return found, False


def _review_provenance_reason(name: str, phase: dict, state: dict) -> str | None:
    """Validate a reviewer receipt without granting or repairing acceptance."""
    status = phase.get("status")
    if status not in {"accepted", "provisional"}:
        return f"{name} review evidence missing (status={status or 'unknown'})"

    verdict_id = phase.get("verdict_id")
    reviewer = phase.get("reviewer")
    if not isinstance(verdict_id, str) or not verdict_id.strip():
        return f"{name} review evidence missing (verdict_id not recorded)"
    if not isinstance(reviewer, str) or not reviewer.strip():
        return f"{name} review evidence missing (reviewer not recorded)"

    executor = phase.get("executor_model")
    if not isinstance(executor, str) or not executor.strip():
        return f"{name} review provenance invalid (executor_model not recorded)"

    executor_family = run_state.model_family(executor)
    reviewer_family = run_state.model_family(reviewer)
    if executor_family == "unknown" or reviewer_family in {"unknown", "deterministic"}:
        return (
            f"{name} review provenance invalid (model families cannot establish "
            "a model review)"
        )
    if phase.get("executor_family") != executor_family:
        return f"{name} review provenance invalid (executor_family inconsistent)"
    if phase.get("reviewer_family") != reviewer_family:
        return f"{name} review provenance invalid (reviewer_family inconsistent)"

    if status == "accepted":
        if phase.get("acceptance_status") != "accepted":
            return f"{name} review provenance invalid (acceptance_status inconsistent)"
        if executor_family == reviewer_family:
            return f"{name} review provenance invalid (accepted review is same-family)"
        if phase.get("review_independence") != "cross-family":
            return f"{name} review provenance invalid (review_independence inconsistent)"
        return None

    if phase.get("acceptance_status") != "provisional":
        return f"{name} review provenance invalid (acceptance_status inconsistent)"
    if executor_family != reviewer_family:
        return f"{name} review provenance invalid (provisional review is not same-family)"
    if phase.get("review_independence") != "same-family":
        return f"{name} review provenance invalid (review_independence inconsistent)"
    policy = state.get("policy")
    if not isinstance(policy, dict) or policy.get("provisional_advances") is not True:
        return (
            f"{name} review provenance invalid "
            "(provisional review cannot advance this run)"
        )
    return None


def evaluate(
    root: str | Path,
    state: dict,
    required_phases: tuple[str, ...] = REQUIRED_PHASES,
    review_phases: frozenset[str] = REVIEW_REQUIRED_PHASES,
) -> GateResult:
    """Check that every required stage has completed, durable evidence."""
    project_root = Path(root).resolve()
    phases = {phase["phase"]: phase for phase in state.get("phases", [])}
    reasons: list[str] = []

    for name in required_phases:
        phase = phases.get(name)
        if phase is None:
            reasons.append(f"{name} evidence missing (phase not recorded)")
            continue
        if phase.get("status") not in {"done", "accepted", "provisional"}:
            reasons.append(
                f"{name} evidence missing (status={phase.get('status', 'unknown')})"
            )
            continue
        if name in review_phases:
            provenance_reason = _review_provenance_reason(name, phase, state)
            if provenance_reason is not None:
                reasons.append(provenance_reason)
                continue
            try:
                receipt = run_state.validate_receipt(project_root, phase["verdict_id"], name, state["run_id"])
                expected = snapshot(project_root, [phase["artifact"]])
                if name == "sec-research-refine-pipeline":
                    expected.update(snapshot(project_root, [f"refine-logs/{n}" for n in ("EXPERIMENT_PLAN.md", "EXPERIMENT_TRACKER.md", "REVIEW_SUMMARY.md")]))
                if any(receipt["snapshot"].get(k) != v for k, v in expected.items()):
                    raise ValueError("review did not cover the phase artifact/section")
            except (ValueError, OSError, KeyError, TypeError) as exc:
                reasons.append(f"{name} invalid review receipt ({exc})")
                continue
        artifact = phase.get("artifact")
        if not artifact:
            reasons.append(f"{name} evidence missing (artifact not recorded)")
            continue
        try:
            artifact_path, anchor = _artifact_target(project_root, artifact)
        except ValueError as exc:
            reasons.append(f"{name} evidence missing ({exc})")
            continue
        if not artifact_path.is_file():
            reasons.append(f"{name} evidence missing (artifact absent: {artifact})")
            continue
        if artifact_path.stat().st_size == 0:
            reasons.append(f"{name} evidence missing (empty artifact: {artifact})")
        if anchor:
            section_exists, section_has_content = _section_has_content(
                artifact_path, anchor
            )
            if not section_exists:
                reasons.append(f"{name} evidence missing (section absent: #{anchor})")
            elif not section_has_content:
                reasons.append(f"{name} evidence missing (section empty: #{anchor})")

    if "sec-research-refine-pipeline" in required_phases:
        for name in ("FINAL_PROPOSAL.md", "EXPERIMENT_PLAN.md", "EXPERIMENT_TRACKER.md", "REVIEW_SUMMARY.md"):
            path = project_root / "refine-logs" / name
            if not path.is_file() or not path.stat().st_size:
                reasons.append(f"refinement output missing or empty: {name}")
    return GateResult("PASS" if not reasons else "BLOCKED", tuple(reasons))


def _gate_section(result: GateResult) -> str:
    lines = [START_MARKER, "## Evidence Gate", f"**Status:** {result.verdict}", ""]
    if result.verdict == "PASS":
        lines.append(
            "All required stage records, review receipts, artifacts, and report "
            "sections are present."
        )
    else:
        lines.append("The workflow is not complete. Required stage evidence is missing:")
        lines.extend(f"- BLOCKED: {reason}" for reason in result.reasons)
    lines.extend([END_MARKER, ""])
    return "\n".join(lines)


def write_report_gate(root: str | Path, report: str | Path, result: GateResult) -> Path:
    project_root = Path(root).resolve()
    report_path = (project_root / report).resolve()
    try:
        report_path.relative_to(project_root)
    except ValueError as exc:
        raise ValueError(f"report escapes project root: {report}") from exc

    report_path.parent.mkdir(parents=True, exist_ok=True)
    original = report_path.read_text(encoding="utf-8") if report_path.exists() else "# Idea Discovery Report\n"
    section = _gate_section(result)
    pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}\n?",
        flags=re.DOTALL,
    )
    if pattern.search(original):
        updated = pattern.sub(section, original)
    else:
        updated = original.rstrip() + "\n\n" + section
    report_path.write_text(updated, encoding="utf-8")
    return report_path


def run(
    root: str | Path,
    run_id: str,
    report: str | Path,
    required_phases: tuple[str, ...] = REQUIRED_PHASES,
    review_phases: frozenset[str] = REVIEW_REQUIRED_PHASES,
) -> GateResult:
    try:
        state = run_state.load_run(str(root), run_id)
    except FileNotFoundError:
        result = GateResult("BLOCKED", ("run state missing",))
        write_report_gate(root, report, result)
        return result

    result = evaluate(root, state, required_phases, review_phases)
    # The gate's verdict lives ONLY in gates.<GATE_NAME>. It must not mark the
    # semantic phases `accepted`: per resumable-runs.md, file-exists evidence
    # can accept a purely mechanical phase, while these five stages carry
    # quality semantics whose acceptance/provisional receipt belongs to their
    # own reviewer gate — and resume relies on done-but-not-reviewed to know a
    # stage still needs its audit.
    run_state.record_gate_result(str(root), run_id, GATE_NAME, result.verdict, list(result.reasons))
    write_report_gate(root, report, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root")
    parser.add_argument("run_id")
    parser.add_argument("--report", default="idea-stage/IDEA_REPORT.md")
    parser.add_argument(
        "--phases",
        default=",".join(REQUIRED_PHASES),
        help="Comma-separated ordered stage names recorded in run_state "
        "(default: the sec-pipeline stage list).",
    )
    parser.add_argument(
        "--review-phases",
        default=",".join(sorted(REVIEW_REQUIRED_PHASES)),
        help="Comma-separated subset of --phases that require accept/"
        "mark-provisional review receipts.",
    )
    args = parser.parse_args()

    required = tuple(p.strip() for p in args.phases.split(",") if p.strip())
    review = frozenset(p.strip() for p in args.review_phases.split(",") if p.strip())
    if not required or not review.issubset(required) or not REVIEW_REQUIRED_PHASES.intersection(required).issubset(review):
        parser.error("nonempty phase list and all required review-bearing stages must be preserved")

    try:
        result = run(args.root, args.run_id, args.report, required, review)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for reason in result.reasons:
        print(f"BLOCKED: {reason}")
    if result.verdict == "PASS":
        print("PASS: idea-discovery evidence gate")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
