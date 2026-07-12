# S56-M-1015-VALIDATION worker evidence

Date: `2026-07-12`. Base revision: `024dea59d40069399858f4e49dfcadb026874ddb`.

The narrow validator copied the exact statement, proof, and an independently written validation
module into a fresh temporary directory, elaborated the statement, then kernel-checked both roots.
`Validation.lean` does not import the proof or obligation tree and reconstructs the quotient branch.
Both roots report exactly `[propext, Classical.choice, Quot.sound]`; forbidden proof tokens and
unsafe declarations are absent. The pinned mathlib checkout is at the manifest revision and clean.

## Commands and results

```text
$ python3 Stage1_Instances/THM-M-1015/check_validation.py
PASS THM-M-1015 validation: exact proof and independent reconstruction kernel-check
axioms: [propext, Classical.choice, Quot.sound]
statement sha256: ec54dada8ac9c934b8863d5e1ae96c5502e6f93f2bb1ef35cb5b488372744fb1
mathlib revision: 8a178386ffc0f5fef0b77738bb5449d50efeea95
exit 0

$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok; 1546 uniform-L0 targets; exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok; 1546 unique targets, ranks 1..1546; exit 0

$ python3 scripts/stage1_target.py show THM-M-1015
rank 294; planned L0/rework_required; theorem_complete false; exit 0

$ python3 Stage1_Instances/THM-M-1015/check_anchor_audit.py
PASS; pinned mathlib anchor and status boundary validated; exit 0

$ python3 Stage1_Instances/THM-M-1015/check_obligation_tree.py
PASS THM-M-1015 obligation tree: 17 obligations, 38 typed edges; exit 0

$ git diff --check -- Stage1_Instances/THM-M-1015 .stage1-worker-selftest.json
no output; exit 0
```

No Lake update/build, dependency fetch, network access, or `.lake` mutation was performed.

## Fail-closed boundary

This is provisional warm-cache worker validation, not release-grade hermetic or independent-runner
evidence. The prerequisite proof awaits master acceptance, and the frozen typed graph predates proof
closure. Cold empty-cache offline replay, full transitive TCB/provenance and SBOM/license evidence,
a second signed independent runner, H0/R0, release, and master acceptance remain open. Consequently
`audit_complete` and `theorem_complete` remain false.
