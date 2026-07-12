# Source-statement crosswalk

## Candidate sources

- Mikhail Gromov, "Pseudo holomorphic curves in symplectic manifolds", *Inventiones
  Mathematicae* **82** (1985), 307-347, DOI `10.1007/BF01388806`. This is a primary discovery
  anchor for the pseudoholomorphic-curve and nonsqueezing machinery behind symplectic rigidity.
  Intake has not established that the metadata's exact closure formulation appears as a numbered
  statement in this paper.
- Yakov Eliashberg, "A theorem on the structure of wave fronts and its application in symplectic
  topology", *Functional Analysis and Its Applications* **21** (1987), 227-232. This is a primary
  discovery anchor commonly associated with C0 symplectic rigidity. A stable original-language or
  translated edition, pinpoint theorem/page, and any correction history still require inspection.
- Dusa McDuff and Dietmar Salamon, *Introduction to Symplectic Topology*, 3rd ed., Oxford
  University Press (2017), DOI `10.1093/oso/9780198794899.001.0001`. This is a secondary
  formulation/checking source, not a replacement for the primary-source audit.

These are discovery anchors only. They have not been archived and hashed in this dossier,
pinpoint-crosswalked, checked for errata, or independently reviewed. They establish neither `H0`
nor any machine status. The repository's year 1989 is retained as untrusted metadata rather than
silently used to alter the bibliographic record above.

## Metadata-to-source crosswalk

| Metadata component | Candidate source interpretation | Formal consequence | Intake disposition |
|---|---|---|---|
| "Gromov-Eliashberg theorem" | C0 closure/rigidity of symplectic diffeomorphisms | sequence/net, topology, map class, and smoothness of the limit must be explicit | family identified; exact root unresolved |
| "rigidity of symplectic structures" | symplectic preservation survives C0 convergence under strong geometric hypotheses | cannot use ordinary continuity of derivatives or C1 convergence as a substitute | paraphrase only |
| authors Gromov/Eliashberg | points to pseudoholomorphic/nonsqueezing machinery and Eliashberg's application | proof attribution must be separated from the exact statement source | provenance candidates only |
| year 1989 | conflicts with dates of obvious candidate papers | edition, publication history, or intended source must be checked | untrusted, unresolved |
| `已验证` | Stage0 screening label | supplies neither reviewed source proof nor Lean evidence | rejected as evidence |

## Required statement crosswalk

Before the next phase can freeze the claim, a source reviewer must:

1. inspect immutable copies of the primary sources and select a pinpoint theorem, page, edition,
   language/translation, and incorporated definitions;
2. transcribe every manifold, dimension, boundary, compactness, smoothness, embedding/bijectivity,
   convergence, and inverse-convergence hypothesis in source order;
3. decide whether the root is the diffeomorphism-group closure theorem or an embedding/local form,
   and record checked implications rather than treating them as identical;
4. distinguish the smooth-limit theorem from the later notion of symplectic homeomorphism and from
   nonsqueezing used in its proof;
5. reconcile the metadata year and inspect corrections, errata, and later edition changes; and
6. obtain independent approval of the source-to-canonical-statement mapping.

The Lean crosswalk must then map manifolds, symplectic forms, pullback, map classes, and the chosen
C0 topology to exact types and predicates, recording absent infrastructure rather than weakening
the theorem. Every credited alternate form requires a kernel-checked transport. Until then, no
canonical formal target or expression fingerprint exists.

