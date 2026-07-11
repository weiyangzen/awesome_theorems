# Statement gate blocker

Item: `S56-M-0123-STATEMENT`  
Theorem: `THM-M-0123`  
Verdict: blocked; no exact canonical Lean target is claimed.

## Exact blocker

The frozen claim requires the native mathematical hypothesis `2 <= genus X`
for a smooth, proper, geometrically connected relative-dimension-one scheme
over a number field. At pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, no scheme-curve genus invariant
or equivalent packaged arithmetic-genus predicate is available. A repository
search for `genus` in all pinned Lean package sources returned no matches.

The legacy `CurvePredicateSlots.genusAtLeastTwo : Prop` is not acceptable: a
caller may instantiate it with an arbitrary proposition unrelated to the
curve. Reusing it, adding a `genus : Nat` field without a checked definition,
or omitting the genus hypothesis would broaden or substitute the theorem.
Consequently an exact expression fingerprint and the required genus-boundary
mutation fixtures cannot truthfully be produced in this node.

`StatementInfrastructure.lean` elaborates only the noncontroversial native API
surface: the number-field base scheme, rational points as sections, smooth
relative dimension one, properness, and geometric connectedness. It contains
no canonical theorem declaration, proof, axiom, placeholder, or genus proxy.

## Environment fingerprint

- Repository base revision: `cf2b907b1d10a3b5c923fc84e10b495a48530690`.
- Lean toolchain: `leanprover/lean4:v4.29.0` (`Lean 4.29.0`).
- mathlib Lake pin and checked dependency revision:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Validation date: 2026-07-12.

## Validation evidence

Commands are run from `Formalizations/Lean` unless stated otherwise. Exact
results are appended after the narrow elaboration check. No dependency update,
fetch, clone, or build is used.

| Command | Result |
|---|---|
| `lake env lean ../../Stage1_Instances/THM-M-0123/StatementInfrastructure.lean` | exit 0; no output; infrastructure elaborated |
| `lake env lean --version` | exit 0; `Lean 4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum lake-manifest.json` | exit 0; `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i '\\bgenus\\b' .lake/packages --glob '*.lean'` | exit 1; no matches (the expected negative search result) |
| `git diff --check -- ../../Stage1_Instances/THM-M-0123` | exit 0; no output |

First failed gate: exact native encoding of the genus-at-least-two hypothesis.
Remaining statement cut set: implement or pin an audited scheme-curve genus
definition, prove that it denotes the source notion, then elaborate the full
target and run the required non-equivalent mutation tests. Until then machine
status remains `M4`, and neither statement acceptance nor theorem completion is
claimed.
