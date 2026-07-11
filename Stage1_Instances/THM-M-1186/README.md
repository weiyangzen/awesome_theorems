# THM-M-1186 rev-5.6 intake

This is the new rev-5.6 `planned` dossier for the repository entry called "McCann theorem" and
described as optimal-transport existence. Historical `S1_M_151.lean` is discovery input only.

## Scope map

| Surface | Provisional scope | Intake boundary |
|---|---|---|
| Human root | existence of a cost-minimizing coupling | The repository name and description do not yet identify one exact primary-source theorem |
| Spaces | compact metric Borel `X` and `Y` | Polish/Radon generality is deferred, not silently claimed |
| Data | probability measures `mu`, `nu`; cost `c : X x Y -> ENNReal` | Measurability consequences and instance requirements need elaboration |
| Cost premise | lower semicontinuity | Bounded-continuous cost is only a special checked legacy branch |
| Conclusion | a coupling attaining the global infimum | All-infinite costs and other boundary mutations remain untested |
| Lean candidate | `StatementShapeCompactMetric` in `S1_M_151` | Exact type, imports, normalized hash, and trust profile belong to statement phase |
| Architecture | coupling nonempty; closed/compact coupling set; lower-semicontinuous cost; extreme-value minimizer; wrapper | No leaf or composition closure is credited |

The main intake risk is semantic: McCann's named 1990s results commonly concern displacement
interpolation and convexity, whereas existence of an optimal coupling is normally the Kantorovich
existence theorem. The crosswalk therefore fails closed at `H3/M4` rather than choosing a source
after seeing the legacy formalization.

## Verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R3]`. The first failed gate is exact
source-statement identification, followed by the Lean statement gate. The theorem is not complete.
