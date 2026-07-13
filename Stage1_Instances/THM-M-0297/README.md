# THM-M-0297 rev-5.6 intake

`THM-M-0297` is the real-analysis catalog item "Marcinkiewicz interpolation theorem." The catalog
attributes it to Jozef Marcinkiewicz in 1939 and supplies only the gloss "interpolation of
weak-type operators" plus an untrusted `verified` label. This identifies a classical theorem
family, but not one proposition with fixed measure spaces, exponents, operator assumptions, and
constant.

## Intake result

This dossier records a fail-closed `planned` instance. It preserves the named weak-to-strong
interpolation family without choosing among materially different formulations: sublinear versus
quasilinear operators, scalar versus vector-valued functions, finite versus sigma-finite or
arbitrary measure spaces, two finite weak-type endpoints versus an endpoint at infinity, simple
functions versus completed `Lp` spaces, qualitative boundedness versus a sharp quantitative norm
estimate, and strong- or weak-type endpoint conclusions.

Marcinkiewicz's two-page note, *Sur l'interpolation d'operations*, C. R. Acad. Sci. Paris 208
(1939), 1272-1273, is a plausible primary historical source lead. Its locator was corroborated
through the reference list of Antoni Zygmund's later paper, *On a theorem of Marcinkiewicz
concerning interpolation of operations*. Neither source is cited by the repository, and no exact
source passage, complete premise map, correction audit, or independent review is accepted here.
The historical result is therefore not silently replaced by a familiar modern textbook version.

## Formal boundary

`IntakeProbe.lean` elaborates pinned `MemLp`, `eLpNorm`, and Chebyshev-Markov interfaces adjacent to
a future formalization. A bounded repo-local and pinned-mathlib name search found no terminal
Marcinkiewicz or weak-type interpolation declaration. These are discovery observations only, not
the dependent anchor audit and not proof evidence.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: a published theorem family and pinpoint primary-source lead are known, but exact
statement selection, assumption and errata mapping, and independent review remain open; no usable
exact formal artifact is credited; and no source-faithful reconstruction can attach to an unfrozen
root. All six downstream tasks remain open. No accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
