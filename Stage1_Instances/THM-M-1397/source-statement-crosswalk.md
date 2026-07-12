# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10174-10179` supplies exactly the title `Adams方法`, attribution
to John Couch Adams, the year 1883, the gloss `多步数值方法`, importance "high," and status
`已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable source ID,
edition, theorem or page locator, recurrence, definition, binder, hypothesis, conclusion, proof
boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:37992-38017` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Inspected source-family discriminator

The Encyclopedia of Mathematics entry "Adams method," permanent revision 45150 dated
2020-04-04, was inspected as an authoritative discovery lead. Its stable revision wikitext has
MediaWiki SHA-1 `ffa19fe8b6a9d8b92728115150593fd6e1350407`, 6,158 bytes, and SHA-256
`0c9a9ad1f5a6e7a2a0ec096553e63ab170ee1027b70f56e4bf48dba4fc910fa1`.
Those byte count and SHA-256 values cover `jq -r` extraction, including its final newline. The raw
6,157-byte wikitext content has SHA-256
`79d65c537e31ebb8591b725ed6671cbaccf818faec85ba6f2bdab21b52f3c7e2`.

The entry describes a finite-difference method for the Cauchy problem `y' = f(x,y)`, first giving
an explicit extrapolation recurrence and then an implicit interpolation recurrence on a constant
grid. It separately states that the implicit formula is more accurate for a fixed index, discusses
a predictor-corrector iteration with a pointwise convergence condition, starting values, an
asymptotic error expression, a scalar-test-equation instability condition, and practical claims.
Its comments identify explicit special cases as Adams-Bashforth methods and implicit special cases
as Adams-Moulton methods.

This multiplicity confirms rather than resolves the catalog ambiguity. The catalog does not cite
the entry, disagrees with its historical date (1883 versus the entry's 1855), and does not select
one formula or result. The entry is a tertiary reference with its own cited sources, not an admitted
primary proof source. No immutable H0 admission, exact proposition, complete assumption and proof
mapping, errata audit, historical reconciliation, or independent review is credited.

## Component crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `Adams方法` | explicit, implicit, or paired multistep construction and associated results | no single declaration follows from the name | method family, not a unique proposition |
| `多步` | dependence on several previous grid values or derivative samples | natural step count, finite index type, history sequence, coefficient vector | count and indexing absent |
| `数值方法` | recurrence, algorithm, approximation, order, convergence, stability, or error theorem | exact `Prop` plus numerical scheme and error definitions | conclusion absent |
| John Couch Adams / 1883 | historical metadata | provenance metadata only | no cited source; inspected lead says 1855 |
| `已验证` | untrusted inventory field | accepted source proof and kernel receipt would be required | no H or M credit |

## Formula-to-theorem boundary

A recurrence definition is not a theorem about accuracy or convergence. Deriving Adams coefficients
from a Lagrange interpolant requires a selected node convention and an integral identity. Local
truncation order does not alone imply global convergence; a convergence theorem needs consistency,
stability and problem regularity in an exact formulation. An implicit Adams-Moulton step also needs
solvability or a specified correction iteration. These boundaries must remain separate downstream
obligations rather than being smuggled into a data structure or premise.

The inspected source's error, stability and practicality passages likewise are not interchangeable
with the explicit or implicit recurrence definitions. No checked implication or equivalence among
candidate roots exists at intake.

## Neighbor and substitution boundary

The surrounding catalog separately names finite-difference methods (`THM-M-1395`), Runge-Kutta
methods (`THM-M-1396`), stiff equations (`THM-M-1398`), and backward differentiation formulas
(`THM-M-1399`). Their broad classes, one-step schemes, problem regimes, and different multistep
coefficients cannot be substituted for Adams methods or inherit proof credit from this intake.

## Source gate

There is no authoritative mathematical proposition selected by the repository. Before leaving
`H5`, an accountable reviewer must redirect the method label to one corrected exact proposition,
preserve an immutable primary or authoritative source, record edition and theorem/section/page,
transcribe the chosen scheme and every incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, and exceptional case, reconcile the 1855/1883 provenance discrepancy,
audit corrections, distinguish all neighboring targets, and obtain independent approval of the
source-to-statement mapping.

`H5` here does not assert that Adams numerical methods are false. It records that the repository
gloss does not determine a truth-valued target that a Lean kernel could check. No H0 crosswalk can
be completed until a proposition is selected.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks `Lagrange.interpolate`, `Lagrange.eval_interpolate_at_node`, `intervalIntegral`,
`IsIntegralCurve`, and `Finset.sum`. These are possible substrate for a future source-selected
encoding, not an Adams statement or proof. A bounded case-insensitive search for numerical
Adams-Bashforth, Adams-Moulton, and multistep terms over pinned mathlib and repo-local Lean sources
found no target occurrence; unrelated Adams spectral-sequence and data-structure names were
excluded. The later immutable formal-candidate audit remains open.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, and statement mutations therefore remain null. No statement elaboration,
formal absence theorem, proof, audit completion, or theorem completion is claimed.
