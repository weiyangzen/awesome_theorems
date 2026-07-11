# Statement-phase validation

Item: `S56-M-0450-STATEMENT`  
Base revision: `e571265c0884ee452ec9fa3e73eb1ae0d04ab128`

All Lean commands ran from `Formalizations/Lean` using the existing pinned `.lake` symlink. No
dependency update, clone, fetch, or build was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0450/Statement.lean` | 0 | `ExactTarget` elaborated as a `Prop`; `#print` exposed the fully elaborated binders, ellipticity premise, Jacobian-point group instance, and finite-generation conclusion |
| `lake env lean ../../Stage1_Instances/THM-M-0450/mutations/removed_hypothesis.lean` | 1 | expected type mismatch; the exact target cannot supply finite generation after removing `E.IsElliptic` |
| `lake env lean ../../Stage1_Instances/THM-M-0450/mutations/changed_domain.lean` | 1 | expected type mismatch; the number-field target cannot be widened to arbitrary fields |
| `lake env lean ../../Stage1_Instances/THM-M-0450/mutations/changed_binder_scope.lean` | 1 | expected type mismatch; an existential curve claim cannot establish the universal target |
| `lake env lean ../../Stage1_Instances/THM-M-0450/mutations/boundary_singular_curve.lean` | 1 | expected type mismatch; the target yields no conclusion for the excluded singular boundary |
| `lake env lean --version` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `lake env lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `lake env lean ../../Stage1_Instances/THM-M-0450/Statement.lean \| sed -n '/^def Stage1Instances.THM_M_0450.ExactTarget/,$p' \| sha256sum` | 0 | normalized printed declaration output SHA-256 `25441c035ace49d13ff9f5f2d0a1c1fbd6c5df9c76ad9674e9fbff0c870a68c1` |

The two imports are minimal at module granularity for this encoding: `Jacobian.Point` provides the
curve, point type, and additive group; `NumberField.Basic` provides the number-field predicate.
No alternate encoding receives machine credit, so no transport wrapper is required at this phase.

This is statement evidence only. `ExactTarget` is a definition of the proposition, not a theorem
body, and the Mordell-Weil theorem remains unproved and incomplete.
