import Mathlib.Combinatorics.SimpleGraph.Extremal.Turan

/-!
# THM-M-0816 discovery-only intake probe

These checks authenticate the pinned Turán-theorem candidate interfaces. They do not choose a
canonical source variant, freeze a formal target, audit terminal proof bodies, or prove THM-M-0816.
-/

#check SimpleGraph.IsTuranMaximal
#check SimpleGraph.turanGraph
#check SimpleGraph.turanGraph_cliqueFree
#check SimpleGraph.isTuranMaximal_iff_nonempty_iso_turanGraph
#check SimpleGraph.card_edgeFinset_turanGraph
#check SimpleGraph.CliqueFree.card_edgeFinset_le
#check SimpleGraph.extremalNumber_top
#check SimpleGraph.card_edgeFinset_eq_extremalNumber_top_iff_nonempty_iso_turanGraph

