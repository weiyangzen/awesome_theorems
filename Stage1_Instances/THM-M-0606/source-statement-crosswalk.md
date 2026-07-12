# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md` names Michel Kervaire and John Milnor, gives the year 1963, and
summarizes the statement only as "classification of homotopy spheres." `Docs/Stage0_Blueprint.md`
repeats that phrase but leaves definitions, hypotheses, proof path, and formal artifacts open. The
manifest's `已验证` value is explicitly untrusted metadata and supplies no rev-5.6 proof credit.

## Primary source candidate

Michel A. Kervaire and John W. Milnor, "Groups of Homotopy Spheres: I," *Annals of Mathematics*,
Second Series 77 (1963), no. 3, 504-537, DOI `10.2307/1970128`. This bibliographic record is the
historical primary-source anchor. The article itself, its numbered results, definitions, hypotheses,
and any errata have not yet been inspected in this intake; consequently it is discovery evidence,
not `H0` evidence.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "homotopy sphere" | smooth oriented manifold with the homotopy type of a sphere | concrete smooth manifold, orientation, and homotopy-equivalence predicate | included; definitions open |
| "classification" | classification under the paper's equivalence relation | quotient/type of classes and a faithful classification proposition | included; exact root open |
| group of homotopy spheres | connected-sum group customarily written `Theta_n` | quotient group with well-defined connected sum | included; source theorem open |
| spheres bounding parallelizable manifolds | subgroup customarily written `bP_(n+1)` | bounding manifold and parallelizability predicates, subgroup map | included; indexing open |
| stable homotopy comparison | comparison involving the stable `J` homomorphism and exceptional terms | concrete stable homotopy objects, map, quotient, and exactness | included; exact sequence open |
| dimension qualifications | high-dimensional and parity/exception clauses | explicit natural-number hypotheses and case boundaries | mandatory; not yet frozen |

## H0 and statement-gate requirements

An independent source review must select a numbered theorem (or a precisely delimited conjunction
of numbered results), record exact pages, ordered assumptions, definitions, notation, proof
dependencies, and errata, and approve a row-by-row source-to-Lean map. The statement must not silently
identify h-cobordism classes with diffeomorphism classes or suppress a low-dimensional exception.

Repository search found no target-specific `THM-M-0606` Lean module or Kervaire-Milnor declaration.
This negative local search is not an external anchor audit. Pinned mathlib and credible external
Lean projects remain to be searched under `S56-M-0606-ANCHOR_AUDIT`, after the exact statement is
frozen.
