# S56-M-1054-VALIDATION worker evidence

Date: `2026-07-12`. Base revision: `6c2108d725fc300302148b2400ef718bbed05d76`.

The exact `Statement.lean -> ObligationTree.lean -> Proof.lean` chain was rebuilt in dependency
order into a newly created temporary output directory using the existing pinned Lake environment.
Lean reached `vonNeumannL2MeanErgodic` and reported exactly `propext`, `Classical.choice`, and
`Quot.sound` for the composition theorem, the imported-body wrapper, and the exact root. The proof
source contains no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe declaration,
`native_decide`, or external oracle.

Pinned provenance was rechecked locally. Mathlib is at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; its tracked worktree is clean. The terminal theorem
occurs at `Mathlib/Analysis/InnerProductSpace/MeanErgodic.lean:89`, whose SHA-256 is
`627c02d75fea2c740dd42d741375b8d38fbc8f85ac4a960ecc9de28995312b9b`.

This is deliberately nonrelease evidence. The clone's `.lake` is a symlink to the canonical warm,
shared cache, and host policy denied `unshare -n`, so neither a cold empty-cache build nor enforced
offline replay occurred. The dossier also lacks versioned accepted foundation and complete TCB
profiles against which to accept the observed axiom closure. This worker/checker is not a distinct,
independently provisioned runner. Consequently the truthful machine classification is `M1`, not
`M0`; audit and theorem completion remain false.

## Commands and results

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1054` | 0 | rank 246; planned; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e...` |
| temporary-directory three-module `lake env lean` recipe from `validation-spec.json` | 0 | exact root elaborated; all three declarations emitted the three-axiom set above |
| `python3 Stage1_Instances/THM-M-1054/check_statement.py` | 0 | exact statement and four structural mutations checked |
| `python3 Stage1_Instances/THM-M-1054/check_obligation_tree.py` | 0 | frozen registry and seven typed graphs passed |
| `python3 Stage1_Instances/THM-M-1054/check_proof.py` | 0 | exact proof integration and pinned hashes passed |
| proof hygiene `rg` over `Proof.lean` | 1 | expected no-match exit |
| `unshare -n true` | 1 | `Operation not permitted`; offline isolation not claimed |
| `python3 Stage1_Instances/THM-M-1054/check_validation.py` | 0 | receipt inputs and fail-closed root decision passed |
| `git diff --check -- Stage1_Instances/THM-M-1054 .stage1-worker-selftest.json` | 0 | no whitespace errors |

First failed theorem gate: `trust.accepted_foundation_profile`. Additional failures are complete
TCB inventory, cold offline replay, independent distinct-runner validation, human-source/readability
review, release, and master acceptance. No theorem completion is claimed.
