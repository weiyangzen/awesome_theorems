# THM-M-1541 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the metadata target named "twistor theory".
The repository source gives only the gloss "complex geometry and physics" and attributes the topic
to Roger Penrose (1967). It does not identify a theorem. Consequently this intake freezes the
ambiguity rather than inventing a convenient twistor theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source record | `THM-M-1541`, "twistor theory", "complex geometry and physics" | Metadata is not an exact mathematical claim |
| Historical subject | Penrose's twistor programme relating complex geometry and space-time physics | A subject or programme is not a proposition |
| Candidate families | projective twistor space/incidence; Penrose transform; nonlinear graviton correspondence; Ward correspondence | Discovery candidates only; none is selected or credited |
| Repo-local discovery | `S1_M_179.lean` contains an axiomatized twistor-space API for the different target `THM-M-1543` | It cannot be substituted for this target and gives no proof credit here |
| Formal target | Lean 4 + pinned mathlib | Module, declaration, binders, hypotheses, and conclusion remain unset pending source disambiguation |
| Foundations | Lean 4 kernel with a later explicit foundation/TCB profile | Exact imports, axioms, computation policy, and environment fingerprint remain open |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The first failed gate is exact
source-statement identification: the available record names a theory rather than a theorem and has
no primary-source theorem/page or assumptions. The statement phase must not proceed until a primary
source and one exact claim are selected without broadening or substitution. No theorem completion,
machine closure, source fidelity, or legacy proof credit is claimed.

## Validation

The commands and exact results in `validation.md` establish target membership, repository-standard
consistency, JSON syntax, and dossier-local hygiene only. Master acceptance and all dependent phases
remain outstanding.
