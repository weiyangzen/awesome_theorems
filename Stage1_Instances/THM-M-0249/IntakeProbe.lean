import Mathlib.Analysis.Analytic.Basic
import Mathlib.Topology.ContinuousMap.StoneWeierstrass

/-!
# THM-M-0249 discovery-only intake probe

These checks authenticate pinned topology, complex-analysis, polynomial-evaluation, and
continuous-map approximation APIs adjacent to Mergelyan's theorem. The star-closure check exposes
a deliberate non-substitute: complex Stone-Weierstrass uses conjugation. This file neither selects
a canonical Mergelyan statement nor declares or proves one.
-/

#check IsCompact
#check IsConnected
#check IsPreconnected
#check ContinuousOn
#check interior
#check AnalyticOnNhd
#check Polynomial.eval
#check Polynomial.toContinuousMapOn
#check polynomialFunctions
#check polynomialFunctions.topologicalClosure
#check polynomialFunctions.starClosure_topologicalClosure
