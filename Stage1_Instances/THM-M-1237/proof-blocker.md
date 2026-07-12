# THM-M-1237 proof execution blocker

Item: `S56-M-1237-PROOF`  
Run date: `2026-07-12`  
Base revision: `3175b20b2d6ae989a526ad94ae0ff0d20df1bc58`

## Verdict

The proof phase is **blocked** and is not self-tested as complete. No proof body was added, no
obligation was reclassified as machine-closed, and no worker self-test manifest is emitted.

The frozen root `Stage1Rev56.THMM1237.Statement` requires a quantitative supercritical
Morrey-Sobolev theorem for the dossier's concrete weak-derivative representation. The preceding
obligation tree exposes its still-open analytic premises as `RepresentativeFamily`,
`HolderEstimateFamily`, and `ValueEstimateFamily`; `root_compose` proves only that these premises
compose to the root. In particular, it is not a proof of any premise and cannot receive root proof
credit.

The pinned mathlib revision contains no declaration matching the Morrey estimate, the construction
of a Holder representative from this `W1pData`, or the required quantitative value estimate. A
fresh source scan found only textual references to Morrey in the proof of Rademacher's theorem.
The immutable external candidates recorded in `anchor-audit.md` likewise do not close the frozen
target. Consequently there is no dependency-legal proof body that can honestly be implemented or
pinned/imported in this phase without developing the missing analysis. Inventing an axiom,
retaining the open premises as theorem arguments, or proving a smoother/subcritical/special-case
statement would violate the assigned gate.

## Exact validation record

Commands were run from the worker clone. The two Lean commands were run from
`Formalizations/Lean`; their output went to `/tmp/thm-m-1237-proof`, so the pinned `.lake` tree was
not modified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard validator passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Ordered 1546-target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-1237` | 0 | Rank 175; `planned`, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, matching the recorded pin |
| `rg -n -i 'morrey\|sobolev.*holder\|holder.*sobolev\|W1p\|weakDerivative.*Holder\|Holder.*weakDerivative' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only four `Morrey` prose hits in `Analysis/Calculus/Rademacher.lean`; no candidate declaration |
| `lake env lean -R ../../Stage1_Instances/THM-M-1237 -o /tmp/thm-m-1237-proof/Statement.olean ../../Stage1_Instances/THM-M-1237/Statement.lean` | 0 | Exact frozen statement elaborated |
| `LEAN_PATH=/tmp/thm-m-1237-proof:$LEAN_PATH lake env lean ../../Stage1_Instances/THM-M-1237/ObligationTree.lean` | 0 | Conditional composition elaborated; `root_compose` reports `[propext, Classical.choice, Quot.sound]` |

## Retry condition and boundary

First failed gate: proof-body availability for `M1237-L-HOLDER`, together with its required
representative and quantitative value-estimate dependencies. Retry only after a placeholder-free
Lean 4 implementation or an immutable, toolchain-compatible external proof body closes these exact
frozen obligations and can be connected through the checked terminal composition.

The current root machine state remains `M3`. Proof, validation, release, master acceptance, and
theorem completion all remain open.
