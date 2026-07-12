# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `Haken定理`, attributes it to Armin Haken, dates it to
1985, and gives only `鸽巢原理证明长度的下界` ("a lower bound on the proof length of the
pigeonhole principle"). Stage0 repeats that phrase and marks the exact definitions, assumptions,
proof route, axioms, and artifact links as open. The rev-5.6 manifest retains `已验证` solely as
`source_status_untrusted`.

This metadata locates a result family, not a proposition: it contains no definition of the formula
family or resolution derivation, no quantifiers, numerical bound, constants, parameter threshold,
theorem number, page, assumptions, proof crosswalk, errata record, or formal artifact.

## Primary-source candidate

The bibliographic candidate matching the repository author, year, and topic is:

Armin Haken, *The intractability of resolution*, Theoretical Computer Science 39 (1985), 297-308.

This citation is an intake locator, not accepted `E4`/`H0` evidence. The source-audit phase must
inspect an immutable copy, identify the exact numbered or displayed statement and pages, transcribe
its definitions and quantifiers, check corrections or errata, map proof nodes to passages, and
obtain independent review. Until then the root is conservatively `H1`.

## Crosswalk

| Repository phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "pigeonhole principle" | exact unsatisfiable CNF family and parameter range | finite variable, literal, clause, CNF, and assignment encodings | family identified; encoding open |
| "proof" | exact resolution rules and derivation validity | typed clauses, derivation steps, initial-clause and inference predicates | absent from repository source |
| "length" | line, clause, literal, symbol, or DAG-node count | a size function on the selected derivation representation | absent from repository source |
| "lower bound" | explicit inequality, constants, and small-parameter threshold | quantified inequality over all valid refutations | absent from repository source |
| Haken / 1985 | likely paper provenance | source revision and source-node ledger | candidate citation only |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports finite-cardinality support and checks `Fin`, `Finset`, `Fintype.card`, and basic
finite-cardinality facts. These are generic representation ingredients only. A scoped mathlib name
search found pigeonhole-principle combinatorics and an LRAT checker, but no repo-local encoding or
declaration for Haken's uniform resolution lower bound. This bounded observation is not the later
immutable anchor audit and gives no machine-proof credit.
