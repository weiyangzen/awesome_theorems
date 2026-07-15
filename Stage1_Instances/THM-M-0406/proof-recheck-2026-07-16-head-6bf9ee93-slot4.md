# THM-M-0406 proof-phase recheck at `6bf9ee93`

Item: `S56-M-0406-PROOF`

Recheck date: 2026-07-16 (Asia/Shanghai)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. A consistent positive proof body cannot be implemented for the
exact frozen Lean proposition. The current placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

kernel-checks against the pinned Lean closure. Its model uses
`boundaryDivisor := Fin 4`, all four components, unit weights and intersection
numbers, true geometric premises, and `curve := Empty`. Every frozen premise
holds while the conclusion would produce an inhabitant of `Empty`.

This refutes the disconnected abstract encoding, not the mathematical
Corvaja--Zannier theorem. `SurfaceData` does not intrinsically relate its
scheme, curve, point, divisor, or predicate fields. `SurfaceDegeneracyEngine`
in `ObligationTree.lean` is definitionally the same refutable proposition; its
conditional adapters add no positive proof body.

The frozen transcription also omits source-required diagonal intersection
equations. The dossier-pinned `math/0206100` source requires
`p_i p_j (D_i . D_j) = c` for every pair, including `i = j`, while
`HasTheoremOneBoundary` guards the equation by `D1 != D2`. Its place set omits
the source's archimedean places, and its geometric interfaces are arbitrary
fields rather than intrinsic objects. Restoring diagonal equations alone
would not eliminate the checked model because its unit data satisfy them too.

The v2 dependency context was audited before this proof recheck. It is empty:
there are no hard parents, ancestors, hard edges, reuse hints, or shared lemma
groups. The new `dependency-reuse-ledger.json` records that empty closure under
schema `stage1-dependency-reuse-ledger/1.1`, graph digest `73e99d22...0eca`,
and context digest `068170c7...5c`. Its structural validator passed. No proof
credit was available or transferred.

No proof body or receipt was added, no obligation was closed, and the proof
item remains `[ ]`. The frozen vector remains `[H1, M4, R3]`; checked negative
evidence supports a fail-closed `[H1, M5, R3]` proposal, but this worker does
not modify authority or promote state. Audit and theorem completion are false.
`.stage1-worker-selftest.json` is deliberately absent.

The generated blueprint and global execution DAG project the obligation-tree
predecessor as worker-provisional `[_]`, while target-owned `task-dag.json`
still records it `open`. There were already 122 `proof-recheck-*` artifacts
before this packet. The five-unresolved-tick split trigger has long fired, so
another identical proof retry cannot progress without upstream repair.

## Failed gate and retry

The first failed gate is `M0406-S-DEFINITIONS` / exact-target consistency and
source fidelity. The remaining root cut set is `M0406-S-DEFINITIONS` and
`M0406-ROOT`.

Master/integration must stop identical proof retries, reopen and split at
`M0406-S-DEFINITIONS`, and authorize a source-faithful proposition whose
intrinsic, noncircular geometric semantics rule out the checked model and
include all source-required intersection and place cases. It must then freeze
a new exact expression and obligation registry and rerun statement,
anchor-audit, and obligation-tree gates. Adding only `Nonempty X.curve`,
assuming the proof engine, or proving a realizable specialization would
substitute the target.

## Validation

