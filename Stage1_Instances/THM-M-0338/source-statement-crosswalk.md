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
| bounded operators | `B(H)` for a separable infinite-dimensional complex Hilbert space | `H →L[ℂ] H` with C-star/operator-order instances | frozen |
| diagonal algebra | operators diagonal in a countable Hilbert basis | `StarSubalgebra` plus exact vanishing of off-diagonal matrix coefficients | frozen |
| state | positive complex-linear functional normalized at one | local `State` over `PositiveLinearMap` | frozen |
| pure | extreme state | local `IsPure` strict convex-decomposition predicate | frozen |
| extension | a state on the full algebra restricting to the given state | equality after subalgebra coercion | frozen |
| unique | exactly one extension among all states | `ExistsUnique` | frozen |
| affirmative solution | every diagonal pure state has a unique extension | `KadisonSingerStatement` | elaborated; primary-source clause review remains open |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
imports the C-star positive-linear-map and bounded-operator APIs and checks their core types. A
bounded name search found no C-star state or pure-state declaration. `Statement.lean` therefore
defines these notions transparently from `PositiveLinearMap`, and its exact target elaborates.
No mathlib theorem candidate receives proof credit here.
