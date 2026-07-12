# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `Gentzen 一致性证明`, the gloss `PA的一致性证明`,
Gerhard Gentzen, and 1936. `Docs/Stage0_Blueprint.md` repeats this metadata but leaves the definitions,
hypotheses, proof path, axioms, and formal artifact open. The rev-5.6 manifest retains `已验证` only
as untrusted source metadata.

## Primary-source locator

The matching historical source is Gerhard Gentzen, "Die Widerspruchsfreiheit der reinen
Zahlentheorie", *Mathematische Annalen* 112 (1936), 493-565. This is a bibliographic discovery
anchor, not yet an immutable source receipt. The exact statement passage, edition/file hash,
definitions, premise boundaries, translation, later corrections or reformulations, and errata have
not been pinned or independently reviewed. No `H0` claim is made.

## Crosswalk

| Repository/source component | Mathematical content to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "PA" / pure number theory | Exact first-order arithmetic language, logical calculus, axioms, and induction schema | object-language syntax, theory, derivation relation, coding invariants | open; mathlib first-order syntax is only nearby infrastructure |
| "consistency" | No derivation of contradiction in that calculus | a literal `not Provable false` or empty-sequent proposition | open; semantic `Theory.IsSatisfiable` is not silently substituted |
| proof reduction | Transformation/normalization of the relevant derivations | recursive reduction and preservation theorems | absent from the local target |
| ordinal assignment | Measure in a notation system below epsilon-zero | notation datatype, comparison, assignment, descent | mathlib has set-theoretic epsilon-zero, not the required checked bridge |
| transfinite induction | Exact schema and metatheory justifying termination | source-bounded induction/well-foundedness theorem | premise strength and packaging open |
| Gentzen, 1936 | Historical proof and foundation boundary | source nodes mapped to obligations | primary bibliographic anchor located; pinpoint audit open |
| `已验证` | inventory status only | none | rejected as H/M evidence |

## Semantic versus syntactic boundary

Pinned mathlib defines `FirstOrder.Language.Theory.IsSatisfiable` semantically by existence of a
model. That can become relevant only after a source-faithful PA theory and checked soundness or
completeness bridge are fixed. Proving semantic satisfiability of an approximate theory would not,
by itself, reconstruct Gentzen's syntactic ordinal-reduction proof and would be a substituted root.

Pinned mathlib also defines the ordinal epsilon function and epsilon-zero as a set-theoretic
ordinal. Gentzen's proof requires an effective notation system, its comparison and fundamental
operations, a proof assignment, and descent under reduction. Equality or adequacy between such a
notation system and mathlib's ordinal boundary must be proved if credited.

Before `H0`, an independent proof-theory reviewer must approve the exact source passage, modernized
statement, assumptions, translation, corrections/errata disposition, and node-by-node proof
boundary. Before statement credit, that approved claim must map to one elaborated Lean proposition
with checked transports and the required mutations.
