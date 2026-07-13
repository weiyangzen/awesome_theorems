# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:242-247` records only:

- title: Cohen structure theorem;
- attribution: Irving Cohen;
- year: 1946;
- gloss: structure of complete Noetherian local rings;
- importance: medium;
- untrusted formalization label: verified.

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:965-990`
repeats this record while explicitly leaving exact definitions and premises, proof route,
equivalent forms, axioms, machine status, and artifact links open. These records establish target
identity and discovery provenance only.

## Primary publication lead

Crossref metadata for DOI `10.1090/S0002-9947-1946-0016094-3` identifies I. S. Cohen, "On the
structure and ideal theory of complete local rings," *Transactions of the American Mathematical
Society* 59(1) (1946), pages 54-106. The retrieved metadata payload had SHA-256
`121788f395a1f06c4b727f5f42b6a2c8d88d6bcfe433e4b4865b279ba321bc20`.

This is a bibliographic lead, not H0 evidence. The publisher PDF returned HTTP 403 during intake,
so no immutable full text, theorem/page selection, incorporated definition chain, premise and
conclusion map, proof boundary, correction/errata audit, or independent review was accepted.

## Modern statement lead

The Stacks Project Section 10.160, tag `0323`, calls tag `032A` Theorem 10.160.8 the Cohen
structure theorem. The inspected page states:

1. if `(R, m)` is a complete local ring, then `R` has a coefficient ring;
2. if `m` is finitely generated, then `R` is isomorphic to a quotient
   `Λ[[x_1, ..., x_n]] / I`, with `Λ` either a field or a Cohen ring.

Definition tag `0324` defines completeness by the canonical isomorphism
`R -> lim_n R / m^n`, including separatedness. Definition tag `0326` gives three coefficient-ring
conditions. The fetched section HTML had SHA-256
`9d6b732c706275cda63bd18865b0c7b7723a65d02bd1b8765ed2d6efa0730e86`.

This inspected modern source makes the ambiguity concrete, but it is mutable web content and has
not been selected as the canonical source, content-pinned at an immutable revision, or
independently reviewed against Cohen's paper. It supplies no H0 and no license to substitute its
exact formulation for the catalogue target.

## Clause crosswalk

| Catalogue phrase | Required source decision | Pinned Lean surface | Intake status |
|---|---|---|---|
| "local rings" | commutative/unital/nontrivial conventions and maximal ideal | `IsLocalRing R`, `IsLocalRing.maximalIdeal R` | interfaces located; source encoding open |
| "complete" | maximal-ideal topology, inverse-limit map, Hausdorff/separated condition | `IsAdicComplete (maximalIdeal R) R` is a candidate | transport from source definition open |
| "Noetherian" | explicit hypothesis or consequence of finite generation plus completeness | `IsNoetherianRing R` | predicate located; quantifier role open |
| hidden residue data | residue field, its characteristic, and whether `p` is zero, nonnilpotent, or nonzero nilpotent in `R` | `IsLocalRing.ResidueField R`, `IsLocalRing.residue R`; `MixedCharZero R p` covers only characteristic-zero ambient rings | partial branch substrate; positive-characteristic and truncated coefficient-ring cases need further encoding |
| "structure" | coefficient ring, power-series quotient, regular-local cover, or another clause | no coefficient-ring or Cohen-root declaration found | unresolved root output |
| power-series presentation | coefficient object, finite variables, ideal, quotient, isomorphism category | `MvPowerSeries σ Λ` | type located; map/quotient theorem absent |
| theorem identity | primary 1946 passage versus a selected modern formulation | no canonical Lean declaration | unresolved |

The pinned theorems `AdicCompletion.isAdicComplete` and
`isLocalRing_of_isAdicComplete_maximal` authenticate nearby completeness infrastructure only. Their
types neither construct a coefficient ring nor give a power-series quotient presentation.

## Missing source-to-statement links

- a lawfully preserved immutable primary or authoritative edition;
- exact theorem number/page and incorporated definition locators;
- all domains, ordered binders, hypotheses, and conclusions;
- the relationship among complete, complete-and-separated, Noetherian, and finitely generated
  maximal-ideal assumptions;
- coefficient-ring definition and complete coverage of coefficient-field, Cohen-ring, and
  truncated `p`-nilpotent cases;
- variable cardinality, quotient ideal, map, and isomorphism conventions;
- proof boundary, dependency map, translations, corrections, and errata;
- independent source reviewer and review receipt;
- checked source-to-Lean identity or transports.

Until these links are accepted, the source axis is H1. The catalogue wording and modern lead are
not a canonical statement, and the `已验证` label is not evidence of either a human-source audit or
a machine proof.

## Non-substitution rule

Future work must not replace this target with an adic-completion fact, a local-ring predicate, a
power-series construction, only one characteristic branch, only the regular case, a domain
specialization, a regular-local consequence, or a different theorem carrying Cohen's name. Any
alternate formulation needs an explicit source decision and a checked logical transport to the
selected canonical proposition.
