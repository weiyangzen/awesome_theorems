import Mathlib.NumberTheory.EulerProduct.DirichletLSeries
import Mathlib.NumberTheory.LSeries.DirichletContinuation
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.NumberField.DedekindZeta

/-!
# THM-M-0425 statement boundary probe at HEAD 739d30014

The repository supplies only the phrase "L-functions of Hecke characters". It
does not select a source-normalized proposition, Hecke-character convention, or
analytic boundary. These checks authenticate the closest pinned number-field
and Dirichlet-character APIs without declaring a canonical target, transport,
mutation fixture, or proof.
-/

namespace Stage1Instances.THM_M_0425

#check NumberField.AdeleRing
#check NumberField.dedekindZeta
#check DirichletCharacter.LSeries_eulerProduct_hasProd
#check DirichletCharacter.LFunction
#check DirichletCharacter.LFunction_eq_LSeries

end Stage1Instances.THM_M_0425
