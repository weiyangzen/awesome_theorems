# THM-M-0115 obligation-tree validator freshness blocker

## Scope and authority

This is the target-scoped fail-closed result for `S56-M-0115-OBLIGATION_TREE` at worker base
`6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049` (tree
`28c148dbd84fbd549c749f060c92c9a3f00b16d0`). It changes no theorem source, frozen registry,
typed graph, phase receipt, validator candidate, later proof evidence, task-state authority, or
theorem-DAG projection.

The authoritative claim order is `(v2_execution_rank=260, phase_layer=3,
phase_item_id=S56-M-0115-OBLIGATION_TREE)`. The item is already `[_]` with `attempts=1`, while its
intra-theorem predecessor `S56-M-0115-ANCHOR_AUDIT` is also `[_]`. The complete
`parent_inspection_order` is exactly empty. The theorem node has no direct hard parent, transitive
hard ancestor, hard edge, reuse hint, or shared-lemma group, so the empty closure was inspected and
no provider proof body, receipt, checkbox state, or acceptance was consumed or transferred.

The current authority bindings are:

| Input | SHA-256 | Git blob |
|---|---|---|
| `Docs/Stage1_Phase_Acceptance_Contracts.json` | `1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4` | `84b92df9eaf457ab954b652c3f20f4d513cf0a88` |
| `Docs/Stage1_Blueprint_v2.md` | `4d2b5c73fb15ea8ae421329ddfd31778ea10cc58a62800fe46fa7a653a58eea8` | `a814c32ed17286a769bcf0d5c47dca1cd760364d` |
| `Docs/Stage1_Blueprint_rev-5.6.md` | `3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8` | `00b304bc44f3d1c52f3723cf1553bb13a2ad4018` |
| `Docs/Stage1_Theorem_DAG_v2.json` | `80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5` | `0ac6bb1325cba226fa9732754c99d3fc7648a59f` |
| `skills/execute-stage1-rev56/SKILL.md` | `ee9b5fded6bc2c7f767799a957a36a6ec24499da23d5b4a65dded0a81624f876` | `c988861b6cd10ffb259bc9e4f39b0ee08fe4c8d5` |

The stable dependency-context digest is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## First failed gate

`G09-FRESHNESS` is the first mandatory replay failure. The HEAD phase contract declares two
scheduler-owned candidate paths, and exactly one exists:

- `Stage1_Instances/THM-M-0115/check_obligation_tree.py`

Its immutable HEAD bytes have SHA-256
`d9efb330e90f9c81fb43e1a2c14a0d97242bd3d85f43d8f38bd72bad32c19aef` and Git blob
`9d4a153e51423864b20c243c2b078929b4e03627`. The exact authority-selected argv was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0115/check_obligation_tree.py
```

It exited `0` and wrote exactly this one JSON object to stdout:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"G09-FRESHNESS","item_id":"S56-M-0115-OBLIGATION_TREE","message":"one or more frozen authority inputs changed","open_obligations":1,"phase":"obligation_tree","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":["Docs/Stage1_Theorem_DAG_v2.json"],"status":"stale","theorem_complete":false,"theorem_id":"THM-M-0115","verdict":"repair_required"}
```

The result is semantically negative despite process success. The validator freezes repository base
`c5037228977a81948bbd6119e1728b4b65b9924e`, tree
`78b2627e717156dffe240bea12d14205af667d2a`, theorem-DAG SHA-256
`fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518`, and the original open row
`[ ]` with `attempts=0`. Current HEAD necessarily differs after integration of the obligation-tree
and later proof handoffs. Because validators are scheduler-owned and immutable, this worker cannot
repair, replace, rename, or supplement it. Exit code zero cannot override `phase_accepted=false` or
`phase_predicate_proven=false`.

The contract also requires a scheduler-owned per-item artifact role map at
`.cron/stage1-v2-app-server/role-maps/S56-M-0115-OBLIGATION_TREE.json`. That map is absent at HEAD,
so complete authority-selected role resolution is independently unavailable. This worker cannot
manufacture it.

## Frozen architecture replay

The selected target artifacts remain HEAD-tracked, byte-bound, and internally coherent:

