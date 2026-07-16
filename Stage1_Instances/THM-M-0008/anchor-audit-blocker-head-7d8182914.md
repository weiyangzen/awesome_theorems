# Anchor-audit scheduler-ownership blocker

Item: `S56-M-0008-ANCHOR_AUDIT`  
Theorem: `THM-M-0008`  
Worker base revision: `7d8182914615a5f5f0445f515fbd635a74bf1faa`  
Worker base tree: `8b4e8697f3cc153b4bc2ae68ff0efc2bf0ccddb3`  
Worker verdict: `blocked`  
Proposed state: `[ ]` (unchanged)  
Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The mandatory HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`. For
`anchor_audit` it declares exactly these scheduler-owned validator candidates:

- `Stage1_Instances/THM-M-0008/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0008/check_anchor.py`

Neither path exists in commit `7d8182914615a5f5f0445f515fbd635a74bf1faa`, and neither exists in
this worker tree. The contract requires exactly one candidate, requires it to exist at the worker
base, and requires its HEAD blob to equal its worker-base blob. The assignment also forbids a worker
from creating, refreshing, renaming, replacing, or deleting either candidate. Therefore no lawful
authority replay or semantic validator result is available. An undeclared adapter, a different
phase's validator, command success, prose output, or a worker-created candidate cannot repair this
gate.

The independent topology gate `G02-TOPOLOGY` is also closed for master acceptance: the sole
intra-theorem predecessor, `S56-M-0008-STATEMENT`, is worker-self-tested `[_]`, not
master-accepted `[x]`. This does not prevent truthful audit observations, but it prevents this phase
from being master-accepted now.

## Claim order and dependency context

The authoritative claim tuple is `(v2_execution_rank=319, phase_layer=2,
phase_item_id=S56-M-0008-ANCHOR_AUDIT)`. The theorem-DAG file SHA-256 is
`6ce46e0d9e79e1a40c423ae1074db34e889702b9a5b5989034cd462615fed604`, and the
target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The complete `parent_inspection_order`, direct-parent list, transitive-ancestor list, hard-edge list,
reuse-hint list, and shared-group list are all empty. The empty sequence was inspected as the
complete closure; no provider declaration, proof body, receipt, checkbox state, or acceptance was
reused or transferred. The existing target-owned dependency ledger binds an earlier graph/base and
is stale for this claim. It was not refreshed because this claim cannot reach a lawful self-test,
and a new ledger alone cannot repair the missing scheduler-owned validator.

## Scoped audit observations

The source statement remains unresolved. The repository supplies only the label `Tor theorem`, the
gloss `properties of the Tor functor`, a 1950s date, and an untrusted `verified` label. It does not
select projective or flat vanishing, balancedness, a degree-zero comparison, a long exact sequence,
or another materially different Tor result. Consequently there is no canonical target expression
or statement fingerprint against which any candidate can be normalized as exact.

The bounded immutable observations available at this base are:

- The repo-local legacy source
  `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_101.lean` is Git blob
  `70f2874396cc1b58f431f1fb0cb85c68aa9dc7be` and SHA-256
  `7e03aff6c78c9558c94c12812692bec84a255dc9289b3d2e844f2e5de111a5b7`.
  It checks genuine Tor definitions, projective-vanishing wrappers, and generic homology-sequence
  substrate. Its terminal `StatementShape` is nonemptiness of an assumption-bearing property
  package whose fields include balanced comparison and long-exactness. It is a legacy M3
  statement/interface candidate, not a source-faithful root proof, and rev-5.6 transfers no proof or
  acceptance credit from it.
- The pinned environment is Lean `v4.29.0` and mathlib revision
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The exact Tor source is
  `Mathlib/CategoryTheory/Monoidal/Tor.lean`, Git blob
  `be278f05b835432cad600a74de58f78c9031162f`, SHA-256
  `63aeefddef4fdbf5f74cade1c13f0d63b742247c2ff2c69a9546454c57d34860`.
  It defines `CategoryTheory.Tor` and `CategoryTheory.Tor'` and proves
  `isZero_Tor_succ_of_projective` and its primed analogue. Its module documentation explicitly says
  that it has almost nothing else, and that the natural isomorphism between the two derivations
  remains future theory. These are pinned M3 substrate and theorem-family candidates; without the
  missing canonical statement they cannot receive exact-root M0 credit.
- A bounded scan of every other materialized Lake package found no additional Tor-family Lean
  declaration. A repo-wide Lean scan found only neighboring or legacy consumers, notably
  `THM-M-0005` and `S1_M_099`; none is an independent exact terminal proof for this unresolved root.
  This is bounded local evidence only, not a global absence or saturation claim.
- Narrow `lake env lean --trust=0` re-elaboration succeeded for the target-owned `Statement.lean`
  vocabulary probe and the tracked legacy `S1_M_101.lean` surface using the existing pinned
  artifacts. The sandbox also emitted non-fatal `Failed to create stream fd: Operation not
  permitted` diagnostics. These checks confirm only that the recorded interfaces elaborate; they
  do not select or prove the root and cannot substitute for the missing phase validator.
- Public Lean 4, statement-only, historical/other-prover, and primary-human-source lanes were not
  completed into content-bound evidence at this base. Network access is denied, no immutable
  external candidate bytes were supplied, and the existing source crosswalk gives only possible
  research loci without a verified edition/theorem/page locator. These lanes remain open rather
  than being misreported as negative results.

The truthful provisional root classification remains `M4`: no usable formal artifact can be
matched to an exact target because the target itself is not selected. The individual mathlib and
legacy surfaces are M3 statement/interface or substrate candidates. No candidate receives root
proof credit, and no H0, M0, R0, `AUDIT-Z`, or `THEOREM-Z` claim follows.

## Commands and results

All commands ran in this worker clone without changing `.lake` or fetching dependencies.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, v2 theorem DAG, seven-phase acceptance contract, execution skill present)` |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | `check_stage1_theorem_dag_v2: ok (1546 theorems, 10822 blueprint states, 2 hard edges, 5 reuse hints, 311 shared groups, acyclic)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0008` | 0 | Rank 101, lifecycle `planned`, baseline `L0`, legacy artifacts unaccepted, and `theorem_complete=false`. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0008/Statement.lean` | 0 | The four pinned Tor vocabulary declarations elaborated; three non-fatal stream-fd sandbox diagnostics were emitted. |
| `cd Formalizations/Lean && lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_101.lean` | 0 | The legacy interface and its Tor/mathlib wrappers elaborated; three non-fatal stream-fd sandbox diagnostics were emitted. |
| `git diff --check -- Stage1_Instances/THM-M-0008 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

No anchor validator command exists to run. In particular, exit zero from either Lean elaboration is
not a semantic anchor-audit result and cannot make `phase_accepted` true.

## Retry condition

The scheduler must commit exactly one declared anchor-audit validator at one of the two contract
candidate paths, then issue a fresh claim whose worker base contains that identical blob. The
statement predecessor must separately obtain master acceptance `[x]` before this phase can pass the
topology gate. A fresh worker can then precommit and execute all seven ordered discovery lanes,
content-bind every result and access failure, refresh the empty dependency ledger to the fresh graph
and base, produce exactly one phase receipt, and replay the unchanged validator.

No `anchor-audit.json`, discovery-evidence artifact, phase receipt, or
`.stage1-worker-selftest.json` is produced by this blocked claim. This blocker grants no phase state
transition, phase acceptance, proof credit, audit completion, theorem completion, or master
acceptance.
