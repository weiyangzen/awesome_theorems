# Exact-statement gate: blocked

Item: `S56-M-1064-STATEMENT`  
Base revision: `446447c65190dc818b074bf543171f807e9b4651`

## Decision

The exact Lean 4 target cannot be truthfully selected from the accepted intake and repository
source record. The complete repository wording is only `随机游走的嵌入` ("embedding of a random
walk"), under the name "Skorokhod embedding". It gives no theorem number, page, or mathematical
statement and does not decide among inequivalent results such as:

- embedding one centered integrable law as Brownian motion at a stopping time;
- iteratively embedding the partial sums of a random walk into Brownian motion;
- embedding a discrete random walk into another discrete-time process; or
- a finite-state specialization.

Even after choosing a family, the record does not fix the increment assumptions, probability
spaces, driving process and filtration, stopping-time ordering and almost-sure finiteness,
equality-in-law granularity, independence or conditional-law clauses, moment control, or treatment
of degenerate distributions. These choices change the proposition. The intake's Skorokhod (1965)
and Root (1969) references are explicitly discovery anchors: no stable edition, pinpoint theorem,
exact wording, assumption crosswalk, or errata review has been accepted. They therefore cannot
authorize one choice.

The repository also has a distinct `Skorokhod表示定理` entry for almost-sure representation of
weak convergence. That theorem is excluded rather than silently conflated with this embedding
target.

Consequently rev-5.6 section 5 fails at canonical mathematical-claim identity, before a canonical
Lean expression exists. Minimal imports, an elaborated-expression fingerprint, checked alternate
encodings, and meaningful removed-hypothesis/domain/binder/boundary mutations cannot be certified
until the source claim is fixed. The machine status remains `M4`; no statement or theorem
completion credit is claimed.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_220.lean` was checked only as discovery input. It
selects a finite-state discrete variant without source authority. Its `SkorokhodEmbeddingData`
contains opaque `finiteExpectationHypotheses`, `independenceHypotheses`, and
`convergenceBridgeHypotheses` fields, while `SkorokhodEmbeddingConclusion` packages the desired
stopping-time and stopped-value law assertions as fields. `StatementShape` then requests that
package. This is a type-correct interface, not an exact sourced Skorokhod theorem, and adopting it
would broaden or substitute the unknown target.

The legacy module elaborates in the pinned environment with four imports:

```lean
import Mathlib.Probability.HasLaw
import Mathlib.Probability.Independence.InfinitePi
import Mathlib.Probability.Martingale.OptionalStopping
import Mathlib.Probability.Process.HittingTime
```

That result establishes only that the historical abstract interface is syntactically and
type-correct. It cannot establish minimal imports for an exact target that has not been identified.

## Required unblock

An accountable source reviewer must select a stable primary-source edition and pinpoint theorem,
then crosswalk its exact random-walk/increment hypotheses, Brownian or discrete driving process,
filtration, ordered stopping times, finiteness, equality-in-law claims, independence, moment
conclusions, and boundary cases to the repository phrase. A later statement worker can then encode
that claim without substitution, minimize its pinned imports, serialize and hash the elaborated
expression, and run the required mutation suite.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. The existing canonical `.lake` artifacts
were reused; no dependency update, fetch, clone, build, or `.lake` mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1064` | exit 0; rank 220, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_220.lean)` | exit 0; no output; legacy abstract interface only |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact canonical source-statement identity. Known failures are the canonical Lean
target, minimal-import determination, expression fingerprint, checked transports, and statement
mutation tests. The assigned phase is blocked rather than self-tested complete, so no
`.stage1-worker-selftest.json` is emitted. No downstream node or theorem-completion state is
advanced.
