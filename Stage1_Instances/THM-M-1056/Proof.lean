import ConcreteProjectionPackage

namespace Stage1Instances.THM_M_1056

universe u v

/-- The exact finite-dimensional real invertible Oseledets theorem. -/
theorem oseledetsMultiplicativeErgodic :
    OseledetsMultiplicativeErgodicTarget.{u, v} :=
  oseledets_multiplicative_ergodic_target

/-- Compatibility name exposing the proof under the target's full stem. -/
theorem oseledetsMultiplicativeErgodicTarget :
    OseledetsMultiplicativeErgodicTarget.{u, v} :=
  oseledetsMultiplicativeErgodic

#print sorries oseledetsMultiplicativeErgodic
#print axioms oseledetsMultiplicativeErgodic

end Stage1Instances.THM_M_1056

