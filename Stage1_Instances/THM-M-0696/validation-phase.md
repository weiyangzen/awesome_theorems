# THM-M-0696 validation handoff

Item: `S56-M-0696-VALIDATION`. Base revision:
`3a479c703900e8096e6b239e7bf5b0da25472b8a`.

The node-scoped validator copied `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and the
separately authored `Validation.lean` exact-type probe into a fresh temporary module directory. It
then elaborated every module with the existing pinned `lake env lean` environment and deleted the
temporary directory. It did not fetch, update, build, or modify `.lake`.

## Exact command and result

```text
$ python3 Stage1_Instances/THM-M-0696/check_validation.py
PASS narrow kernel replay: exact frozen root elaborated from a fresh temporary module directory
PASS trust observation: exact root reports propext, Classical.choice, and Quot.sound
PASS local provenance: statement, registry denominator, clean pinned mathlib, and source hygiene agree
STALE frozen graph: it predates Proof.lean and remains H1/M3/R3 pending master reconciliation
BLOCKED release gates: warm shared .lake, incomplete TCB/SBOM archive, and no distinct independent runner
exit 0
```

Additional checks:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0696` | exit 0: rank 737, planned, L0/rework_required, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-0696` | exit 0 |

## Boundary

The exact root elaborates without placeholders or unsafe declarations, and its observed trust set is
`propext`, `Classical.choice`, and `Quot.sound`. The pinned mathlib checkout is at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and clean.

This is intentionally nonrelease evidence. The canonical warm `.lake` link is shared; there is no
cold empty-cache offline restoration, complete transitive TCB/SBOM archive, independent platform,
or distinct signed verifier. The frozen typed graph also predates the proof and remains open at
`H1/M3/R3`; only the master may reconcile it. Therefore this receipt self-tests the validation
phase but does not claim accepted M0, theorem completion, release, or master acceptance.
