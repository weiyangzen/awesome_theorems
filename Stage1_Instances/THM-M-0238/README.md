# THM-M-0238 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `阿贝尔定理`
(Abel theorem) in the complex-analysis lane. The repository gives Niels Abel, the year 1827, and
only the gloss `椭圆积分的反演` ("inversion of elliptic integrals"). Its catalog label `已验证`
("verified") is untrusted metadata under rev-5.6 and supplies no human-source or Lean proof credit.

Those fields identify a historical theorem family in which inverting a genus-one elliptic integral
produces elliptic functions. They do not select a proposition. The integral or algebraic curve,
nonsingularity assumptions, normalization, basepoint, path and branch, period lattice, local or
global inverse relation, domain and codomain, and intended conclusion are all open. Choosing a
familiar Legendre, Jacobi, or Weierstrass formulation without a source-approved crosswalk would
broaden or substitute the target.

An immutable scan of Niels Henrik Abel's 1827 *Recherches sur les fonctions elliptiques* was
inspected only far enough to authenticate the bibliographic lead and its opening topic discussion.
No exact source proposition, complete definition chain, proof boundary, correction history, or
independent review is admitted. The separate targets `THM-M-0239` (Jacobi inversion) and
`THM-M-0240` (Abel-Jacobi) prevent silently widening this target to general Abelian integrals or
Jacobians.

The provisional root vector is `[H1, M4, R4]`: a historically proved family and a primary-source
lead are identified, but the exact source statement is not accepted; no source-identical usable
Lean theorem is credited; and no source-faithful proof reconstruction exists. `IntakeProbe.lean`
checks adjacent pinned Weierstrass-function APIs only. No canonical mathematical or Lean
proposition, H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
