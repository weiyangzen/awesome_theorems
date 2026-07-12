# THM-M-1028 rev-5.6 intake

This directory is the `planned` intake dossier for the classical path-regularity theorem for a
real Wiener (Brownian) process: paths are almost surely continuous and almost surely nowhere
differentiable on nonnegative time.

The historical module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_221.lean` is discovery
input only. It provides a useful proposed object boundary and checked adjacent wrappers, but its
terminal conclusion is packaged as assumed structure data. It therefore supplies no rev-5.6
statement or proof credit.

The exact statement and bounded anchor audit are now inputs to frozen obligation registry version
1. The root cut set is the continuous-modification package and the nowhere-differentiability
package; `ObligationTree.lean` checks only their conditional composition. The root remains
`[H2, M2, R4]`. No audit completion or theorem completion is claimed.
