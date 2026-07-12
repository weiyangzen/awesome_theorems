# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2216-2221` supplies exactly the name
`Rellich-Kondrachov紧嵌入定理`, attribution Franz Rellich / Vladimir Kondrachov, year 1930,
the gloss `Sobolev空间的紧嵌入`, importance "high", and status `已验证`. Git blame places
all six uncited lines at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, definition,
domain, exponent, hypothesis, conclusion, proof boundary, or formal artifact.

`Docs/Stage0_Blueprint.md:8521-8546` repeats that gloss while leaving the formal system,
foundations, exact definitions and premises, proof route, dependencies, equivalent statements,
logical principles, machine status, and artifact links open. Its generic assertion that a closed
result is known is not source evidence. Rev-5.6 therefore retains `已验证` only as untrusted
metadata and resets this target to `L0 / rework_required`.

The attribution/date pair also needs review: the repository combines Rellich and Kondrachov but
gives only 1930, while its own discovery material lists a 1930 Rellich paper and a 1945 Kondrachov
paper. Intake does not manufacture a single joint 1930 source.

## Duplicate-target boundary

`Docs/researches/math_theorems.md:9045-9050` contains the same broad gloss under the shorter name
"Rellich-Kondrachov theorem" in the PDE category. Rev-5.6 maps that record to the distinct target
`THM-M-1238`. The two IDs may later select the same proposition, different variants, or require a
catalog deduplication decision, but no such decision is accepted here. Neither target inherits the
other's statement, state, or evidence.

## Source leads, not H0 evidence

The distinct `THM-M-1238` intake records three bibliographic leads:

- Franz Rellich, "Ein Satz uber mittlere Konvergenz," *Nachrichten von der Gesellschaft der
  Wissenschaften zu Gottingen, Mathematisch-Physikalische Klasse* (1930), 30-35.
- V. I. Kondrachov, "On certain properties of functions in the space Lp," *Doklady Akademii Nauk
  SSSR* 48 (1945), 563-566.
- Robert A. Adams and John J. F. Fournier, *Sobolev Spaces*, second edition, Academic Press (2003),
  Chapter 6 compact embedding results.

This intake inspected the repository's bibliographic record, not immutable copies of those
sources. The leads supply no accepted theorem/page transcription, definition chain, premise and
assumption mapping, proof boundary, correction/errata result, or independent review. They are
therefore discovery inputs only, not `H0` evidence. The modern formulation must not be silently
attributed verbatim to either historical paper.

## Crosswalk

| Repository phrase | Mathematical choice that must be sourced | Required Lean component | Intake status |
|---|---|---|---|
| "Sobolev spaces" | order, weak derivatives, `W^{k,p}` or `W_0^{k,p}`, norm, scalars | concrete function space or predicate with its topology and norm | family only; all choices open |
| "embedding" | source and target spaces plus canonical inclusion | explicit continuous linear map or source-matched map | absent |
| "compact" | compact operator, compact bounded images, relative compactness, or subsequence form | `IsCompactOperator`, `IsCompact`, closure/image, or a checked equivalent | conclusion kind known; representation open |
| domain | Euclidean set or manifold, dimension, boundedness, boundary/extension regularity, measure | domain type/set, restricted measure, regularity predicates | absent |
| exponents | `p`, `q`, Sobolev order, subcritical inequality, endpoints | exponent types, arithmetic, and side conditions | absent |
| Rellich / Kondrachov | historical variant and genealogy selected by a pinpoint source | no direct machine credit | two source leads and inconsistent catalog date |
| 1930 | possible Rellich publication year | no proposition or proof credit | cannot date Kondrachov's later generalization without review |
| `已验证` | untrusted catalog status | no Lean expression or kernel evidence | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
elaborates general `L^p`, compact-operator, bounded-image, and Sobolev-inequality APIs. A bounded
name search for `Rellich`, `Kondrachov`, and `RellichKondrachov` finds no matching mathlib source.
The available `SobolevInequality` declarations are continuous estimates for sufficiently smooth
compactly supported functions, not a compact embedding theorem.

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_176.lean`, owned by the distinct
`THM-M-1238`, reports an external `abenenson/rellich-kondrachov` project and a revision. This intake
did not fetch, pin, import, or recheck that project. The legacy `RellichKondrachovData` also stores
the desired compact embedding as a field, so its projection does not encode or prove a
source-faithful Rellich-Kondrachov theorem. Comprehensive formal discovery and terminal-body audit
remain the downstream anchor-audit task after statement identity is fixed.

Before `H0`, an independent reviewer must approve an immutable source edition and exact locator,
the complete row-by-row statement and assumption mapping, historical attribution, translations,
corrections and errata, and the relationship to the duplicate target.
