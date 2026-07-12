# Proof-phase validation record

Item: `S56-M-0312-PROOF`  
Base revision: `3d8dd27e4ff1200a2d9c8daaa9cae8072eca6241`

## Implemented closure

`Proof.lean` implements both frozen proof interfaces and composes them through
`root_of_equicontinuity_packages` to obtain the exact `UniformBoundednessTarget`. The first body
specializes pinned mathlib's `WithSeminorms.banach_steinhaus` to the norm seminorm and discharges
its bounded-range premise from `PointwiseBounded`. The second selects implication 5 to 2 from
`NormedSpace.equicontinuous_TFAE`. A separate exact-type wrapper checks the pinned public
`banach_steinhaus` declaration without substituting a narrower theorem.

Lean elaborated all four declarations and reported exactly `propext`, `Classical.choice`, and
`Quot.sound` for each. No `sorry`, `admit`, declared axiom, `sorryAx`, or unsafe declaration occurs
in the proof module. This is proof-phase evidence only: master acceptance, full transitive
provenance/trust validation, human-source closure, readable reconstruction, hermetic replay, and
independent release validation remain downstream gates. It therefore makes no theorem-completion
claim.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. The existing pinned `.lake` environment was used;
no update, build, fetch, clone, or dependency mutation ran. The two intermediate `.olean` files
were emitted only to resolve sibling imports and deleted immediately after the scoped check.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0312` | 0 | rank 814, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean -R ../.. -o ../../Stage1_Instances/THM-M-0312/Statement.olean ../../Stage1_Instances/THM-M-0312/Statement.lean` | 0 | exact statement dependency elaborated |
| `cd Formalizations/Lean && LEAN_PATH=../../Stage1_Instances/THM-M-0312 lake env lean -R ../.. -o ../../Stage1_Instances/THM-M-0312/ObligationTree.olean ../../Stage1_Instances/THM-M-0312/ObligationTree.lean` | 0 | frozen composition dependency elaborated |
| `cd Formalizations/Lean && LEAN_PATH=../../Stage1_Instances/THM-M-0312 lake env lean -R ../.. ../../Stage1_Instances/THM-M-0312/Proof.lean` | 0 | both interface bodies, composed exact root, and pinned wrapper elaborated; four axiom reports each contained only `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0312/check_obligation_tree.py` | 0 | 15 obligations, 28 typed edges, frozen denominator `78cf9737...0548ff` passed |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b\|sorryAx\|unsafe' Stage1_Instances/THM-M-0312/Proof.lean` | 1 | expected no-match result |
| `sha256sum Stage1_Instances/THM-M-0312/Proof.lean` | 0 | `11a309b1f5c76210304376a88919e319253953587a5c0f64530ae99842395350` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git diff --check -- Stage1_Instances/THM-M-0312 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The assigned proof source is self-tested and suitable for provisional `[_]` integration review.
The authoritative lifecycle remains `planned`, the accepted-state set remains empty, and
`audit_complete=false` / `theorem_complete=false` until later nodes receive their own receipts.
