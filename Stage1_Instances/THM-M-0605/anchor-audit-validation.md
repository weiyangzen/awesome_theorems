# Anchor-audit validation record

Item: `S56-M-0605-ANCHOR_AUDIT`  
Base revision: `c8bb1d8f046a4b2816eb059edc201b88d2063f42`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact source-level candidate
`exists_homeomorph_isEmpty_diffeomorph_sphere_seven` in
`Mathlib/Geometry/Manifold/PoincareConjecture.lean:64-68`. The checked theorem
in `AnchorAudit.lean` re-elaborates the canonical definitions verbatim and
transports between the expanded binder form and packaged target in both
directions.

The candidate is introduced with `proof_wanted`, not `theorem`. Pinned
Batteries temporarily elaborates such a signature through a helper axiom
inside `withoutModifyingEnv`, then discards it. A Lean environment probe
confirms that the name is absent after import. It is therefore an exact
statement anchor, not a proof body.

Bounded external searches found no proof-bearing Lean 4 candidate. Their
negative results are discovery evidence, not a global absence proof. The root
remains `M4` with `formalization_debt`; theorem proof and theorem completion
are both false, and master acceptance remains outstanding.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | rank 643, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/batteries rev-parse HEAD` | 0 | `756e3321fd3b02a85ffda19fef789916223e578c` |
| Sourcegraph queries listed in `anchor-audit.json` | 0 | exact/phrase matches led only to mathlib's source marker; no retained proof candidate found |
| immutable `google-deepmind/formal-conjectures` tree search recorded in `anchor-audit.json` | 0 | complete 1,204-path response had no matching path |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0605/AnchorAudit.lean` | 0 | checked exact bidirectional transport and retained-name absence |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | ledger, manifest pins, source hashes, exact marker, and discard semantics passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0605/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0605 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, build, dependency clone/fetch, or `.lake` mutation was
performed. Existing pinned artifacts were used directly.
