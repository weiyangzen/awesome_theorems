# Source-statement crosswalk

| Claim component | Human source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Catalog label “paradifferential operator” | Repository records attribute the item to Jean-Michel Bony (1981) | none | Identifies a subject, not an exact theorem |
| Catalog gloss “a tool for nonlinear PDE” | `Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` | none | Motivation only: no domains, binders, assumptions, or conclusion |
| Paradifferential calculus introduced for nonlinear PDE | J.-M. Bony, *Calcul symbolique et propagation des singularités pour les équations aux dérivées partielles non linéaires*, Annales scientifiques de l'École Normale Supérieure, 4e série 14 (1981), no. 2, 209–246, DOI `10.24033/asens.1404` | not yet located | Primary publication identified at discovery level; theorem/page/assumption/errata and immutable-file audit remain open |
| Operator definition from a symbol and frequency localization | Bony 1981, definitions within the symbolic-calculus development | future definition, not itself the root theorem | Quantization, cutoff, symbol class, base domain, and equivalence of conventions are unfrozen |
| Mapping/continuity estimates | candidate theorem family in paradifferential calculus | none | Cannot be selected without exact spaces and regularity indices |
| Symbolic composition, adjoint, or paralinearization | candidate theorem families in Bony's calculus | none | Mutually different propositions; none is licensed by the catalog gloss |

The crosswalk deliberately stops before assigning a canonical proposition. In particular, Bony's
paraproduct decomposition is the neighboring catalog target `THM-M-1301`; using it here would merge
two distinct records. Likewise, proving an arbitrarily chosen Sobolev boundedness statement would
broaden the supplied metadata into details it never states and narrow the mathematical theory to a
single result without source authority.

Before the dependent statement phase can pass, a reviewer must provide a primary-source theorem or
definition-plus-property pinpoint, exact assumptions and conclusion, edition/file hash and errata
check, and a reason that this proposition is the intended identity rather than merely a theorem
about paradifferential operators. Only then may a Lean expression and checked transports be frozen.
The primary citation above is discovery evidence and does not justify `H0`.
