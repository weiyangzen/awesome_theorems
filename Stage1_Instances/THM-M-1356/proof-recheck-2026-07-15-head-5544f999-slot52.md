# THM-M-1356 current-base proof blocker recheck

Item: `S56-M-1356-PROOF`

Intent: `prove`

Recorded: `2026-07-15T19:24:51+08:00` (`Asia/Shanghai`)

Base revision: `5544f9995d9309455a212b6530b9787b9df26345`

Base tree: `4ecc83ea665c779cce229732c817da1547135594`

## Verdict

`blocked`. No placeholder-free all-degree proof body was implemented or found
for the exact target
`Stage1Instances.THM_M_1356.RouthHurwitzTarget`. The proof item remains `[ ]`,
and the lifecycle remains `planned`. The unreconciled authoritative instance
vector remains `[H1, M4, R4]`; the statement, anchor, and obligation-tree
worker artifacts provisionally propose `[H1, M3, R4]`, but no integration
acceptance has promoted that proposal.

The existing `Proof.lean` remains genuine partial work. Its four declarations
prove the exact degree-one polynomial adapter, root characterization, unique
Hurwitz minor, and stability/minor equivalence. A fresh trust-zero replay and
`assert_no_sorry` probes passed. The canonical target quantifies over every
positive degree, however, so this finite specialization closes none of the 45
machine-required obligations in the frozen registry and cannot satisfy this
proof phase.

The only `THM-M-1356` proof-relevant target-local delta since the prior
current-base recheck at `a60b47b4` is that prior Markdown blocker itself. The
target proof source, registry, graph, dependency pin, target-manifest entry,
execution-skill input, and this item's DAG entry are unchanged. Global
blueprint and DAG entries advanced only for other theorem IDs.
The two exact directional cut nodes are still open:

- `M1356-B-STABLE-TO-MINORS`
- `M1356-B-MINORS-TO-STABLE`

Their missing implementation frontier includes the alternating even/odd
construction, signed Euclidean/Sturm sequence, Hermite hodograph and Cauchy
index bridges, regular and nonregular Routh cases, Hurwitz-block elimination,
and leading-minor product identity. The checked declarations in
`ObligationTree.lean` take both complete directions as explicit premises and
therefore supply composition only, not either proof body.

## First Failed Gate

The first workflow failure is prerequisite acceptance and freshness:
`S56-M-1356-OBLIGATION_TREE` is worker-provisional rather than master-accepted,
and its checker rejects the current base at a stale hard-pinned revision before
its substantive checks. Independently, the first proof-content failure is the
absence of an exact arbitrary-degree engine upstream of both directional cuts;
the bounded local and pinned scan found no placeholder-free implementation of
the required Hermite/Cauchy/Sturm/Routh and Hurwitz-minor-product packages.

Scoped exact-topic scans again found no named Routh-Hurwitz,
Hermite-Biehler, Hurwitz-matrix/determinant criterion, Lienard-Chipart, or
Cauchy-index Lean terminal in the bounded pinned mathlib, `flt-regular`, and
repo-local source set. The previously recorded immutable near-candidate
`PerAlexandersson/RealRooted@634a949d31683785b4181efbba6faff31e81e006`
remains ineligible: its relevant Hermite-Biehler, Hurwitz-matrix, and stable-to-
matrix declarations contain explicit `sorry`. Its proposed no-open-right-half-
plane and infinite-total-nonnegativity interfaces are also materially different
from the frozen finite strict-minor target.

