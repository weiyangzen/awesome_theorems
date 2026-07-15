# THM-M-1085 validation-phase evidence

Item: `S56-M-1085-VALIDATION`. Base revision:
`4ba3f2fd1e609b5958f24e0415eef9300da16924`; base tree:
`6abc1f64758c17a59dad8c80ac44f238983dc720`.

## Validation scope

The structured recipe re-elaborates the exact statement, the conditional composition interfaces,
the twenty implemented finite-law declarations, and two separately written partial probes in
disposable output space. Every Lean subprocess uses `--trust=0`, one Lean thread, fixed locale and
timezone, and a Bubblewrap network namespace. `Validation.lean` neither states nor proves
`SlepianTarget` or `LawSlepianTarget`; its same-worker checks corroborate only existing reductions
and are not distinct-runner evidence.

The exact target `Stage1Instances.THM_M_1085.SlepianTarget` remains open at `M4`.
`slepianTarget_of_law` consumes the uninhabited proposition `LawSlepianTarget`; it is a valid
conditional reduction, not a root proof. The frozen cut set remains `M1085-N-LAWS`,
`M1085-C-INTERPOLATION`, `M1085-L-INTERPOLATION-ID`, `M1085-L-MIXED-SIGN`, and
`M1085-L-LIMIT`.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused without mutation. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or network operation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1085
  exit 0: rank 527, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-1085/check_statement.py
  exit 0: exact target expression and four structural mutations checked; expression SHA-256
  2af285ae0bb208a80c325d1b8ba89cd273b83d01b2fef018b13e2feca9d43315

python3 Stage1_Instances/THM-M-1085/check_obligation_tree.py
  exit 0: 17 obligations and 65 typed edges passed; root open at M4

python3 -B Stage1_Instances/THM-M-1085/check_validation.py
  exit 0 in the final recorded 82-second run: exact statement, conditional interfaces, twenty
  partial proof declarations, and two same-worker differential probes elaborated under network
  isolation; stdout was 864 bytes in 9 lines with SHA-256
  db184cbd160b77951137b76b05523f0604ed9d6511bae719c08c6587428947f6; frozen hashes, hygiene,
  dependency pin, selected provenance, and open-root decisions agreed

python3 -m json.tool Stage1_Instances/THM-M-1085/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1085/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m1085-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1085/check_validation.py
  exit 0: validator bytecode compiled outside the repository tree

rg -n --glob '*.lean' '<prohibited construct pattern>' Stage1_Instances/THM-M-1085
  exit 1 with empty output: expected pass; no placeholder, bodyless, unsafe, external,
  implementation escape, or native-oracle construct occurred in Lean source

git diff --check -- Stage1_Instances/THM-M-1085 .stage1-worker-selftest.json
git diff --no-index --check /dev/null <each new validation artifact>
  exit 0 for the scoped tracked check; each no-index check returned Git's expected status 1 for
  an added file with no whitespace diagnostics
```

The snapshot-bound `check_proof.py` and its wrapper are intentionally not validation recipes: they
assert the old proof-phase base revision, pre-integration proof state, and proof-phase dirty-file
set. This phase binds their committed hashes and proof receipt, then replays the actual Lean
declarations directly.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact statement replay | pass | The frozen target and checked direct shape elaborate at the recorded expression fingerprint. |
| Conditional composition | pass, not root closure | Both checked bridges consume an open proposition with the exact required target. |
| Partial proof replay | pass, no frozen-node closure | Twenty finite-law, mean, covariance, matrix, and Gaussian-law declarations elaborate; accepted and provisional closed-obligation sets remain empty. |
| Placeholder and unsafe boundary | pass | Lean sorry reports and a comment-stripped scan found no prohibited proof mechanism. |
| Trust observation | provisional pass | Checked declarations use only `propext`, `Classical.choice`, and `Quot.sound`; the foundation profile and complete TCB closure remain open. |
| Selected provenance | provisional pass | Frozen local hashes and clean pinned mathlib revision/tree/remote/license agree; complete transitive provenance and SBOM do not exist. |
| Structured authority | fail closed | `S56-M-1085-PROOF` is only `[_]`; no proof receipt or obligation is master-accepted. |
| Root kernel closure | fail closed | `LawSlepianTarget` has no inhabitant; the interpolation, mixed-sign, and limit route remains open. |
| Hermetic replay | fail closed | Shared warm `.lake`; no clean checkout, empty-cache bootstrap, offline restoration, deterministic bundle, or complete TCB/SBOM. |
| Independent verification | fail closed | Differential probes share this worker, checkout, kernel, and cache; no distinct signed verifier or independent release checker exists. |

The first node gate is `dependency.S56-M-1085-PROOF.master_acceptance`; the first mathematical gate
is `proof.root_kernel_closure`; the first release gate is `S56-10.6-HERMETIC-COLD-BUILD`. The root
vector remains `[H1, M4, R4]`. `audit_complete=false` and `theorem_complete=false`. This packet
claims no E0/E1, M0, accepted state, complete validation, release, or master acceptance.
