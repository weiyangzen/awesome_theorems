# Intake validation

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

The intake used these repository-root commands:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0391
  exit 0: rank 5, planned, L0, rework_required=true, theorem_complete=false
python3 -m json.tool Stage1_Instances/THM-M-0391/instance.json
  exit 0
```

These checks validate intake structure and JSON syntax only. They do not elaborate Lean, validate a
proof, establish H0, or satisfy any statement/audit/proof/release node.

## Statement validation

Base revision: `7303634b5bee63e4735691cc42a5633b2bbbecbe`.

The statement phase used the repository-pinned toolchain directly, avoiding a Lake dependency
fetch because the exact target needs only Lean core `Init`:

```text
elan run leanprover/lean4:v4.29.0 lean --version
  exit 0: Lean 4.29.0; commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
elan run leanprover/lean4:v4.29.0 lean Stage1_Instances/THM-M-0391/Statement.lean
  exit 0; exact target, iff transport, and two mutation counterexamples elaborated
sha256sum Stage1_Instances/THM-M-0391/Statement.lean Formalizations/Lean/lean-toolchain
  exit 0: a8665695641932dcea97bab10143a73155e45c685fff03cfec6a19689b3f936f
          651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2
```

`MihailescuTarget` has the exact ordered `Nat` binders, five intake hypotheses, and exceptional
tuple conclusion. `mihailescuTarget_iff_legacyStatementShape` checks the alternate conjunction
encoding in both directions. The two mutation theorems show that changing either exponent bound
from `1 <` to `0 <` admits a concrete non-exceptional solution. These results satisfy only the
statement node; they provide no universal proof body and do not change H/M/R debt or completion.
