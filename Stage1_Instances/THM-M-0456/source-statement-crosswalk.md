# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` attributes the result to Aleksei Parshin, dates it to 1968, and
describes it only as “proof of the function-field Mordell conjecture.” `Docs/Stage0_Blueprint.md`
repeats this metadata while leaving definitions, hypotheses, proof route, and machine artifact
open. Its `已验证` value is explicitly untrusted under rev-5.6.

## Candidate primary sources

- A. N. Parshin, *Algebraic curves over function fields. I* (1968), the historical paper normally
  associated with the function-field Mordell result.
- Ju. I. Manin, *Rational points on algebraic curves over function fields* (1963), an earlier
  characteristic-zero source that must be checked to distinguish attribution, formulation, and
  the exact theorem intended by the repository label.

These bibliographic leads are discovery anchors, not `H0`: a stable edition/translation, theorem
number or page, all definitions and assumptions, and relevant errata have not yet been inspected.
The statement phase must not manufacture those details from the theorem's name.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| “function field” | function field of a base curve | concrete field plus curve/function-field relation | included; encoding open |
| “Mordell conjecture” | rational points on a genus `> 1` curve | curve object, genus predicate, rational-point set | included |
| characteristic zero | excludes positive-characteristic pathologies | `CharZero` and exact constant-field hypotheses | candidate assumption |
| non-isotrivial | excludes constant families with potentially infinite points | source-faithful isotriviality predicate | essential; definition open |
| “proof” / `已验证` | human theorem claimed by inventory | inspected proof and/or kernel receipt | no credit |

## Lean boundary

No target-specific legacy module was found. Repository searches locate adjacent Mordell/Faltings,
Mordell-Weil, and function-field infrastructure, but no declaration identified as Parshin's
terminal theorem. Those results cannot be substituted. Anchor audit must search the pinned mathlib
revision and credible Lean 4 projects, recording exact declaration types and proof provenance.

Before `H0`, an independent reviewer must verify the selected primary edition, theorem/page,
constant-field and isotriviality conventions, assumptions and errata, and approve a row-by-row
source-to-canonical-Lean mapping.

