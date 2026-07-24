#!/usr/bin/env python3
"""Collect and mark idempotent Habitat Sol writers-input inbox items.

The collector fingerprints normalized notes so the daily canon curator receives
only content that has not already been dispositioned. It deliberately keeps
state in the repository: the editorial decision trail travels with the canon.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

STATE_RELATIVE_PATH = Path("writers-input/.inbox-state.json")
INBOX_RELATIVE_PATH = Path("writers-input/inbox.md")
SCHEMA_VERSION = 1


def normalize_note(text: str) -> str:
    """Normalize presentation-only variation while preserving substantive text."""
    text = unicodedata.normalize("NFKC", text).strip()
    return re.sub(r"\s+", " ", text)


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def load_state(state_path: Path) -> dict[str, Any]:
    if not state_path.exists():
        return {"schema_version": SCHEMA_VERSION, "items": {}}
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid state JSON: {state_path}: {exc}") from exc
    if not isinstance(state, dict) or state.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported state schema in {state_path}; expected {SCHEMA_VERSION}."
        )
    if not isinstance(state.get("items"), dict):
        raise ValueError(f"State file {state_path} must contain an object at 'items'.")
    return state


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp_path.replace(path)


def inbox_items(inbox_path: Path) -> list[dict[str, Any]]:
    if not inbox_path.exists():
        raise FileNotFoundError(f"Inbox not found: {inbox_path}")

    items: list[dict[str, Any]] = []
    in_notes = False
    for line_number, raw_line in enumerate(inbox_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped.startswith("## "):
            in_notes = stripped.casefold() == "## notes"
            continue
        if not in_notes or not stripped.startswith("-"):
            continue
        candidate = re.sub(r"^-\s*", "", stripped).strip()
        if not candidate or candidate.startswith("<!--"):
            continue
        normalized = normalize_note(candidate)
        if not normalized:
            continue
        items.append(
            {
                "source_line": line_number,
                "text": candidate,
                "normalized": normalized,
                "fingerprint": fingerprint(normalized),
            }
        )
    return items


def collector_payload(repo: Path) -> dict[str, Any]:
    inbox_path = repo / INBOX_RELATIVE_PATH
    state_path = repo / STATE_RELATIVE_PATH
    state = load_state(state_path)
    all_items = inbox_items(inbox_path)
    pending = [item for item in all_items if item["fingerprint"] not in state["items"]]
    return {
        "schema_version": SCHEMA_VERSION,
        "inbox": str(INBOX_RELATIVE_PATH),
        "state": str(STATE_RELATIVE_PATH),
        "source_item_count": len(all_items),
        "handled_count": len(all_items) - len(pending),
        "pending_count": len(pending),
        "pending": pending,
    }


def mark_processed(args: argparse.Namespace, repo: Path) -> dict[str, Any]:
    state_path = repo / STATE_RELATIVE_PATH
    state = load_state(state_path)
    available = {item["fingerprint"]: item for item in inbox_items(repo / INBOX_RELATIVE_PATH)}
    if args.fingerprint not in available:
        raise ValueError("Fingerprint is not present in the current ## Notes inbox items.")
    if args.fingerprint in state["items"]:
        raise ValueError("Fingerprint is already handled; state was not changed.")

    state["items"][args.fingerprint] = {
        "normalized_text": available[args.fingerprint]["normalized"],
        "source_line_at_processing": available[args.fingerprint]["source_line"],
        "processed_at": args.processed_at or utc_now(),
        "disposition": args.disposition,
        "destinations": args.destination or [],
        "rationale": args.rationale,
    }
    atomic_write_json(state_path, state)
    return {
        "status": "recorded",
        "fingerprint": args.fingerprint,
        "state": str(STATE_RELATIVE_PATH),
        "entry": state["items"][args.fingerprint],
    }


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Habitat Sol repository root (default: current directory).")
    parser.add_argument("--mark-processed", action="store_true", help="Record one final item disposition in state.")
    parser.add_argument("--fingerprint", help="SHA-256 fingerprint from collector output.")
    parser.add_argument(
        "--disposition",
        choices=[
            "writer-guidance", "story-seed", "observation", "character-pressure",
            "provisional-decision", "canon-clarification", "open-question",
            "duplicate/no-change", "needs-creator",
        ],
        help="Final handling class for a marked item.",
    )
    parser.add_argument("--destination", action="append", help="Repository-relative destination; repeat as needed.")
    parser.add_argument("--rationale", help="One concise explanation of the final disposition.")
    parser.add_argument("--processed-at", help="ISO-8601 UTC timestamp override, primarily for reproducible tests.")
    return parser


def main() -> int:
    args = parser().parse_args()
    repo = Path(args.repo).resolve()
    try:
        if args.mark_processed:
            missing = [name for name in ("fingerprint", "disposition", "rationale") if not getattr(args, name)]
            if missing:
                raise ValueError("--mark-processed requires " + ", ".join("--" + x.replace("_", "-") for x in missing))
            result = mark_processed(args, repo)
        else:
            result = collector_payload(repo)
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
