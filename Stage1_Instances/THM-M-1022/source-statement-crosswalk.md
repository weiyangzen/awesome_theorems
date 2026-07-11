# Source-statement crosswalk

## Candidate primary source

George Polya, "Remarks on characteristic functions", in *Proceedings of the Berkeley Symposium on
Mathematical Statistics and Probability* (University of California Press, 1949), pp. 115-123, is
the historical primary-source candidate. The bibliographic identification is only a discovery
anchor: the exact theorem/page, original wording, definitions, and errata have not yet been
inspected, so this is not `H0` evidence.

## Crosswalk

| Repository/source phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "特征函数的充分条件" | sufficient, not necessary, criterion | existence of a probability measure with prescribed characteristic function | included |
| normalization | `f 0 = 1` | equality at zero | included |
| symmetry | real even function / symmetric law | `Function.Even f` and invariant measure | included; source wording open |
| decay | limit zero at positive infinity | `Tendsto f atTop (nhds 0)` | included |
| convexity | convex on `[0, infinity)` | `ConvexOn R (Set.Ici 0) f` or exact scalar API | included; encoding open |
| characteristic function | Fourier transform of a probability law | mathlib characteristic-function API and convention | API audit open |

Before `H0`, an independent reviewer must inspect a stable scan/edition and approve the theorem
anchor, every assumption, conclusion strength, notation, and errata. Before statement acceptance,
the crosswalk must also identify the pinned mathlib declarations and elaborate the exact target.
