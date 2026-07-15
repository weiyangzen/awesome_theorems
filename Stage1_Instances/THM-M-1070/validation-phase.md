# THM-M-1070 validation-phase evidence

Item: `S56-M-1070-VALIDATION`. Base revision:
`be35cd8f5123e9d06247b12859f3843bdd90c66f`; base tree:
`a275a21a449fbcbd6c2333f5cfe737e906b20db6`.

## Narrow validation

The structured recipe re-elaborates the frozen predicate, its direct expansion, the conditional
obligation composition, the two mathlib anchor probes, and all four proof-phase declarations.
Lean runs at trust level zero with fresh temporary local outputs. The complete Python recipe and
every child Lean process run in one Bubblewrap network namespace with a read-only host root,
private writable `/tmp`, a cleared environment, fixed locale and timezone, and one Lean thread.
`Validation.lean` adds no theorem, lemma, or definition; it applies Lean's transitive sorry and
axiom collectors to the existing proof declarations.

The checked declarations are sorry-free and report exactly `propext`, `Classical.choice`, and
`Quot.sound`. Frozen local hashes agree, as do the pinned mathlib revision, tree, origin, license,
selected source blobs, and compiled-object hashes.

This is intentionally a negative-root validation. The canonical target is the predicate
`IsLevyProcess P X` for arbitrary `P` and `X`, not an existence theorem supplied with clause
hypotheses. The conjunction composers remain conditional; `isLevyProcess_zero` specializes the
process and assumes `P` is a probability measure; `zeroMeasure_not_isLevyProcess` supplies a
countermodel to unconditional arbitrary-`P` closure. Thus zero frozen obligations gain proof
credit, the exact root stays `[H1, M3, R4]`, and `audit_complete` and `theorem_complete` remain
false.

## Commands and results

Commands ran from this worker clone on 2026-07-15 (`Asia/Shanghai`). The automation-provided
canonical `.lake` symlink was reused without mutation. No `lake update`, `lake build`, dependency
clone/fetch, checkout, or network request was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1070` | 0 | rank 512; planned L0/rework-required target; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1070/check_obligation_tree.py` | 0 | 13 obligations and 26 typed edges passed; denominator `c5866f4be491aa8209171938c78c36bde996941a27c87686d2a109d6679c5aa9`; root open M3 |
| execute the `validation-spec.json` `argv` without shell interpolation | 0 | network-isolated trust-zero replay passed for the exact statement, anchors, conditional composition, and four proof declarations; exact root and release gates remained fail-closed |
| `python3 -m json.tool` over the validation spec, receipt, and root self-test | 0 | all three JSON artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1070-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-1070/check_validation.py` | 0 | validator syntax checked outside the repository tree |
| prohibited-device scan over target Lean sources | 1, expected | no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/oracle/external escape, or `native_decide` found |
| `git diff --check -- Stage1_Instances/THM-M-1070 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The structured recipe's captured semantic output is 688 bytes with SHA-256
`09daf9f1b520e22f31d9d0c2a069e740de7bc810481d937b33d993ae571473f3`:

```text
PASS THM-M-1070 network-isolated trust-zero replay of the frozen statement, conditional composition, and four proof-phase declarations
PASS hygiene and observed trust: checked declarations are sorry-free and use exactly propext, Classical.choice, and Quot.sound
PASS selected local provenance: frozen hashes, clean mathlib pin/tree/origin/license, selected sources, and oleans agree
OPEN exact root: the canonical target is a predicate over arbitrary P and X; the specialized witness and conditional composers close no frozen obligation
BLOCKED release gates: proof dependency/master acceptance, complete provenance/TCB, cold empty-cache hermetic replay, and distinct-runner verification
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | The exact statement, checked expansion, anchor probes, conditional composers, and four proof declarations elaborate at trust level zero. |
| Placeholder and observed axiom boundary | provisional pass | Transitive sorry checks pass; observed axioms are exactly the selected classical trio. This is not an accepted foundation/TCB closure. |
| Selected provenance | provisional pass | Local inputs and selected mathlib sources/oleans are hash-bound at the clean pin. Complete transitive body, import, and TCB provenance is absent. |
| Proof dependency and exact root | fail closed | The proof predecessor is only `[_]` and its own evidence says the proof phase is incomplete, zero frozen obligations close, and the arbitrary-`P`, arbitrary-`X` root remains M3. |
| Human source and readability | fail closed | The instance remains H1/R4, with no independently accepted pinpoint H0 source review or R0 reconstruction. |
| Hermetic release replay | fail closed | The run uses a shared warm dependency cache, not a clean checkout with empty caches, cold rebuild, offline restoration, and a complete SBOM/TCB archive. |
| Independent verification | fail closed | `Validation.lean` is a same-worker trust probe. There is no distinct signed verifier, independently provisioned runner/cache, second attestation, or independent minimal verifier. |

The first node gate is
`dependency.S56-M-1070-PROOF.master_acceptance_and_exact_root_closure`; the first release gate is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE`. The validation node is self-tested only as an honest,
nonrelease blocked receipt. It grants no accepted obligation state, `M0-*`, `E0/E1`, `AUDIT-Z`,
`THEOREM-Z`, release, theorem completion, or master acceptance.
