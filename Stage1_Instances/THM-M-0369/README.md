# THM-M-0369 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"vector-valued inequality". The inventory gives only the gloss "boundedness of vector-valued
operators", a collective attribution, and the twentieth century. It does not identify an operator
or state an inequality.

The wording can denote materially different results: a Fefferman-Stein vector-valued maximal
inequality, a Marcinkiewicz-Zygmund extension of a scalar operator, a square-function estimate, or
boundedness of one operator acting on Banach-valued functions. Their hypotheses, exponent ranges,
constants, and even their formal domains differ. Selecting one from the title alone would replace
the repository target with invented mathematics.

This intake therefore freezes the ambiguity and exclusion boundary rather than a proposition. The
root remains `[H3, M4, R4]`. A pinned Lean probe confirms only nearby infrastructure for `MemLp`,
`Lp`, continuous linear maps, operator norm bounds, and convolution. Those APIs are encoding
ingredients, not an exact vector-valued inequality or proof. Exact commands and results are in
`validation.md`.
