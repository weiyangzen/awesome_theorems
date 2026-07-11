# Source-statement crosswalk

| Claim component | Source anchor | Intake assessment |
|---|---|---|
| Manin-Mumford conclusion for an abelian variety in characteristic zero | M. Raynaud, "Sous-variétés d'une variété abélienne et points de torsion", in *Arithmetic and Geometry*, Vol. I, Progress in Mathematics 35, Birkhäuser (1983), pp. 327-352 | Primary proof source identified; exact theorem/page and hypotheses must be checked against a fixed scan before H0 |
| Repository source wording | `Docs/researches/math_theorems.md`: "曲线上挠点的分布" (distribution of torsion points on curves) | Secondary metadata gloss; insufficient as an exact proposition |
| Curve/Jacobian version | Specialization of the abelian-subvariety theorem after choosing an embedding into the Jacobian | Requires explicit hypotheses and a checked derivation; not interchangeable at intake |
| Finite-union equality versus containment of torsion intersection | Standard equivalent presentations of Manin-Mumford | Equivalence is plausible but uncredited until assumptions and Lean transports are checked |
| Lean expression | No repository-local declaration has been selected | `M4`; module/API discovery belongs to statement and anchor-audit phases |

The date `1963` and attribution to Manin and Mumford in repository metadata describe the conjecture's
origin, not a proof citation. Raynaud's paper is the proof anchor. This intake does not claim that a
public Lean formalization exists and does not turn the metadata label `已验证` into machine evidence.

Follow-up source work must pin a scan or edition by digest, locate the exact theorem and all ambient
conventions, review corrections or errata, map every assumption to the canonical statement, and
obtain independent review. Until then the human axis is `H1`.

