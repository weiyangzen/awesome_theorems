# Machine-checked audit — S5-CLM-00003516

The three claim-owned Lean files are checked separately with the tracked Lean
toolchain and `lake env lean --trust=0`. Their executable surfaces contain only
theorem and lemma declarations: no `sorry`, `admit`, axiom, unsafe declaration,
opaque declaration, local definition, abbrev, notation, syntax, macro, instance,
coercion, or namespace alias.

The terminal audit queries report no axioms for the three audit declarations.
The frozen declaration `Arxiv.«2602.05192».four_3` is mentioned to bind source
identity but is never used as a proof term, because its provider body contains
`sorryAx`. Structured declaration and dependency evidence is in
`machine-closure.json`; its remaining machine cut set is empty and its proposed
classification is `M0-L` pending canonical-Master recomputation.
