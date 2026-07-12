# THM-M-1439 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for catalog target `THM-M-1439`,
`Lyubich证明` ("Lyubich proof"). The repository supplies Mikhail Lyubich, the year 1999, and the
gloss `Feigenbaum猜想的解析证明` ("an analytic proof of the Feigenbaum conjecture"). It supplies no
citation, definitions, ordered binders, hypotheses, conclusion, or formal artifact. The catalog's
`已验证` value is untrusted metadata under rev-5.6.

The 1999 primary paper strongly identifies the intended result family, but not one canonical root.
Its introduction states a three-clause Hyperbolicity Theorem for real bounded-type renormalization
and separate Hairiness, Self-Similarity, Universality, Hausdorff-dimension, and QC theorems. The
paper's abstract describes the Feigenbaum-Coullet-Tresser conjecture as hyperbolicity of the
bounded-type renormalization transformation, while the catalog calls the item a proof rather than a
proposition. Selecting the Hyperbolicity Theorem, the parameter-scaling Universality Theorem, their
conjunction, or the stationary period-doubling specialization would change the target. The nearby
catalog entries `THM-M-1437` (Feigenbaum universality) and `THM-M-1438` (Lanford proof) make that
boundary material.

This intake freezes that ambiguity instead of choosing from memory. The provisional root vector is
`[H5, M4, R4]`: `H5` classifies the received proof label and gloss as not yet a stable proposition;
it does not challenge Lyubich's published results. No exact formal artifact or readable proof can
attach to an unidentified root.

`instance.json` is the structured scope authority. `scope-map.md` records proposition-changing
choices and exclusions; `source-statement-crosswalk.md` maps the catalog wording to the inspected
primary paper. All six dependent phases remain open in `task-dag.json`. `IntakeProbe.lean` checks
only adjacent pinned APIs and states no target theorem. No H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
