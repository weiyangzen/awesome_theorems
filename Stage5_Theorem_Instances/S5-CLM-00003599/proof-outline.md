# Proof outline

1. **Frozen statement.**  The target is the exact infimum assertion
   `IsGLB {L | ∃ f, IsAdmissible f ∧ maxBoundaryLength f = L} 2`, with no
   additional hypotheses.
2. **Semantic expansion.**  `IsAdmissible` expands to a positive finite root
   product whose roots lie in the closed unit disk; `maxBoundaryLength` is the
   supremum of the Hausdorff lengths of connected-component frontiers of the
   sublevel set.
3. **Lower-bound branch.**  Establish that every admissible polynomial has a
   boundary-length value at least two, preserving the component and frontier
   hypotheses in the root node.
4. **Attainment/upper-bound branch.**  Exhibit the resolved extremal value two
   and show it belongs to the admissible value set, then combine the two
   inequalities using the `IsGLB` characterization.
5. **Composition and audit.**  The machine DAG records each branch, its exact
   output, formal anchor, downstream use, exceptional case, and trust boundary;
   the readable ledger maps every node injectively to one anchored fragment.

The source record is statement-only (`sorryAx` in the provider), so its proof
claim is never treated as an oracle.  Canonical Master must independently
replay the expanded root in its pinned environment.
