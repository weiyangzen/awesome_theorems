# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Catalogue claim | Repository research catalogue: "paradifferential methods for nonlinear PDE" | none | Describes a theory; it has no binders, hypotheses, or conclusion |
| Primary theory | Bony, *Calcul symbolique et propagation des singularites pour les equations aux derivees partielles non lineaires*, Ann. Sci. ENS 14 (1981), 209-246, DOI 10.24033/asens.1404 | none located or checked | Primary discovery anchor identified; exact proposition/page and immutable artifact pin remain open |
| Product decomposition | Candidate identity splitting a product into low-high, high-low, and comparable-frequency interactions | no selected declaration | Leading statement family, but notation, domain, and convergence conditions are not frozen |
| Continuity estimates | Candidate mapping estimates on Holder/Besov-type spaces | nearby repository code only contains abstract proposition fields | Distinct theorem family; must not be silently merged into the decomposition identity |
| PDE application | Paradifferential linearization and propagation-of-singularities results | none | Downstream application family, not interchangeable with the decomposition formula |

The source title and repository label do not select one theorem. In particular, an algebraic-looking
dyadic formula is not meaningful without fixing cutoffs and the topology in which its series converge.
The statement phase must obtain and hash an immutable primary copy, pinpoint the selected result,
transcribe every binder and hypothesis, inspect corrections, and only then elaborate a Lean target.

Discovery link (not an accepted evidence receipt):
<https://doi.org/10.24033/asens.1404>

No `H0` or machine-closure claim is made. The repo-local `S1_M_182.lean` paraproduct fields are an
object-model boundary and cannot serve as a theorem candidate or proof.
