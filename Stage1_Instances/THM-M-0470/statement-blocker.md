# Exact-statement gate: blocked

Item: `S56-M-0470-STATEMENT`  
Theorem: `THM-M-0470`  
Base revision: `5efc9accb7b7d20411403a280fb058cb19aea566`

## Decision

An exact Lean 4 target cannot yet be truthfully elaborated from the frozen evidence. The intake
identifies Ullmo's 1998 paper as the likely historical theorem, but explicitly leaves its exact
source notation, premise mapping, algebraic-geometric encoding, and height normalization open. The
repository contains only the metadata gloss "proof of the Bogomolov conjecture" and a DOI discovery
link; it contains no inspected immutable copy, exact theorem/page statement, or errata disposition.
The upstream `INTAKE` node is also only worker-self-tested (`[_]`), not master-accepted.

The proposed prose root still leaves choices that change the proposition:

- whether the curve and Abel-Jacobi embedding are defined over the number field or only after
  base change to its algebraic closure, and what point or degree-one divisor supplies the embedding;
- whether the root quantifies over all such embeddings/polarizations or fixes one, and whether its
  conclusion is invariant under those choices;
- the precise smoothness, projectivity, geometric connectedness/integrality, and genus hypotheses;
- the symmetric theta line bundle/divisor and normalization of the Neron-Tate height;
- whether the height inequality is strict or non-strict and whether the small-point conclusion is
  finiteness, non-Zariski-density, or positivity of an essential minimum;
- the exact field of algebraic points and the transports among the finite-set, non-density, and
  essential-minimum forms.

Choosing answers at this phase would invent missing mathematics. In particular, the intake phrase
"embed using a degree-one divisor" is not sufficient to fix the field of definition or existence
assumption. Replacing the missing curve, Jacobian, polarization, and canonical-height semantics by
arbitrary Lean types, functions, and predicates would elaborate only an assumed abstract proxy, not
Ullmo's theorem. No such proxy, axiom, bodyless declaration, or weakened special case was added.

Pinned mathlib at the recorded revision has general schemes, abelian group schemes, number fields,
ordinary height infrastructure, and elliptic-curve Jacobian-coordinate APIs. The scoped search found
no general Jacobian-of-a-curve construction, Abel-Jacobi embedding, Neron-Tate height on that
Jacobian, or Ullmo/Bogomolov statement. Thus no minimal import set for the exact root can presently
be demonstrated. Machine status remains `M4`; statement acceptance and theorem completion are
false.

## Validation evidence

Validation date: 2026-07-12 (Asia/Shanghai). Commands ran from this worker clone, except commands
explicitly prefixed by `cd Formalizations/Lean`. Existing `.lake` artifacts were read only; no
update, build, clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0470` | 0 | Rank 316; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8acc...f1d2` and `321626c8...d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Ullmo|Positivite et discretion|Bogomolov conjecture|Neron.?Tate|canonical height|Jacobian' --glob '!Stage1_Instances/THM-M-0470/**' .` | 0 | Found metadata, related theorem dossiers, and elliptic-curve/interface artifacts only; no source-frozen target for `THM-M-0470` |
| `rg -n -i 'Neron.?Tate|canonicalHeight|CanonicalHeight|Ullmo|Bogomolov|Abel.Jacobi|Picard.*curve|curve.*Picard|genus' Formalizations/Lean/.lake/packages/mathlib/Mathlib/AlgebraicGeometry Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/Height` | 1 | No matching general curve/Jacobian/canonical-height theorem API (`rg` exit 1 means no match) |

There is no honest `lake env lean <target>.lean` check: the exact expression required by the node is
not determined and the necessary semantic API is absent. Parser-only validation of an abstract
stand-in would not meet the exact-statement gate.

## Retry condition

First master-accept an intake backed by an immutable inspection of Ullmo's theorem statement. That
record must freeze the source theorem/page, corrections, every field-of-definition and geometric
hypothesis, the Abel-Jacobi and theta choices, height normalization, inequality convention, and
small-point conclusion. It must either select one form or provide checked transports among the
finite, non-density, and essential-minimum forms. A later statement execution can then implement or
pin the required Lean interfaces, elaborate the exact expression with minimized imports,
fingerprint it, and mutation-test the choices above.

The assigned deliverable is blocked rather than self-tested to completion, so no
`.stage1-worker-selftest.json` is emitted.
