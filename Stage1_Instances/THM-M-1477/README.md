# THM-M-1477 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `A-稳定性`
(A-stability). The catalog supplies only the gloss `数值方法的稳定性` (stability of numerical
methods), attributes the item to Germund Dahlquist in 1963, and labels it `已验证`. Those fields do
not form a truth-valued proposition with ordered binders, hypotheses, and a conclusion. The
verified label is untrusted metadata and supplies neither source nor proof credit.

In numerical ODE analysis, A-stability can name a property of a method, a stability-region
inclusion, a scalar stability-function inequality on a left half-plane, or a root condition for a
linear multistep characteristic polynomial. Dahlquist's 1963 work is also associated with the
order barrier for A-stable linear multistep methods. These are not interchangeable statements. The
catalog fixes no method class, test equation and sign convention, stability function or polynomial
pair, root multiplicity condition, half-plane boundary convention, consistency/order assumptions,
or conclusion. Selecting a definition, implicit Euler example, Runge-Kutta criterion, or Dahlquist
barrier theorem would invent proposition-changing mathematics.

Germund G. Dahlquist's article *A special stability problem for linear multistep methods*, BIT 3(1),
27-43 (1963), DOI `10.1007/BF01963532`, was identified through bibliographic metadata as a strong
primary-source lead matching the catalog author and year. The catalog does not cite it, and no
exact proposition, incorporated-definition chain, proof boundary, correction record, or
independent review was admitted. It therefore supplies discovery evidence only, not `H0` credit.

Pinned mathlib supplies generic polynomial evaluation, complex norms, and metric closed-ball
interfaces. `IntakeProbe.lean` authenticates those adjacent APIs only. It neither defines an ODE
method nor states an A-stability predicate or theorem, and it supplies no canonical statement or
proof credit. A bounded exact-topic search found no numerical A-stability declaration in pinned
mathlib or repo-local Lean; the later anchor-audit phase remains responsible for exhaustive
candidate and provenance work.

The provisional vector is `[H5, M4, R4]`. Here `H5` classifies the received label and gloss as not
yet a stable proposition; it does not say that correctly stated A-stability results are false or
open. All six downstream phases remain open. No H0, M0, R0, exact mathematical or Lean statement,
accepted proof state, audit completion, theorem completion, accepted receipt, or master acceptance
is claimed.
