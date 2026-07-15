# THM-M-0729 proof blocker at `6bf9ee93` (slot47)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Recorded at: `2026-07-16T04:56:24+08:00`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. No eligible placeholder-free Lean 4 body closes either inclusion required by the exact
root `Stage1Instances.THM_M_0729.PCPTheorem`. The proof item stays `[ ]`, lifecycle stays
`planned`, and the root vector stays `[H3, M3, R4]`. Audit completion and theorem completion remain
false.

The mandatory v2 dependency inspection was completed before proof search. `THM-M-0729` has no
direct hard parents, transitive hard ancestors, hard edges, reuse hints, or shared groups. The new
`dependency-reuse-ledger.json` records that empty audited closure using schema 1.1 and the supplied
graph digest `73e99d22...0eca`, context digest `068170c7...c5c`, and exact worker base. The scheduler's
ledger validator accepted it with zero inspections and zero reuse decisions. Thus no unresolved
cross-theorem compatibility issue blocks this target and no ancestor transfers proof credit.

## Exact Blocker

The immediate machine cut remains both directional packages:

- `M0729-D-NP-PCP`: construct a logarithmic-randomness, constant-query, perfect-completeness,
  soundness-one-half checker from every verifier-based NP witness. This is the substantive PCP
  theorem. The repository and pinned dependencies contain no verifier-to-constraint reduction,
  robustness/gap theorem, PCP composition development, or checked resource transport.
- `M0729-D-PCP-NP`: construct an NP verifier from each frozen PCP witness. Existing
  `ProofProgress*` bodies already prove finite reachable-position serialization, a global
  polynomial certificate-size bound including short inputs, exhaustive coin enumeration, and the
  exact Boolean certificate characterization. The remaining body is a bundled
  `TM2ComputableInPolyTime encodePair encodeBool` implementation of that verifier with a polynomial
  runtime proof.

The reverse machine obligation is not a small wrapper. It must compose and iterate the arbitrary
machines carried by the checker, enumerate exponentially many strings in a logarithmic random
length, compute their queries, decode the finite certificate, and prove the resulting runtime
polynomial using the particular `InPCPLogConst` bounds. A bare `Checker` need not itself have
logarithmic random length, so the convenient universal premise in the existing conditional bridge
cannot be proved from checker fields alone. Pinned mathlib provides only the relevant structures
and identity implementation; `Turing.TM2ComputableInPolyTime.comp` is a discarded `proof_wanted`
marker, not an importable theorem.

No definitional shortcut exists. Zero randomness has one coin function, so soundness one half
forces rejection rather than making no-instances vacuous. Oracle proofs reduce extensionally to
finitely many reachable positions, but the polynomial-time machine witness remains real. The
checked `root_of_directionalPackage` assumes both complete inclusions and gives no credit for them.
Adding another conditional wrapper would duplicate the already checked reverse bridge without
closing a frozen obligation, so no such body was added.

The phase prerequisite `S56-M-0729-OBLIGATION_TREE` is still provisional `[_]`, not master accepted.
That independently prevents master acceptance of this proof node.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch/checkout, network command, or `.lake` mutation
was run. All Lean outputs were confined to a disposable `/tmp` tree and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 | The v2 subvalidator detected the expected integration-bound inventory delta caused by the required new ledger. Fresh generation differs only for this target's `structured_json_files` list (29 checked-in versus 30 fresh). Workers may not edit the authoritative generated DAG. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Same isolated post-ledger delta: fresh generation adds `Stage1_Instances/THM-M-0729/dependency-reuse-ledger.json`. The integration lane regenerates the DAG after preserving this blocker batch. |
| `python3 scripts/stage1_target.py check` | 0 | Passed all 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; all four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and hashes agreed; no exact root candidate is claimed; root M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both directional packages remain open. |
| Scheduler `validate_dependency_reuse_ledger` with exact graph/context/base | 0 | Accepted the schema-1.1 ledger with an empty audited closure. |
| Disposable eight-module `lake env lean --trust=0 -t0 -R` replay | 0 | `Statement`, all five `ProofProgress*` modules, `ObligationTree`, and `ProofBlockerProbe` elaborated against pinned artifacts. |
| Direct `lake env lean --trust=0 -t0 .../Statement.lean` | 0 | Elaborated and printed the exact set-equality target. |
| Prohibited-device scan of all nine target Lean sources | 1 expected | No `sorry`, `admit`, `sorryAx`, `axiom`, bodyless constant, `opaque`, `unsafe`, `external`, `native_decide`, or `implemented_by` device. |
| Scoped exact-PCP source search | 0 | 59 matching lines; no terminal directional inclusion or exact-root body; output SHA-256 `9e7dba7a...e935368b`. |
| Pinned composition-source check | 0 | `TM2ComputableInPolyTime.comp` occurs only as `proof_wanted` at `Computable.lean:284`. |
| Frozen target-input diff since `260bbb3ef` | 0 | Statement, proof-progress sources, obligation data, toolchain, dependency manifest, and target manifest are unchanged. |

The trust-zero disposable olean hashes are bound in the paired JSON artifact. The environment is
Lean `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, pinned mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, and validation trust level zero.

## Reopen Condition

Split the oversized proof item into dependency-legal forward and reverse children. The forward
lane must implement the full frozen PCP reduction packages. The reverse lane must implement and
time-bound the explicit bundled TM2 verifier using the particular PCP witness's logarithmic and
query bounds. An alternative is an immutable, compatible terminal Lean 4 proof of the exact target
with complete body/dependency/license provenance and repo-local checking.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0729-PROOF`, close either inclusion or the root, promote scheduler state, or claim audit
completion, validation, release, theorem completion, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely complete, `.stage1-worker-selftest.json` remains
absent.
