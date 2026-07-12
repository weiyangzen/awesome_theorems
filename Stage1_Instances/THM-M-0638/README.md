# THM-M-0638 rev-5.6 intake

`THM-M-0638` is the point-set-topology catalog entry for the Tychonoff fixed-point theorem. The
repository supplies only Andrey Tychonoff, the year 1935, and the gloss "a fixed point on a locally
convex space." This dossier records a fail-closed `planned` intake; it does not turn that gloss or
the inherited `verified` label into an exact proposition or proof.

## Intake result

The source family is the existence of a fixed point for a continuous self-map of a compact convex
subset of a locally convex topological linear space. A stable digitization of Tychonoff's 1935
paper was inspected and contains that result on printed page 770. Exact adoption still requires an
independent review of the paper's incorporated definitions, separation convention, nonemptiness,
translation, proof boundary, and errata. Consequently the canonical mathematical statement and
Lean target remain null at intake rather than silently importing statement-phase conclusions.

The catalog also schedules `THM-M-0317` for the same named theorem under functional analysis. Its
already integrated dossier and later-phase artifacts are useful immutable discovery inputs, but
they confer no status, receipt, proof, or ownership on this target. Whether the two IDs should be
merged, retained as aliases, or assigned distinct formulations is an integration decision that
must precede statement acceptance.

## Formal boundary

`IntakeProbe.lean` elaborates the pinned locally-convex, compactness, convexity, continuity,
invariance, and fixed-point vocabulary needed by the candidate family. It states no target theorem
and supplies no proof body. A bounded name search found no exact Tychonoff fixed-point declaration
in pinned mathlib; similarly named Tychonoff results there concern compact products and are
explicitly outside this target.

The provisional vector is `[H1, M4, R4]`. A published source and exact theorem-family lead are
known, but source-to-target identity and independent review are open; no exact usable formal
artifact is credited; and no source-faithful readable proof reconstruction is accepted. All six
downstream tasks remain open. Neither audit completion nor theorem completion is claimed.
