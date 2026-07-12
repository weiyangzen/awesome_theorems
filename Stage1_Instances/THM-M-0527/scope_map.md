# THM-M-0527 scope map

The terse repository phrase is interpreted as the standard classification theorem, not as the
entire subject of covering-space theory. The pointed form is canonical because it gives actual
subgroups of a fixed fundamental group; the familiar unpointed form is retained as an alternate
form requiring a checked quotient-by-conjugacy bridge.

| Surface | Frozen intake scope | Later gate still open |
|---|---|---|
| Base | A path-connected, locally path-connected, semilocally simply connected space `X`, with `x0 : X` | Select exact pinned-mathlib predicates and universe levels |
| Coverings | Path-connected covering maps `p : E -> X`, with `e0 : E` and `p e0 = x0` | Define the structure/category and pointed isomorphism relation without quotient ambiguity |
| Fundamental group | `pi_1(X,x0)` and the homomorphism induced by `p` | Freeze the exact mathlib declaration and coercions |
| Forward map | `p` maps to `range(p_*) <= pi_1(X,x0)` | Elaborate range and prove invariance under pointed covering isomorphism |
| Reverse map | A subgroup determines a connected covering with that induced image | Freeze the construction and its use of universal covers or path classes |
| Pointed conclusion | A bijection of pointed-covering isomorphism classes with subgroups | Construct an exact Lean type and mutation-test every hypothesis |
| Unpointed conclusion | Covering isomorphism classes correspond to conjugacy classes of subgroups | Checked transport from the pointed theorem; no credit at intake |
| Boundary cases | The trivial one-sheeted cover and universal cover are included when defined | Record top/bottom subgroup behavior in statement mutations |
| Broader categorical form | All covers versus fundamental-group actions is outside the canonical root | May later be a refinement, never a substituted root |

Disconnected total spaces, non-covering local homeomorphisms, and classification over bases without
the stated hypotheses are out of scope. Path lifting, homotopy lifting, monodromy, and injectivity
of `p_*` are expected proof dependencies, but none alone proves the correspondence.
