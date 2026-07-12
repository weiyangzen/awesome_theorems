# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6586-6591`, introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, contains the entire record:

- title: `Keighery定理`;
- attribution: `众多数学家` (many mathematicians);
- period: `20世纪` (twentieth century);
- statement gloss: `设计的渐近存在性` (asymptotic existence of designs);
- importance: high; and
- status: `已验证`.

`Docs/Stage0_Blueprint.md:24548-24573` repeats this metadata and explicitly leaves the exact
definitions and premises, proof route, dependencies, equivalent formulations, foundations, machine
status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`. None of these secondary
inventory records is a primary theorem source or proof receipt.

## Literal crosswalk

| Repository element | Required mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `Keighery theorem` | stable author/result identity and exact source locator | canonical declaration identity and provenance | no matching design-theory identity located; possible corruption |
| "design" | a fixed incidence structure and its parameters | point type, block carrier, finiteness, cardinality and incidence predicates | all choices open |
| "existence" | exact or approximate existence, multiplicity, labeling and construction policy | one `Prop` with ordered binders, hypotheses and existential conclusion | conclusion strength open |
| "asymptotic" | fixed parameters, varying parameter, threshold dependency and all sufficiently large quantifier | ordered threshold/existence/universal binders | quantifier order and domain open |
| many mathematicians / twentieth century | provenance and historical scope | documentation only | no edition, theorem, page, proof boundary or errata |
| `已验证` | untrusted inventory metadata | accepted source review and kernel evidence would be required | no H or M credit |

## Uncredited identity lead

Peter Keevash, *The existence of designs*, arXiv `1401.3665v4` (27 November 2024), is a strong
discovery lead rather than an accepted correction. The inspected PDF has SHA-256
`892d8b968c3e56e588297fdc72ef67e36efe9a32173228412b310de63d00eccf`.

Its introduction defines a design with parameters `(n,q,r,lambda)` as a set of `q`-subsets of an
`n`-set such that every `r`-subset lies in exactly `lambda` blocks. It records the necessary
conditions

```text
choose (q - i) (r - i) divides lambda * choose (n - i) (r - i)
```

for every `0 <= i <= r`, and calls the assertion that these conditions suffice apart from finitely
many `n`, for fixed `q`, `r`, and `lambda`, the Existence Conjecture. It says that the paper proves
the conjecture in general. The paper's Theorem 1.4 is a more general typical-hypergraph
decomposition theorem; its text says constant-multiplicity designs follow from Theorem 1.10.

This matches the catalog gloss unusually well and the surname differs by only a few letters. It
still does not establish identity. The repository spelling, collective attribution, twentieth-century
period, absent parameter contract, and absent locator do not select this source or distinguish its
exact design corollary from its decomposition theorems. No Keevash proposition is therefore adopted
as the canonical target, no source status is upgraded to H0, and the PDF is not added as a
repository-owned source packet.

Version selection is substantive. The v4 acknowledgements report an error found in the first
version and another error in a simplification between the first two versions. If this candidate is
ever admitted, its correction history and the relationship between the chosen corollary and the
general Theorems 1.4 and 1.10 must be audited; an early-version citation cannot be inherited.

## Alternative family boundary

The Keevash paper itself distinguishes the general exact result from Wilson's resolution of the
`r = 2` case and from the Erdos-Hanani/Rodl approximate-design result. That distinction matters here:
the catalog places Wilson's theorem in `THM-M-0899`, immediately before this target, while an
approximate packing theorem does not assert exact coverage. A spelling correction, a Wilson
specialization, a Steiner-system specialization, and a general hypergraph-decomposition theorem
are not interchangeable statements.

## Required source admission

Before the statement phase can leave `H5`, an accountable reviewer must correct or confirm the
catalog identity from an immutable authoritative source; reconcile the name, attribution, and date;
select a precisely located theorem or corollary; transcribe every definition, ordered binder,
hypothesis, divisibility condition, threshold dependency, conclusion, and exceptional case; audit
versions, corrections, and errata; and justify why the result belongs to `THM-M-0900` rather than a
neighbor. A second reviewer must approve that mapping.

Only then may a statement worker encode the same claim in Lean, minimize imports, serialize its
elaborated expression and environment, check alternate transports, and run the required statement
mutations. Until then the canonical mathematical statement, Lean expression, expression hash, and
checked transports remain null.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded
case-insensitive search found no `Keighery`, `Keevash`, block-design, Steiner-system, or `t`-design
target. Pinned `Finset.powersetCard`, `Finset.mem_powersetCard`,
`Finset.card_powersetCard`, and `Nat.choose` are useful adjacent APIs only. This is intake discovery,
not the later exhaustive anchor audit and not evidence of a source-faithful formal theorem.
