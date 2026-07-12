# THM-M-1363 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `混沌理论`
(chaos theory). The repository supplies only that field name, a collective twentieth-century
attribution, and the gloss `确定性系统的混沌行为` (chaotic behavior of deterministic systems).
It gives no citation, definition of chaos, deterministic system, binder-complete proposition,
hypothesis, or conclusion. The catalog's `已验证` (verified) field is explicitly untrusted metadata.

## Intake result

The gloss names a subject and phenomenon, not one truth-valued claim. It does not even say whether
all deterministic systems, some system, or a specified family should be chaotic. A universal
reading is false for identity and constant systems; an existential reading still lacks both a
system and a chaos definition.

Possible readings include Devaney chaos, sensitive dependence, positive topological entropy,
Li-Yorke scrambled sets, mixing, symbolic dynamics, a horseshoe theorem, or a theorem that a named
system is chaotic. They use different spaces, time models, regularity, hypotheses, and conclusions.
The ODE catalog category is inventory metadata and does not authorize silently restricting the
target to a smooth real flow.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 11.3, was inspected
as an authoritative discovery source. It explicitly warns that authors use different definitions,
then contrasts sensitivity plus transitivity with Devaney's definition for continuous discrete
maps. This supports the ambiguity diagnosis, but the catalog does not cite or select that source,
definition, or its lemma from chaos to sensitive dependence. None receives canonical-statement or
H0 credit.

## Formal boundary

`IntakeProbe.lean` checks only pinned flow, invariance, periodic-point, topological-transitivity,
and topological-entropy interfaces adjacent to possible later encodings. A bounded lexical search
found no exact chaos, chaotic, Devaney, or sensitive-dependence declaration in repo-local Lean or
pinned `Mathlib/Dynamics`. Existing APIs are substrate, not a selected chaos predicate or theorem.
Neither observation is an exhaustive anchor audit or supplies a proof body.

The provisional root vector is `[H5, M4, R4]`. `H5` says this catalog field/phenomenon wording is
not yet a stable proposition; it does not say that correctly stated chaos theorems are false. All
six downstream tasks remain open. No canonical Lean expression, H0, M0, R0, accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.
