# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives the title "harmonic function", attribution "many
mathematicians", eighteenth century, and the statement "a solution of Laplace's equation".
`Docs/Stage0_Blueprint.md` repeats these fields and leaves exact definitions, prerequisites, proof,
axioms, equivalences, and machine status open. Neither record supplies a bibliography, edition,
theorem number, page, proof, or errata. The label `已验证` is explicitly untrusted rev-5.6 metadata.

No primary-source candidate is asserted at intake. In particular, the phrase appears definitional
and does not say what proposition is to be proved. Inventing a biconditional or selecting a regularity
theorem would broaden the record, so source fidelity remains `H4`.

## Crosswalk

| Source element | Information fixed | Information required for Lean | Intake result |
|---|---|---|---|
| "harmonic function" | names the mathematical object | an independently sourced predicate or definition | unresolved |
| "solution" | satisfaction of an equation | solution notion and quantifier scope | unresolved |
| "Laplace's equation" | conventionally `Delta u = 0` | domain, derivatives, Laplacian definition, equality locus | unresolved |
| eighteenth century / many mathematicians | broad historical context | none | cannot identify a source theorem |
| `已验证` | repository screening label | kernel receipt and inspectable proof | no credit |

## Candidate statement shape, not frozen

A later source might justify a shape such as: for an open set `Omega` in a finite-dimensional real
space and a twice differentiable real-valued function `u`, `u` is harmonic on `Omega` if and only if
its Laplacian vanishes at every point of `Omega`. This row is only a search specification. It is not
the canonical statement, because the current source does not define either side independently or
establish that an equivalence is intended.

The next gate is primary-source identification followed by a row-by-row assumption and definition
crosswalk. Only after that may a canonical Lean expression and minimal imports be frozen.

