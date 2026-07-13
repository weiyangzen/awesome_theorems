# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:2209-2214` supplies exactly the title `延拓定理`, attribution
Sergei Sobolev, year 1936, the gloss `Sobolev函数的延拓`, importance "high," and status `已验证`.
Git blame places all six uncited lines at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, definition,
domain class, Sobolev space, exponent, hypothesis, conclusion, estimate, proof boundary, or formal
artifact.

`Docs/researches/math_theorems.md:9059-9064` repeats those six lines byte for byte. This is duplicate
repository provenance, not a second source witness or theorem obligation. Unlike nearby duplicated
topics, rev-5.6 contains only one Stage0 and manifest target for this wording: `THM-M-0308`. The
duplicate row therefore creates no second target, denominator entry, source credit, or proof credit.

`Docs/Stage0_Blueprint.md:8494-8519` repeats the gloss while explicitly leaving the formal system,
foundations, precise definitions and premises, proof route, dependencies, equivalent forms,
logical principles, machine status, and artifacts open. Its generic claim that a closed result is
known is not source evidence. Rev-5.6 retains `已验证` only as untrusted metadata and resets this
target to `L0 / rework_required`.

## Component crosswalk

| Catalog component | Mathematical information fixed | Prospective Lean component | Intake assessment |
|---|---|---|---|
| "extension theorem" | a theorem family involving an extension | an existential map, operator, or universal extension construction | exact conclusion and quantifier order absent |
| "Sobolev functions" | some Sobolev regularity is involved | a source-selected `W^{k,p}`, fractional, homogeneous, or zero-boundary space | order, exponent, norm, quotient, and value type absent |
| "extension" | output should agree with input on a domain | restriction or almost-everywhere equality plus weak-derivative compatibility | domain, agreement relation, linearity, boundedness, estimate, and support behavior absent |
| Sergei Sobolev / 1936 | historical metadata lead | immutable source identity and pinpoint crosswalk | no cited work, edition, theorem, page, translation, or genealogy |
| repeated catalog row | duplicate inventory text | no additional Lean node | no independent evidence or denominator credit |
| `已验证` | untrusted inventory label | source review and kernel evidence would be required | no H or M credit |

## Source boundary

No primary or authoritative mathematical source is identified at intake. The label may refer to
several inequivalent modern extension theorems, and the catalog's attribution and date do not
select among their domain, order, exponent, operator, or estimate conventions. Selecting the
standard Lipschitz-domain `W^{k,p}` theorem now would add mathematics absent from the record.

The provisional human status is `H5`: the received target is not yet one stable proposition. This
does not claim that classical extension theorems are false, open, or historically unsupported.
The statement phase must first preserve an immutable source, locate an exact theorem and all
incorporated definitions, map every assumption and conclusion, reconcile genealogy and translation,
inspect corrections and errata, and obtain independent source review.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
general `L^p`, continuous-linear-map, and Sobolev-inequality interfaces. A bounded lexical search
found no exact Sobolev extension declaration in repo-local Lean or pinned mathlib. The historical
`S1_M_175.lean` artifact belongs to `THM-M-1237` and treats a domain extension package as an open
input while explicitly withholding terminal Sobolev-space infrastructure. It is a neighboring
discovery input, not a candidate proof for this target.

These observations are scoped intake evidence only. They are not an exhaustive external-project
search, the downstream immutable anchor audit, a global nonexistence claim, or proof evidence.

## First downstream gate

An accountable reviewer must select and independently approve a pinpoint source proposition fixing
the ambient and domain, extension-domain hypotheses, Sobolev model and parameters, value type,
operator/existence form, restriction identity, norm estimate, constant dependencies, support
behavior, and all endpoint and degenerate cases. Only then may the statement phase choose minimal
imports, serialize the elaborated expression and environment, check alternate transports, and run
the required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
