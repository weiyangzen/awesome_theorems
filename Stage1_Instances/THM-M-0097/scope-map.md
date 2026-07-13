# Scope map

## Preserved theorem family

The intake preserves the semisimple-Lie-group character family indicated by the catalog. The 1951
source lead may root the claim at the trace/distribution-character construction, while a likely
later root says that this distribution is represented by a locally integrable or analytic
function on a regular locus. This is a scope description, not a frozen canonical proposition.

The inspected 1956 paper proves in Theorem 6 that the character of a `quasi-simple`
representation of a connected semisimple Lie group coincides with an analytic function on its
set of quasi-regular elements. Later results and modern references often package stronger or
differently stated regularity, local-integrability, or character-formula theorems. The statement
phase must select exactly one source-rooted claim rather than merge these variants.

## Decisions required at statement freeze

1. Select the exact source result: a trace/distribution construction from the 1951 note, the 1956
   Theorem 6, a later global regularity theorem, a local-integrability theorem, or a formula.
2. Fix whether the group is connected semisimple, reductive, linear, finite-center, real or
   complex, and record every topology, smooth-manifold, Haar, and countability hypothesis.
3. Define the representation class: the paper's `quasi-simple` Hilbert-space representations,
   irreducible admissible representations, Harish-Chandra modules, or another source class.
4. Define the character construction, including the test-function space, integrated operator,
   trace or summability condition, Haar normalization, and equality of distributions.
5. Define regular, regular semisimple, and quasi-regular elements and decide the exact open locus.
6. Choose the conclusion: analytic representation on the locus, local integrability on all of the
   group, equality almost everywhere, or an explicit Cartan/Weyl formula.
7. Fix real versus complex scalars, Lie algebra complexification, universal-enveloping-algebra
   center, central and infinitesimal characters, and all action/inverse conventions.
8. Freeze ordered binders, universe levels, typeclasses, hypotheses, conclusion, foundation/TCB/
   computation profiles, minimal imports, and any alternate encodings with checked transports.

Each choice changes the proposition or proof boundary. Intake leaves it open.

## Boundary and degenerate cases

Source review must address the trivial group; compact versus noncompact groups; groups with
nontrivial or infinite center; disconnected groups; finite-dimensional and trivial
representations; zero character; singular elements and the complement of the chosen regular
locus; whether quasi-regular is strictly larger than regular; Haar rescaling; empty support; and
real-valued versus complex-valued test functions. It must also distinguish equality as
distributions, pointwise equality on an open set, and almost-everywhere equality of locally
integrable representatives.

## Excluded substitutions

- The Weyl character formula for finite-dimensional compact-group representations is a different
  target and does not prove Harish-Chandra regularity for infinite-dimensional representations.
- Weyl's dimension formula, Peter-Weyl completeness, Plancherel, Paley-Wiener, orbital-integral,
  discrete-series existence, local trace formula, and local Langlands are distinct results.
- Algebraic `Representation`, `LieAlgebra.IsSemisimple`, Haar-measure, distribution, or local-
  integrability infrastructure alone does not construct a distribution character or prove its
  regularity.
- An analytic theorem only for compact groups or finite-dimensional representations cannot replace
  a selected noncompact semisimple-group root.
- An explicit formula on one Cartan subgroup does not by itself establish global distributional
  regularity or local integrability.
- A structure carrying `realizesHarishChandraCharacter : Prop`, or a theorem returning data already
  stored in a field, supplies no root proof.
- A bounded search, theorem name, `#check`, numerical character table, or the untrusted `已验证`
  label supplies no H or M credit.

## Neighbor boundaries

`THM-M-0089` owns Peter-Weyl, `THM-M-0090` the Weyl character formula, `THM-M-0091` the Weyl
dimension formula, and `THM-M-0092` the Cartan-Weyl theorem. `THM-M-0063` owns local Langlands and
contains only abstract Hecke/Harish-Chandra data fields. None grants status to this target by name
or proximity.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks adjacent algebraic representation,
semisimple Lie-algebra, Lie-group, Haar-measure, local-integrability, test-function, and
distribution interfaces. Current distribution support is for open subsets of finite-dimensional
real normed spaces and is not already the required global distribution theory on a Lie group.
The bounded exact-topic search found no terminal Harish-Chandra declaration. This is discovery
evidence, not the later exhaustive anchor audit or a proof of global absence.
