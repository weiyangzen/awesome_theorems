#!/usr/bin/env python3
"""Report that the THM-M-0914 intake snapshot has been superseded."""

from pathlib import Path
import json


HERE = Path(__file__).resolve().parent


def main() -> None:
    receipt = json.loads((HERE / "intake-receipt.json").read_text(encoding="utf-8"))
    supersession = receipt.get("supersession_state", "")
    expected = "superseded_for_current_dossier_replay_by_S56-M-0914-STATEMENT"
    if not supersession.startswith(expected):
        raise SystemExit("intake receipt is not marked as superseded by the statement phase")
    raise SystemExit(
        "historical intake snapshot superseded; validate current scope with "
        "Stage1_Instances/THM-M-0914/check_statement.py"
    )


if __name__ == "__main__":
    main()
