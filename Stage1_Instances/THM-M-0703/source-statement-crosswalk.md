# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `类型论`, attributes it to Bertrand
Russell and Alonzo Church, gives the year 1940, and supplies only `简单类型论` ("simple type
theory") as its statement. Stage0 repeats these fields while marking the exact definitions,
assumptions, proof process, dependencies, axioms, and machine artifact as open. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted`.

This metadata names a subject or formal system, not a proposition. It gives no edition, section or
theorem number, page, formal syntax, hypotheses, conclusion, proof, errata, or formal artifact. The
1940 date and Church attribution suggest a historical source location, but do not authorize
choosing a proposition from it. Russell's inclusion also leaves the intended historical
formulation unclear.

## Candidate source work

Church's 1940 paper *A Formulation of the Simple Theory of Types* is a candidate primary locator,
not an accepted statement source at intake. A source audit must inspect an immutable edition and
identify whether the repository intends a definition/presentation or a particular proved
metatheorem. It must record the exact section or theorem and page, notation, assumptions, proof
boundary, and errata, then obtain independent review. Textbooks about simply typed lambda calculus
may help disambiguate later terminology but cannot silently replace the historical target.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "simple types" | base types closed under function type | an inductive object-language type grammar | candidate only |
| "theory" | terms, contexts, typing, conversion, logical constants, or semantics | explicit syntax and judgments, not native Lean typing alone | unspecified |
| Russell/Church | historical type hierarchy or Church 1940 higher-order logic | a pinpoint immutable source mapping | locator only |
| `1940` | likely Church-era formulation | edition, section/theorem, and page | insufficient to select a claim |
| a possible metatheorem | soundness, normalization, consistency, or another result | a concrete proposition with all hypotheses | absent from source record |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe uses only Lean's prelude and checks polymorphic identity, function composition, product and
sum type formers, and equality elimination. These demonstrate that the intended metatheory can
express basic typed encodings. They neither define a simply typed object language nor state or
prove any metatheorem about one. A later anchor audit must search only after the exact source claim
and discovery protocol are frozen.
