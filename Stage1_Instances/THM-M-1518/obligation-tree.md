# THM-M-1518 frozen obligation architecture

The canonical route is: differentiate the action to obtain the first-variation
integral, combine it with stationarity to get the weak Euler-Lagrange equation,
integrate the velocity term by parts using endpoint-zero variations, apply the
fundamental lemma with the continuity upgrade needed for a pointwise interior
result, then compose into the exact frozen target.

## M1518-root
Exact canonical statement; open.
## M1518-s-definitions
Checked statement definitions and types.
## M1518-s-boundary
Checked zero-variation and nondegenerate-interval boundaries; other listed cases remain in scope.
## M1518-s-foundation
Release-time transitive axiom and TCB audit; open.
## M1518-n-differentiate
Differentiate under the interval integral; open critical bridge.
## M1518-n-weak
Checked conditional transport from stationarity and the variation identity to weak form.
## M1518-l-ibp
Fixed-endpoint integration by parts; open critical lemma.
## M1518-l-fundamental
Fundamental lemma and a.e.-to-pointwise continuity upgrade; open critical lemma.
## M1518-l-weak-pointwise
Conditional analytic package joining the preceding two lemmas; open.
## M1518-t-assemble
Kernel-checked conditional composition into the exact root.
## M1518-x-source
Pinpoint human-source boundary; open and carries no machine credit.
## M1518-x-provenance
Release provenance overlay; open and carries no proof credit.

Every leaf has a 40-step split budget. The current minimal open root cut set is
`M1518-N-DIFFERENTIATE`, `M1518-L-IBP`, and `M1518-L-FUNDAMENTAL`.
