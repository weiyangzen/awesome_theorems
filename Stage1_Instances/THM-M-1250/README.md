# THM-M-1250 rev-5.6 intake

This is the `planned` dossier for the Stage0 entry "Schwartz space" (`Schwartz空间`), whose source
gloss is "the space of rapidly decreasing functions". The source entry names a mathematical
object, not one particular proposition. Accordingly, intake freezes the object-level scope without
inventing a theorem: the dependent statement phase must select and justify an exact proposition.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Canonical object | smooth scalar-valued functions on a finite-dimensional real vector space whose derivatives decay faster than every polynomial | This descriptive definition is not yet an elaborated Lean proposition |
| Lean representation | mathlib's `SchwartzMap E F`, notation `𝓢(E, F)` | Candidate discovered through repo-local imports; exact type and minimal import remain unchecked |
| Defining conditions | smoothness and weighted derivative/seminorm bounds | Equivalence between the human definition and mathlib's representation remains a statement obligation |
| Core structure | zero/addition/scalar multiplication and the locally convex/topological structure exposed by mathlib | No closure or theorem credit is claimed |
| Closure operations | differentiation, multiplication by polynomial/coordinate functions, Fourier transform | Candidate downstream scope only; each needs an explicit selected proposition |
| Domains | canonical human scope: `R^n -> C`, `n >= 0`; possible Lean generalization to normed spaces | A broader polymorphic mathlib type may not silently replace the canonical finite-dimensional claim |
| Exclusions | tempered distributions, the strong dual, distributions of compact support, and PDE results using test functions | These are adjacent theories, not this target |

The intake lifecycle is `planned`, with provisional vector `[H2, M3, R3]`. The first failed gate is
the exact-statement gate: the metadata does not specify a proposition, and there is no expression
fingerprint, environment fingerprint, checked transport, or mutation result. This dossier therefore
does not claim theorem completion or inherit the untrusted Stage0 label `已验证`.

