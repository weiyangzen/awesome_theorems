# THM-M-1552 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the metadata label "tau function". The source
record says only "tau functions of integrable systems"; that phrase denotes a family of
constructions, not one source-identifiable theorem. Accordingly, intake freezes the ambiguity and
does not promote the legacy Lean model or its `StatementShape` to the canonical theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human claim | Existence/characterization of a tau function for a specified integrable hierarchy | The hierarchy and theorem are absent from the source metadata |
| Candidate branches | KP, 2D Toda, KdV finite-soliton determinant, Sato Grassmannian, Fredholm determinant, isomonodromic systems | Exactly one branch and a primary theorem must be selected before statement work |
| Tau object | A scalar function of hierarchy times, with branch-specific regularity and normalization | `Time -> Complex` is only a candidate representation |
| Characterization | Hirota/residue identity, determinant formula, or reconstruction of hierarchy fields | These are not interchangeable without checked hypotheses and transports |
| Degeneracies | zero/constant tau, gauge rescaling, zeros of tau, singular reconstruction charts | No blanket exclusion is inferred |
| Lean discovery | legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_211.lean` | Discovery input only; its proposition-valued model fields can assume the desired conclusion |
| Foundations | Lean 4 kernel plus pinned mathlib | Exact toolchain, imports, axioms, and computation profile remain open |

The provisional scope is therefore an open task DAG: identify the intended primary-source theorem;
freeze its hierarchy, domains, normalization, hypotheses, and conclusion; then elaborate the exact
Lean target. No proof, wrapper, source fidelity, or legacy status receives credit at intake.

## Intake verdict

Lifecycle is `planned`; root vector is `[H5, M4, R3]`. The first failed gate is source
identification: the metadata does not determine a theorem without inventing mathematics. The
dependent statement phase must not proceed until that ambiguity is resolved from a primary source.
The theorem is not complete.

## Validation

The commands and results in `validation.md` establish target membership, repository-standard
consistency, JSON syntax, and dossier-local integrity only. Master acceptance and all dependent
phases remain outstanding.
