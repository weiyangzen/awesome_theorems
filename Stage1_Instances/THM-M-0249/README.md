# THM-M-0249 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named Mergelyan's
theorem. The repository attributes it to Sergei Mergelyan in 1951 and supplies only the gloss
"polynomial approximation of continuous functions on compact sets." Its `已验证` ("verified")
label is untrusted metadata under rev-5.6, not a source audit or machine-proof claim.

The gloss identifies the classical complex polynomial-approximation family, but it omits clauses
that make the theorem true: the compact subset of the complex plane must have connected
complement, and the continuous function must be holomorphic on the set's interior. It also does
not fix the uniform-approximation formulation, positivity and quantifier order for the error,
polynomial evaluation encoding, or boundary cases. Intake does not silently add those clauses.

An immutable secondary source snapshot and a versioned modern paper were inspected as source
leads. They agree on the standard family: for compact `K` in `C` with connected complement, each
complex-valued function continuous on `K` and holomorphic on its interior is uniformly
approximable by complex polynomials. They also point to Mergelyan's 1951 and 1952 works. Neither is
the catalog's cited primary edition, and no primary theorem/page, definition chain, errata audit,
or independent review is admitted. They support only provisional `H1`.

Pinned mathlib provides complex analytic predicates, compactness and connectedness, polynomial
evaluation, and continuous-map polynomial APIs. It also proves real Weierstrass approximation and
complex Stone-Weierstrass density only after adjoining conjugation. `IntakeProbe.lean`
authenticates these adjacent interfaces and the non-substitution boundary. A bounded topic search
found no exact Mergelyan declaration. No canonical mathematical or Lean statement is frozen.

The provisional vector is `[H1, M4, R4]`: a credible source route exists but exact primary-source
fidelity is unaudited; no usable exact formal proof is credited; and no source-faithful readable
proof reconstruction exists. `instance.json` is the structured scope authority and `task-dag.json`
keeps all six downstream phases open. No H0, M0, R0, accepted state, audit completion, theorem
completion, or master acceptance is claimed.
