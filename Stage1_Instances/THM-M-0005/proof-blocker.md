# THM-M-0005 proof-phase blocker

Item: `S56-M-0005-PROOF`  
Base revision: `29490c1ef89c2a6c9eb8dcfc4888b8761f710422`  
Attempt date: 2026-07-12 (Asia/Shanghai)

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof body was added, no
obligation was marked closed, and no worker self-test manifest was written.

The frozen root is the existence, for every commutative principal ideal domain `R`, of the
ten-field `NaturalKunnethSequence R` in `KunnethStatement.lean`. The existing
`ObligationTree.lean` only proves conditional composition: `assemble_sequence` accepts all ten
fields as arguments, and `root_compose` accepts an already constructed sequence family. Neither
declaration supplies a root-critical mathematical field.

The first failed proof cut is the chain-level product comparison:

- `M0005-CHAIN-FREE`: projectivity/freeness for the singular-chain model is open.
- `M0005-EZ-MAP`, `M0005-EZ-EQUIV`, and `M0005-EZ-NAT`: the Eilenberg-Zilber comparison,
  equivalence, and naturality are open.
- `M0005-ALG-MAPS`, `M0005-ALG-ZERO`, `M0005-ALG-EXACT`, and `M0005-ALG-NAT`: the algebraic
  Kunneth maps, complex condition, exactness, and naturality are open.

These leaves feed the direct-sum transport and the target's tensor/Tor component equations. Thus
none can be bypassed by the field constructor without assuming the theorem being proved.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides singular homology,
`Tor`, and short-exact-sequence infrastructure, but the accepted anchor audit found no Kunneth or
Eilenberg-Zilber closure. The only located external Lean candidate,
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`, has placeholders in
every root-critical path and does not exactly inhabit the frozen target. Importing or wrapping it
would therefore not be a proof.

## Validation evidence

Commands ran in the worker clone. The canonical pinned `.lake` link was reused; no update, build,
clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets with ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Confirmed rank 100, `planned`, `rework_required`, and `theorem_complete: false`. |
| `rg -n '\\b(sorry\|admit\|axiom)\\b' Stage1_Instances/THM-M-0005 --glob '*.lean'` | 1 | No prohibited proof token occurs in the owned Lean sources. Exit 1 means no match. |
| temporary copy followed by `cd Formalizations/Lean && lake env lean -R /tmp/thm-m-0005-proof-olean -o /tmp/thm-m-0005-proof-olean/KunnethStatement.olean /tmp/thm-m-0005-proof-olean/KunnethStatement.lean` | 0 | The exact statement elaborated; four unused-variable warnings only. |
| `cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-0005-proof-olean lake env lean ../../Stage1_Instances/THM-M-0005/ObligationTree.lean` | 0 | Conditional composition elaborated; its printed profile contains only `propext`, `Classical.choice`, and `Quot.sound`. This does not close a mathematical leaf. |

The pre-existing untracked `Formalizations/Lean/.lake` link makes this nonrelease evidence.

## Required unblock condition

Provide local placeholder-free Lean bodies, or an immutable placeholder-free dependency, for the
chain projectivity, Eilenberg-Zilber, and algebraic Kunneth branches at the frozen types. Then prove
the direct-sum transports, tensor/Tor component equations, two-variable naturality, and exact root
composition. Until those bodies pass exact-type and trust checks, the root remains open at
`[H1, M3, R3]`, and this proof item cannot truthfully receive `[_]` or theorem-completion credit.
