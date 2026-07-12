# THM-M-1520 proof execution receipt

Item: `S56-M-1520-PROOF`. Base revision:
`dd9a9ee3ccb2b4ae62a9105910ca0d54da3c9540`. Intent: `prove`.

## Implemented bodies

`Proof.lean` adds two exact, local, placeholder-free boundary proofs:

| Declaration | Frozen obligation branch | Result |
|---|---|---|
| `Stage1.THM_M_1520.timeZero_measurePreserving` | `M1520-S-BOUNDARY`, `t = 0` | the flow identity rewrites the time-zero map to `id`, whose volume preservation is supplied by pinned mathlib |
| `Stage1.THM_M_1520.zeroDimension_measurePreserving` | `M1520-S-BOUNDARY`, `n = 0` | extensionality proves the zero-dimensional phase space is subsingleton, so every time map is `id` |

These bodies close only two boundary cases. They do not prove `M1520-N-FLOW`,
`M1520-B-DIVERGENCE`, `M1520-C-VARIATION`, `M1520-L-JACOBIAN`, `M1520-L-CHANGE`,
`M1520-T-ALL-TIMES`, or the exact root. No declaration of `LiouvilleStatement` is claimed.

## Exact validation

Commands were run from the repository root. The local `Statement.olean` used for the narrow module
check was deleted immediately afterward; `.lake` was not modified.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1520` | 0 | rank 189; planned; L0/rework-required; theorem incomplete |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP="$(cd Formalizations/Lean && lake env printenv LEAN_PATH):Stage1_Instances/THM-M-1520"; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1520 Stage1_Instances/THM-M-1520/Statement.lean -o Stage1_Instances/THM-M-1520/Statement.olean; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1520 Stage1_Instances/THM-M-1520/Proof.lean; rm -f Stage1_Instances/THM-M-1520/{Statement,Proof}.{olean,ilean}` | 0 | pinned Lean elaborated both bodies; `#print axioms` reported exactly `[propext, Classical.choice, Quot.sound]` for each and no `sorryAx` |
| first development attempt of the same narrow Lean recipe | 1 | rejected invalid `MeasurePreserving.id` argument spelling and the unavailable inferred `Subsingleton (PhaseSpace 0)`; both were repaired by using argument `μ` and an explicit extensionality proof; this failed attempt carries no proof credit |
| `rg -n '(^|[[:space:]])(sorry|admit)([[:space:]]|$)|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1520` followed by `test $? -eq 1` | 0 | no forbidden proof devices or axiom declarations |
| `python3 Stage1_Instances/THM-M-1520/check_obligation_tree.py` | 0 | frozen registry remains structurally valid: 16 obligations and 32 typed edges |
| `git diff --check -- Stage1_Instances/THM-M-1520` | 0 | no scoped whitespace errors |

## Blocker and verdict

Verdict: `blocked`; no state change. The first failed completion gate is machine closure of
`M1520-T-ALL-TIMES`. The pinned mathlib revision has no theorem deriving a differentiable spatial
flow, its determinant evolution, or nonlinear change of variables from the frozen time-derivative
hypotheses. The audited external candidates likewise do not prove this proposition. Implementing
that missing analysis would require a substantial new ODE-with-parameters and measure
change-of-variables development, not a valid wrapper or import available in this execution tick.

Lifecycle stays `planned`; root vector stays `[H2, M3, R3]`; `audit_complete=false` and
`theorem_complete=false`. The remaining root cut is `M1520-T-ALL-TIMES`. Retry requires pinned,
kernel-checked implementations of the positive-dimensional analytic obligations and their checked
composition into `LiouvilleAnalyticPackage`. Because the assigned proof phase is not complete, no
`.stage1-worker-selftest.json` is emitted.
