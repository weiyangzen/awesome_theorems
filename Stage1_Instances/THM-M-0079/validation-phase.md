# THM-M-0079 validation-phase evidence

Item: `S56-M-0079-VALIDATION`. Base revision:
`db6914155f1f63e835364b89ba0a3b25f1d7f936`.

## Verdict

`self_tested_pending_master_acceptance`. The fail-closed validator replayed the exact frozen
Nielsen-Schreier statement, all five frozen composition declarations, all thirteen local proof
declarations, both exact proof roots, the pinned terminal declaration, and a separately written
exact adapter in fresh temporary output space. Every checked declaration uses only `propext`,
`Classical.choice`, and `Quot.sound`. Frozen local inputs, seven selected source/blob/olean
boundaries, the clean pinned mathlib revision, and tool identities agree. Lean `assert_no_sorry`
and a supplemental comment-stripped scan found no prohibited proof mechanism.

This is deliberately nonrelease evidence. The proof prerequisite is only provisional,
`M0079-S-FOUNDATION` and nine internal source-composition harnesses are open, and the run reused the
shared warm `.lake` artifacts. `Validation.lean` imports neither `Proof` nor `ObligationTree`, but it
shares the worker, checkout, cache, and mathematical route. It is same-worker differential
corroboration, not distinct signed independent verification. The accepted vector remains
`[H1, M3, R4]`; audit and theorem completion are false.

## Commands and exact results

Validation ran on 2026-07-13 (`Asia/Shanghai`). The existing pinned `.lake` artifacts were reused
without mutation. No Lake update/build, dependency clone/fetch, checkout, or `.lake` write ran.

```text
python3 -B Stage1_Instances/THM-M-0079/check_validation.py
  exit 0: exact statement, five compositions, thirteen proof declarations, two proof roots,
  terminal, and differential exact-root adapter elaborated; selected trust/provenance passed;
  authority, complete trust, cold hermetic, and independent-runner gates failed closed

bash Stage1_Instances/THM-M-0079/check_proof.sh
  exit 0: isolated exact proof replay passed; the terminal and thirteen local declarations were
  sorry-free and used exactly propext, Classical.choice, and Quot.sound

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0079
  exit 0: rank 1105, planned, L0/rework_required, theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-0079/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0079/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: validation recipe, receipt, and worker packet parse as JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0079-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0079/check_validation.py
  exit 0: validator compiled outside the repository tree

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\b' \
  Stage1_Instances/THM-M-0079/{Statement,ObligationTree,Proof,Validation}.lean
  exit 1 with empty output: expected pass, no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-0079 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The older `validation-specs.json` is not current proof-validation evidence. It belongs to
`S56-M-0079-OBLIGATION_TREE`, validates only the frozen architecture and conditional interfaces,
and grants `closure_credit=false`. Its phase-bound predecessor checkers are not rerun here. The new
`validation-spec.json` owns this validation node without changing the frozen architecture.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Exact statement, five compositions, thirteen proof declarations, two exact proof roots, terminal, and separate adapter elaborate in fresh temporary output space. |
| Placeholder and unsafe boundary | pass | `assert_no_sorry`, fourteen proof sorry reports, two differential sorry reports, and a supplemental scan found no placeholder, bodyless, unsafe/native/oracle, or external implementation construct. |
| Trust observation | provisional pass | Checked declarations use only `propext`, `Classical.choice`, and `Quot.sound`; `M0079-S-FOUNDATION` and complete transitive trust closure remain open. |
| Selected provenance | provisional pass | Frozen hashes, terminal body identity, seven source/blob/olean triples, clean mathlib revision/tree, remote, license, manifest, and tool hashes agree. This is not complete transitive declaration/TCB/SBOM provenance. |
| Internal composition | fail closed | Five frozen abstract-child compositions check locally, but nine deeper source-body certificates still lack exact child harnesses and receive no per-node closure credit. |
| Structured authority | fail closed | The proof prerequisite is only `[_]`; the instance and graph remain H1/M3/R4 with `root_closed=false`, no accepted receipt, and no accepted closed obligation. |
| Hermetic replay | fail closed | Shared warm `.lake`; no immutable clean checkout, cold empty-cache offline restoration, enforced network namespace, complete bootstrap/TCB inventory, or deterministic restorable archive. |
| Independent verification | fail closed | The separate adapter shares the route, worker identity, checkout, and cache; no distinct signed verifier, independent runner, or independently implemented minimal verifier exists. |

The first failed node gate is `dependency.S56-M-0079-PROOF.master_acceptance`; the first failed
release gate is `S56-10.6-HERMETIC-COLD-BUILD`. This validation implementation is genuinely
self-tested, but it grants no accepted `M0-W`, release-grade `E0/E1`, `AUDIT-Z`, `THEOREM-Z`,
release, or theorem-completion credit.
