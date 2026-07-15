# THM-M-1146 proof recheck at `a60b47b4`

Item: `S56-M-1146-PROOF`

Date: `2026-07-15`

Base revision: `a60b47b4551b044fd5fad26599908ccef4000024`

## Verdict

`blocked`. The exact frozen Schwarz-reflection target remains open at the real-axis harmonic-gluing
obligation `M1146-L-GLUING`. This attempt nevertheless adds four placeholder-free proof bodies in
`ProofNext.lean`: continuity of the odd reflection on each closed half-plane portion of the exact
domain, continuity on the full symmetric domain, and checked pointwise composition of the strict
upper, strict lower, and assumed axis branches into `ReflectedHarmonicPackage`.

The new continuity proof uses the frozen setwise continuity and zero boundary trace directly. It
does not assume differentiability on the axis and earns no harmonic-gluing credit. The conditional
branch composer keeps the axis theorem as an explicit premise and therefore is not a root proof.
No `.stage1-worker-selftest.json` was written: the assigned proof phase is incomplete, the root
remains `M3`, and theorem completion is false.

## Remaining Blocker

Pinned mathlib provides real Laplacian calculus, off-axis conjugation preservation, Poincare
primitives on convex sets, local holomorphic representatives on full harmonic balls, piecewise
continuity, and Morera interfaces. It still supplies no theorem deriving `HarmonicAt` on the axis
from one-sided harmonicity, continuity, and zero trace. A primitive/reflection route requires new
boundary-extension and rectangle-cancellation theorems. A disk-local Poisson/maximum-principle
route can now be described, but the available target-local Poisson construction is ATLAS-derived
under a CC BY-NC/no-training rider and has an unresolved provenance boundary; it cannot be silently
imported as accepted proof credit. A clean-room replacement would be substantial.

## Validation

All Lean checks reused the automation-provided pinned `.lake` symlink read-only. No Lake update,
Lake build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | Rank 351; planned; L0/rework-required; theorem incomplete |
| `timeout 900 env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1146/check_statement.py` | 0 | Exact expression hash `14336b88...deef53d`; all five mutations killed |
| `python3 Stage1_Instances/THM-M-1146/check_obligation_tree.py` | 0 | 18 obligations and 40 typed edges passed; root open M3 |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `ProofNext.lean` | 0 | All four modules elaborated; every printed proof body used only `propext`, `Classical.choice`, and `Quot.sound` |
| prohibited-construct scan over owned Lean files | 1 | Expected no-match exit; no placeholder, bodyless axiom, unsafe/oracle, or native shortcut found |
| `python3 -m json.tool Stage1_Instances/THM-M-1146/proof-recheck-2026-07-15-head-a60b47b4.json` | 0 | Structured blocker record is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1146` plus added-file whitespace checks | 0 / expected added-file status | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent |

Environment: Lean `4.29.0` commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Reopen Condition

Resume after a placeholder-free implementation of axis harmonic gluing and its boundary/locality
prerequisites, or an immutable compatible terminal proof whose exact type, provenance, license,
trust closure, and composition can all be checked without dependency mutation. This packet is
blocker evidence, not a proof receipt or a request for scheduler promotion.
