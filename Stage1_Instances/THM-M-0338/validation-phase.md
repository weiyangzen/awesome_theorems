# THM-M-0338 validation phase

Item: `S56-M-0338-VALIDATION`. Base revision:
`38502dd8cfdb1c7b89d62d802952ab596838ec7e`.

## Verdict

`blocked`. This phase self-tests a truthful negative validation decision; it
does not validate the Kadison-Singer theorem. The proof prerequisite is only
provisional. It proposes `M0338-E-EXTENSION`, but accepted closure remains
empty and the uniqueness half has no proof body. The exact root therefore
remains `[H1, M3, R4]`; no `M0-*`, `E0`, `E1`, accepted validation state,
audit completion, or theorem completion is claimed.

The frozen graph still includes `M0338-E-EXTENSION` in its authoritative open
cut. The proof receipt proposes the smaller remaining cut
`M0338-KS-PAVING`, `M0338-W-MSS`, `M0338-X-SOURCE`, and
`M0338-X-FOUNDATION`. Validation preserves both views rather than changing
authority that belongs to the integration lane.

## Executed validation

`Validation.lean` imports the integrated proof module but adds no mathematical
proof. It applies elaborator-aware `assert_no_sorry`, `#print sorries`, and
`#print axioms` checks to the conditional composition and both extension-
existence declarations, then observes their transitive declaration closure.
The validator replays `Statement.lean`, `ObligationTree.lean`, `Proof.lean`,
and `Validation.lean` at `--trust=0` inside Bubblewrap with isolated network,
a read-only host root, fixed locale/timezone/thread count, and a fresh writable
output directory.

This is narrow warm-cache evidence only. It reuses the automation-provided
canonical `.lake` compiled artifacts without mutation. The checker invokes no
Lake command, update, build, clone, fetch, or network operation.

| Gate | Result |
|---|---|
| Exact target and narrow kernel replay | provisional pass: the statement, conditional composition, and two extension-existence declarations elaborate at trust zero |
| Placeholder/unsafe observation | provisional pass: three `assert_no_sorry` checks; observed closure has no unexpected bodyless nonaxiom or unsafe declaration |
| Axiom observation | exactly `propext`, `Classical.choice`, and `Quot.sound`; no accepted foundation-policy decision follows |
| Selected direct provenance | provisional pass: local hashes, pinned mathlib revision/tree/origin/license, and three source/olean boundaries agree |
| Proof dependency and exact root | fail closed: the proof node lacks master acceptance and `ExtensionAtMostOne` plus every substantive uniqueness branch remains open |
| Complete trust/provenance | fail closed: transitive artifact origin, accepted foundation profile, and complete TCB/SBOM remain absent |
| Hermetic release | fail closed: worker clone and shared warm cache, no cold empty-cache build or offline restoration |
| Independent verification | fail closed: same worker, checkout, toolchain, and cache; no second signed attestation or independent verifier |
| Source/readability | fail closed: primary-source H0 mapping/errata review and independent R0 review remain open |

## Commands and results

Commands ran on 2026-07-15 (Asia/Shanghai) from the worker root unless noted.
The final self-test records these exact results:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0338` | 0 | rank 831, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0338/check_statement.py` | 0 | expression hash and all four structural mutations passed |
| `python3 Stage1_Instances/THM-M-0338/check_anchor_audit.py` | 0 | exact statement-only boundary and pinned candidate probes passed |
| `python3 Stage1_Instances/THM-M-0338/check_obligation_tree.py` | 0 | 16 obligations and 70 typed edges passed; root remains M3/open |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0338/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | network-isolated trust-zero replay, receipt, selected provenance, and fail-closed decisions passed |
| `python3 -m json.tool ...` for the validation spec, receipt, blocker, and worker packet | 0 | all validation JSON artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0338-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0338/check_validation.py` | 0 | validator compiled outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-0338 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The validation runner's exact summary is:

```text
PASS narrow kernel replay: exact statement, conditional composition, and two extension-existence declarations elaborated at trust zero
PASS trust observation: all three declarations report only propext, Classical.choice, and Quot.sound; closure has no unexpected bodyless or unsafe declaration
PASS selected provenance: frozen hashes, three direct mathlib source/olean boundaries, toolchain pins, license, and clean pinned revision agree
OPEN exact root: extension uniqueness, paving, Weaver/MSS, source, and foundation obligations remain open at M3
FAIL CLOSED complete trust/provenance: accepted foundation policy, transitive artifact provenance, and full TCB/SBOM inventory are absent
FAIL CLOSED release gates: shared warm cache is not cold hermetic evidence and this worker is not an independent verifier
```

The first failed workflow gate is
`dependency.S56-M-0338-PROOF.master_acceptance_and_M0338-U-UNIQUE.root_closure`.
Retry requires a master-accepted predecessor with placeholder-free uniqueness
and Kadison-Singer/MSS bodies and a premise-free root, followed by accepted
source/readability and complete trust/provenance review, clean cold offline
replay, and distinct signed independent verification.
