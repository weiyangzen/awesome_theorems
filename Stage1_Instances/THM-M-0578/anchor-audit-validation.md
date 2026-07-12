# Anchor-audit validation record

Item: `S56-M-0578-ANCHOR_AUDIT`  
Base revision: `f247e0d21ae7b4235e6bc7f78c1fad05b754ff16`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact source-level candidate
`exists_homeomorph_isEmpty_diffeomorph_sphere_seven` in
`Mathlib/Geometry/Manifold/PoincareConjecture.lean`. It is introduced with
`proof_wanted`, not `theorem`. Pinned Batteries checks that signature using a
temporary helper axiom under `withoutModifyingEnv` and removes the declaration.
A Lean environment probe confirms that the name is absent after import. It is
statement discovery, not a proof body.

Bounded Sourcegraph and GitHub repository searches returned zero results, and
the complete 1,204-path tree of `google-deepmind/formal-conjectures` at
immutable revision `b2e608fc52d765510915a244bb69b1a2741acc3c` contained no
matching path. GitHub code search returned HTTP 401, so no negative result is
claimed for that lane. These searches are discovery evidence, not proof of
global absence.

The exact root remains `M4` with `formalization_debt`. There is no external
proof body to integrate. Neither theorem proof nor completion is claimed, and
master acceptance remains outstanding.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | rank 622, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/batteries rev-parse HEAD` | 0 | `756e3321fd3b02a85ffda19fef789916223e578c` |
| four GitHub REST repository searches in `anchor-audit.json` | 0 | each returned `total_count=0`, `incomplete_results=false` |
| four Sourcegraph archived/fork-inclusive Lean queries in `anchor-audit.json` | 0 | each returned `done=true`, `matchCount=0` |
| GitHub REST code search for `exotic sphere language:Lean` | HTTP 401 | authentication unavailable; response SHA-256 `b7dbd1...e29e`; no negative result claimed |
| GitHub recursive tree for `google-deepmind/formal-conjectures` at `b2e608...acc3c` | 0 | `truncated=false`, 1,204 paths, no matching path; SHA-256 `76fa3f...efc61` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0578/AnchorAudit.lean` | 0 | marker shape and sphere APIs elaborated; retained-name absence assertion passed |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | ledger, pins, source hash, exact marker, and discard semantics passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0578/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0578 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, build, dependency clone/fetch, or `.lake` mutation was
performed. The existing pinned artifacts were used directly.
