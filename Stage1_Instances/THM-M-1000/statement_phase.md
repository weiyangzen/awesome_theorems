# Statement phase: blocked at exact-target identification

Item: `S56-M-1000-STATEMENT`  
Base revision: `b15861ce0ba012fa04e8c728e6bacbc35a359aea`

## Decision

The exact Lean 4 target cannot be elaborated from the repository source. The complete source claim
available for `THM-M-1000` is the label `transportation inequality` and the phrase
`最优传输的集中`. It supplies no formula, source pinpoint, domain, quantifier order, hypotheses,
cost or distance, entropy convention, conclusion, or constants. As the accepted intake records,
this is compatible with materially different results including Talagrand's Gaussian `T2`
inequality and Marton-style transport/concentration inequalities. Choosing one would substitute a
theorem rather than transcribe the source.

The legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_280.lean` does elaborate, but it explicitly calls
its declaration a conservative statement shape and selects a generic `T2`-implies-concentration
package without source authorization. Under rev-5.6, that legacy declaration is discovery input
only. It cannot supply exact-statement identity, and therefore its successful elaboration is not a
statement-gate pass for this item.

Consequently no canonical module, declaration/expression, elaborated-expression hash, checked
alternate transport, or mutation suite can truthfully be frozen. The first failed gate is
`source_statement_identification`; the machine debt remains `M4`. No proof closure or theorem
completion is claimed.

## Minimal-import investigation

The legacy module declares these seven imports:

```lean
import Mathlib.InformationTheory.KullbackLeibler.ChainRule
import Mathlib.InformationTheory.KullbackLeibler.Basic
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Measure.LevyProkhorovMetric
import Mathlib.MeasureTheory.Measure.Tight
import Mathlib.Probability.Independence.Basic
import Mathlib.Topology.MetricSpace.Basic
```

They are not certified as minimal imports for the canonical theorem because no canonical theorem
has been identified. Import minimization and mutation testing before source disambiguation would
only validate the legacy substitution.

## Validation evidence

The worker reused the canonical pinned `.lake` directory through the clone's untracked
`Formalizations/Lean/.lake` symlink. It did not update, fetch, clone, or otherwise mutate Lake
dependencies.

| Command | Exit | Exact result / boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1000` | 0 | Rank 280; `planned`; `L0`; `rework_required: true`; legacy artifacts unaccepted; theorem incomplete |
| `lake env lean --version` (cwd `Formalizations/Lean`) | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `lake env lean AwesomeTheorems/Stage1/S1_M_280.lean` (cwd `Formalizations/Lean`) | 0 | Legacy module elaborated and printed its declarations, including `StatementShape`; this checks syntax/types only and does not establish source fidelity |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1000/intake.json` | 0 | Respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and `ed2be54e25389a57b3f04d47c5c780faa67caa575d944a77412a070e2c2ceb4d` |

## Retry condition

Provide or locate an authoritative source pinpoint with the displayed proposition. It must fix the
spaces and measures, cost/distance convention, admissibility and finiteness conditions, absolute
continuity or moment hypotheses, binder order, conclusion, and constant normalization. The
statement phase can then transcribe that proposition, minimize imports against it, fingerprint the
elaborated expression and environment, compile any credited transports, and run the required
removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

This phase is blocked and is not self-tested as a completed statement node. Therefore no
`.stage1-worker-selftest.json` is emitted.
