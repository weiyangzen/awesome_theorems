# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records only the title `超紧基数`, attributes it to "many
mathematicians", dates it to the twentieth century, and says `超紧基数的性质` ("properties of
supercompact cardinals"). Stage0 repeats this and leaves the exact definition, assumptions, proof,
dependencies, axioms, and formal artifact open. The rev-5.6 manifest preserves `已验证` solely as
`source_status_untrusted`.

These records provide no theorem, definition variant, edition, page, hypotheses, conclusion, or
proof source. The intake therefore cannot truthfully assign a canonical proposition or `H0` status.

## Candidate source work

The later source audit must locate an immutable primary or authoritative passage defining
supercompactness and an exact theorem stating the intended property. It must record edition,
definition/theorem number and page, assumptions, proof boundary, corrections/errata, and an
independent review. General textbook knowledge that standard embedding and fine-normal-ultrafilter
formulations are related is only a search map, not an accepted equivalence or source crosswalk.

## Crosswalk

| Repository phrase | Mathematical choice still required | Required Lean component | Intake status |
|---|---|---|---|
| "cardinal `kappa`" | initial ordinal/cardinal and ambient universe conventions | `Cardinal`, lifts, ordinal/cardinal interfaces | nearby API probed; exact domain open |
| "supercompact" | embedding or ultrafilter definition and exact quantification over `lambda` | encoded membership models plus elementary embedding, or fine normal complete ultrafilter on `P_kappa(lambda)` | absent |
| "properties" | one precise implication, equivalence, existence, or consequence | concrete proposition with ordered binders and hypotheses | absent |
| target model closure | internal/external sets, transitivity, `lambda`-sequence closure | ZF/ZFC model semantics and closure predicate | absent |
| `已验证` | untrusted inventory label | no proposition and no proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe
checks `Cardinal`, `Cardinal.IsRegular`, `Cardinal.IsInaccessible`, `Ultrafilter`, first-order
`ElementaryEmbedding`, and `ZFSet`. They show that neighboring encoding ingredients exist. They do
not define supercompactness or supply an exact property theorem. A bounded name/content search found
no supercompact-cardinal declaration in pinned mathlib; this negative result is not a substitute for
the later immutable formal-anchor audit.
