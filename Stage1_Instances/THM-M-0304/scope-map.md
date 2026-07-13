# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0304`, the label `莫里定理`, the attribution Charles Morrey, the
year 1940, and the gloss `Sobolev函数的Holder连续性`. Importance `高` and status `已验证` are
inventory metadata, not mathematical-source or kernel evidence.

The gloss identifies a Morrey-Sobolev Holder-continuity family. It does not select one Sobolev
space, domain, exponent regime, representative relation, estimate, or source theorem.

## Proposition-changing decisions

The statement phase must freeze all of the following from an approved pinpoint source:

- Euclidean, manifold, metric-measure, or other domain; dimension; local, whole-space, compact-
  support, bounded-domain, or closure scope; measure, topology, and boundary or extension regularity;
- integer or fractional differentiability order, homogeneous or inhomogeneous Sobolev convention,
  weak-derivative or other encoding, and almost-everywhere quotient semantics;
- exponent type and exact dimension-order-exponent relation, including strictness, critical and
  subcritical regimes, and the `p = infinity` endpoint;
- scalar or vector codomain, real or complex scalars, finite-dimensionality, completeness, and every
  other typeclass or universe assumption;
- existence and uniqueness convention for a concrete representative and the exact almost-everywhere
  agreement relation;
- Holder exponent, whether control is local, on the domain, or on its closure, the exact norm or
  seminorm estimate, constant dependencies, and whether a pointwise or supremum bound is included;
- empty or null domain, zero dimension, zero function, zero gradient, disconnected or irregular
  domain, endpoints, and every other degenerate or boundary case.

The familiar candidate `1 <= n < p < infinity`, `alpha = 1 - n/p`, first-order scalar
`W^{1,p}` data, and a Holder representative with a quantitative bound is recorded only as a
candidate family. It is not the canonical statement until the source, duplicate identity, and all
choices above are approved.

## Neighbor and duplicate boundaries

- `THM-M-1242` (`Morrey不等式`) has the same catalog attribution, year, and gloss under a distinct
  PDE title and target ID. Identity, variant selection, and proof ownership remain integration-lane
  decisions; its dossier supplies discovery only.
- `THM-M-0303` (`索伯列夫嵌入定理`) is the broader real-analysis Sobolev embedding target and may
  not be substituted for this Morrey-labeled root.
- `THM-M-1237` (`Sobolev嵌入定理`) is a separately retained PDE target whose selected
  supercritical bounded-domain statement and Lean artifacts do not transfer to this ID.

## Explicit non-substitutes

- a smooth compact-support Gagliardo-Nirenberg-Sobolev norm inequality without a Sobolev-class
  representative or Holder estimate;
- generic `HolderOnWith` infrastructure or the implication from Holder control to continuity;
- plain continuity without the source-selected Holder exponent and quantitative estimate;
- one special dimension, smooth-function case, endpoint, vector-valued, higher-order,
  metric-measure, Campanato, or Morrey-space generalization selected only for convenience;
- a structure, predicate, certificate, or hypothesis that stores the desired representative,
  agreement, Holder control, or estimate as assumed data;
- the untrusted catalog status, a citation, a declaration name, or a successful API probe used as
  statement or proof evidence.

## First downstream blocker

Before statement execution, accountable reviewers must resolve the `THM-M-0304` / `THM-M-1242`
identity and ownership boundary, select a lawful immutable primary or authoritative edition,
inspect the 1942 correction and any other errata, and approve an exact row-by-row map of definitions,
ordered binders, hypotheses, conclusion, proof boundary, constant conventions, and degenerate cases.
