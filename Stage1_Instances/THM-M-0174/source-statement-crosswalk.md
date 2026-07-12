# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` name Friedrich Hirzebruch, give
the year 1954, and gloss the result as "the signature of a manifold and the integral of the
`L`-class." They do not specify the manifold hypotheses, dimension, coefficients, normalization,
edition, theorem/page, proof, or formal artifact. Their `已验证` label is untrusted intake metadata
under rev-5.6 and supplies neither `H0` nor machine-proof credit.

## Candidate primary sources

- Friedrich Hirzebruch, *Neue topologische Methoden in der algebraischen Geometrie*, Ergebnisse
  der Mathematik und ihrer Grenzgebiete, volume 9, Springer (1956). This historical monograph is a
  primary source candidate for the signature theorem and its multiplicative-sequence formulation.
- Friedrich Hirzebruch, *Topological Methods in Algebraic Geometry*, third enlarged English
  edition, Springer (1966). This is a stable authorial edition candidate for comparing terminology
  and normalization with the German source.

The exact theorem/section/page, incorporated definitions, edition differences, and errata have not
been inspected in a pinned copy. These citations are discovery anchors only. A modern textbook may
assist interpretation but cannot replace the primary-source review required for `H0`.

## Crosswalk

| Repository/source component | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "manifold" | closed oriented smooth manifold `M` | manifold, compactness/no-boundary, orientation, dimension `4k` | included; exact source hypotheses open |
| "signature" | signature of the symmetric intersection form in degree `2k` | finite-dimensional cohomology, cup-product pairing, signature | included; coefficient and sign conventions open |
| `L`-class | multiplicative characteristic class of `TM` determined by the Hirzebruch power series | Pontryagin classes and `L_k` polynomial in rational cohomology | included; normalization open |
| "integral" | evaluation of the top-degree class on `[M]`, not a measure-theoretic integral | oriented fundamental class and Kronecker/evaluation pairing | included; representation open |
| equality | `sign(M) = <L_k(TM),[M]>` | exact equality with rational-to-integer bridge | human scope frozen; formal target open |

## Boundary and proof-route map

A later proof architecture is expected to expose at least the construction of the intersection
pairing, Poincare-duality nondegeneracy, the Pontryagin/`L`-class package, fundamental-class
evaluation, and the global argument identifying the two genera (or an equivalent signature-operator
index route with checked transports). This is only a scope map. It is not an accepted proof tree or
readable reconstruction.

Before `H0`, an independent reviewer must inspect an immutable primary-source edition, record the
pinpoint theorem and all incorporated definitions, map every assumption and normalization, check
edition corrections and errata, and approve the source-to-Lean rows. The statement phase must then
kernel-elaborate the exact target and mutation-test dimension, closedness, orientation, tangent
bundle, pairing, and boundary conventions.

## Existing Lean boundary

The intake searches found no theorem-specific repository Lean artifact. An identifier search of the
existing pinned mathlib source found no Hirzebruch signature theorem or `L`-class declaration. This
does not establish global absence: the anchor-audit phase must run its precommitted repository,
mathlib, and external-project searches at immutable revisions and inspect exact declaration types,
bodies, axioms, and dependency feasibility.
