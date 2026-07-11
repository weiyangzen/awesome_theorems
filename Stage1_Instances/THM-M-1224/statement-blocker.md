# S56-M-1224-STATEMENT blocker

Item: `S56-M-1224-STATEMENT`  
Theorem: `THM-M-1224` (Grillakis regularity theorem)  
Base revision: `f7e53d5271124f8d66209dd8f2ef42b15d5c6553`

## Verdict

The rev-5.6 exact-statement gate is blocked. No canonical Lean target, expression fingerprint,
checked alternate transport, or statement receipt is claimed, and this worker does not claim the
statement node as self-tested.

The repository source record supplies only the label `Grillakis定理`, the year 1990, and the gloss
`NLW的正则性`. The intake conservatively selects the three-dimensional defocusing energy-critical
quintic equation as the intended family, but deliberately leaves statement-changing source facts
open. In particular, no inspected immutable source copy and theorem/page locator fixes:

- whether the 1990 or 1992 paper supplies the canonical result and how the two results differ;
- the exact initial-data class, including smoothness order, compact support, decay, and finite-energy
  conditions;
- the source's nonlinearity assumptions and whether the pure quintic equation is itself the stated
  theorem or a specialization;
- the precise solution notion, global time domain, uniqueness claim, and regularity conclusion;
- the derivative, sign, energy, and boundary-at-infinity conventions; or
- exceptional and zero-data cases and any published errata.

These choices change ordered binders, hypotheses, and conclusion. Selecting them from the short
metadata, bibliography, or remembered modern formulations would invent missing mathematics and
could substitute a later specialization for Grillakis' exact theorem. Consequently the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations also cannot be
meaningfully certified.

## Lean boundary checked

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_155.lean` elaborates in the pinned environment, but
it is not an exact target. Its `StatementShape` quantifies over an abstract `NLWRegularityData`; the
caller supplies proposition fields for the NLW equation, initial-data compatibility, nonlinearity,
energy estimate, and compactness package. Its conclusion is local pointwise Holder regularity on an
arbitrary cylinder, rather than the intake's concrete global smooth solution claim on
`Real x Real^3`. Crediting that package would be a broadened/substituted theorem. The file itself
labels the terminal theorem incomplete.

Pinned mathlib contains the generic analysis declarations used by that module, but a scoped source
search found no `Grillakis` or critical nonlinear-wave theorem. This is negative boundary evidence,
not the downstream anchor audit.

No `Statement.lean`, proof, axiom, bodyless declaration, `sorry`, placeholder theorem, or fake
result was introduced. The root vector remains `[H2, M4, R4]`, and theorem completion remains false.

## Environment fingerprint

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `f62446641a2a0d22723d2814fbb3a9b3ae518e45b10eb5078a4409e61cf7c210`.

## Commands and exact results

All commands ran in this worker clone. Lean used only the existing pinned `.lake` artifacts; no
update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1224` | 0 | rank 155; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_155.lean` | 0 | Legacy abstract statement-shape module elaborated and printed its checked declarations; no exact-target credit |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json AwesomeTheorems/Stage1/S1_M_155.lean` | 0 | hashes match the environment fingerprint above |
| `rg -n -i 'Grillakis\|critical nonlinear.*wave\|nonlinear wave.*critical\|wave equation with a critical' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no match in pinned mathlib |
| `git diff --check -- Stage1_Instances/THM-M-1224` | 0 | no whitespace errors |

## Retry condition

Provide an immutable copy of the selected primary paper with a theorem/page locator, surrounding
definitions, and errata status. A reviewed row-by-row crosswalk must then freeze the data class,
nonlinearity, solution and uniqueness notions, time domain, regularity conclusion, conventions,
and boundary cases. Only then can the statement phase encode the exact proposition with minimal
imports, serialize its elaborated expression and environment, and run the required mutations.

Until that source amendment exists, section 5/5.1 statement identity is the first failed gate.
Because the assigned phase is blocked rather than genuinely completed, no
`.stage1-worker-selftest.json` is emitted.
