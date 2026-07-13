# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1647-1652` supplies exactly the Chinese title "Little Picard
theorem," Emile Picard, 1879, the gloss "a nonconstant entire function takes all complex values
with at most one exception," high importance, and status `已验证` ("verified"). All six uncited
lines entered the repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record
contains no bibliography, formula, definitions, ordered binders, proof boundary, corrections,
errata, or formal artifact.

`Docs/Stage0_Blueprint.md:6329-6354` repeats the gloss while explicitly leaving the formal system,
logical foundation, precise definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine state, and artifact links open. Its generic planning language is not
theorem evidence. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets
the target to `L0 / rework_required`.

## Source status

The classical theorem family is historically established, so it is provisionally `H1`, not an open
problem. No source is admitted to H0. Immutable revision 48178 (6 June 2020) of the Encyclopedia of
Mathematics entry "Picard theorem" was inspected. It states that any nonconstant entire function
takes every finite complex value with possibly one exception, and equivalently that a holomorphic
map from the complex plane to itself omitting at least two points is constant. It cites Picard,
"Sur une propriete des fonctions entieres," *C.R. Acad. Sci. Paris* 88 (1879), pages 1024-1027,
and later Picard sources. This is a pinpoint authoritative secondary statement and primary-source
lead, but not an inspected proof passage or accepted source packet. One observed live HTML response
had SHA-256 `a8dfc1c128ae962f9dc3fabddc057a4e191c1ea8631fee95bac4d894c9cf09d7`;
the wrapper bytes varied on repeat access, so only `oldid=48178` is treated as the content-revision
identity and the response hash is not presented as a stable source pin.

Separately, a NUMDAM copy of E. Picard, "Sur une classe de fonctions non
uniformes," *Bulletin de la Societe Mathematique de France* 7 (1879), pages 102-104, DOI
`10.24033/bsmf.163`, was inspected because its author and year match the catalog. Its text concerns
series representations of multivalued functions near prescribed branch points, not the catalog's
entire-function range statement. It is therefore rejected as a proof source for this target. This
negative source check prevents a same-year citation from being silently promoted to H evidence.

The statement/source phases must locate and preserve the actual theorem passage and incorporated
definitions, record edition and page/theorem identifiers, map every assumption and conclusion,
audit proof dependencies and errata, and obtain an independent review. A familiar textbook slogan
or historical date cannot fill those fields by convention.

## Component crosswalk

| Repository phrase | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| "function" | complex-valued map on the whole complex plane | `f : ℂ -> ℂ` | recognizable domain; exact binder freeze pending |
| "entire" | holomorphic at every finite complex point | `Differentiable ℂ f` or `AnalyticOnNhd ℂ f Set.univ` | pinned APIs exist; source convention and transport open |
| "nonconstant" | no single value is taken at every input | `not exists c, f = Function.const Complex c`, or an explicitly equivalent witness form | encoding and binder order open |
| "takes all complex values" | membership in the image/range | `w ∈ Set.range f`, equivalently `exists z, f z = w` | representation transport open |
| "with at most one exception" | the omitted-value set has cardinality zero or one | `((Set.range f)ᶜ).Subsingleton` or `encard <= 1` | most direct candidates; neither selected yet |
| exceptional-value form | there exists `a` such that every `w != a` is attained | `exists a, forall w, w != a -> exists z, f z = w` | candidate equivalent classically; witness may be attained |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be needed | no H or M credit |

## Neighbor and strength boundary

The target is global on the complex plane. `THM-M-0229` concerns neighborhoods of essential
singularities and cannot donate its statement or proof. `THM-M-0224` and `THM-M-0235` record
Liouville and open mapping respectively; those may become proof ingredients but are weaker than
the Little Picard root. The catalog says nothing about values being taken infinitely often, so the
stronger multiplicity conclusion often associated with Big Picard is outside this intake.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
elaborates relevant differentiability, analyticity, range, subsingleton/cardinality, Liouville,
open-mapping, meromorphic, and value-distribution interfaces. The pinned value-distribution tree
contains the first main theorem but no second main theorem or evident Little Picard declaration.
It also checks `Complex.differentiable_exp` and `Complex.range_exp`, which show within the pinned
environment that the exponential is entire and has range `{0}ᶜ`; this is sharpness evidence only.
A bounded search of pinned mathlib, the pinned `flt-regular` dependency, and repo-local Lean sources
found no exact terminal theorem. These are discovery observations only: the downstream anchor audit
must precommit a broader query ledger, inspect candidates and proof-body provenance, and decide
integration status at immutable revisions.
