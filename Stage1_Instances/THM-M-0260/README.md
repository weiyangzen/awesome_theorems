# THM-M-0260 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for catalog target `THM-M-0260`,
"Yoccoz theorem" (`约科兹定理`). The repository supplies the attribution Jean-Christophe Yoccoz,
the year 1988, and only the gloss `Siegel盘的线性化` ("linearization of Siegel disks"). It gives no
primary-source locator, definitions, ordered binders, hypotheses, conclusion, or formal artifact.
The catalog's `已验证` label is explicitly untrusted under rev-5.6.

That gloss does not select a single theorem. It may refer to analytic linearization of a holomorphic
germ under the Brjuno arithmetic condition, Yoccoz's converse for a corresponding quadratic
polynomial when that condition fails, a biconditional specialized to quadratic polynomials, or a
related conclusion about the existence or boundary of a Siegel disk. These differ in domain,
quantifier order, arithmetic predicate, normalization, local/global dynamics, and conclusion.
Selecting one from the name would substitute mathematics not fixed by the catalog.

The repository also contains `THM-M-1432`, a distinct target with the same gloss, attribution, and
year. It remains a separate target and supplies no statement or proof credit here.

The provisional root vector is `[H5, M4, R4]`. `H5` classifies the received wording as not yet a
stable proposition; it does not say that standard Yoccoz results are false or open. `M4` and `R4`
record that no exact formal artifact or proof reconstruction can attach to an unidentified root.
`IntakeProbe.lean` checks only adjacent pinned analytic, unit-disc, and semiconjugacy APIs and states
no target theorem.

`instance.json` is the structured scope authority. `scope-map.md` freezes the proposition-changing
choices, and `source-statement-crosswalk.md` preserves the source boundary. All six dependent phases
remain open in `task-dag.json`. No exact Lean statement, H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
