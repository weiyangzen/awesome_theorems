# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1640-1645` supplies exactly the Chinese title "Riemann mapping
theorem," Bernhard Riemann, 1851, the gloss "a simply connected domain is conformally equivalent
to the unit disk," high importance, and status `已验证` ("verified"). All six lines entered the
repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
bibliographic work, edition, theorem number, page, definition of domain or conformal equivalence,
hypotheses, proof boundary, errata, or formal artifact.

`Docs/Stage0_Blueprint.md:6302-6327` repeats the gloss while explicitly leaving the target formal
system, logical foundation, precise definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine status, and artifact links open. Its generic planning
text that a closed result is believed to exist is not source evidence. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Source status

The classical theorem is historically established, so the theorem family is provisionally H1
rather than an open mathematical problem. No source is admitted to H0 at intake. The source phase
must identify an immutable primary or authoritative edition, pinpoint the exact theorem and every
incorporated definition, map all assumptions and conclusion clauses, inspect corrections and
errata, record dependent source IDs, and obtain an independent source review. A familiar textbook
formulation or broad historical citation cannot fill the catalog's missing premises by convention.

## Crosswalk

| Repository phrase | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| "domain" | nonempty connected open subset, or another source-defined object | `U : Set ℂ` with explicit `U.Nonempty`, `IsOpen U`, and connectedness assumptions as required | definition and redundant/explicit hypotheses open |
| "simply connected" | path connected plus null-homotopic loops under a fixed convention | `IsSimplyConnected U` and a checked convention bridge | pinned API probed; source equivalence open |
| proper planar domain | exclusion of `U = Set.univ` or an equivalent nontrivial-complement hypothesis | `U ≠ Set.univ`, `∃ z, z ∉ U`, or source-selected equivalent | absent from catalog; essential for truth |
| "unit disk" | open disk `{z : ℂ | norm z < 1}` | `Complex.UnitDisc` or `Metric.ball (0 : ℂ) 1` | both APIs available; representation transport open |
| "conformally equivalent" | global biholomorphism, normally holomorphic in both directions | subtype equivalence/homeomorphism plus analytic forward and inverse predicates | no canonical interface selected |
| existence | a map/equivalence exists for every eligible domain | ordered universal and existential binders | exact binder order open |
| normalized form | optional base-point image and derivative normalization, with uniqueness | additional point binder, normalization hypotheses, and uniqueness conclusion | not present in catalog; excluded unless source-selected |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

## Alternate-form boundary

A conformal equivalence of subtypes, an ambient bijection mapping one set onto another, an analytic
open partial homeomorphism, and a pair of inverse analytic maps are plausible encodings, but none
is credited until the statement phase compiles checked equality, iff, or implication transports.
The general uniformization theorem may imply a planar version only through additional
classification and transport obligations; it is not definitionally the same root.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe
checks the complex unit disk, open sets, simply connected sets, analyticity, homeomorphisms, and
local conformality. A bounded exact-topic search found no Riemann-mapping, biholomorphic-unit-disk,
or conformal-equivalence theorem declaration in pinned mathlib or the repo-local Lean tree. The
probe and search are discovery inputs only. They do not elaborate the target, establish an
expression fingerprint, complete an anchor audit, or supply proof evidence.

A discovery lead for the downstream audit is Vincent Beffara's public `vbeffara/RMT4` project,
reported at immutable revision `69a9efe77e912647d651aa7368856955b24dca2f`. Its `RMT4/Main.lean`
reportedly exposes `RMT` for an open connected proper planar set satisfying a `has_primitives`
hypothesis, with an injective differentiable map whose image is the unit ball. This is not admitted
machine evidence: the revision was not fetched into this worker, and exact source/target identity,
the simple-connectedness-to-primitives bridge, proof-body provenance, placeholders, axioms, trust,
license, toolchain compatibility, and repo-local integration all belong to
`S56-M-0227-ANCHOR_AUDIT`. No M1 or stronger status is assigned.
