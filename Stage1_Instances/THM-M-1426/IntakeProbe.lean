import Mathlib.Data.Rel
import Mathlib.Dynamics.Ergodic.MeasurePreserving

/-!
# THM-M-1426 discovery-only intake probe

These checks authenticate adjacent pinned relation and measure-preserving APIs. They neither define
a multivalued random dynamical system nor select or prove a theorem about one.
-/

open MeasureTheory

#check SetRel
#check SetRel.comp
#check SetRel.image
#check SetRel.image_comp
#check MeasurableSpace
#check Measure
#check MeasurePreserving
#check MeasurePreserving.iterate
