# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names the Kadison-Singer problem, attributes it to Richard
Kadison and Isadore Singer, dates it to 1959, and gives only `纯态的唯一延拓` ("unique extension
of pure states"). Stage0 repeats this gloss while leaving exact definitions, assumptions, proof
route, axioms, and artifacts open. The manifest deliberately preserves `已验证` only as
`source_status_untrusted`; it supplies no proof credit.

## Human-source candidates

Richard V. Kadison and Isadore M. Singer, "Extensions of pure states", *American Journal of
Mathematics* 81 (1959), no. 2, pp. 383-400, is the primary-source candidate. It has not yet been
inspected here at problem/theorem/page and clause granularity or checked for errata, so it supports
only a discovery-level `H1`, not `H0`.

Adam Marcus, Daniel A. Spielman, and Nikhil Srivastava, "Interlacing Families II: Mixed
Characteristic Polynomials and the Kadison-Singer Problem", *Annals of Mathematics* 182 (2015),
pp. 327-350, is a proof-source candidate for the affirmative resolution. Its equivalence route to
the literal pure-state claim must be audited node by node later; its title is not a crosswalk.

## Crosswalk

| Repository/source concept | Mathematical content to freeze | Candidate Lean component | Intake status |
|---|---|---|---|
| bounded operators | `B(l2(N))` as a unital complex C-star algebra | `ContinuousLinearMap` plus C-star instances | foundational API probed |
| diagonal algebra | operators diagonal in the standard basis, as a closed star subalgebra | `StarSubalgebra` plus a construction not yet identified | encoding open |
| state | positive complex-linear functional normalized at one | `PositiveLinearMap` plus normalization | partial ingredients probed |
| pure | extreme state or equivalent indecomposability condition | no pinned declaration identified by bounded search | missing encoding |
| extension | a state on the full algebra restricting to the given state | function equality after the subalgebra inclusion | encoding open |
| unique | exactly one extension in the source-specified class | `ExistsUnique` or a subsingleton extension subtype | encoding open |
| affirmative solution | the unique-extension assertion holds for every diagonal pure state | canonical proposition | exact source mapping open |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
imports the C-star positive-linear-map and bounded-operator APIs and checks their core types. A
bounded name search found no C-star state or pure-state declaration. This does not prove absence
from all possible encodings, but it establishes that substantial definitions are still required
before exact elaboration. No mathlib theorem candidate receives statement or proof credit here.
