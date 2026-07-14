# THM-M-1078 validation-phase evidence

Item: `S56-M-1078-VALIDATION`. Base revision:
`15d20dda8662e4144f32be899edc174f7a431574`; base tree:
`b39eec687e4f172c4ce04e08a255e593a428cf95`.

## Narrow validation

The structured recipe re-elaborates the frozen target and its generated exact-target transport,
the conditional root composer, and the two proof-phase declarations. Lean runs at trust level zero
with fresh temporary local outputs. The complete Python recipe and all child Lean processes run in
one Bubblewrap network namespace with a read-only host root, private writable `/tmp`, cleared
environment, fixed locale and timezone, and one Lean thread. `Validation.lean` adds no theorem,
lemma, or definition; it applies Lean's transitive sorry and axiom collectors to the existing proof.

The checked declarations are sorry-free and report no axiom outside `propext`,
`Classical.choice`, and `Quot.sound`. Frozen local hashes agree, as do the pinned mathlib revision,
tree, origin, license, selected source blobs, and compiled-object hashes.

This is intentionally a negative-root validation. `Proof.lean` proves the genuine horizon-local
fact that terminal `MemLp (f n) p mu` propagates to `k <= n`. The frozen conditional interface asks
for `MemLp (f k) p mu` at every future `k` as well, which is false in general and cannot consume the
proved body. The external Burkholder theorem is absent from the pinned dependency closure. Thus the
graph's accepted numerator remains empty, the exact root stays `[H2, M2, R4]`, and both
`audit_complete` and `theorem_complete` remain false.

## Commands and results

Commands ran from the worker clone on 2026-07-15 (`Asia/Shanghai`). The automation-provided
canonical `.lake` symlink was reused without mutation. No `lake update`, `lake build`, dependency
clone/fetch, or network request was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1078` | 0 | rank 520; planned L0/rework-required; theorem incomplete |
| execute the `validation-spec.json` `argv` without shell interpolation | 0 | network-isolated trust-zero replay passed for the exact statement, conditional composition, and horizon-local proof unit; exact root and release gates remained fail-closed |
| `python3 Stage1_Instances/THM-M-1078/check_obligation_tree.py` | 0 | 15 obligations and 51 typed edges passed; frozen root open M2 |
| `python3 Stage1_Instances/THM-M-1078/check_proof.py` | 0 | proof source, partial receipt, axiom boundary, and open root passed |
| `bash Stage1_Instances/THM-M-1078/check_exact_composition.sh` | 0 | conditional composer and generated exact-target transport elaborated |
| `python3 -m json.tool` over the validation spec, receipt, and root self-test | 0 | all three JSON artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1078-pycache python3 -m py_compile Stage1_Instances/THM-M-1078/check_validation.py` | 0 | validator syntax checked outside the target path |
| `git diff --check -- Stage1_Instances/THM-M-1078 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The structured recipe's captured semantic output is 663 bytes with SHA-256
`f223f533b878d832607ead649e47ab4c2f9dfe3bdcedfaa40bd1731f8c871c99`:

```text
PASS THM-M-1078 network-isolated trust-zero replay of the frozen statement, conditional composition, and horizon-local proof unit
PASS hygiene and observed trust: checked declarations are sorry-free and use only propext, Classical.choice, and Quot.sound
PASS selected local provenance: frozen hashes, clean mathlib pin/tree/origin/license, selected sources, and oleans agree
OPEN exact root: the external Burkholder body is absent and the all-future conditional interface cannot consume the proved k <= n bridge
BLOCKED release gates: proof dependency/master acceptance, complete provenance/TCB, cold empty-cache hermetic replay, and distinct-runner verification
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | The exact statement, generated transport, conditional composer, and two partial proof declarations elaborate at trust level zero. |
| Placeholder and observed axiom boundary | provisional pass | Transitive sorry checks pass; observed axioms are exactly the selected classical trio. This is not accepted complete TCB closure. |
| Selected provenance | provisional pass | Local inputs and selected mathlib sources/oleans are hash-bound at the clean pin. The external terminal body and complete transitive provenance are absent. |
| Proof dependency and exact root | fail closed | The proof node is provisional and partial; its `k <= n` bridge cannot inhabit the frozen all-future interface, and no external transform body is locally available. |
| Hermetic release replay | fail closed | The run uses a shared warm dependency cache, not a clean checkout with empty caches, cold rebuild, offline restoration, and a complete SBOM/TCB archive. |
| Independent verification | fail closed | `Validation.lean` is a same-worker trust probe. There is no distinct signed verifier, independently provisioned runner/cache, second attestation, or independent minimal verifier. |

This is self-tested validation-node evidence only for its narrow, explicitly bounded scope. It
grants no accepted obligation closure, `M0-*`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem
completion, or master acceptance.
