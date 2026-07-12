# Source-statement crosswalk

## Primary-source anchors

- Andre Weil, "Numbers of solutions of equations in finite fields," *Bulletin of the American
  Mathematical Society* **55** (1949), 497-508, DOI
  `10.1090/S0002-9904-1949-09219-4`. This is the historical conjecture source. A stable scan must
  be inspected to transcribe its precise setup and numbered assertions before statement freeze.
- Pierre Deligne, "La conjecture de Weil. I," *Publications Mathematiques de l'IHES* **43**
  (1974), 273-307, DOI `10.1007/BF02684373`. This is a primary proof source for the remaining
  Riemann-hypothesis/weight assertion, not by itself an unchecked license to import modern package
  conventions into Weil's wording.
- Bernard Dwork, "On the rationality of the zeta function of an algebraic variety," *American
  Journal of Mathematics* **82** (1960), 631-648, DOI `10.2307/2372974`. This is a primary proof
  source for rationality only and cannot close the full target.

These bibliographic records are discovery anchors, not an `H0` crosswalk, immutable source
snapshots, formal proof evidence, or accepted receipts. The exact theorem/page ranges, definitions,
assumptions, later corrections, and division of proof responsibility still require independent
inspection.

## Crosswalk

| Repository/source phrase | Intended component | Required Lean-side object or proposition | Intake status |
|---|---|---|---|
| "algebraic variety" | smooth projective variety over `F_q` for the full package | concrete finite-type geometric object, structural hypotheses, and dimension | included; encoding open |
| zeta function | exponential generating series of extension-field point counts, equivalently an Euler product | formal power series/rational function plus a checked equivalence if both forms are credited | included; normalization open |
| rationality | zeta series is represented by a rational function | exact numerator/denominator identity | included; exact statement open |
| functional equation | duality relates values at `t` and an inverse `q`-scaled argument | normalized equation with dimension, Euler characteristic, and sign | included; constants open |
| Betti-number assertion | degrees of factors match appropriate cohomological Betti numbers | selected cohomology theory and finite-dimensional rank statement | included; comparison conventions open |
| Riemann hypothesis | degree-`i` reciprocal roots have weight `i` | complex embeddings and absolute-value equation involving `q^(i/2)` | included; root convention open |

## Metadata and machine boundary

Stage0 supplies only the title, the gloss "properties of zeta functions of algebraic varieties,"
the year 1949, Andre Weil's name, and an untrusted `已验证` label. It omits every hypothesis and
does not say whether "Weil conjectures" means the entire package. The named theorem and gloss make
the four-part interpretation the narrowest historically standard intake scope, but a primary scan
must confirm the exact root before Lean elaboration.

Repository search found no target-specific legacy priority slot or accepted Lean artifact for
`THM-M-0191`. No declaration name, import, external Lean project, or machine-checked body is
credited at intake. Before `H0`, an independent reviewer must approve a versioned row-by-row map
from the selected source statements and assumptions, including errata, to the canonical claim.
