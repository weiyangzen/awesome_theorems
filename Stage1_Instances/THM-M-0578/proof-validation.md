# THM-M-0578 proof-phase blocker

Item: `S56-M-0578-PROOF`  
Date: `2026-07-12`  
Base revision: `15c189e825a13df6978f1010a5e2e9a7ddb27692`

## Verdict

`blocked`: no eligible proof body for the exact Milnor exotic seven-sphere
target exists in the repository or pinned mathlib closure. The checked theorem
`ObligationTree.root_of_exoticWitnessPackage` is only conditional composition:
its argument already contains the smooth manifold, the homeomorphism to the
fixed unit seven-sphere, and the proof that the diffeomorphism type is empty.
No declaration constructs that package.

The first failed proof gate is terminal proof-body availability for
`M0578-C-BUNDLE`. The remaining root cut is `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF`. Closing it requires formalizing the
Milnor bundle with its dimension and orientation conventions, establishing the
homeomorphism to the standard topological sphere, computing the distinguishing
smooth invariant for both manifolds, and deriving `IsEmpty` for every
diffeomorphism.

Pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains only the source marker
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`; it leaves no
environment declaration or proof body to import. The bounded local search
found only that marker, legacy metadata strings, and this dossier. No premise,
axiom, placeholder, weaker homotopy-sphere claim, or changed sphere was added.

Because the assigned proof phase is not self-tested complete, this attempt
deliberately does not create `.stage1-worker-selftest.json`.

## Narrow validation evidence

All commands ran in the worker clone. The existing
`Formalizations/Lean/.lake` entry reuses the canonical pinned artifacts and was
not modified. No update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passes: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622, lifecycle `planned`, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges pass; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| temporary owned `Statement.olean`, then `LEAN_PATH=... lake env lean ObligationTree.lean`, then removal | 0 | Exact statement and conditional composition elaborate; `#print axioms` reports only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n -i 'MilnorExoticSphereTarget\|exists_homeomorph_isEmpty_diffeomorph_sphere_seven\|Milnor.*sphere\|exotic.*7.?sphere\|exotic.*seven' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Hits are confined to this dossier, three legacy metadata files, and mathlib's `proof_wanted` marker; no terminal body was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-0578/proof-blocker.json` | 0 | Blocker record is valid JSON. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx' Stage1_Instances/THM-M-0578 --glob '*.lean'` | 1 | No prohibited Lean token; exit 1 means no match. |
| `git diff --check -- Stage1_Instances/THM-M-0578` | 0 | No whitespace errors. |

The toolchain is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`. Machine status remains M4,
theorem completion remains false, and master acceptance is still required.
