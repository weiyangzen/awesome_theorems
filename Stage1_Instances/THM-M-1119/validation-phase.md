# THM-M-1119 validation-phase evidence

Item: `S56-M-1119-VALIDATION`. Base revision:
`3d3099d0d4002093cf89da97132bdf954605810b`; base tree:
`17ea0daeddceb9742a5df33c247d624d2842c520`.

## Narrow validation

The structured recipe re-elaborates the frozen statement, its conditional two-bound composer, and
the 13 receipt-listed proof declarations. Lean runs at trust level zero with fresh temporary local
outputs.
The complete checker and every child Lean process run in one Bubblewrap network namespace with a
read-only host root, private writable `/tmp`, cleared environment, fixed locale and timezone, and
one Lean thread. `Validation.lean` imports neither `Proof` nor `ObligationTree`; it independently
reconstructs open-graph monotonicity and the parameter-zero product measure.

All checked declarations are sorry-free and report exactly `propext`, `Classical.choice`, and
`Quot.sound`. Frozen local hashes agree, as do the pinned mathlib revision, tree, origin, license,
and source cleanliness.

This is intentionally a negative-root validation. Neither one-half threshold inequality has a
proof body, the conditional composer cannot construct its own premises, and the accepted numerator
remains empty. The exact root stays `[H2, M4, R4]`; `audit_complete` and `theorem_complete` remain
false. The undated `proof-blocker.md` is a superseded historical narrative; the current structured
authority used here is `proof-blocker-current.json`.

## Commands and results

Commands ran from the worker clone on 2026-07-15 (`Asia/Shanghai`). The automation-provided
canonical `.lake` symlink was reused without mutation. No `lake update`, `lake build`, dependency
clone/fetch, or network request was run.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1119` | 0 | rank 559; planned L0/rework-required; theorem incomplete |
| `/usr/bin/bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --unshare-net --die-with-parent --clearenv --setenv HOME /tmp --setenv PATH /usr/bin:/bin --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 /usr/bin/python3 -I -B Stage1_Instances/THM-M-1119/check_validation.py` | 0 | network-isolated trust-zero replay passed for the exact statement, conditional composer, partial proof bodies, and two differential probes; root/release gates remained fail-closed |
| `python3 -m json.tool Stage1_Instances/THM-M-1119/validation-spec.json; python3 -m json.tool Stage1_Instances/THM-M-1119/validation-receipt.json; python3 -m json.tool .stage1-worker-selftest.json` | 0 | all three JSON artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1119-pycache python3 -m py_compile Stage1_Instances/THM-M-1119/check_validation.py` | 0 | validator syntax checked outside the target path |
| `git diff --check -- Stage1_Instances/THM-M-1119 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The structured recipe's semantic output is 680 bytes with SHA-256
`70ff49f5a2d2a303a7ca7e9524289f110183ad829f1c22a0f45eae4a1017c65d`:

```text
PASS THM-M-1119 network-isolated trust-zero replay of the frozen statement, conditional composer, and 13 partial proof declarations
PASS differential validation: two no-proof-import elementary probes elaborate and are sorry-free
PASS observed trust: all checked declarations use only propext, Classical.choice, and Quot.sound
PASS selected provenance: frozen local hashes and clean pinned mathlib revision, tree, origin, and license agree
OPEN exact root: neither one-half threshold inequality is inhabited; zero frozen obligations are closed
BLOCKED release gates: proof dependency/root closure, complete provenance/TCB, cold empty-cache replay, and distinct-runner verification
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | The exact statement, conditional composer, 13 partial proof declarations, and two differential probes elaborate at trust level zero. |
| Placeholder and observed axiom boundary | provisional pass | Transitive sorry checks pass; observed axioms are exactly the selected classical trio. This is not accepted complete TCB closure. |
| Selected provenance | provisional pass | Local inputs and the clean pinned mathlib revision, tree, origin, and license are hash-bound. The missing terminal bodies and complete transitive provenance stay open. |
| Proof dependency and exact root | fail closed | The proof node is provisional and partial; neither threshold terminal is inhabited and zero frozen obligations are closed. |
| Hermetic release replay | fail closed | The run uses a shared warm dependency cache, not a clean checkout with empty caches, cold rebuild, offline restoration, and a complete SBOM/TCB archive. |
| Independent verification | fail closed | The differential probes share this worker, checkout, binary, and cache. There is no distinct signed verifier, independently provisioned runner/cache, or independent minimal verifier. |

This is self-tested validation-node evidence only for its narrow, explicitly bounded scope. It
grants no accepted obligation closure, `M0-*`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem
completion, or master acceptance.
