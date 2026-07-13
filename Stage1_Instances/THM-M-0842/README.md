# THM-M-0842 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`Simonovits稳定性` (Simonovits stability). The repository gives Miklós Simonovits, the year 1968,
and only the gloss `极值图的稳定性` (stability of extremal graphs). It supplies no formula,
ordered binders, hypotheses, conclusion, source locator, or formal artifact. The manifest's
`已验证` field is expressly untrusted metadata.

## Intake result

The author-hosted scan of Simonovits's 1968 paper *A method for solving extremal problems in graph
theory, stability problems* was inspected. It establishes the intended extremal-graph stability
family, but it contains several related results. In particular, its general stability framework,
Theorem 7, and concrete Theorem 8(a) do not have the same hypotheses or conclusion. Modern sources
also commonly state either an arbitrary-forbidden-graph edit-distance theorem or a clique-free
edge-deletion theorem.

The catalog does not choose among those variants. This intake therefore does not silently replace
the target by Turán's exact theorem, the Erdős-Stone asymptotic density theorem, a spectral
stability theorem, a clique-only quantitative strengthening, or one of Simonovits's later exact
extremal results. The dependent statement phase must select and independently review one immutable
source proposition before it freezes Lean binders.

## Formal boundary

Pinned mathlib provides `SimpleGraph.turanGraph`, clique-freeness, colorability, extremal numbers,
and edge deletion. `IntakeProbe.lean` checks only those adjacent interfaces. A bounded search found
no Simonovits or extremal-stability declaration at the pinned revision. A later mathlib-history
commit and a public Lean project contain Erdős-Stone results, not the structural stability theorem
requested here; neither is in this repository's pinned validation closure.

The provisional vector is `[H1, M4, R4]`: a published primary proof family is identified, but the
exact statement, incorporated assumptions, errata status, and source-to-node map remain open; no
usable exact formal target has been located; and no readable proof route can be reconstructed
against an unfrozen root. All six downstream phases remain open. No canonical statement, H0, M0,
R0, accepted proof state, audit completion, theorem completion, accepted receipt, or master
acceptance is claimed.
