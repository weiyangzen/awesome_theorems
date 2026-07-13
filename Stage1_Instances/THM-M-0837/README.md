# THM-M-0837 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Robertson-Sanders-Seymour-Thomas证明` (Robertson-Sanders-Seymour-Thomas proof). The catalog gives
Robertson and coauthors, the year 1997, and only the gloss `四色定理的新证明` ("a new proof of the
Four-Colour Theorem"). It supplies no citation, exact proposition, definitions, ordered binders,
hypotheses, conclusion, proof-object boundary, or formal artifact. Its `已验证` value is untrusted
metadata under rev-5.6.

The matching 1997 JCTB article is a strong bibliographic lead. An author-maintained summary and the
authors' inspected 1996 announcement separate several possible targets: the ordinary Four-Colour
Theorem conclusion, the RSST proof/provenance package, the reducibility and unavoidability clauses
for 633 good configurations, and a quadratic four-colouring algorithm. The catalog does not say
which is the root. Selecting the ordinary conclusion alone would also erase the RSST proof-route
identity and silently overlap `THM-M-0833`, the separate generic Four-Colour Theorem target.

This intake freezes that ambiguity rather than manufacturing or borrowing a theorem. The
provisional vector is `[H5, M4, R4]`: `H5` classifies the received proof-family label as not yet a
stable truth-valued proposition; it does not question the Four-Colour Theorem or the published RSST
results. `M4` records that no exact usable Lean artifact is credited, and `R4` records that a
source-faithful readable proof cannot attach to an unidentified root.

The structured scope authority is `instance.json`. `scope-map.md` and
`source-statement-crosswalk.md` preserve the proposition-changing choices, source leads, computer
boundary, and neighboring-target exclusions. All six downstream phases remain open in
`task-dag.json`. `IntakeProbe.lean` authenticates only the pinned simple-graph colouring API; it
does not define planarity, state the Four-Colour Theorem, or prove an RSST clause.

No canonical mathematical or Lean proposition, H0, M0, R0, accepted proof state, audit completion,
theorem completion, accepted receipt, or master acceptance is claimed.
