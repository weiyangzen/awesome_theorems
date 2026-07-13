# THM-M-1595 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Polar码`
(`polar codes`). The mathematical catalog gives only Erdal Arikan, 2009, and the gloss
`达到香农限的码` (a code achieving the Shannon limit). Those fields identify a coding-theory
result family, not one binder-complete proposition.

Arikan's 2009 paper was inspected as the direct primary-source lead. It separates channel
polarization (Theorems 1 and 2), block-error results for polar coding (Theorems 3 and 4), and
encoding/decoding complexity (Theorem 5). These results differ in channel symmetry, frozen-bit
choice, error averaging, conclusion, and proof obligations. The catalog cites none of them and
does not say whether "Shannon limit" means symmetric capacity for any binary-input discrete
memoryless channel or Shannon capacity for the symmetric subclass.

The intake therefore does not silently conjoin or select a familiar theorem. The provisional root
vector is `[H1, M4, R4]`: the exact primary paper and multiple proved candidate roots are known,
but the catalog-to-source selection, complete assumption/errata mapping, and independent review
remain open; no exact usable formal artifact is credited; and no readable proof reconstruction is
possible before the root is frozen. The catalog's `已验证` field supplies no proof credit.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` record the proposition-changing decisions and source boundary.
All six dependent phases remain open in `task-dag.json`. `IntakeProbe.lean` checks only adjacent
pinned probability, entropy, Hamming-distance, and matrix APIs. It states and proves no polar-code
theorem. No canonical statement, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed.
