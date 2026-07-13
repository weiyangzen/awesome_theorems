# THM-M-0279 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository's real-analysis
record of Holder's inequality. The catalog attributes the result to Otto Holder in 1889 and gives
only the gloss `L^p空间的乘积积分` (the integral of a product in `L^p` spaces). Its `已验证`
(verified) value is untrusted metadata and supplies no source-fidelity or proof credit.

The wording identifies the product-integral Holder family, but not one exact proposition. It does
not select the measure space, scalar codomain, raw functions versus `Lp` classes, absolute/normed
versus signed product, finite versus endpoint exponents, integral convention, hypotheses, binder
order, or boundary cases. The institutional scan of Holder's 1889 paper *Ueber einen
Mittelwerthssatz* is a historical source lead, but it contains finite weighted mean and power-sum
inequalities rather than a verbatim modern measure-integral statement. The exact derivation, modern
source proposition, correction audit, and independent review are not admitted here.

Pinned mathlib contains several close but inequivalent formal surfaces: `(E)NNReal` lintegral
inequalities, Bochner-integral norm and nonnegative-real variants, and a generalized extended-
exponent `eLpNorm` inequality. `IntakeProbe.lean` authenticates those APIs and their axiom reports
only. It does not select or state the canonical target. The separate target `THM-M-0310` owns the
stronger `L^p`-duality family and supplies no statement or proof credit to this target.

The provisional vector is `[H1, M3, R4]`: the classical published theorem family and a concrete
bibliographic lead are known but exact source fidelity remains open; direct pinned exact-topic APIs
elaborate but no canonical root, transport, provenance, or proof is credited; and no source-faithful
proof reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the ambiguity and non-substitution boundaries, while
`task-dag.json` leaves all six downstream phases open. No exact statement, H0, M0, R0, accepted
proof state, audit completion, theorem completion, or master acceptance is claimed.
