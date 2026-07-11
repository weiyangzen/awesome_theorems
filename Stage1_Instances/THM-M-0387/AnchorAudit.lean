import AwesomeTheorems.NumberTheory.THM_M_0387.StatementAndReductionPath
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path
import AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath

/-!
# THM-M-0387 anchor audit probes

These commands re-elaborate the exact types and report the transitive axioms of
the strongest locally available immutable candidates. They do not prove the
unconditional root.
-/

#check FermatLastTheorem
#check FermatLastTheorem.of_odd_primes
#check fermatLastTheoremThree
#check fermatLastTheoremFour
#check flt_regular

#check AwesomeTheorems.NumberTheory.THM_M_0387.fermatLastTheoremRootStatement_iff
#check AwesomeTheorems.NumberTheory.THM_M_0387.fermatLastTheoremRootOfOddPrimesPath
#check AwesomeTheorems.NumberTheory.THM_M_0387.flt3Path
#check AwesomeTheorems.NumberTheory.THM_M_0387.flt4Path
#check AwesomeTheorems.NumberTheory.THM_M_0387.regularPrimesPath

#print axioms FermatLastTheorem.of_odd_primes
#print axioms fermatLastTheoremThree
#print axioms fermatLastTheoremFour
#print axioms flt_regular
#print axioms AwesomeTheorems.NumberTheory.THM_M_0387.fermatLastTheoremRootOfOddPrimesPath
#print axioms AwesomeTheorems.NumberTheory.THM_M_0387.flt3Path
#print axioms AwesomeTheorems.NumberTheory.THM_M_0387.flt4Path
#print axioms AwesomeTheorems.NumberTheory.THM_M_0387.regularPrimesPath
