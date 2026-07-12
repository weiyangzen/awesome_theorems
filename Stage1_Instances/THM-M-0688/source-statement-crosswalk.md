# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `序数记号`, attributes it to "many
mathematicians", dates it only to the twentieth century, and states `大序数的记号系统` ("notation
systems for large ordinals"). `Docs/Stage0_Blueprint.md` repeats that metadata. The rev-5.6
manifest preserves `已验证` only as `source_status_untrusted`. No definition, ordinal bound,
theorem, hypotheses, conclusion, proof source, edition, page, or formal artifact is supplied.

The adjacent entries on transfinite induction and ordinal analysis locate the broad subject area,
but adjacency does not determine a statement and is not source evidence.

## Candidate source work

An authoritative proof-theory source must be selected at the statement phase. It must explicitly
define the intended notation system and state the proposition to be formalized. The audit must
record edition, definition/theorem and page, ordinal boundary, assumptions, proof boundary, and
errata, followed by independent source review. Until that happens, naming a particular system,
ordinal, theorem, or historical author as canonical would be speculation rather than an `H0`
crosswalk.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "notation system" | inductive syntax or recursive codes | a concrete type such as a source-matched inductive or code subtype | absent; mathlib candidate API probed |
| "ordinal" | denotation/order type of each valid notation | semantics into `Ordinal` or a checked intrinsic-order correspondence | candidate only |
| "large" | epsilon-zero, Gamma-zero, or a stronger proof-theoretic bound | an exact ordinal expression and strict/non-strict coverage boundary | absent from source record |
| "system" | normal forms, comparison, arithmetic, or fundamental sequences | source-matched operations and invariants | absent from source record |
| implied theorem | existence, coverage, uniqueness, correctness, effectiveness, or well-foundedness | one exact `Prop` with all binders and hypotheses | absent from source record |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.SetTheory.Ordinal.Notation` and `Mathlib.SetTheory.Ordinal.Veblen`. It checks
the types of `ONote`, its denotation and normal-form predicate, the subtype `NONote`, its denotation,
well-founded order theorem, arithmetic correctness theorem, and the Veblen function. Mathlib's
module documentation describes `NONote` as normal ordinal notations below epsilon-zero, while its
Veblen module notes a construction up to Gamma-zero. These are distinct candidate ingredients.
The probe neither identifies which one the repository intended nor supplies the missing canonical
proposition. A later immutable anchor audit must examine declarations and terminal proof
provenance after the statement has been frozen.
