#!/usr/bin/env python3
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-1526"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
SOURCE = OWNED / "Statement.lean"
META = OWNED / "statement.json"


def run(*argv: str) -> str:
    completed = subprocess.run(argv, cwd=LEAN_ROOT, text=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, check=True)
    return completed.stdout


def explicit_expression(output: str) -> str:
    marker = "def Stage1Instances.THM_M_1526.FreeDiracFactorizationTarget"
    start = output.find(marker)
    if start < 0:
        raise AssertionError("explicit target expression was not printed")
    return output[start:].strip()


def main() -> None:
    data = json.loads(META.read_text())
    output = run("lake", "env", "lean", "../../Stage1_Instances/THM-M-1526/Statement.lean")
    expression_hash = hashlib.sha256(explicit_expression(output).encode()).hexdigest()
    file_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert expression_hash == data["canonical_formal_target"]["elaborated_expression_sha256"]
    assert file_hash == data["canonical_formal_target"]["statement_file_sha256"]

    text = SOURCE.read_text()
    canonical = re.search(r"def FreeDiracFactorizationTarget : Prop :=(.*?)/-- A named alternate", text, re.S)
    assert canonical
    body = canonical.group(1)
    for required in ("deriv_commute", "Module Complex Psi", "forall psi : Psi", "D.mass ^ 2"):
        assert required in text if required == "deriv_commute" else required in body
    for mutation in ("mutationRemovedDerivativeCommutation", "mutationChangedScalarDomain",
                     "mutationChangedBinderScope", "mutationPositiveMassOnly"):
        assert mutation in text
    print(f"statement check: ok; expression_sha256={expression_hash}; file_sha256={file_hash}")


if __name__ == "__main__":
    main()
