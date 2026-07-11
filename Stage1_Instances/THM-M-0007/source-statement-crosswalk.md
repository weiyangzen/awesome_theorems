# Source-statement crosswalk

## Primary source anchor

Charles A. Weibel, *An Introduction to Homological Algebra*, Cambridge Studies in Advanced
Mathematics 38, Cambridge University Press, 1994, section 5.8, especially Theorem 5.8.3
(Grothendieck spectral sequence). This identifies the intended theorem family and the standard
acyclicity hypothesis. The exact printed definitions, page numbering for the consulted impression,
and errata still require direct inspection before `H0`; this citation is an intake anchor only.

## Crosswalk

| Source component | Repository/Lean candidate | Intake disposition |
|---|---|---|
| abelian categories and enough injectives | `Category`, `Abelian`, `HasInjectiveResolutions` | included; exact placement of instances open |
| left-exact additive `F`, `G` | additive functors plus `PreservesFiniteLimits` in legacy module | candidate encoding; equivalence to source convention unchecked |
| `F` sends injectives to `G`-acyclic objects | legacy `GrothendieckAcyclicity` uses vanishing `G.rightDerived n` for `n > 0` | plausible translation; exact quantifiers must be audited |
| `E_2^{p,q} = R^pG(R^qF(X))` | legacy `E₂Term` | object expression discovered, not a page construction |
| convergence to `R^{p+q}(G F)(X)` | legacy `CompositeDerivedTarget` | target object discovered; convergence is not formalized there |
| spectral sequence and naturality | legacy boundary uses an arbitrary `Type` and two `Prop` fields | insufficient; must use typed spectral-sequence/convergence APIs |

The legacy external anchor names in `S1_M_094.lean` point to Joel Riou's derived-categories work at
recorded revisions, but dependency compatibility and terminal proof provenance belong to the later
anchor-audit node. They receive no intake proof credit.

Before source fidelity can reach `H0`, a reviewer must consult the stable primary text, transcribe
all hypotheses and the exact convergence conclusion, map its notation definition-by-definition,
check relevant errata, and independently approve the crosswalk.
