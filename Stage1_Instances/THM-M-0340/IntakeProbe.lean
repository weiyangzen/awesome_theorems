import Mathlib.Algebra.Group.Action.Equidecomp
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Geometry.Euclidean.Sphere.Basic

#check Equidecomp
#check fun {X G : Type} [SMul G X] (f : Equidecomp X G) => f.source
#check fun {X G : Type} [SMul G X] (f : Equidecomp X G) => f.target
#check EuclideanSpace
#check Metric.ball
#check Metric.closedBall
#check Metric.sphere
#check IsometryEquiv
#check AffineIsometryEquiv
