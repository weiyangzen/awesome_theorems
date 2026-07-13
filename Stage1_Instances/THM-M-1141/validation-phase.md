# THM-M-1141 validation-phase result

Item `S56-M-1141-VALIDATION` was run against base revision
`c45f3c7090cb4adf616d45e5414985f956e807b2` (tree
`da6f991c07f11e8608ddc090af9356558d64d360`). Validation added no analytic
Harnack proof content. It copied `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` into a fresh temporary directory and ran
the pinned Lean kernel at trust level zero with outbound networking isolated.
`Validation.lean` imports `Proof`; its separately written bodies are
same-worker, import-dependent checks, not an independent implementation.
The phase verdict is `blocked`; `[_]` denotes only the implemented and
self-tested negative validator packet, never successful closure of its failed
gates or acceptance of the theorem.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The frozen statement, conditional ratio composition, proof-phase positivity and chain packages, and two separately written import-dependent probes elaborate. |
| Placeholder/unsafe/oracle hygiene | pass in inspected modules | Comment-aware scans found no `sorry`, `admit`, `sorryAx`, bodyless local declaration, unsafe declaration, external implementation, or native oracle in the four replayed modules. |
| Axiom observation | provisional pass | Five unique declarations across seven reports have exactly `propext`, `Classical.choice`, and `Quot.sound`; no accepted complete foundation/TCB profile exists. |
| Local provenance and pins | partial pass | Frozen source hashes, the registry denominator, Lean/Lake pins, and the clean pinned mathlib revision agree. No proof receipt or complete transitive terminal-body/TCB packet exists. |
| Exact source-statement identity | fail closed | The selected book fixes `n > 1`, but `Statement.lean` quantifies every `n : Nat` and `scope-map.md` explicitly retains dimension zero. No checked extension covers dimensions 0 and 1. |
| Exact root kernel closure | fail | The local analytic Harnack estimate, compact cover, connected-domain chain, and uniform comparison are unproved; only conditional composition is checked. The root remains `M3`. |
| Hermetic release replay | fail closed | Network isolation and fixed locale/timezone were used, but Lean reused the shared warm `.lake`; this was not a clean empty-cache cold build or offline restoration and has no complete TCB/SBOM archive. |
| Independent verification | fail closed | `Validation.lean` imports the proof module and supplies same-worker checks, not a distinct identity, independently provisioned runner/cache, second signature, or independently implemented release verifier. |

The first failed gate is `S56-5.1-EXACT-SOURCE-STATEMENT-IDENTITY`. A previously
audited source finding records the convention on printed page 1 of the authors'
PDF and Theorem 3.6 on printed page 48; this recipe did not retain or rehash the
PDF bytes. The recorded PDF SHA-256 is
`4e64124f7e36993ee784e575a024505f99d484ccf959d2d3864eae9232af8bf1`.
The statement-owning lane must repair or justify the dimensional scope before
the statement-dependent registry and proof evidence can be credited.

The committed `validation-blocker.*` pair records the earlier non-executable
blocked run. Its statements that no receipt or self-test existed describe that
run and are superseded only on that narrow historical point by this packet.
The substantive blocker decisions are unchanged. `instance.json` also predates
the validation packet and therefore omits its files from `owned_artifacts`; the
validation phase does not silently rewrite that earlier-phase authority.

## Commands and results

No command ran `lake update`, `lake build`, dependency clone/fetch, or a write
to `.lake`.

```text
$ python3 -B Stage1_Instances/THM-M-1141/check_validation.py
exit 0; network-isolated trust-zero replay passed for three local packages;
source identity, exact root, complete trust/provenance, cold hermetic, and
independent gates were reported fail-closed

$ python3 Docs/tools/check_stage1_standard.py
exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

$ python3 scripts/stage1_target.py check
exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-1141
exit 0; rank 346, planned lifecycle, theorem_complete=false

$ python3 -B Stage1_Instances/THM-M-1141/check_obligation_tree.py
exit 0; 11 obligations and 67 typed edges passed; root remains open M3

$ python3 -B Stage1_Instances/THM-M-1141/check_proof.py
exit 0; positivity and finite-chain propagation passed; analytic uniform
comparison remains open

$ git diff --check -- Stage1_Instances/THM-M-1141 .stage1-worker-selftest.json
exit 0; no tracked-diff whitespace errors. The validator separately checked all
six untracked changed files for final newline, CR/NUL, and trailing whitespace.
```

## Retry condition

First add the inherited `2 <= n` scope or prove a checked extension for low
dimensions, then refreeze all statement-dependent artifacts. Close the analytic
root packages next. Release validation additionally requires accepted complete
trust/provenance, a clean empty-cache network-denied offline restoration, and a
distinct signed independently provisioned verifier.

This is a self-tested validation runner and truthful negative gate result. It
is provisional `[_]` worker evidence only; `audit_complete=false` and
`theorem_complete=false`.
