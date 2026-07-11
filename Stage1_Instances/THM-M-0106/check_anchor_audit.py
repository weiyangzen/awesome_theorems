#!/usr/bin/env python3
"""Check the anchor module and its definitional match to the frozen target."""

from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN = ROOT / "Formalizations" / "Lean"

statement = (HERE / "Statement.lean").read_text()
statement = statement[: statement.rfind("set_option pp.explicit true in")]
anchor = (HERE / "AnchorAudit.lean").read_text()
anchor = "\n".join(line for line in anchor.splitlines() if not line.startswith("import "))
combined = "import Mathlib.RingTheory.NoetherNormalization\n" + statement + "\n" + anchor + """

namespace Stage1Instances.THM_M_0106
universe u
example : NoetherNormalizationTarget.{u} ↔ FrozenTargetAuditExpression.{u} := Iff.rfl
end Stage1Instances.THM_M_0106
"""

with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=HERE, delete=False) as f:
    f.write(combined)
    temporary = Path(f.name)
try:
    result = subprocess.run(
        ["lake", "env", "lean", str(temporary)], cwd=LEAN, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
finally:
    temporary.unlink()
print(result.stdout, end="")
if result.returncode:
    raise SystemExit(result.returncode)
print("anchor_audit: ok; audit expression definitionally matches frozen statement")
