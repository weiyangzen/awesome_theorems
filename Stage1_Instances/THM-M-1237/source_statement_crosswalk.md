# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Supercritical first-order embedding | L. C. Evans, *Partial Differential Equations*, 2nd ed., AMS GSM 19 (2010), section 5.6.3, Theorem 6 (Morrey's inequality) | future exact root in `AwesomeTheorems.Stage1.S1_M_175` | Primary textbook theorem family located; edition scan, exact page/formula, hypotheses, and errata still require audit, so no `H0` claim |
| Holder exponent `alpha = 1 - n/p` when `p > n` | Evans, section 5.6.3, Morrey inequality and the subsequent Sobolev-space consequence | `HolderOnWith`-based conclusion candidate | Exponent convention and endpoint exclusions must be checked against the source and Lean API |
| Passage from smooth Euclidean functions to `W^{1,p}` classes | Evans, sections 5.2 and 5.6 (weak derivatives, approximation, inequalities) | `MemLp`, weak-derivative, AE representative, and density APIs | The historical file exposes candidate data but does not supply an accepted weak-derivative/Sobolev-space bridge |
| Bounded-domain conclusion | R. A. Adams and J. J. F. Fournier, *Sobolev Spaces*, 2nd ed., Academic Press (2003), embedding/extension-domain chapters | extension operator, restriction, and closure-domain Holder statement | Corroborating monograph only at intake; exact theorem number/page and domain regularity crosswalk remain open |
| Quantitative norm estimate | Same Morrey-Sobolev sources; constant depends on dimension, exponent, and domain/extension data | normed embedding theorem candidate | Constant dependencies and norm normalization must be frozen, not hidden in an unconstrained proposition field |

The title “Sobolev embedding theorem” names a family, not one proposition. This intake selects the
supercritical first-order bounded-domain form because it matches the legacy description “Sobolev
space into continuous functions” while retaining the stronger Holder exponent and estimate that
make the mathematical boundary testable. The critical (`p = n`) and subcritical (`p < n`) targets
have different codomains and are excluded rather than silently merged into this root.

The historical local `StatementShape` is not treated as a source-statement match: Sobolev
membership, the exponent gap, the extension package, agreement of representatives, and the
embedding estimate are partly opaque `Prop` fields. The statement phase must replace or refine this
with concrete definitions, inspect actual declaration types, serialize the normalized expression,
check all transports, and mutation-test dimension, exponent, domain, representative, and boundary
conditions.

No immutable source receipt or `H0` status is asserted. Follow-up work must record exact edition
files/hashes, pages and displayed formulas, source assumptions, known errata, and independent review.