## Narrow Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout repair, or `.lake` mutation was performed. Fresh Lean sources and
objects were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git status --short && git rev-parse HEAD && git rev-parse HEAD^{tree} && date --iso-8601=seconds` | 0 | Pre-edit status contained only the automation-provided `?? Formalizations/Lean/.lake`; HEAD/tree matched the identities above; run timestamp was `2026-07-15T19:17:36+08:00`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets passed. |
| `python3 scripts/stage1_target.py show THM-M-1356` | 0 | Rank 966; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-1356/check_statement.py` | 0 | Expression SHA-256 `7901eb74...98bf`; all four mutations distinguished; all three import-deletion probes failed as required; pinned mathlib revision agreed. |
| `python3 -B Stage1_Instances/THM-M-1356/check_anchor_audit.py` | 0 | Exact local statement only; pinned-mathlib exact-topic terminal inventory and external terminal-candidate inventory empty; support/catalog entries remain nonterminal; provisional root `M3`. |
| `python3 -B Stage1_Instances/THM-M-1356/check_obligation_tree.py` | 1 | The predecessor checker still stops at its stale hard-pinned base `431e77db...`; this is a prerequisite freshness failure, not a Lean proof failure. |
| `jq -r '.replay_recipe' Stage1_Instances/THM-M-1356/proof-recheck-2026-07-15-head-5544f999-slot52.json \| bash` | 0 | The embedded recipe replayed the sources with the direct pinned Lean executable selected by `lake env` and `--trust=0 -t0`; every source elaborated, each degree-one declaration was sorry-free and used exactly `propext`, `Classical.choice`, and `Quot.sound`, `Proof.olean` SHA-256 was `dbd13ed0...e66cf`, and the replay-log SHA-256 was `80069c16...aefc`. |
| `jq -r '.prohibited_construct_scan' Stage1_Instances/THM-M-1356/proof-recheck-2026-07-15-head-5544f999-slot52.json \| bash` | 0 | The embedded comment/string-stripped scan found no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/oracle construct, `native_decide`, `implemented_by`, `run_tac`, or proof placeholder. |
| `jq -r '.exact_topic_scans' Stage1_Instances/THM-M-1356/proof-recheck-2026-07-15-head-5544f999-slot52.json \| while IFS= read -r command; do status=0; bash -c \"$command\" \|\| status=$?; test \"$status\" -eq 1; done` | 0 | The wrapper passed after both underlying `rg` lanes returned their expected no-match exit 1; the bounded scoped scan found no named all-degree candidate. |
| `jq -r '.obligations as $o \| [$o\|length, ([$o[]\|select(.machine_eligibility==\"required\")]\|length), ([$o[]\|select(.machine_eligibility==\"required\" and .terminal_proof_body_id==null)]\|length)] \| @tsv' Stage1_Instances/THM-M-1356/obligation-registry.json` | 0 | 50 obligations; 45 machine-required; all 45 required terminal body IDs remain null. |
| `git diff --name-status a60b47b4551b044fd5fad26599908ccef4000024..HEAD -- Stage1_Instances/THM-M-1356/Statement.lean Stage1_Instances/THM-M-1356/ObligationTree.lean Stage1_Instances/THM-M-1356/Proof.lean Stage1_Instances/THM-M-1356/obligation-registry.json Stage1_Instances/THM-M-1356/typed-graphs.json Stage1_Instances/THM-M-1356/anchor-audit.json Stage1_Instances/THM-M-1356/validation-specs.json Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json skills/execute-stage1-rev56/SKILL.md Docs/Stage1_Targets_rev-5.6.json` | 0 | Empty over statement, composer, proof, registry, graph, audit, validation specs, pins, target manifest, and execution skill; only the prior blocker report entered this target. |
| `jq -r '.final_artifact_checks' Stage1_Instances/THM-M-1356/proof-recheck-2026-07-15-head-5544f999-slot52.json \| bash` | 0 | JSON syntax, handoff invariants, source registry counts, typed-edge count, whitespace, the two scoped paths, and deliberate self-test absence passed; both no-index checks returned their expected difference status. |

The literal multiline replay, prohibited-scan, topic-scan, and final-artifact
recipes are embedded in the JSON handoff and are invoked by the recorded
`jq -r ... | bash` commands. This keeps the Markdown summary readable while
preserving exact replayable command bytes.

Pinned identities were Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, mathlib commit/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, and `flt-regular`
commit/tree `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`.

## Retry Boundary

Implement the frozen all-degree Hermite/Cauchy/Sturm/Routh and Hurwitz-minor
product packages without placeholders, then close and compose both directional
cut nodes. Alternatively, provide an immutable, license-compatible exact Lean
4 terminal whose type, dependencies, provenance, placeholders, axioms, and
trust closure can be checked in the pinned environment.

There are three earlier proof-blocker files in the owned path, representing at
most two prior execution records: one JSON/Markdown pair and one Markdown-only
recheck. The authoritative item still records zero attempts and no children.
The integration lane must reconcile those records with the attempt ledger and
apply the rev-5.6 five-tick split rule if its actual threshold is reached before
continuing to redispatch this root-sized item. This worker does not edit the
authoritative DAG or generated checklist.

This artifact is current-base nonrelease blocker evidence only. It does not
satisfy `S56-M-1356-PROOF`, close a frozen obligation or the root, change
scheduler state, or claim proof completion, audit completion, theorem
completion, validation, release, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.
