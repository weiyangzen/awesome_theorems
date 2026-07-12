# THM-M-0526 proof-phase validation

Item: `S56-M-0526-PROOF`  
Base revision: `b17067c5d92786b270337cbdd3bfaf74df7773f9`

## Result

Blocked, with a real partial proof. `Proof.lean` closes the frozen
`SVK-MAP-FUNCTORIALITY` leaf and its `SVK-SQUARE` parent by kernel-checked
reduction on path-homotopy representatives. It also supplies the exact
cover-parametric square package expected by `compose_root`.

The assigned proof phase is not complete. Pinned mathlib contains no
Seifert-van Kampen theorem, and the frozen obligation tree still requires the
eight geometric and algebraic leaves below. In particular, neither a lift
existence package nor a lift uniqueness package can truthfully be supplied by
the available library. No `SeifertVanKampenTarget` proof is declared and no
worker self-test receipt is emitted.

## Remaining root cut set

- `SVK-LEBESGUE-NUMBER`
- `SVK-CHANGE-BASEPATH`
- `SVK-WORD-DEFINITION`
- `SVK-REFINEMENT-INVARIANCE`
- `SVK-HOMOTOPY-INVARIANCE`
- `SVK-LIFT-HOM`
- `SVK-GENERATION`
- `SVK-AGREEMENT-ON-WORDS`

## Validation evidence

Commands were run from `Formalizations/Lean` on 2026-07-12. The temporary
output directory avoids mutating the shared pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `rm -rf /tmp/thm-m-0526-proof-olean && mkdir -p /tmp/thm-m-0526-proof-olean/Stage1_Instances/THM-M-0526` | 0 | fresh narrow output directory |
| `lake env lean -R ../.. -o /tmp/thm-m-0526-proof-olean/Stage1_Instances/THM-M-0526/Statement.olean ../../Stage1_Instances/THM-M-0526/Statement.lean` | 0 | exact frozen statement elaborated; only the pre-existing unused-section-variable warning |
| `LEAN_PATH=/tmp/thm-m-0526-proof-olean lake env lean -R ../.. -o /tmp/thm-m-0526-proof-olean/Stage1_Instances/THM-M-0526/ObligationTree.olean ../../Stage1_Instances/THM-M-0526/ObligationTree.lean` | 0 | typed interfaces and composition certificates elaborated |
| `LEAN_PATH=/tmp/thm-m-0526-proof-olean lake env lean ../../Stage1_Instances/THM-M-0526/Proof.lean` | 0 | both new theorem bodies elaborated; axiom reports contain `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` |
| `rg -n '\\bsorry\\b|sorryAx|\\baxiom\\b|admit|placeholder' ../../Stage1_Instances/THM-M-0526/Proof.lean` | 1 | expected negative search; no forbidden proof device |
| `git diff --check -- Stage1_Instances/THM-M-0526` (repository root) | 0 | no whitespace errors |

First failed gate: all required proof bodies are not implemented. The exact
blocker is the absence of formal loop-subdivision, choice-independence,
homotopy-grid, and generation developments needed to construct the two open
packages. This is proof debt, not a missing dependency that may be fetched.
