# Source-statement crosswalk

| Claim component | Human source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Almost-everywhere convergence of time averages for an integrable observable under a measure-preserving transformation | G. D. Birkhoff, "Proof of the Ergodic Theorem", *Proceedings of the National Academy of Sciences* 17 (1931), 656-660, DOI `10.1073/pnas.17.12.656` | Iterates, normalized finite sums, `Filter.Tendsto`, and almost-everywhere predicates | Primary proof source located, but exact notation/premise and errata crosswalk is not accepted: `H1` |
| Identification of the limit in the general non-ergodic case | Modern formulation: conditional expectation of `f` on the invariant sigma-algebra | Conditional expectation and invariant measurable structure | Required bridge; exact primary/modern theorem pinpoint and Lean API audit remain open |
| "Space average" is the constant `integral f dmu` | Ergodic specialization on a probability space: invariant integrable functions are almost everywhere constant | Ergodicity bridge plus integral normalization | This is the crucial restriction missing from the Stage0 slogan; it requires a checked composition certificate later |
| Almost-everywhere, rather than pointwise-everywhere, equality | The pointwise ergodic theorem's exceptional null set | `∀ᵐ x ∂mu, ...` candidate encoding | The qualifier is mandatory and may not be strengthened without a separate theorem |
| Integrability and measure preservation | Hypotheses of the classical theorem | `MeasureTheory.Integrable f` and a measure-preserving-map predicate/candidate structure | Exact binder order and minimal assumptions are deferred to statement elaboration |

The 1931 paper establishes the historical theorem family but this intake does not claim that its
terminology is already a one-line match for the proposed modern probability-space signature.
The statement phase must freeze whether averages use `Finset.range N`, how division and `N = 0`
are represented, which ergodicity predicate is canonical, and whether the root is real-valued or a
more general Banach-valued theorem. It must also test deletion of ergodicity, preservation, and
integrability, and must distinguish almost-everywhere convergence from `L1` convergence.

Discovery link (not an immutable evidence receipt):

- Birkhoff 1931: <https://doi.org/10.1073/pnas.17.12.656>

No `H0` or machine-closure claim is made. Required follow-up includes obtaining a content-hashed
source copy, page-level premise mapping, errata/correction search, a modern formulation source,
mathlib/external Lean declaration audit, and independent review.
