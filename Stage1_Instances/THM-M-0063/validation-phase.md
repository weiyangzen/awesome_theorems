# THM-M-0063 validation-phase evidence

Item: `S56-M-0063-VALIDATION`. Base revision:
`1944ddb6f503b699293e82f18d19efe0f32b4380`.

## Verdict

`self_tested_pending_master_acceptance`. The fail-closed validator replayed the exact frozen Cayley
statement, all six frozen compositions, all twelve proof declarations, both exact proof roots, the
pinned terminal, and a separately written exact adapter in fresh temporary output space. All
checked declarations use only `propext`, `Classical.choice`, and `Quot.sound`. Frozen local inputs,
five selected source/blob/olean boundaries, the clean pinned mathlib revision, and tool identities
agree. No prohibited proof mechanism was found.

This is deliberately nonrelease evidence. The proof prerequisite is only provisional, the
foundation certificate and complete transitive trust closure are open, and the run reused the
shared warm `.lake` artifacts. The same-worker adapter imports neither `Proof` nor `ObligationTree`,
but shares the checkout, cache, and underlying proof route. It is not distinct signed independent
verification. The accepted vector remains `[H1, M3, R4]`; theorem completion is false.

## Commands and exact results

Validation ran on 2026-07-13 (`Asia/Shanghai`). The existing pinned `.lake` artifacts were reused
read-only. No Lake update/build, dependency clone/fetch, checkout, or `.lake` mutation ran.

```text
python3 -B Stage1_Instances/THM-M-0063/check_validation.py
  exit 0: exact statement, six compositions, twelve proof declarations, two proof roots, pinned
  terminal, and differential exact-root adapter elaborated; selected trust/provenance passed;
  authority, complete trust, cold hermetic, and independent-runner gates failed closed

bash Stage1_Instances/THM-M-0063/check_proof.sh
  exit 0: isolated exact proof replay passed; twelve declarations were sorry-free and used only
  propext, Classical.choice, and Quot.sound

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0063
  exit 0: rank 1094, planned, L0/rework_required, theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-0063/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0063/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: validation recipe, receipt, and worker packet parse as JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0063-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0063/check_validation.py
  exit 0: validator compiled outside the repository tree

rg -n -i --glob '*.lean' '<prohibited construct pattern>' \
  Stage1_Instances/THM-M-0063/{Statement,ObligationTree,Proof,Validation}.lean
  exit 1 with empty output: expected pass, no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-0063 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The older frozen `validation-specs.json` is not reported as current proof validation. It belongs to
`S56-M-0063-OBLIGATION_TREE`, validates architecture and conditional interfaces, and grants
`closure_credit=false`. The node-specific `validation-spec.json` records this narrow validation
without altering the frozen architecture.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The exact statement, all proof declarations, every frozen composition, two exact proof roots, terminal, and separate adapter elaborate in fresh temporary output space. |
| Placeholder and unsafe boundary | pass | `assert_no_sorry`, all twelve proof sorry reports, and a comment-stripped scan found no placeholder, bodyless, unsafe/native/oracle, or external implementation construct. |
| Trust observation | provisional pass | Checked declarations use only the observed `propext`, `Classical.choice`, and `Quot.sound`; `M0063-S-FOUNDATION`, an accepted theorem-specific policy, and complete transitive trust closure remain open. |
| Selected provenance | provisional pass | Frozen hashes, terminal/body identity, five source/blob/olean triples, clean mathlib revision/tree, remote, license, manifest, and tool hashes agree. This is not complete transitive declaration/TCB/SBOM provenance. |
| Structured authority | fail closed | The proof prerequisite is only `[_]`; the instance and graph remain H1/M3/R4 with `root_closed=false`, no accepted receipt, and no accepted closed obligation. |
| Frozen recipe freshness | fail closed | `validation-specs.json` belongs to the obligation-tree snapshot and expressly grants no closure credit; only the new validation-node recipe applies to this run. |
| Hermetic replay | fail closed | Shared warm `.lake`; no immutable clean checkout, cold empty-cache offline restoration, enforced network namespace, complete bootstrap/TCB inventory, or deterministic restorable archive. |
| Independent verification | fail closed | The separate adapter shares the route, worker identity, checkout, and cache; no distinct signed verifier, independent runner, or independently implemented minimal verifier exists. |

The first failed node gate is `dependency.S56-M-0063-PROOF.master_acceptance`; the first failed
release gate is `S56-10.6-HERMETIC-COLD-BUILD`. This validation implementation is genuinely
self-tested, but it grants no accepted `M0-W`, release-grade `E1`, `AUDIT-Z`, `THEOREM-Z`, release,
or theorem-completion credit. `audit_complete=false` and `theorem_complete=false` remain explicit.
