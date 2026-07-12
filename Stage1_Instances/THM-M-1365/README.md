# THM-M-1365 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `Smale马蹄`
(`Smale horseshoe`). The repository attributes the item to Stephen Smale, dates it to 1967, and
gives only the gloss `混沌的几何模型` (`a geometric model of chaos`). It supplies no mathematical
definition, truth-valued proposition, hypotheses, conclusion, source citation, or formal artifact.
The catalog status `已验证` is untrusted metadata under rev-5.6.

The name and gloss do not select one theorem. They can denote the planar horseshoe construction,
compactness and invariance of its maximal invariant set, conjugacy to the full two-sided shift,
structural persistence under perturbation, a global sphere diffeomorphism, or the homoclinic-point
theorem often called the Smale-Birkhoff homoclinic theorem. These claims use different maps,
domains, regularity assumptions, invariant sets, iterates, and conclusions.

Smale's 1967 survey *Differentiable Dynamical Systems* was inspected as a primary discovery
source. Section 1.5 defines the shift and a geometric planar construction, then states several
distinct propositions and a homoclinic theorem. The repository does not cite that paper or choose
among those results. Intake therefore freezes the ambiguity instead of silently replacing the
catalog gloss by Proposition (5.3), Proposition (5.4), Theorem (5.5), or their conjunction.

The provisional root vector is `[H5, M4, R4]`: `H5` says that the received catalog wording is not
yet a stable truth-valued proposition, not that standard horseshoe theorems are false. A pinned
Lean probe checks only generic stream, semiconjugacy, periodic-point, and homeomorphism APIs. It
states and proves no target theorem.

The structured scope authority is `instance.json`; the proposition boundary is in `scope-map.md`;
the literal and primary-source mapping is in `source-statement-crosswalk.md`; and all six dependent
phases remain open in `task-dag.json`. No H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
