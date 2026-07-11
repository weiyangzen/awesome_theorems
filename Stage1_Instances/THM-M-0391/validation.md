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

## Validation-phase execution

Item: `S56-M-0391-VALIDATION`

Base revision: `66630bedafa43a769b94226b7431188dea47edf1`

Validation timestamp: `2026-07-11T19:22:28Z`

The validation phase reran the exact statement and the only proof-phase closure,
`M0391-B-EE`. `Validation.lean` reconstructs that elementary branch independently:
it casts the equation to integers and factors the difference of squares, rather
than reusing the proof phase's successor-square argument. `check_validation.py`
independently checks the frozen hashes, all 15 registry/node identities, proof-graph
reachability and acyclicity, the receipt's one-obligation closure boundary, the
open-root flag, the toolchain/dependency pins, placeholder policy, elaboration,
and axiom reports.

All commands ran from the repository root unless a working directory is shown.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0391
  exit 0: execution rank 5; planned; theorem_complete=false

(cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0391/Statement.lean)
  exit 0 with no output

(cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0391/Proof.lean)
  exit 0: evenEvenImpossible depends on [propext, Quot.sound]

(cd Formalizations/Lean && lake env lean \
  ../../Stage1_Instances/THM-M-0391/Validation.lean)
  exit 0: independentEvenEvenImpossible has the exact branch type and depends
  on [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0391/check_validation.py
  exit 0: exact partial proof re-elaborated; independent M0391-B-EE probe
  passed; root remains open

python3 -m json.tool \
  Stage1_Instances/THM-M-0391/validation-receipt.json
  exit 0

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0391/{Statement,Proof,Validation}.lean
  exit 1 with empty output: pass, no prohibited local declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0391
  exit 0 with no output
```

The structured recipes are recorded in `validation-receipt.json`. They used the
existing pinned Lean 4.29.0 toolchain and the canonical read-only `.lake` reuse;
there was no update, build, fetch, clone, or network use.

This is truthful validation of one partial proof obligation, not successful
full-root validation. The first node gate failure is the open proof dependency:
fourteen frozen root-relevant obligations and root composition remain unclosed.
Consequently there is no root axiom/provenance closure. The worker also cannot
supply an empty-cache cold build, offline archive restoration, distinct signed
runner, independent release verifier, SBOM/license bundle, H0/R0 reviews, or a
deterministic release bundle. `audit_complete=false` and
`theorem_complete=false`; the root vector remains `[H1, M4, R4]`.
