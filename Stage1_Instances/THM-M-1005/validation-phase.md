# THM-M-1005 validation-phase evidence

Item: `S56-M-1005-VALIDATION`. Base revision:
`3bb4cb3ae15dff8b48c93242019edec3bf858e48` (tree
`8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc`).

## Verdict

`self_tested_pending_master_acceptance`. The fail-closed recipe freshly elaborates the exact frozen
statement, conditional composition boundary, vendored analytic proof body, proof wrappers, exact
proof root, and a separately written exact-root reconstruction. The Lean subprocesses run with a
read-only host root, fresh temporary output directory, fixed locale/timezone/umask, and no network
namespace. Both exact roots report precisely `propext`, `Classical.choice`, and `Quot.sound`; Lean's
transitive `assert_no_sorry` check passes for the vendored terminal and differential root.

This remains nonrelease evidence. `S56-M-1005-PROOF` is worker-provisional, `M1005-S-FOUNDATION`
and complete transitive trust/TCB/SBOM closure are open, and the canonical warm `.lake` cache was
reused read-only. `Validation.lean` imports neither `Proof` nor `ObligationTree`, but shares the same
worker, checkout, cache, and vendored analytic terminal. It is differential transport evidence, not
a distinct proof body, independently provisioned runner, signed attestation, or independently
implemented minimal verifier.

Structured authority also disagrees: `instance.json` records `[H2, M4, R4]`, while the frozen graph
and proof receipt describe accepted `[H2, M3, R4]`. Validation does not rewrite that state; the
weaker `[H2, M4, R4]` is reported pending master reconciliation. No obligation or root is accepted,
and `audit_complete=false` and `theorem_complete=false` remain explicit.

## Commands and exact results

Validation ran on `2026-07-14` (`Asia/Shanghai`). No `lake update`, `lake build`, dependency clone or
fetch, checkout, or `.lake` mutation was run by this worker. One read-only attempt to resolve the
recorded upstream PR commit triggered Git promisor-object lookup and failed without retrieving an
object; therefore only the structured Lean replay itself is claimed as network-denied.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1005
  exit 0: rank 285, planned, legacy artifacts unaccepted, theorem_complete=false

bash Stage1_Instances/THM-M-1005/check_validation.sh
  exit 0: network-isolated statement, conditional composition, vendored analytic body, proof root,
  and differential root elaborated; exact roots used propext, Classical.choice, and Quot.sound;
  vendored terminal and differential root were transitively sorry-free

python3 -B Stage1_Instances/THM-M-1005/check_validation.py
  exit 0: exact kernel replay, selected trust/provenance, input and receipt freshness, structured
  authority boundary, and worker packet passed; authority, complete trust, cold hermetic, and
  distinct-runner gates failed closed

python3 -B Stage1_Instances/THM-M-1005/check_statement.py
  exit 0: canonical expression SHA-256
  32343e66034f94d4afabc10f4d15cbae77daf650c757023a2142aafba50366e5 and four mutations passed

python3 -B Stage1_Instances/THM-M-1005/check_obligation_tree.py
  exit 0: 14 frozen obligations and 48 typed edges passed; its intentionally pre-proof root remains
  open at M3 with M1005-T-STRONG-ESTIMATE in that snapshot's cut set

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}
git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1
  exit 0: pinned revision 8a178386...ea95, tree bdc39a31...c2b, and empty status

python3 -m json.tool on validation-spec.json, validation-receipt.json, and worker packet
PYTHONPYCACHEPREFIX=/tmp/stage1-m1005-validation-pycache python3 -m py_compile check_validation.py
  exit 0: JSON parsed and Python compiled outside the repository tree

rg -n '<prohibited construct pattern>' target Lean sources
  exit 1 with empty output: expected pass; no executable placeholder, axiom declaration,
  unsafe/native/oracle, opaque/bodyless, or external implementation construct found

git diff --check -- Stage1_Instances/THM-M-1005 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The proof-phase `check_proof.py` is deliberately not reused after installing this validation worker
packet because it binds the root packet to `S56-M-1005-PROOF`. The new validator independently binds
the proof receipt and replays the actual Lean sources. The older `validation-specs.json` remains the
obligation-tree architecture recipe and is not relabeled as validation-node evidence.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Exact target, proof, frozen composition, and differential root freshly elaborate. |
| Placeholder and unsafe boundary | pass | `assert_no_sorry`, printed sorry reports, and comment-stripped scans pass. |
| Trust observation | provisional pass | Exact roots use exactly the observed three axioms; accepted foundation policy and full TCB closure remain open. |
| Selected provenance | provisional pass | Target and denominator hashes, vendored/upstream identities, pinned mathlib commit/tree/source/blob/olean/license, and tool digests agree. The upstream source identity is inherited from the proof receipt because the PR commit is not locally recoverable. |
| Structured authority | fail closed | Proof is only `[_]`; no obligation is accepted; M4/M3 projections conflict and need master reconciliation. |
| Hermetic replay | fail closed | Shared warm `.lake`; no immutable clean checkout, empty-cache bootstrap, offline restoration, deterministic bundle, or complete SBOM/TCB inventory. |
| Independent verification | fail closed | Same worker, checkout, cache, and analytic terminal; no distinct signed runner or independent minimal verifier. |

The first failed node gate is `dependency.S56-M-1005-PROOF.master_acceptance`; the first failed release
gate is `S56-10.6-HERMETIC-COLD-BUILD`. The validation implementation is genuinely self-tested, but
it grants no accepted `M0-L`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit.
