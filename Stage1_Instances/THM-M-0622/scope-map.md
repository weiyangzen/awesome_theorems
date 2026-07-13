# Scope map

## Received scope

The catalog fixes a recognizable family: a continuous function on a closed subset of a normal
space extends continuously to the ambient space. It does not say which continuous functions,
codomain, range or norm guarantee, or convention for normality is intended. Stage0 explicitly
leaves the exact definitions, assumptions, proof route, equivalent forms, axioms, machine status,
and formal artifacts open.

## Source boundary

Tietze's 1915 article, *Uber Funktionen, die auf einer abgeschlossenen Menge stetig sind*, was
inspected from the Göttingen digitization. On printed page 14, Satz 3 states that a bounded
continuous real-valued function on a closed subset `T` of a Frechet class `E` extends to a
continuous function on all elements of `E`. Here a Frechet class is a metric space as defined on
printed page 12. The scan supports the attribution and a precise historical result, but independent
German transcription/translation, proof mapping, corrections, and the transport from metric
spaces to the catalog's general normal-space wording remain open.

## Decisions required at statement freeze

1. Admit one source-faithful root: Tietze 1915 Satz 3, the standard real-valued theorem on a normal
   space, or an explicitly reviewed implication/transport between them.
2. Fix the codomain as `Real` or justify a broader target such as `Complex`, a finite-dimensional
   real vector space, or an abstract `TietzeExtension` space. These are not definitionally the same
   theorem.
3. Decide bounded versus arbitrary continuous functions and whether preserving an interval, sign,
   range bounds, or the bounded-function norm is part of the conclusion.
4. Fix the separation convention. Mathlib's `NormalSpace` means separation of disjoint closed sets
   and does not include `T1Space`; `T4Space` adds `T1Space`. Historical and modern sources vary.
5. Fix the ambient universe, `TopologicalSpace X`, closed subset `s : Set X`, subtype-domain
   encoding, ordered binders, implicit typeclass assumptions, and equality versus pointwise
   extension conclusion.
6. Decide whether empty `X` or `s`, singleton spaces, constant and unbounded functions, and
   non-T1 normal spaces are included. The generic mathlib interface has no nonempty hypothesis.
7. Freeze checked transports among a bundled continuous-map restriction, an unbundled pointwise
   equation, a closed embedding, and any bounded or interval-preserving form.
8. Independently review the primary scan, exact transcription and translation, incorporated
   definitions, proof boundary, corrections and errata, and source-to-modern implication.

## Candidate formal surfaces not selected

- `ContinuousMap.exists_restrict_eq` expresses extension from a closed subset of a mathlib
  `NormalSpace` into any codomain with `TietzeExtension`; specializing the codomain to `Real` is a
  natural modern candidate.
- `BoundedContinuousFunction.exists_norm_eq_restrict_eq_of_closed` is a stronger same-norm theorem
  for bounded real-valued maps and is close to the historical bounded clause.
- `ContinuousMap.exists_restrict_eq_forall_mem_of_closed` handles arbitrary real-valued continuous
  maps while preserving a nonempty order-connected range set.
- `Real.instTietzeExtension` packages the real-valued full theorem; complex and finite-dimensional
  vector codomains live in `Mathlib.Analysis.Complex.Tietze`.
- Mathlib's `docs/1000.yaml` maps the named 1000-theorems entry to the bounded closed-embedding
  declaration. That is discovery metadata, not a source-identity certificate.

## Explicit exclusions

- Do not replace the general family with an interval-only, bounded-only, Euclidean-only, compact,
  metric, complex-valued, vector-valued, or closed-embedding form without an approved transport.
- Do not silently add `T1Space` or silently omit it; normality conventions must be source-mapped.
- Do not confuse Urysohn's lemma, Dugundji's extension theorem, Whitney extension, a retraction
  theorem, or an extension from a dense set with this target.
- Do not encode the result as `TietzeExtension Real`, a structure field, an axiom, or a hypothesis
  and then project the desired existential as if that supplied an independent proof.
- Do not treat the catalog's `已验证` label, the theorem name, the 1000-theorems mapping, an API
  probe, or a successful unrelated build as statement or proof evidence.

## Retry condition

The statement phase may start after an accountable reviewer selects and independently verifies one
immutable source proposition, its definitions and exact scope, and every proposition-changing
transport to the intended normal-space formulation. It must then elaborate that exact Lean target
with minimal pinned imports and run removed-hypothesis, changed-domain, binder-scope, and boundary
mutations.
