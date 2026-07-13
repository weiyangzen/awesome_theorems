import Mathlib.Combinatorics.Configuration
import Mathlib.Combinatorics.SimpleGraph.Basic

/-!
# THM-M-0896 discovery-only intake probe

These checks authenticate adjacent pinned incidence-configuration, projective-plane, and graph
interfaces. They do not select a finite geometry, construct a graph from it, state the catalog's
unspecified relationship, or supply theorem-proof credit.
-/

#check Configuration.Nondegenerate
#check Configuration.HasPoints
#check Configuration.HasLines
#check Configuration.HasPoints.existsUnique_point
#check Configuration.HasLines.existsUnique_line
#check Configuration.ProjectivePlane
#check Configuration.ProjectivePlane.order
#check Configuration.ProjectivePlane.card_points_eq_card_lines
#check Configuration.ProjectivePlane.card_points
#check Configuration.ProjectivePlane.card_lines
#check SimpleGraph
#check SimpleGraph.Adj
#check SimpleGraph.incidenceSet
