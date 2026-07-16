# THM-M-0177 statement handoff: blocked

Item: `S56-M-0177-STATEMENT`

Base revision: `1cc6aa61bb055a5c032297ee457905c849af7608`

Verdict: `blocked`; the item stays `[ ]` and no exact Lean target or phase completion is claimed.

## Exact-target gate

The intake selects the classical smooth quasi-projective formula

`ch(f_! E) * td(T_Y) = f_*(ch(E) * td(T_X))`.

The pinned Lean closure can express schemes, `IsProper`, and `Smooth`, but it has no compatible
concrete API for the K/G-theory carrier, K/G-theoretic proper pushforward, rational Chow theory and
its proper pushforward, Chern character, tangent and Todd classes, or the required
quasi-projectivity/base convention. Therefore the selected equation cannot be typed faithfully.

The historical repo-local module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_121.lean` does not repair this gap. Its
`GRRFormalData` structure makes `KTheory`, `ChowTheory`, multiplication, both pushforwards, the
Chern character, and Todd classes arbitrary caller-supplied fields. The module itself calls
`StatementShape` an abstract statement shape, not the concrete theorem. Crediting it would replace
GRR by a model-parametric equality rather than elaborate the intake-selected mathematics.

`Statement.lean` and the older `StatementProbe.lean` therefore check only the concrete
scheme/proper/smooth boundary. They contain no canonical target, proof, transport, mutation fixture,
or abstract stand-in. The successful kernel elaborations are adjacent-interface evidence only.

## Dependency and reuse audit

The authoritative graph SHA-256 is
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`; the target context digest is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The theorem node has no direct hard parent, transitive hard ancestor, hard edge, reuse hint, or
shared lemma group. Thus the exact `parent_inspection_order` is empty and the complete traversal has
zero visits. `dependency-reuse-ledger.json` records that audited empty closure. No provider body or
acceptance was imported, copied, transported, or inherited; emptiness is not an independence claim.

## Evidence-contract boundary

The HEAD statement contract requires exactly one validator at
`Stage1_Instances/THM-M-0177/check_statement.py` or
`Stage1_Instances/THM-M-0177/check_statement_artifacts.py`. The validator must already exist at the
worker base and retain the same HEAD Git blob. Neither candidate exists at base/HEAD
`1cc6aa61bb055a5c032297ee457905c849af7608`. A worker-created validator is expressly ineligible for
authority replay, so none is fabricated.

Exactly one node receipt is provided in `statement-receipt.json`. It includes every contract field,
records the required role paths, binds the already-HEAD-tracked crosswalk by SHA-256 and Git blob,
and leaves new/self-referential final byte bindings explicitly to integration. Those null final
bindings are blocker facts, not positive role-binding evidence. Because the exact target and
contract validator gates are false, the phase is not genuinely self-tested and no
`.stage1-worker-selftest.json` is emitted.

## Validation

All commands used the automation-provided canonical `.lake` artifacts read-only. No update, build,
clone, fetch, or dependency mutation ran.

| Command | Exit | Meaning |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Pre-edit assurance, v2 DAG, seven-phase contract, and skill structure passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | Pre-edit 1546-node graph, 10,822 state snapshot, edges, hints, groups, and acyclicity passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, 12 common gates, and 23 source references passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0177` | 0 | Rank 121, planned, legacy evidence unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0177/Statement.lean` | 0 | Contract-selected scheme/proper/smooth boundary elaborated; no GRR target credit |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0177/StatementProbe.lean` | 0 | Scheme/proper/smooth adjacent boundary elaborated; no GRR target credit |
| `cd Formalizations/Lean && lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_121.lean` | 0 | Historical abstract statement shape elaborated; no concrete-target credit |
| exact symbol search in pinned `Mathlib` and `Archive` | 1 | Expected no-match for concrete GRR/Chow/Chern/Todd/KTheory/quasi-projective names; bounded search only |

After target-owned JSON is added, the checked-in theorem-DAG evidence inventory is expected to be
stale until the master integration lane regenerates the read-only projection. This worker does not
edit that authority. The post-edit graph validator, aggregate standard check, and execution-cron
validate-only command each exit 1 on this same deterministic inventory mismatch; the phase-contract
checker and target-manifest checks continue to pass.

## Retry condition

Pin or implement compatible concrete Lean APIs for scheme K/G-theory, rational Chow theory, both
proper pushforwards, Chern character, tangent and Todd classes, and quasi-projectivity/base
conventions. The scheduler must also provide a declared validator already tracked at the next claim
base. A later statement attempt can then encode the intake-selected formula, minimize imports, bind
the elaborated expression and environment, check transports, and kill the four mandatory mutation
classes. Until then, statement acceptance, proof credit, audit completion, and theorem completion
remain false.
