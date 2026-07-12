# THM-M-0650 validation-phase result

Item `S56-M-0650-VALIDATION` was run against the proof-phase snapshot. The
narrow kernel, observed-axiom, placeholder, immutable-pin, and proof-body
provenance checks pass. The exact `TarskiVaughtTarget` root wrapper and the
more general embedding terminal wrapper both elaborate against pinned Lean
4.29.0 and mathlib `8a178386`.

## Exact result

The structured recipe in `validation-spec.json` was run from repository root
on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0650/check_validation.py
  exit 0
  ok: exact Tarski-Vaught statement and proof wrappers elaborated against pinned Lean/mathlib
  ok: both proof declarations report only propext, Classical.choice, and Quot.sound
  ok: placeholder, frozen-input, terminal-source, license, manifest-pin, and clean-mathlib checks passed
  stale: the frozen graph predates Proof.lean and still reports M0650-T-EMBEDDING open
  blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification
```

The validator invokes `lake env lean` narrowly. It writes `Statement.olean`
only to a fresh system temporary directory, prepends that directory to
`LEAN_PATH`, elaborates `Proof.lean`, and deletes the directory. It checks that
the existing mathlib checkout is clean and at the manifest revision. No Lake
update/build, clone, fetch, network access, or dependency mutation occurs.

## Gate decisions

| Gate | Decision | Evidence or failure |
| --- | --- | --- |
| Narrow kernel replay | pass | The exact statement, embedding terminal wrapper, and exact root wrapper elaborate. |
| Placeholder/unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the checked local or terminal dependency sources. |
| Axiom observation | provisional pass | Both proof declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; no release-grade transitive TCB certificate is claimed. |
| Provenance and pin | pass | Frozen input hashes, terminal/wrapper source hashes, license hash, manifest revision, installed mathlib HEAD, and clean dependency status agree. |
| Structured state freshness | fail closed | The proof receipt records a locally closed root, but the frozen typed graph predates proof integration and still reports `M0650-T-EMBEDDING` open. Only the master may reconcile it. |
| Hermetic release replay | fail closed | This run reused shared warm `.lake` artifacts; there was no immutable clean checkout, empty-cache cold build, offline archive restoration, complete TCB/SBOM closure, or second platform. |
| Independent verification | fail closed | This is one worker and mutable clone, without a distinct verifier identity, independently provisioned runner, second signed attestation, or independently implemented minimal verifier. |

This is truthful self-tested validation-phase evidence, not theorem completion.
It grants no `E0/E1`, accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or
master-acceptance credit. `theorem_complete=false`.
