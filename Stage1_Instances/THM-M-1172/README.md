# THM-M-1172 rev-5.6 intake

This directory is the `planned` intake for elliptic `W^{2,p}` regularity. The theorem name alone
does not determine a unique theorem: interior and global estimates, divergence and nondivergence
form operators, coefficient classes, domains, boundary data, and exponent ranges differ. This
intake therefore freezes the intended family as a second-order uniformly elliptic boundary-value
regularity result, while requiring the statement phase to select one exact primary-source theorem.

The legacy Lean module is discovery input only. Its `StatementShape` assumes second-derivative
`MemLp` and an estimate as fields, so it receives no rev-5.6 statement or proof credit. The
provisional root vector is `[H2, M4, R4]`; no canonical Lean target, audit completion, or theorem
completion is claimed. Exact intake checks are recorded in `validation.md`.
