# THM-M-0528 validation-phase result

Item `S56-M-0528-VALIDATION` was run against the integrated proof snapshot. The
exact statement, conditional composition certificate, proof root, and a
proof-independent reconstruction all kernel-elaborate against pinned Lean
4.29.0 and mathlib. This is narrow, provisional validation rather than release
evidence.

## Exact result

The structured recipe ran from repository root on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0528/check_validation.py
  exit 0
  ok: exact statement, conditional composition, proof root, and independent exact-root reconstruction elaborated freshly
  ok: checked declarations report only propext, Classical.choice, and Quot.sound
  ok: frozen hashes, proof receipt, clean mathlib pin, terminal source, and compiled artifact passed
  stale: frozen graph predates proof closure and still reports M0528-X-ANCHOR open
  blocked: cold empty-cache hermetic replay, complete transitive TCB/SBOM closure, and distinct-runner verification
```

The validator copies the four Lean modules to a fresh temporary directory,
invokes `lake env lean` narrowly, and deletes the directory afterward. It
checks mathlib's clean revision, terminal source and `.olean` hashes, proof
receipt inputs, registry denominator, prohibited tokens, and observed axioms.
It performs no update, build, clone, fetch, or dependency mutation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The exact statement, conditional composition, proof root, and independent reconstruction elaborate freshly. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the four modules. |
| Trust observation | provisional pass | All checked declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. Full TCB policy closure is absent. |
| Local provenance | pass | Frozen hashes, proof receipt, clean pinned mathlib revision, terminal source hash, and terminal `.olean` hash agree. |
| Exact root kernel closure | pass locally | Both `coveringLiftUniqueness` and the proof-independent reconstruction inhabit the frozen target. |
| Structured-state freshness | fail closed | The frozen graph predates proof closure and still records `root_closed=false` with `M0528-X-ANCHOR` open. |
| Transitive trust/provenance | fail closed | No complete content-addressed declaration/import closure or compiler/bootstrap/executable TCB inventory exists. |
| Human source/readability | fail closed | Exact primary-source H0 review and independent R0 reconstruction are absent. |
| Hermetic release replay | fail closed | The run reused the shared warm `.lake`; no clean checkout, empty-cache build, offline restoration, or complete SBOM/license archive was produced. |
| Independent verification | fail closed | The separate implementation ran in this same worker/cache, without a distinct identity, provisioned runner, signature, or independent minimal verifier. |

The first release-level failure is rev-5.6 section 10.6's cold empty-cache
hermetic replay. Consequently `audit_complete=false` and
`theorem_complete=false`; this receipt grants no `E0/E1`, accepted `M0`,
`AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance credit.
