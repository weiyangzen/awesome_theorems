# Source-statement crosswalk

## Repository wording

The repository catalog at `Docs/researches/math_theorems.md:977` identifies only a Chinese label
rendered as "Burnside-Young theorem", W. Burnside/A. Young attribution, the decade "1900s", and
the topic gloss "representation theory of symmetric groups". The Stage0 record repeats that gloss
while leaving the definitions, premises, conclusion, proof route, dependencies, axioms, machine
status, and artifact links open. Neither record gives a work, edition, theorem number, page, field,
range of `n`, equivalence convention, construction, conclusion, corrections, or errata.

## Candidate clauses

| Candidate clause | Evidence | Statement disposition |
|---|---|---|
| finite symmetric group `S_n` | repository topic only | plausible vocabulary; exact group and range unresolved |
| complex representations | legacy discovery artifact only | not source-admitted |
| finite dimensionality | legacy prose only | not source-admitted; not encoded by `Rep.{0}` alone |
| irreducible representation isomorphism classes | legacy discovery artifact only | not source-admitted |
| partitions of `n` | legacy discovery artifact only | not source-admitted |
| classification equivalence | legacy discovery artifact only | not source-admitted |
| `n = 0` and `n = 1` | no repository source wording | boundary policy unresolved |

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_050.lean` selects the familiar
partition-indexing interpretation, but it explicitly calls itself a statement shape and reports no
terminal proof. Under the uniform L0 rework rule it is discovery input, not source or exact-target
authority.

## Competing interpretations

The catalog gloss does not distinguish the representation-isomorphism classification from an
irreducible-character classification, Young's rule, branching results, Young's orthogonal form, or
another early result in symmetric-group representation theory. These statements are not
definitionally interchangeable. Selecting one because it is convenient to encode would change the
mathematical proposition.

## Required resolution

The statement gate requires one admitted primary or approved-authoritative passage with a stable
edition, theorem/page locator, incorporated definitions, exact assumptions and conclusion, proof
boundary, correction and errata disposition, exact translation, and independent review. That
decision must fix the coefficient field and characteristic, range of `n`, symmetric-group model,
finite-dimensionality convention, representation and equivalence models, construction, conclusion,
and degenerate cases. Until then the canonical human statement, Lean target, expression fingerprint,
credited transports, and mutations remain null or unexecutable.

This crosswalk is a truthful blocker record. It supplies no H0, exact-statement, proof, audit, or
theorem-completion credit.
