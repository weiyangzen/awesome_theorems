# THM-M-1006 proof phase blocked at current base

Item: `S56-M-1006-PROOF`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

Worker: `slot26`

Observed theorem DAG SHA-256:
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`

Dependency context SHA-256:
`dbf2f1ec34c3dde9ae50b65dd981d204d30a808415241c42493778c88b0da32e`

## Verdict

`blocked`. No sound positive proof can inhabit the exact frozen declaration
`Stage1Instances.THM_M_1006.StatementShape`. It quantifies the same finite constants before every
real-valued discrete martingale and horizon for every real `p > 0`. Its upper comparison is false
at `p = 1 / 2` for martingales with unrestricted jumps. The proof phase therefore remains `[ ]`;
this report supplies no proof receipt, root credit, audit completion, or theorem-completion claim.

For each integer `N >= 2`, take `q = 1 / N^2`. While active, let the process increment by `+1`
with probability `1-q` and by `-(1-q)/q` with probability `q`, then freeze after the rare jump.
The increments have conditional mean zero. At horizon `N`, the finite martingales detailed in
`counterexample-analysis.md` satisfy

```text
E[M_N^(1/2)] >= (1/2) * N^(1/2),
E[Q_N^(1/4)] <= N^(1/4) + 2^(1/4).
```

Their ratio is unbounded, contradicting the single finite upper constant in the frozen target.
This refutes the selected unrestricted discrete encoding, not the classical continuous-martingale
Burkholder-Davis-Gundy theorem.

`Counterexample.lean` kernel-checks supporting algebra and asymptotics only. It does not formalize
the complete probability spaces, filtrations, martingale witnesses, lintegrals, moment estimates,
or `Not (StatementShape (1 / 2))`; it is not claimed as a full kernel refutation.

## Dependency and reuse audit

The required schema-1.1 ledger was created before any proof editing and passed the production
validator. There are no direct hard parents, transitive hard ancestors, hard edges, or direct reuse
hints. All three weak shared-module groups were inspected through actual member theorems:

- `THM-M-1005` supplies a Doob maximal estimate, not a maximum/quadratic-variation comparison.
- `THM-M-1078` concerns a martingale-transform estimate for `p > 1`, not this two-sided target.
- The shared mathlib martingale imports supply common APIs but no exact BDG proof body.

No shared result was accepted for reuse, and no future consumer-validation receipt was fabricated.
The ledger SHA-256 is
`37ab318baf7a797fdcc12718d77c0673008f38d8ef76275f02553de82920be6f`.

The intra-theorem predecessor `S56-M-1006-OBLIGATION_TREE` is also only worker-provisional `[_]`,
not master-accepted `[x]`. That independently prevents dependency-legal proof-node acceptance.

## Current validation

No `lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. The automation-provided `.lake` symlink was reused read only, making this nonrelease
evidence.

| Command | Exit | Exact result |
| --- | ---: | --- |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` before creating the required derived ledger | 0 | `check_stage1_theorem_dag_v2: ok (1546 theorems, 10822 legacy states preserved, 2 hard edges, 5 reuse hints, 310 shared groups, acyclic)` |
| integration-equivalent temporary graph regeneration followed by `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | Regeneration included the new ledger inventory; the fresh graph then passed the same 1546-theorem/10822-state/acyclic checks. The worker restored the supplied graph bytes afterward rather than modifying authority. |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | Rank 286, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| production `validate_dependency_reuse_ledger` with the scheduler graph digest and base revision | 0 | `PASS dependency reuse ledger: 0 hard-context inspections, 3 decisions` |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | 18 obligations and 49 typed edges passed; denominator `12818dc1...14dac6f`; root open M3; both directional packages M4. |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, `Counterexample.lean`, and `ObligationTree.lean` | 0 | All four modules elaborated in the pinned Lean 4.29.0/mathlib environment. |
| pinned-mathlib BDG search | 0 | Only adjacent Doob `maximal_ineq` and an unrelated polynomial comment matched; no exact BDG/quadratic-variation declaration was found. |
| token-anchored prohibited-device scan over owned `*.lean` | 1 | Expected no-match exit; no `sorry`, `admit`, axiom/bodyless declaration, unsafe/oracle device, `native_decide`, or `run_tac` was found. |

The isolated replay used temporary copies and the canonical pinned `LEAN_PATH`. The checked local
declarations' printed axiom sets remain subsets of `propext`, `Classical.choice`, and `Quot.sound`,
with no `sorryAx`. `Proof.lean` still proves only telescoping, zero-start reconstruction, and the
horizon-zero leaves. `ObligationTree.lean` only conditionally assembles assumed lower and upper BDG
packages; neither file supplies the missing root body.

After creating `dependency-reuse-ledger.json`, the fresh-generation branch of
`check_stage1_theorem_dag_v2.py` reports that the checked-in graph differs because the current
working-tree inventory sees the newly required ledger. An integration-equivalent temporary
regeneration and validation passed; the supplied graph was then restored byte-for-byte because the
worker may not edit that authority. The integration lane will perform the same regeneration in its
artifact transaction. The ledger validates against the exact scheduler-supplied graph and context digests.
`python3 Docs/tools/check_stage1_standard.py` was also attempted but did not finish during the
saturated shared-worker run and was interrupted; no pass is claimed for that command.

## Retry condition

The master must reopen the statement phase and select a source-faithful valid formulation, then
accept its new fingerprint and an append-only obligation-registry delta before re-running anchor,
obligation-tree, and proof work. Suitable repairs include a valid exponent range, sufficient jump
control, or the intended continuous-martingale formulation. Alternatively, the task may be
explicitly redirected to a complete kernel-checked counterexample theorem.

Because this assigned proof phase is genuinely incomplete, `.stage1-worker-selftest.json` is
deliberately absent.
