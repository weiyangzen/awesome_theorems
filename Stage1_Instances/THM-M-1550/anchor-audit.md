# Anchor audit record

Item: `S56-M-1550-ANCHOR_AUDIT`  
Audit date: `2026-07-12`  
Base revision: `08764d477205bbae07c32197a9a83ac6c07866c9`

## Result

The pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact
leaf theorem `spectrum.units_conjugate` in
`Mathlib.Algebra.Algebra.Spectrum.Basic`. Its source type says that conjugating an element of an
algebra by a unit preserves its algebra spectrum. `AnchorAudit.lean` instantiates it at finite
complex matrices with the exact multiplication order used by the frozen `ConjugatesAt` predicate.
Lean elaborated the wrapper. The pinned source contains a concrete proof body, and a token scan of
that module found no `sorry`, `admit`, `axiom`, or `unsafe` occurrence.

The historical `S1_M_209.lean` file contains three useful wrappers ending at the same mathlib
theorem, but remains discovery input: it predates the rev-5.6 statement and its broader data package
does not itself confer proof or status credit. No external terminal theorem was found in immutable
tree scans of physlib and SciLean at the revisions recorded in `anchor-audit.json`. Those negative
path scans are bounded evidence, not a claim that all public Lean code was exhaustively searched.
Live GitHub repository searches for `"Lax pair"`, `isospectral`, and `"integrable systems"` with
language `Lean` also returned zero repositories on the audit date; because search results are
mutable, they are supplemental discovery only and are not used as immutable evidence.

No candidate closes the whole frozen theorem by itself. The root is nevertheless structurally
close: its supplied `ConjugatingEvolutionOn` hypothesis exposes the unit witnesses required by the
mathlib leaf. The actual root composition belongs to the later obligation-tree and proof phases.
Current machine debt is therefore `formalization_debt`, not an external integration debt, and this
audit makes no theorem-completion claim.

## Commands and exact results

All repository commands ran in this worker clone. Lean reused the canonical pinned `.lake`; no
update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` for 15 assurance groups, 1546 uniform-L0 targets, and the execution skill |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1550` | 0 | rank 209, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n "LaxPair\|Lax pair\|isospectral\|integrable system\|Toda lattice\|KdV Lax\|inverse scattering" Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no terminal Lax/integrable-system occurrence in pinned mathlib; exit 1 is ripgrep's no-match result |
| `rg -n "units_conjugate" Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | located the terminal spectrum theorem in `Algebra/Algebra/Spectrum/Basic.lean:435` and its reverse-order companion |
| immutable GitHub recursive-tree path scans of physlib `9492c3...18e` and SciLean `95f811...5c5` for `lax\|isospectral\|integrable\|toda\|kdv` | 1 | both trees downloaded successfully; ripgrep found no matching paths |
| `lake env lean ../../Stage1_Instances/THM-M-1550/AnchorAudit.lean` | 0 | exact finite-matrix wrapper and the fully explicit type of `spectrum.units_conjugate` elaborated |
| `rg -n "sorry\|admit\|axiom\|unsafe" Formalizations/Lean/.lake/packages/mathlib/Mathlib/Algebra/Algebra/Spectrum/Basic.lean` | 1 | no placeholder, added-axiom, or unsafe token; exit 1 is ripgrep's no-match result |
| `lake env lean ../../Stage1_Instances/THM-M-1550/Statement.lean` | 0 | frozen canonical statement and its checked transports still elaborate |
| `git diff --check -- Stage1_Instances/THM-M-1550` | 0 | no whitespace errors |

Status boundary: this is a self-tested anchor-audit receipt pending master acceptance. It advances
neither the obligation tree nor proof, validation, release, or theorem-completion gates.
