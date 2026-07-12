# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `哥德尔不完备性定理`, attributes it to Kurt
Goedel, gives the year 1931, and states only `包含算术的一致系统不完全` ("a consistent system
containing arithmetic is incomplete"). Stage0 repeats this wording and leaves the definitions,
assumptions, proof path, axioms, and formal artifact unspecified. The rev-5.6 manifest carries
`已验证` only in the explicitly untrusted source-status field.

This is secondary inventory metadata, not an edition/page-level primary citation. It also does not
say whether "Goedel's incompleteness theorem" means the original first theorem, Rosser's theorem,
or a modern generalization.

## Source fidelity blocker

The gloss omits effective axiomatizability. Without it, the natural universal reading is false:
true first-order arithmetic is a complete consistent theory extending arithmetic, though not an
effective theory. The original and Rosser variants also use different consistency assumptions.
Consequently, adding the familiar missing conditions without an immutable source would broaden or
replace the supplied wording rather than crosswalk it.

The source audit must identify an exact edition and theorem locator, record its object theory,
proof calculus, coding/effectivity assumptions, consistency notion, conclusion, dependencies, and
errata, and obtain independent mathematical review. No `H0` source is claimed here.

## Crosswalk

| Repository phrase | Material mathematical choice | Required Lean component | Intake status |
|---|---|---|---|
| "system" | language, axioms, proofs, and derivability | first-order syntax plus an explicit theory/proof predicate | absent |
| "contains arithmetic" | extension or interpretation of a named weak arithmetic | encoded numerals, arithmetic symbols, and representability interface | absent |
| "consistent" | consistency, omega-consistency, 1-consistency, or soundness | exact predicate over derivations/models | ambiguous |
| omitted effectivity | recursive axiomatization or recursively enumerable theorem set | computable encoding/enumeration and proof checker | required to repair literal scope; absent |
| "incomplete" | a sentence with neither it nor its negation derivable | sentence coding, negation, derivability, and scoped existential | ambiguous |
| `已验证` | untrusted inventory label | no proposition or proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Logic.Godel.GodelBetaFunction` and `Mathlib.ModelTheory.Encoding`. It checks
the beta function, its finite-sequence decoding theorem, and first-order term/formula encodings.
The beta-function module explicitly says it is a step toward *eventually* including a first
incompleteness proof. Thus these declarations are prerequisites or candidate leaves only; none is
an anchor for the root target. A full immutable external-project search belongs to the later
anchor-audit phase.
