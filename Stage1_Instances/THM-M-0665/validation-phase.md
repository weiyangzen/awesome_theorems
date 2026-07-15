# S56-M-0665-VALIDATION worker evidence

Item: `S56-M-0665-VALIDATION`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Validation time: `2026-07-15T12:07:41+08:00`

## Result

The structured recipe ran inside an outer Bubblewrap network namespace with a cleared environment,
read-only host tree, private writable `/tmp`, fixed locale/timezone/umask, and one Lean thread. In a
fresh output directory it elaborated `Statement.lean`, all fourteen partial bodies in `Proof.lean`,
and three separately written elementary checks in `Validation.lean` at Lean trust level zero. The
differential module imports only `Statement`. All seventeen checked bodies passed `assert_no_sorry`;
the machine-derived axiom union was exactly `Classical.choice`, `Quot.sound`, and `propext`.

This is deliberately a blocked, partial validation verdict. There is no unconditional body of
`Stage1Instances.THM_M_0665.PilaWilkie`, no frozen obligation is credited closed, and the root stays
`H1/M3/R4`. The remaining cut is `M0665-C-PARAM`, `M0665-L-DERIVATIVE`,
`M0665-L-ARITHMETIC`, `M0665-L-DROP`, and `M0665-L-COUNT`. Root provenance and transitive trust
cannot close without a root body. The proof prerequisite is provisional rather than master-accepted.

The validator also bound all local inputs, the clean mathlib revision/tree/origin/license, and the
source/blob/olean hashes of the six direct statement imports. The shared `flt-regular` checkout has
no resolvable `HEAD`, so root-project Lake environment discovery is unavailable. Per worker policy,
nothing was fetched, repaired, built, or mutated; the validator derived the read-only path from the
clean pinned mathlib project, used only complete already-present dependency outputs needed by this
target, and records the missing artifact as a blocker.

The fresh-output replay is not the release protocol: the worker checkout is dirty, the dependency
cache is warm, no cold empty-cache rebuild or offline archive restoration occurred, and the
same-workspace differential module is not a distinct signed independent runner. Audit completion,
theorem completion, release, accepted state, and master acceptance remain false.

## Commands and exact results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0665` | 0 | rank 709, planned lifecycle, hard-statement-first lane, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0665/check_obligation_tree.py` | 0 | 20 obligations and 48 typed edges passed; root remains open M3 |
| recorded `bwrap ... python3 -I -B Stage1_Instances/THM-M-0665/check_validation.py` recipe | 0 | network-isolated trust-zero fresh-output replay, axiom checks, hash/pin/provenance checks, and fail-closed gate decisions passed |
| `python3 -m json.tool` on validation spec, receipt, and worker packet | 0 | all structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0665-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0665/check_validation.py` | 0 | validator syntax compiled outside the repository |
| prohibited Lean construct scan over the target's Lean files | 1 (expected no-match) | no executable `sorry`, `admit`, bodyless declaration, unsafe/oracle device, or native bypass found |
| `git diff --check -- Stage1_Instances/THM-M-0665 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The current-head proof-phase Python checker is intentionally not used as validation evidence: it
binds its historical proof worker base revision and therefore fails freshness at this later head.
This phase independently replays the hash-bound proof source instead.
