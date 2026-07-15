# THM-M-1285 validation-phase record

Item: `S56-M-1285-VALIDATION`. Base revision:
`be35cd8f5123e9d06247b12859f3843bdd90c66f`.

## Scope and result

The narrow replay copied `Statement.lean`, `ObligationTree.lean`, `Proof.lean`,
and `Validation.lean` into a fresh temporary directory. Each module was
elaborated with the pinned Lean 4.29.0 executable at `--trust=0`, a read-only
host filesystem, fixed locale/timezone/thread count, and a Bubblewrap network
namespace with no network interface. Existing canonical pinned `.lake`
artifacts were reused read-only; no update, build, clone, fetch, or dependency
mutation was performed.

`Validation.lean` introduces no theorem or definition. It applies Lean's
transitive sorry collector and axiom printer to the exact root, the conditional
composition theorem, the statement transport, and every named proof theorem.
The exact root and every checked proof declaration report only `propext`,
`Classical.choice`, and `Quot.sound`, and all are sorry-free.

This is strong narrow worker evidence, not release evidence. The proof
predecessor remains provisional, the obligation registry and typed graphs are
the frozen pre-proof authority, and the theorem-specific foundation policy is
unaccepted. The warm shared dependency closure is not a cold empty-cache
replay. The trust probe shares this worker, checkout, Lean kernel, and cache, so
it is not the distinct signed verifier required by section 10.7.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1285` | 0 | Rank 456; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1285/check_obligation_tree.py` | 0 | Frozen 16-obligation, 83-edge architecture passed; authoritative root remains open at `M3`. |
| `bash Stage1_Instances/THM-M-1285/check_validation.sh` | 0 | Four fresh network-isolated `--trust=0` oleans compiled; 16 declarations were sorry-free and every observed axiom set was within the three classical mathlib axioms. Output SHA-256: `10efa8204a65ffe25156c02e2a12f82268b63a5644c6df2abe7fb221f190c47c`. |
| `python3 -I -B Stage1_Instances/THM-M-1285/check_validation.py` | 0 | Item/DAG identity, exact target, frozen hashes, proof provenance, hygiene, selected mathlib provenance, tool identities, receipt, and worker packet passed while missing release gates failed closed. |
| `python3 -m json.tool` on the validation spec, receipt, and worker packet | 0 | All three structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1285-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-1285/check_validation.py` | 0 | Validator syntax passed without writing into the repository. |
| scoped prohibited-construct `rg` over the four Lean modules | 1 | Expected empty-output pass: no prohibited construct was found. |
| `git diff --check -- Stage1_Instances/THM-M-1285 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The exact target, checked transport, conditional composition, complete local proof, and trust probe elaborate at trust zero. |
| Placeholder/unsafe hygiene | provisional pass | Lean transitive sorry checks plus a comment-aware local scan passed. |
| Axiom observation | provisional pass | All checked proof declarations report exactly the three recorded mathlib classical axioms, but no accepted theorem-specific foundation profile exists. |
| Selected provenance | provisional pass | Local bodies, frozen inputs, toolchain files, mathlib pin/tree/origin/license, and selected support-source blobs are bound. Complete transitive provenance remains open. |
| Proof dependency | fail closed | `S56-M-1285-PROOF` is `[_]`, not master-accepted. |
| Structured authority | fail closed | Registry/graphs retain planned fingerprints, no accepted evidence, and pre-proof root cut `M1285-T-PACKAGE`. |
| Hermetic release | fail closed | The run is network-isolated but reuses warm shared `.lake`; it is not an empty-cache clean-checkout offline restoration. |
| Independent verification | fail closed | The trust probe shares this worker, checkout, kernel, and cache; no distinct identity, signed attestation, or independent minimal verifier exists. |

The first failed node gate is proof master acceptance. Accepted state remains
`[H2, M3, R3]`; `audit_complete=false` and `theorem_complete=false`.
