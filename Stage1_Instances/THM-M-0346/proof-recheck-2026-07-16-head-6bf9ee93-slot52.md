# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-16T04:54:37+08:00`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test or node receipt is
issued.

The required v2 dependency audit is now recorded in `dependency-reuse-ledger.json`. The target has
no hard parents, transitive hard ancestors, hard edges, or reuse hints. Its only context is weak
shared-module group `SHARED-MODULE-4767ccab76f484cf`. The other inspected member,
`THM-M-0290`, has intake `[_]`, every later phase `[ ]`, no canonical statement, no obligation
registry, and no proof body. The group is therefore `not_applicable` for reuse and supplies no proof
credit. The repository's own `validate_dependency_reuse_ledger` function accepted the ledger with
graph digest `73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`
and target context digest `d6e79958da4ef9b20a9008758c46ec989dc931f0bd70085ea89fcd58dbb6567d`.

The existing `Proof.lean` remains genuine partial proof work. A trust-zero replay checks the
canonical `Lp` representative's `MemLp` certificate, the period-one and exponent-two side
conditions, an adapter from an upstream-shaped theorem, exact equality of its dossier-local cutoff
with `symmetricPartialSum`, and conditional composition into the exact
`Stage1.THM_M_0346.CarlesonTarget`. All six declarations are sorry-free and depend only on
`propext`, `Classical.choice`, and `Quot.sound`.

This does not prove the analytic premise `RawCarlesonHunt`. The local
`upstreamPartialFourierSum` models the audited API, but the actual external
`partialFourierSum'` is not imported. The literal upstream `carleson_hunt` concludes almost
everywhere under default `volume`, whereas the local adapter assumes explicit `haarAddCircle`.
At period one mathlib exposes the expected measure equality, but the exact upstream declaration and
bridge are not present to kernel-check. Thus
`carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget` is conditional
composition, not a proof of its premise or the root.

The first failed gate is `M0346-L-CARLESON-HUNT`. The existing pinned packages contain neither a
Carleson package nor declarations named `carleson_hunt` or `partialFourierSum'`. Mathlib's
`hasSum_fourier_series_L2` proves convergence in the `Lp` Hilbert space, not pointwise or
almost-everywhere convergence. Its pointwise theorem requires a continuous function with summable
Fourier coefficients. Neither result closes the frozen arbitrary-`L2` target.

The audited external Lean-4.29 candidate has a literal `sorry` body and a different mathlib pin.
The source-complete candidate targets Lean `v4.30.0-rc2` and another mathlib revision; it is absent
from the pinned closure and lacks repo-local terminal-body, trust, license, and reproducibility
validation. Importing it or migrating global pins is outside this worker's ownership and no-fetch,
no-`.lake`-mutation constraints.

The frozen registry remains authoritative. Its remaining root cut is
`M0346-C-REPRESENTATIVE`, `M0346-N-NORMALIZATION`, `M0346-N-CUTOFF`,
`M0346-L-CARLESON-HUNT`, and `M0346-T-AE-REP`. Existing adapter bodies are partial evidence only;
this recheck does not rewrite the frozen pre-proof closure observation or claim an obligation
closed.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were confined to `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network request, external checkout, source import, or `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| Initial `python3 Docs/tools/check_stage1_standard.py` | 0 | Pre-ledger assurance preflight passed. |
| Initial `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | All 1,546 nodes, 10,822 legacy states, two hard edges, five reuse hints, and 310 shared groups passed; graph acyclic. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; lifecycle planned; L0/rework-required; theorem incomplete. |
| Repository `validate_dependency_reuse_ledger` on the new target ledger, with supplied graph digest and base revision | 0 | Schema 1.1, exact context arrays, empty hard closure, and the one weak-group non-reuse decision passed. |
| Byte comparison for inspected `THM-M-0290` artifacts | 0 | Instance, task DAG, statement blocker, intake probe, and intake receipt matched the authoritative checkout. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884fc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| Isolated replay of copied `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` below `/tmp`, using the Lean binary and `LEAN_PATH` obtained through existing `lake env`, with `LEAN_NUM_THREADS=1`, `timeout 600`, `--trust=0`, and `-t0` | 0 | Exact target, six adapters, and conditional composition elaborated; all bodies were sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-mechanism scan over the three owned Lean sources | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom/constant, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide` occurred. |
| Existing-package, source, and build-artifact scans for the Carleson package/API | 0 aggregate | Empty output; no `carleson_hunt`, `partialFourierSum'`, or compiled Carleson-Hunt artifact exists in the pinned closure. |
| Read-only source inspection of mathlib near misses and the pre-existing upstream cache | 0 | Pinned mathlib results mismatch; Lean-4.29 upstream has `sorry`; source-complete upstream has incompatible pins and unresolved integration/trust boundaries. |
| Scoped diff from preceding recheck base `aba6e7a3` through current `HEAD` over canonical proof, registry, graph, anchor, pins, lakefile, and target manifest | 0 | No canonical proof or pin input changed. |
| Post-ledger `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | The mandated ledger exposes a global generator bug: the validator says ledgers are excluded from theorem-DAG discovery, but the generator adds the ledger to `structured_json_files`. Global tooling is outside worker ownership. |
| Post-ledger `python3 Docs/tools/check_stage1_standard.py` | 1 | Failed only through the same theorem-DAG deterministic-generation mismatch. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |

Source SHA-256 values are `a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d`
for `Statement.lean`, `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`, and `dbb718dbad1143a5423b426a916ef88b5c8f736965acbe7a7c4ead7772088bb1`
for `ObligationTree.lean`. Replay object SHA-256 values were
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82`,
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`, and
`2085328b3e8be96e6954d75a039f0ccc981a88cd07885f2d827273028968b7c5`.

## Boundary and retry condition

Lifecycle stays `planned`; the root stays `[H3, M3, R4]`; `audit_complete=false` and
`theorem_complete=false`. The predecessor obligation-tree node is provisional and pending master
acceptance. The planned intake authority also remains stale relative to later statement/tree
artifacts; reconciling it is outside this proof worker's phase. This record changes no scheduler
state, accepts no receipt, and supports no proof-completion, validation, release, audit-completion,
theorem-completion, or master-acceptance claim.

Resume after the integration lane provides an immutable, license-reviewed, placeholder-free
Carleson package compatible with the repository pins, or after a deliberate repository-wide pin
migration. Then import the real theorem, validate the external partial-sum and volume/Haar
transports, audit its transitive terminal bodies and axioms, and compose the exact root. The master
should separately repair theorem-DAG generation so the required dependency ledger is excluded from
the evidence inventory as promised by the validator contract. Until the proof body exists,
`.stage1-worker-selftest.json` must remain absent.
