# THM-M-0233 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the argument principle. The
repository supplies the Chinese title `辐角原理`, attributes it to Augustin Cauchy in 1831, and
gives only the gloss `全纯函数零点与极点个数公式` (a formula counting zeros and poles of a
holomorphic function). Its `已验证` label is untrusted catalog metadata under rev-5.6, not a
source audit, an exact Lean proposition, or proof evidence.

The gloss identifies a classical theorem family but is not binder complete. Taken literally,
"holomorphic" conflicts with the mention of poles unless it means meromorphic, analytic except at
poles, or holomorphic on a punctured region. The record also omits the contour class and
orientation, the domain and interior, boundary nonvanishing and pole exclusions, multiplicity,
whether the root is the logarithmic-derivative integral formula, the phase-change formula, or both,
and every degenerate case. Intake does not silently choose those proposition-changing clauses.

NIST DLMF version 1.2.7, section 1.10(iv), "Phase (or Argument) Principle," equation 1.10.9 was
inspected as an authoritative modern source lead. It states, for a positively traversed closed
contour `C`, that when the singularities inside `C` are poles and `f` is analytic and nonvanishing
on `C`,

```text
N - P = (1 / (2*pi*i)) * integral_C (f'(z) / f(z)) dz
      = (1 / (2*pi)) * Delta_C phase(f(z)),
```

where `N` and `P` count zeros and poles inside `C` with multiplicity. This strongly disambiguates
the family, but the catalog does not cite DLMF, the inherited simple-contour/interior and
analyticity conventions still require an exact definition crosswalk, and no independent source
review is recorded. It is therefore an `H1` lead, not `H0` evidence.

Pinned mathlib provides meromorphic orders and divisors, logarithmic derivatives, circle
integrals, and Jensen's formula. `IntakeProbe.lean` authenticates representative interfaces. A
bounded search found no named terminal argument-principle or winding-number declaration. Jensen's
formula and Cauchy-integral lemmas are ingredients or related results, not substitutes for the
source claim.

The provisional vector is `[H1, M4, R4]`: a modern statement lead is inspected but exact source
identity, assumptions, corrections, and independent review are open; no usable exact formal
artifact is credited; and no source-faithful proof reconstruction exists. `instance.json` is the
structured scope authority and `task-dag.json` keeps all six downstream phases open. No H0, M0,
R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
