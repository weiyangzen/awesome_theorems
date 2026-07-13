import Mathlib.Combinatorics.SimpleGraph.Coloring
import Mathlib.Combinatorics.SimpleGraph.Finite

/-!
# THM-M-0858 discovery-only intake probe

These checks authenticate the pinned graph-coloring, local-finiteness, degree, connected-component,
and graph-isomorphism interfaces needed to encode Brooks's printed 1941 theorem. The envelope is a
source-scope candidate only; the dependent statement phase owns the canonical declaration,
expression fingerprint, transports, and mutation tests.
-/

universe u

namespace Stage1Instances.THM_M_0858

/-- Candidate encoding of Brooks's `n`-simplex: a complete graph on `n + 1` vertices. -/
def IsNSimplex {W : Type*} (H : SimpleGraph W) (n : Nat) : Prop :=
  Nonempty (H ≃g SimpleGraph.completeGraph (Fin (n + 1)))

/--
Candidate encoding of the exact theorem paragraph on printed page 194. `SimpleGraph` supplies the
loopless, no-parallel-edge interpretation; source admission and that transport remain open.
-/
def Brooks1941SourceEnvelope : Prop :=
  ∀ {V : Type u} (G : SimpleGraph V) [G.LocallyFinite] (n : Nat),
    2 < n ->
    (∀ v, G.degree v ≤ n) ->
    (∀ c : G.ConnectedComponent, ¬ IsNSimplex c.toSimpleGraph n) ->
    G.Colorable n

#check SimpleGraph.Coloring
#check SimpleGraph.Colorable
#check SimpleGraph.LocallyFinite
#check SimpleGraph.degree
#check SimpleGraph.ConnectedComponent
#check SimpleGraph.ConnectedComponent.toSimpleGraph
#check SimpleGraph.completeGraph
#check SimpleGraph.Iso
#check SimpleGraph.colorable_iff_forall_connectedComponents
#check IsNSimplex
#check Brooks1941SourceEnvelope

end Stage1Instances.THM_M_0858
