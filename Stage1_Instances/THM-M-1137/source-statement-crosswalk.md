# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies the title "mean-value property", attribution "many
mathematicians", nineteenth century, and the phrase "the mean value of harmonic functions".
`Docs/Stage0_Blueprint.md` repeats the phrase while leaving definitions, prerequisites, proof,
axioms, equivalences, and machine status open. Neither record gives a bibliography, edition,
theorem number, page, proof, or errata. The `已验证` label is explicitly untrusted metadata under
rev-5.6 and receives no source or kernel credit.

No primary-source candidate is asserted at intake. The phrase does not distinguish the sphere and
ball theorems, their converse, or a characterization. Choosing among them now would substitute a
more precise theorem for the recorded source, so fidelity remains `H4`.

## Crosswalk

| Source element | Information fixed | Information required for Lean | Intake result |
|---|---|---|---|
| "harmonic functions" | identifies the subject | domain, codomain, regularity, Laplacian/harmonic predicate | unresolved |
| "mean value" | indicates an averaging identity | sphere or ball, measure, normalization, integral API | unresolved |
| "property" | suggests a theorem or characterization | implication direction and complete binder scope | unresolved |
| nineteenth century / many mathematicians | broad historical context | none | cannot identify a source theorem |
| `已验证` | repository screening label | inspectable proof and kernel receipt | no credit |

## Candidate shapes, not frozen

A source may justify a sphere identity saying that a harmonic function's value at a center equals
its normalized surface integral on every sphere whose closed ball lies in the domain. Another may
state the analogous normalized volume integral over the ball, or an equivalence between harmonicity
and one or both identities. These are search specifications only, not canonical statements.

The next gate is primary-source identification followed by a row-by-row mapping of assumptions,
definitions, degeneracies, and conclusion to an exact Lean expression with minimal pinned imports.