| Role | Path | SHA-256 | Git blob |
|---|---|---|---|
| obligation registry | `Stage1_Instances/THM-M-0115/obligation-registry.json` | `1259038b59ce7429205a1813b97c31f2be5075b7c6ee784f3d602110d13f37c3` | `35fdecd564804042680386ee7a0bfabb57637894` |
| typed graph bundle | `Stage1_Instances/THM-M-0115/typed-graphs.json` | `ccf1757734fe4f37aae3bc65bebcb9fbf63a65f6d59031f74156607df91a768a` | `8ae46f25af81916f2077a5cc93e09f9c52be41b0` |
| readable tree | `Stage1_Instances/THM-M-0115/obligation-tree.md` | `5d950dd6abbc4a58761c7588afd057f1d615de8d4d776d6168c01e5996450113` | `04032d0efbb145f842635d2742053c8be85449eb` |
| composition source | `Stage1_Instances/THM-M-0115/ObligationTree.lean` | `7aeb4e6dfe6789365302e1ca6cc92ab8278233b9710d19b8882e3e76616f5c7e` | `8d6130f9d5ca054488c7e886f7c9009d64a1eae9` |
| existing phase receipt | `Stage1_Instances/THM-M-0115/obligation-tree-receipt.json` | `38623d2be0d7be786abd96d3b3d8344e6dd5a01d9453401fe29111eeaecf5e80` | `655b4d3e76ecd8b9605cc91fc8e685aa7a894b54` |

The registry still contains 32 canonical obligations with denominator
`f1455869731874b94cb533d3a6ee70bb15d428438472ffc205b63888eae68527`. The bundle still contains
seven typed graphs, 192 edges, three conditional composition certificates, eleven explicitly
unverified decompositions, and no accepted closed obligation. A trust-zero scratch replay of
`Statement.lean` followed by `ObligationTree.lean` succeeded using the existing pinned `.lake`
artifacts read-only. `ObligationTree.lean` output SHA-256 was
`094da5e8c6f0fbd2c688a04aef2378d689f8592f3708bda077cee0adbc15e2b8`; each of its three composers
reported exactly `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`.

These bounded checks show that the integrated architecture bytes remain coherent. They do not turn
the stale mandatory semantic replay into positive phase evidence, populate any mathematical child
premise, or establish master acceptance, `AUDIT-Z`, or `THEOREM-Z`.

## Dependency-ledger ownership boundary

The canonical `dependency-reuse-ledger.json` now belongs to the later integrated proof phase. It
binds `S56-M-0115-PROOF`, layer 4, repository revision
`307c34d30fc3763c82a944a142ae922b48ff18aa`, and theorem-DAG digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`; its current SHA-256 is
`7df2ec53f34afc9ac1f82b34a255baef5d4795568f2f2ff19e69e504e876c62d` and it is content-bound by
the proof receipt and proof validator. Replacing it with an obligation-tree ledger would corrupt
that later evidence. The original obligation-tree empty ledger is preserved in Git history and had
the same empty closure and stable context digest. No phase-scoped ledger path is authorized by the
current contract. Accordingly this recheck records the empty audit here without overwriting the
canonical later-phase ledger or pretending it was refreshed for this base.

## Bounded checks and retry

The following commands were run from this worker clone:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure, target set, v2 graph, seven-phase contract, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 states, two hard edges, five reuse hints, 311 shared groups, and acyclicity passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique L0/rework-required targets passed |
| `python3 scripts/stage1_target.py show THM-M-0115` | 0 | rank 23 target remains planned and theorem-incomplete |
| exact scheduler validator argv above | 0 | typed result was `stale` / `repair_required`; phase predicate false at `G09-FRESHNESS` |
| scratch `lake env lean --trust=0` replay of `Statement.lean`, then `ObligationTree.lean` | 0, 0 | exact three conditional composers elaborated with the declared axiom boundary |

No `lake update`, `lake build`, dependency clone/fetch, network access, or `.lake` mutation was used.
The automation-provided canonical `.lake` symlink remains a pre-existing untracked path.

This run deliberately emits no new `obligation-tree-receipt.json` and no
`.stage1-worker-selftest.json`: the mandatory semantic validator did not prove the phase predicate,
and there is no truthful positive self-test to hand off. Root status remains `H4/M3/R4`,
`audit_complete=false`, and `theorem_complete=false`.

Retry only after the scheduler publishes a refreshed, unique obligation-tree validator and the
required authority-owned role map at a new claim base containing those exact blobs. The scheduler
must also define a phase-scoped ledger binding or otherwise resolve the canonical-ledger ownership
collision with the later proof evidence. A fresh worker can then replay the unchanged candidate,
bind all selected roles, and report the validator's actual semantic result.
