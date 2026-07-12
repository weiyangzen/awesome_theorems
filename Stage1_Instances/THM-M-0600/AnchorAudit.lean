import Mathlib.Analysis.Calculus.ImplicitContDiff
import Mathlib.LinearAlgebra.QuadraticForm.Real
import Mathlib.LinearAlgebra.QuadraticForm.Signature

/-!
# THM-M-0600 anchor-audit probes

These exact-type probes verify the strongest relevant declarations found in the
pinned mathlib revision. They are ingredients only, not a proof of the Morse
lemma target.
-/

noncomputable section

namespace Stage1Instances.THM_M_0600.AnchorAudit

open QuadraticMap
open QuadraticForm

example {M : Type*} [AddCommGroup M] [Module Real M]
    [FiniteDimensional Real M] (Q : QuadraticForm Real M)
    (hQ : (associated (R := Real) Q).SeparatingLeft) :
    ∃ w : Fin (Module.finrank Real M) -> Real,
      (∀ i, w i = -1 ∨ w i = 1) ∧
        Equivalent Q (weightedSumSquares Real w) :=
  QuadraticForm.equivalent_one_neg_one_weighted_sum_squared Q hQ

example {R M : Type*} [Field R] [LinearOrder R] [IsStrictOrderedRing R]
    [AddCommGroup M] [Module R M] [FiniteDimensional R M]
    (Q : QuadraticForm R M) :
    sigPos Q + sigNeg Q +
        Module.finrank R Q.radical = Module.finrank R M :=
  QuadraticForm.sigPos_add_sigNeg_add_radical

example {E : Type*} [NormedAddCommGroup E] [NormedSpace Real E]
    [CompleteSpace E] {f : E -> E} {a : E} {n : WithTop ENat}
    {f' : E ≃L[Real] E} (hf : ContDiffAt Real n f a)
    (hf' : HasFDerivAt f (f' : E →L[Real] E) a) (hn : n ≠ 0) :
    ContDiffAt Real n (hf.localInverse hf' hn) (f a) :=
  hf.to_localInverse hf' hn

end Stage1Instances.THM_M_0600.AnchorAudit
