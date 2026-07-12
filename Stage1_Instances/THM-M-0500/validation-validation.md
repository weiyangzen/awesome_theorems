# THM-M-0500 validation-phase handoff

Item: `S56-M-0500-VALIDATION`. Base revision:
`028e2535b68678b8296e63e2cacb05ed9775a2d8`.

The narrow structured recipe freshly elaborates the frozen statement transport, conditional
composition certificate, exact proof wrapper, pinned terminal declaration, and a separately written
exact-root reconstruction. The reconstruction imports neither `Proof` nor `ObligationTree`; it uses
the checked unbounded encoding and `Nat.forall_exists_prime_gt_and_eq_mod`. That declaration calls
`Nat.infinite_setOf_prime_and_eq_mod` in pinned mathlib, so this is differential wrapper/encoding
evidence, not a second terminal proof body or release-grade independent verification.

All checked declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. The runner
also checks input freshness, the frozen 14-obligation denominator, the proof receipt, prohibited
constructs, pinned mathlib commit/tree/cleanliness, and direct source and `.olean` hashes for
`Mathlib/NumberTheory/LSeries/PrimesInAP.lean`.

## Commands and exact results

Commands ran on 2026-07-12 (`Asia/Shanghai`).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0500
  exit 0: rank 877, planned, legacy artifacts unaccepted, theorem_complete=false

python3 Stage1_Instances/THM-M-0500/check_validation.py
  exit 0: exact statement, composition, proof root, and differential root replay passed;
  exact axiom observation and direct pinned provenance passed; stale authoritative graph,
  transitive trust/provenance, cold hermetic, and distinct-runner gates failed closed

python3 Stage1_Instances/THM-M-0500/check_proof.py
  exit 0: proof source/input hashes and exact proof-bearing wrapper passed

python3 Stage1_Instances/THM-M-0500/check_obligation_tree.py
  exit 0: 14 frozen obligations, 26 typed edges, and denominator passed; the pre-proof
  M3/root-open observation remains unchanged

python3 -m json.tool Stage1_Instances/THM-M-0500/validation-phase-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0500/validation-receipt.json
  exit 0: both validation artifacts are valid JSON

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0500 --glob '*.lean'
  exit 1 with empty output: pass; no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-0500 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The validator copies the four Lean modules into a temporary directory under `Formalizations/Lean`,
emits `Statement.olean` only there, prepends that directory to the pinned `LEAN_PATH`, and removes
the directory automatically. No `lake update`, `lake build`, dependency clone/fetch, network
request, or `.lake` mutation was performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact target transport, conditional composition, proof root, upstream declarations, and differential root freshly elaborate. |
| Placeholder/unsafe | pass | Comments-stripped target modules and the direct terminal mathlib source contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration. |
| Trust observation | provisional pass | Every checked declaration reports exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Direct provenance | pass | Frozen hashes, proof receipt, clean pinned mathlib commit/tree, and terminal source/compiled artifact agree. |
| Dependency acceptance | fail closed | The proof receipt is worker-provisional and has no master acceptance established in this clone. |
| Structured-state freshness | fail closed | The frozen pre-proof graph still records `root_closed=false`, `M3`, and open `M0500-T-NONSUM` / `M0500-L-SUPPORT`; a worker may not rewrite it. |
| Transitive trust/provenance | fail closed | Complete declaration/body/import closure, accepted foundation policy, full TCB, SBOM/licenses, and restoration archive are absent. |
| Hermetic reproduction | fail closed | The shared warm `.lake` was reused; there was no immutable clean checkout, cold empty-cache build, host-enforced network denial, or offline restoration. |
| Independent verification | fail closed | The differential module ran in this worker/cache and shares its terminal proof body; there is no distinct verifier identity, runner, signature, or independent minimal verifier. |

This validation node is genuinely self-tested as a provisional, fail-closed worker handoff. It does
not grant `E0/E1`, accepted `M0-W`, `AUDIT-Z`, `THEOREM-Z`, release, or master acceptance.
`audit_complete=false` and `theorem_complete=false` remain mandatory. The first node gate is proof
dependency master acceptance; the first release-specific gate is the section 10.6 cold empty-cache
hermetic replay.
