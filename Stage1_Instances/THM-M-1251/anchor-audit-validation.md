# Anchor-audit validation record

Item: `S56-M-1251-ANCHOR_AUDIT`  
Base revision: `f58cf2c65a6c9fda32651887cd15949b3a85108c`

## Result

Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact anchor selected
by the frozen statement. `TemperedDistribution E F` is an abbreviation for continuous linear maps
from complex Schwartz maps to `F`, with `PointwiseConvergenceCLM` topology. The local theorem
`AnchorAudit.exactMathlibAnchor` rechecks the entire quantified canonical target by `rfl`. Lean's
axiom report contains only the declared standard mathlib foundations `propext`,
`Classical.choice`, and `Quot.sound`, with no placeholder or target-specific assumption. This
candidate is therefore classified `M0-W` at the formal-anchor node.

That result is intentionally topology-sensitive. The mathlib source explicitly says it uses
pointwise convergence rather than a strong topology. A repository-wide pinned-source search found
no terminal Schwartz strong-dual equivalence. The immutable
`mrdouglasny/gaussian-field@d63a28568a75d99f6cb27af1f888a49a69855a66` archive supplies a real
`WeakDual` configuration abbreviation and Schwartz nuclearity infrastructure, but neither matches
nor strengthens the canonical complex pointwise-dual target. No external dependency is warranted.

The external search was bounded by endpoint availability and is not a claim that no other Lean 4
project exists. More importantly, this audit does not claim theorem completion: primary-source H0,
the obligation tree, downstream acceptance, hermetic validation, readability review, and release
remain open.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Existing canonical `.lake` artifacts were reused;
no dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1251` | 0 | rank 171, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1251/Statement.lean` | 0 | Frozen target and transport re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1251/AnchorAudit.lean` | 0 | Five declarations checked; exact wrapper elaborated; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-1251/check_anchor_audit.py` | 0 | Audit boundary, exact anchor, manifest revision, installed HEAD, and source form agreed |
| `rg -n -i 'Schwartz.*dual|dual.*Schwartz|StrongDual.*Schwartz|Schwartz.*StrongDual|TemperedDistribution' Formalizations/Lean/.lake/packages/mathlib Formalizations/Lean/.lake/packages/flt-regular --glob '*.lean'` | 0 | Exact pointwise definition and related uses; no terminal Schwartz strong-dual equivalence |
| immutable `gaussian-field` archive inspection plus `sha256sum` | 0 | Commit HEAD confirmed; near-miss source hashes recorded in `anchor-audit.json`; toolchain v4.30.0 |
| `git diff --check -- Stage1_Instances/THM-M-1251` | 0 | No whitespace errors |

## Status boundary

The exact formal anchor has no repo-local integration debt. The stronger strong-dual interpretation
remains `M4`, but it is excluded from the frozen statement. Master acceptance and every later
rev-5.6 node remain required before any theorem-completion claim.
