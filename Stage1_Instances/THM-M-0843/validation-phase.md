# THM-M-0843 validation-phase evidence

Item: `S56-M-0843-VALIDATION`. Base revision:
`d750776142c633e42858cebfc67c5c2664d419d7`.

The scoped validator copied the frozen statement, obligation composition,
proof, and differential probe into a fresh temporary module directory. It
then kernel-checked the exact pinned terminal, the frozen terminal-to-root
composition, both proof-phase roots, and a separately written exact root that
imports neither `Proof` nor `ObligationTree`.

Every checked proof-bearing declaration reports only `propext`,
`Classical.choice`, and `Quot.sound`. The validator also checks the target and
registry fingerprints, local placeholder/unsafe/oracle hygiene, the clean
pinned mathlib revision and tree, all directly inventoried regularity source
hashes, the terminal olean, and the mathlib license.

## Commands and results

Validation ran in the worker clone on 2026-07-13. The canonical pinned
`.lake` artifacts were reused without update, build, clone, fetch, or other
dependency mutation.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0843
  exit 0: rank 1032, planned, L0/rework_required,
  theorem_complete=false

python3 -B Stage1_Instances/THM-M-0843/check_validation.py
  exit 0: exact-root replay, trust observation, direct provenance, hygiene,
  and architecture checks passed; authoritative, hermetic, and independent
  release gates failed closed

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0843-validation-pycache \
  python3 -m py_compile \
  Stage1_Instances/THM-M-0843/check_validation.py
  exit 0: checker syntax compiled outside the owned path

python3 -m json.tool \
  Stage1_Instances/THM-M-0843/validation-spec.json
python3 -m json.tool \
  Stage1_Instances/THM-M-0843/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for all three JSON artifacts

git diff --check -- Stage1_Instances/THM-M-0843 \
  .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The checker obtains the pinned Lean executable and `LEAN_PATH` through
`lake env`, writes temporary oleans only under `Formalizations/Lean`, and
removes that directory after the run.

## Gate decisions

| Gate | Decision | Evidence or boundary |
|---|---|---|
| Exact kernel replay | provisional pass | The exact terminal, frozen composition, both proof roots, and differential exact root elaborate. |
| Placeholder and unsafe policy | pass | The five checked Lean modules contain no proof placeholder, added axiom, opaque/unsafe injection, oracle, or native decision shortcut. |
| Trust observation | provisional pass | All checked proof-bearing declarations report exactly the three expected principles. Complete release TCB closure is absent. |
| Direct provenance | pass | The immutable mathlib pin/tree is clean; the inventoried regularity sources, terminal olean, and license hashes agree. Complete transitive provenance remains open. |
| Architecture boundary | preserved | Thirty-eight proof-graph IDs are root-reachable, while all 18 internal source-body decomposition plans remain unverified and receive no individual closure credit. |
| Authoritative state | fail closed | The proof prerequisite is not master accepted. The frozen graph remains `[H1, M3, R4]`, `root_closed=false`, with zero accepted closed obligations. |
| Hermetic release | fail closed | A shared warm `.lake` was reused; there is no clean empty-cache offline replay, complete TCB/SBOM closure, or deterministic restorable evidence archive. |
| Independent verification | fail closed | `Validation.lean` is separate source but ran in this clone/shared cache, not on a distinct independently provisioned signed runner with a minimal verifier. |

This is genuinely self-tested validation-node evidence pending master
acceptance. It is not release-grade `E1`, accepted `M0-W`, `AUDIT-Z`,
`THEOREM-Z`, release, or theorem completion. `audit_complete=false` and
`theorem_complete=false` remain mandatory.
