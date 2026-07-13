# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6607-6612` supplies exactly the title
`Bose-Shrikhande-Parker定理`, attribution `Bose/Shrikhande/Parker`, year 1960, gloss
`Euler猜想的否定`, importance `高`, and status `已验证`. All six lines originate at repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no citation, definition,
formula, domain, binder, hypothesis, conclusion, exceptional case, proof boundary, correction
history, or formal artifact.

`Docs/Stage0_Blueprint.md:24629-24654` repeats the gloss and explicitly leaves the formal system,
foundation, precise definitions and premises, proof route, dependencies, equivalent statements,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Mathematical component to freeze | Prospective Lean component | Intake result |
|---|---|---|---|
| `Euler猜想` | exact historical proposition, including order domain and nonexistence quantifier | a fully quantified proposition over pairs of Latin squares | referent recognizable but not defined or cited |
| `否定` | logical negation, a counterexample theorem, a uniform construction, or a complete classification | `Not P`, an existential witness family, or an iff statement | materially different strengths; no root selected |
| Bose/Shrikhande/Parker, 1960 | publication and proof provenance | pinpoint source ledger and proof-node crosswalk | matching primary source inspected; independent acceptance open |
| `已验证` | untrusted inventory metadata | no proposition or proof term | explicitly rejected as H0 or machine evidence |

## Inspected primary-source lead

R. C. Bose, S. S. Shrikhande, and E. T. Parker, *Further Results on the Construction of Mutually
Orthogonal Latin Squares and the Falsity of Euler's Conjecture*, *Canadian Journal of Mathematics*
12 (1960), pages 189-203, DOI `10.4153/CJM-1960-016-5`. The official Cambridge version-of-record
PDF inspected during intake has 15 pages, 1,337,286 bytes, and SHA-256
`cbd6489e0c3f7657a65b75ca4c2e09b3b7c9906919ed2a6b9cdc56bad6925107`.

Printed page 189 describes Euler's conjecture as nonexistence of two orthogonal Latin squares of
order `v = 4t + 2`. Printed page 190 defines a Latin square of order `v` as an arrangement of `v`
symbols in a `v x v` square with each symbol exactly once in every row and column. It defines two
squares as orthogonal when, after superposition, each symbol of the first occurs exactly once with
each symbol of the second. The introduction says the paper proves the conjecture false for all
`v = 4t + 2 > 6`.

Printed page 202, Theorem 10 states: "There exist at least two orthogonal Latin squares of any order
`v > 6`." Printed page 203 then defines a positive integer `v > 2` as Eulerian when two orthogonal
Latin squares of order `v` do not exist and concludes that 6 is the only Eulerian number. The proof
of Theorem 10 depends on the paper's preceding design and construction results, including a finite
range lemma and Theorem 8; those proof nodes, incorporated references, and computation checks have
not been mapped or independently reviewed here. The page-203 unique-exception conclusion also uses
the known nonexistence result at order six; Theorem 10 itself proves only the `v > 6` existence
family.

This is strong `H1` source evidence, not H0. The repository does not cite the paper or select
Theorem 10, its congruence-specialized introduction claim, one counterexample, or the final
classification phrasing. The PDF was inspected temporarily but is not a repository-preserved
immutable source packet. Corrections, errata, incorporated results, every proof node, assumption
transport, and an independent source review remain open.

Crossref metadata for the DOI independently reports the three authors, title, journal volume 12,
year 1960, and pages 189-203. The observed 6,009-byte mutable response had SHA-256
`706ed0be2b21971ede7d51d90a2e6ee05faf52eef92776847d1eb541e9d1c256`. It is discovery provenance,
not source or proof acceptance.

## Scope distinctions and exclusions

- A single pair of order-10 orthogonal Latin squares refutes the universal conjecture but is weaker
  than the primary paper's Theorem 10.
- Existence for every `v = 4t + 2 > 6` tracks the conjectured family, while Theorem 10 states the
  stronger existence result for every order greater than 6.
- The source-exact final classification says that among positive `v > 2`, a pair exists exactly
  when `v != 6`. Extending it to all positive orders adds convention-sensitive orders one and two,
  including whether a pair means distinct members of a family or may repeat the unique order-one
  square; it is not identical to Theorem 10 alone.
- `THM-M-0902` is the separate Euler-conjecture target. Its future statement, evidence, or status
  does not transfer automatically, and this target must not be turned into an audit of that item.
- Existence of one Latin square, mutually orthogonal families of unspecified size, a lower bound on
  the maximum number `N(v)` other than the selected threshold, or an orthogonal array without a
  checked transport cannot substitute for the selected root.

## Lean boundary and source gate

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks finite matrices, finite index types, cardinality, function bijectivity, and products. A
bounded name/text search found no obvious Latin-square, orthogonal-Latin-square, Bose, Shrikhande,
or Parker declaration. These are substrate and bounded-discovery observations only, not a complete
anchor audit or an absence claim about external Lean projects.

Before statement acceptance, accountable reviewers must preserve a lawful immutable source
edition, choose the exact root and its relationship to `THM-M-0902`, freeze all definitions,
ordered binders, hypotheses, conclusions, strict inequalities, congruence conditions, small orders,
and representation transports, audit corrections and incorporated sources, map every material
proof node, and independently approve the source-to-Lean crosswalk. Until then the canonical
statement, formal expression, fingerprint, alternate encodings, and obligation registry remain
null.
