# THM-M-0642 rev-5.6 intake

This directory is the self-tested `planned` intake dossier for the catalog item
`Nielsen不动点定理` (Nielsen fixed-point theorem). The repository supplies only the gloss
`不动点类的理论` ("the theory of fixed-point classes"), an attribution to Jakob Nielsen,
and the date 1921. That wording identifies a theory rather than one truth-valued proposition.

The intake therefore leaves the canonical mathematical statement and Lean target null. In
particular, it does not silently choose among the construction of fixed-point classes, their
index and essentiality, homotopy invariance of the Nielsen number, Nielsen's homotopy lower bound,
or a surface-specific minimum theorem. The adjacent Wecken and Lefschetz results remain separate
targets.

A primary bibliographic lead is J. Nielsen, *Uber die Minimalzahl der Fixpunkte bei den
Abbildungstypen der Ringflachen*, *Mathematische Annalen* 82, 83-93, DOI
`10.1007/BF01457977`. Crossref and Springer expose conflicting 1920/1921 date conventions, while
the Goettingen digitization supplies a stable scan. No exact proposition, assumptions, proof
boundary, or correction history from that article has yet been admitted or independently
crosswalked, so it is discovery evidence only.

`IntakeProbe.lean` checks adjacent pinned fixed-point and homotopy APIs. It does not define a
Nielsen class or elaborate the catalog target. The provisional vector is `[H5, M4, R4]`: `H5`
classifies the received wording as an unstable proposition, not the mathematical theory as false
or unsolved. There is no accepted proof state, source acceptance, audit completion, theorem
completion, or master acceptance.
