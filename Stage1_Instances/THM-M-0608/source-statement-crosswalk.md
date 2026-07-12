# Source-statement crosswalk

## Candidate primary sources

- Edward Witten, "Monopoles and Four-Manifolds", *Mathematical Research Letters* **1** (1994),
  769-796, DOI `10.4310/MRL.1994.v1.n6.a13`. This is the primary discovery anchor for the
  four-manifold invariants defined from the monopole equations. The statement phase must inspect a
  stable copy and record exact page/equation/proposition boundaries; this intake has not done that.
- Nathan Seiberg and Edward Witten, "Electric-Magnetic Duality, Monopole Condensation, and
  Confinement in N=2 Supersymmetric Yang-Mills Theory", *Nuclear Physics B* **426** (1994), 19-52,
  DOI `10.1016/0550-3213(94)90124-4`; erratum **430** (1994), 485-486, DOI
  `10.1016/0550-3213(94)00449-8`. This is primary physical background for the low-energy monopole
  theory, but it is not by itself a source for one exact four-manifold invariance theorem.

These entries are discovery anchors only. They have not been pinned as immutable source artifacts,
checked against all errata, crosswalked at theorem/page granularity, or independently reviewed, so
they do not establish `H0` or any machine status.

## Metadata-to-source crosswalk

| Metadata component | Candidate source interpretation | Formal consequence | Intake disposition |
|---|---|---|---|
| "Seiberg-Witten invariants" | Witten's monopole-equation construction yields a family indexed by `Spin^c` data | the index set, codomain, orientation, dimension, and choice-independence theorem must be explicit | family identified; root theorem unresolved |
| "invariants of four-manifolds" | likely diffeomorphism information obtained from moduli-space counts | category of manifolds and precise equivalence notion must be stated | too broad to elaborate |
| year 1994 and authors Seiberg/Witten | points to the papers above | bibliography helps discovery but does not select a theorem | retained as provenance only |
| `已验证` | untrusted Stage0 screening label | supplies neither source review nor kernel evidence | rejected as evidence |

## Required statement crosswalk

Before the next phase can freeze a canonical claim, a source reviewer must:

1. select a stable edition of the primary mathematical source and record a pinpoint statement,
   equations and incorporated definitions by page;
2. enumerate the manifold, orientation, Betti-number, `Spin^c`, genericity, regularity, expected
   dimension, and coefficient hypotheses actually used;
3. distinguish definition of the count from gauge invariance, compactness, transversality,
   orientation, and metric/perturbation independence;
4. record the `b2+ > 1`, `b2+ = 1`, and reducible-solution boundaries rather than combining their
   conclusions;
5. inspect corrections and errata, including whether the cited Seiberg-Witten erratum changes any
   incorporated input; and
6. obtain independent approval of the source-to-canonical-statement mapping.

The Lean-side crosswalk must then map each sourced object and hypothesis to an exact type or
predicate, record any missing analytic/gauge-theory infrastructure as a blocker, and kernel-check
every credited alternate encoding. Until that work is complete, there is no canonical formal
target and no statement fingerprint.

