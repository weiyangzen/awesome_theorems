# THM-M-0554 proof-phase recheck at `11a448c9` (slot 19)

Item: `S56-M-0554-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `11a448c97289d30fe7c8c05dbac5a283a9d00896`

Base tree: `a79f60552d328e98302026909ec6676cb6cd6ea2`

## Verdict

`blocked`. No source-faithful Atiyah-Hirzebruch spectral-sequence proof body is
present in the repository or pinned dependency closure, and none was added.
The exact root remains open at `M4`; this attempt adds no proof receipt,
composition certificate, debt-vector change, or state transition.

The first failed gate is exact-statement fidelity. The intended theorem assumes
a reduced generalized cohomology theory and a genuine finite-CW structure. The
frozen Lean interface does not encode reducedness. Its `pointIsPoint`,
`exactnessAxiom`, `wedgeAxiomOrRepresentability`, `finiteCW`, `exhaustive`, and
`cellAttachments` fields store propositions rather than proofs. The output
chooses the propositions `coefficientConvention`, `strongConvergence`, and
`naturalityInSpace`; `filtrationIsInducedBy` is the tautology
`K.skeleton = K.skeleton`. Therefore kernel inhabitance of the literal target
would not establish the canonical mathematical claim. A previously checked
zero-object/`True` inhabitant is deliberately rejected as a fake result and is
not retained or credited.

The dependency authority is also unresolved. The blueprint records
`S56-M-0554-OBLIGATION_TREE` only as provisional `[_]`. The local intake
authority still has a null canonical module, declaration, expression hash, and
environment fingerprint; `task-dag.json` is unfrozen and marks proof blocked by
predecessors. A proof-only worker cannot replace these predecessor artifacts.

The frozen registry remains structurally valid but has no closed obligations
or composition certificates. Its immediate root cut is:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

The pinned packages contain generic spectral-sequence, CW-complex, and
singular-homology substrate only. The current pinned-package term scan found no
AHSS/generalized-cohomology/exact-couple/strong-convergence proof body.
Mathlib's spectral-object source still describes the intended
`spectralSequence`, `homologyData`, and `spectralSequenceHomologyData`
constructions as `TODO`.

## Validation

All Lean validation reused the automation-provided symlink to the canonical
pinned Lake artifacts. No update, build, dependency clone/fetch, network action,
or `.lake` mutation was performed. The generated Lean object was written to a
temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains open at `M4` with no composition certificate. |
| Isolated pinned `lean --trust=0 -t0` recipe below | 0 | `Statement.lean` elaborated with Lean 4.29.0; the temporary `Statement.olean` was removed. The command emitted no diagnostics. |
| `rg -n -i --glob '*.lean' 'Atiyah[-_ ]?Hirzebruch|AtiyahHirzebruch|\bAHSS\b|generalized[ _-]*(co)?homology|exact[ _-]*couple|strong[ _-]*convergence' Formalizations/Lean/.lake/packages` | 1 | Expected no-match result: no pinned terminal proof candidate. |
| The same search outside this dossier and `.lake` | 0 | Target-specific hits are the legacy `S1_M_106.lean` interfaces and explicit debt gates, not a terminal proof body. |
| `rg -n --pcre2 '^\s*(?:sorry|admit|axiom)(?:\s|$)|\bsorryAx\b|^\s*unsafe(?:\s|$)' Stage1_Instances/THM-M-0554 --glob '*.lean'` | 1 | Expected no-match result: no prohibited declaration token occurs in owned Lean sources. |
| `lake env lean --version`; `lake --version`; pinned mathlib revision/tree checks | 0 | Lean `4.29.0` commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`. |
| `sha256sum` on the pinned mathlib spectral-object source plus its `TODO` scan | 0 | Source SHA-256 `2ce62b9d...740aa`; the three intended generic constructors remain documented as `TODO`. |

The exact Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-proof-recheck-11a448c9.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Statement.olean" Statement.lean
```

## Retry Condition

First publish and master-accept a source-faithful corrected statement, reconcile
the instance/task/statement authorities, and issue obligation-registry version
2. Then implement and compose all four root-cut packages without placeholders.
An alternative is an immutable compatible Lean 4 AHSS proof whose exact type,
terminal body, provenance, trust closure, and child composition all validate.

This is current-base blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close any obligation, complete the audit or theorem, or
authorize master acceptance. Because the assigned proof phase is not genuinely
self-tested complete, `.stage1-worker-selftest.json` remains absent.