All commands ran in this worker clone against existing pinned Lean/Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, network
access, or intentional `.lake` mutation was performed. The direct pinned Lean
binary and existing canonical Lake library paths were used after concurrent
`lake env` queries stalled under repository-wide worker load. Temporary Lean
objects and logs were written under `/tmp`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| Read both blueprints, the execution skill, manifest/DAG entries, and target artifacts | 0 | Ownership, dependency, exact-target, proof, blocker, split-trigger, evidence, and no-overclaim rules reviewed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Completed successfully with no output. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10,822 legacy states, two hard edges, five hints, 310 groups, and acyclicity passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| Pre-write `git status --short --untracked-files=all`; `git rev-parse HEAD HEAD^{tree}` | 0 | Only `?? Formalizations/Lean/.lake`; base `6bf9ee93...cff`, tree `24acf86e...295`. |
| Invoke `validate_dependency_reuse_ledger` from `scripts/stage1_execution_cron.py` | 0 | Schema, graph/context/base bindings, and empty parents/ancestors/decisions/unresolved obligations passed. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | Fourteen obligations and 26 typed edges passed; denominator `46deb9e2...d90a7`; predecessor root open M4. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates, immutable pins, and substrate witnesses passed; root open. |
| Isolated pinned `lean --trust=0 -t0` replay below | 0 | From 04:50:26 through 04:51:40 +08:00, statement/proof exited 0. Both countermodel declarations reported `[propext, Classical.choice, Quot.sound]`; output/olean hashes were `0f59d348...385b`, `942b7cc7...a1f8`, and `deafda33...a27`. |
| Three parallel read-only reviews of rules, DAG/reuse closure, and proof obstruction | 0 | All confirmed the required empty ledger and exact-root refutability. No reviewer edited the repository. |
| Direct Lean identity, binary hash, and pinned package `HEAD`/tree checks | 0 | Lean 4.29.0 commit `98dc76e3...6740`; binary `3e0d0d3d...28bbf`; mathlib `8a178386...ea95` / `bdc39a31...e5c2b`; flt-regular `56161b6e...1a27` / `32c9eace...c893`. |
| Broad prohibited-construct scan over owned Lean files | 1 | Expected no-match exit; no `sorry`, `admit`, bodyless declaration, unsafe escape, `implemented_by`, or `native_decide` occurs. |
| Count pre-existing `proof-recheck-*` artifacts | 0 | Before this packet: `total=122 json=60 md=62`; authoritative proof attempts remain zero. |
| `python3 -m json.tool` plus ledger/blocker-invariant checks | 0 | Recorded after write: structured artifacts parsed; base, ledger, blocked state, refutation, incomplete phase, empty receipts, and no-selftest fields passed. |
| `git diff --check -- Stage1_Instances/THM-M-0406 .stage1-worker-selftest.json` | 0 | No whitespace errors in the assigned owned path. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion manifest exists because the proof phase is blocked. |
| Post-write `python3 Docs/tools/check_stage1_theorem_dag_v2.py` and `python3 Docs/tools/check_stage1_standard.py` | 1 | Expected worker-delta failure: the fresh inventory sees the new target-owned ledger/blocker JSON, but this worker is forbidden to regenerate the authoritative v2 DAG. The integration lane explicitly regenerates and revalidates it after copying blocked artifacts. |

The isolated replay copied `Statement.lean` and `Proof.lean` to a temporary
directory, invoked the Lean 4.29.0 binary from the pinned toolchain with
`--trust=0 -t0`, and used only the pre-existing canonical `.lake` library
paths. It compiled `Statement.lean` to a temporary `Statement.olean`, then
compiled `Proof.lean` with that directory prepended to `LEAN_PATH`.

Current input and output hashes:

| Input or output | SHA-256 |
|---|---|
| `Statement.lean` | `9d6e2a94131455eedcee2ae75765746958988f23f6398cc5c4ea3fbc193258ec` |
| `ObligationTree.lean` | `bbcd4865cc660a210b104c50e19d5ca66055dacdab07182f6d4693c096f3f02c` |
| `Proof.lean` | `afeb346ab8f1ff9e41b87395744faa7a352509d28ef842f10f18a3ec00874aaf` |
| `obligation-registry.json` | `90d988ef727c9f1cbe99cfffb73c21b05f32f6d0b61a2177b624217cfb4612b6` |
| `typed-graphs.json` | `f4da55995c5413f92314904e9687721153b52e7d1d1e1e27fe551f0d7333da17` |
| `anchor-audit.json` | `8e0f84a533e183b8b70ef48955d9fa2dc8dbf39274f4345c600c8f2c143cfd21` |
| `task-dag.json` | `e9888fdc413651364b476cea0d55cad197eddd433d1a2a818b23f1da3093c2f6` |
| `dependency-reuse-ledger.json` | `915dd6e956e5f42b2fc29bf4d319cc58f13383e0479febb92b15e43ae1607950` |
| statement output | `0f59d3486b6464922278f83f5e3871c79e0c2e7964d1e3a8a412f16e567b385b` |
| proof output | `942b7cc706eaa0b7aa1143e3ecfba1f8387659e19954b5b978ea77b98188a1f8` |
| temporary `Statement.olean` | `deafda332045568236e3354ba2870233cfdfd906e0105c9eb67b8fc575004a27` |

The structured companion record binds source hashes, exact results,
environment pins, dependency context, the countermodel, source-fidelity
failures, independent reviews, blocker, retry condition, and changed paths.
This current-base packet is durable blocker evidence only. It is not a proof,
completion receipt, scheduler transition, or theorem-completion claim.
