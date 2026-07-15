# THM-M-0339 validation phase

Item: `S56-M-0339-VALIDATION`. Base revision:
`e4c6d32d1eb44bab8a06b606e6f2274e442d7f45`.

## Verdict

`blocked`. This phase self-tests a truthful negative validation decision; it does not validate the
theorem. The proof prerequisite is provisional and closes zero frozen obligations. `Proof.lean`
contains seven elementary parameter branches and an exact composition only from the explicit,
unproved `HardRegimeEngine`. Consequently the canonical MSS partition root remains `M4` and no
`M0-*`, `E0`, `E1`, accepted state, audit completion, or theorem completion is claimed.

The frozen graph records the minimal open frontier as `M0339-L-THEOREM14`. The later proof receipt
expands the unresolved package debt to `M0339-C-RANDOM`, `M0339-C-MCP`,
`M0339-L-REALROOTED`, `M0339-L-INTERLACING`, `M0339-L-BARRIER`, and
`M0339-L-THEOREM14`. Validation preserves both views instead of reconciling authoritative state.

## Executed validation

`Validation.lean` imports the proof module but adds no mathematical proof. It applies mathlib's
elaborator-aware `assert_no_sorry` and `#print sorries` checks to all eight proof-phase declarations,
then observes their transitive declaration closure. The validator runs `Statement.lean`,
`Proof.lean`, and `Validation.lean` at `--trust=0` inside Bubblewrap with an isolated network, a
read-only host root, fixed locale/timezone/thread count, and a fresh writable output directory.

This is narrow warm-cache evidence only. It reuses the automation-provided `.lake` compiled
artifacts. The final self-test invokes no Lake command, update, build, clone, fetch, dependency
write, or network operation. Earlier exploratory Lake attempts unexpectedly launched an undeclared
`flt-regular` fetch and mutated its shared `FETCH_HEAD`. Those attempts are invalid evidence; the
worker did not repair or revert the shared cache. The final checker reads the missing `HEAD` ref
locally and fails the Lake/hermetic gate without invoking Lake.

| Gate | Result |
|---|---|
| Exact target and narrow kernel replay | provisional pass: statement, seven elementary bodies, and conditional composition elaborate at trust zero |
| Placeholder/unsafe observation | provisional pass: eight `assert_no_sorry` checks; observed closure has no bodyless nonaxiom or unsafe declaration |
| Axiom observation | `propext`, `Classical.choice`, and `Quot.sound`; no accepted foundation-policy decision follows |
| Selected direct provenance | provisional pass: local hashes, pinned mathlib revision/tree/origin/license, and three source/olean boundaries agree |
| Complete trust/provenance | fail closed: transitive artifact origin, accepted foundation profile, and complete TCB/SBOM remain absent |
| Exact root | fail closed: `HardRegimeEngine` has no premise-free terminal body; zero frozen obligations close |
| Hermetic release | fail closed: dirty worker clone, shared warm cache, broken Lake recipe, no cold empty-cache build or offline restoration |
| Independent verification | fail closed: same worker, checkout, toolchain, and cache; no second signed attestation or independent verifier |
| Source/readability | fail closed: primary-source H0 mapping/errata review and independent R0 review remain open |

## Commands and results

Commands ran on 2026-07-15 (Asia/Shanghai) from the worker root unless noted.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0339` | 0 | rank 832, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0339/check_obligation_tree.py` | 0 | 19 obligations and 35 typed edges passed; frozen root remains M4/open |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0339/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | network-isolated trust-zero replay, receipt, selected provenance, and fail-closed decisions passed |
| `python3 -m json.tool ...` for the spec, receipt, and worker packet | 0 | all validation JSON artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0339-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0339/check_validation.py` | 0 | validator compiled outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-0339 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The first failed gate is
`dependency.S56-M-0339-PROOF.master_acceptance_and_M0339-L-THEOREM14.root_closure`.
Retry requires a master-accepted predecessor with a placeholder-free hard MSS proof package and
premise-free exact root, followed by accepted source/readability and complete trust/provenance
review, clean cold offline replay, and distinct signed independent verification.
