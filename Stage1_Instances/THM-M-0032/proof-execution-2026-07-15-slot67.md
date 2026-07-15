# THM-M-0032 partial proof execution (slot67)

Item: `S56-M-0032-PROOF`

Base: `20808d65f53d8801e78f061504b93bb7efd49489` / tree
`a5bf33a278a7a285878c89177838ae1a0dcc9990`

## Verdict

`no_state_change`, with one self-tested frozen obligation proposed as worker state `[_]`.

`DomainProof.lean` now gives a placeholder-free inhabitant of the exact frozen
`RegularLocalDomainPackage`. The proof derives `IsDomain R` from `[CommRing R]` and
`[IsRegularLocalRing R]` without strengthening the target. It inducts on the maximal ideal's
`spanFinrank`; the positive branch proves regularity of a quotient by a minimal generator, uses
minimal-prime analysis and prime avoidance, and finishes the contradiction with Krull intersection
and Nakayama cancellation.

This supplies provisional closure evidence only for `M0032-N-DOMAIN`. It does not manufacture the independent
`M0032-A-PRIME-ELEMENT` package, so the existing conditional Kaplansky composition still cannot
close the UFD target. The root stays `[H1, M3, R4]`, accepted receipts remain empty, and
`theorem_complete=false`.

## Validation

All Lean checks reused the automation-provided canonical pinned `.lake` symlink without update,
build, clone, fetch, checkout, or mutation. The runner creates fresh outputs under `/tmp`, invokes
the existing Lean 4.29.0 toolchain directly through `lake env`, and removes the temporary directory.

| Command | Exit | Result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-0032/check_proof.sh` | 0 | `Statement.lean`, `ObligationTree.lean`, and `DomainProof.lean` elaborated at `--trust=0 -t0`; both public domain declarations passed `assert_no_sorry` and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranked targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | Rank 1076; planned; L0/rework-required; theorem incomplete. |
| `rg -n -i --pcre2 '(^|[^[:alnum:]_])(sorry\|admit\|sorryAx\|native_decide\|axiom\|constant\|opaque\|unsafe\|extern\|external\|implemented_by\|run_tac)([^[:alnum:]_]|$)' Stage1_Instances/THM-M-0032/DomainProof.lean` | 1 | Expected no-match: no executable placeholder, bodyless declaration, unsafe/oracle boundary, or native shortcut was found. |
| `rg -n -i --glob '*.lean' 'IsRegularLocalRing\|regularLocalRing_isUFD\|auslander_buchsbaum_UFD\|uniqueFactorizationMonoid.*regular\|regular.*uniqueFactorizationMonoid\|isDomain_of_isRegularLocalRing' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | No UFD terminal exists in pinned mathlib outside this dossier. |
| `test ! -e Formalizations/Lean/.lake/packages/mathlib/Mathlib/RingTheory/RegularLocalRing/UFD.lean` | 0 | The exact upstream UFD module remains absent from the pinned closure; separate presence probes also found all seven of its direct imports absent. |
| `python3 Stage1_Instances/THM-M-0032/check_proof.py` | 0 | Source, exact frozen interface, pins, receipt, blocker boundary, and worker packet passed fail-closed checks. |
| `git diff --check -- Stage1_Instances/THM-M-0032 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The root checker for the predecessor obligation-tree phase is not used as proof evidence because it
expects that predecessor worker's ephemeral root packet. The proof runner instead recompiles the
statement and frozen composition before checking the new exact package.

## Remaining blocker

`M0032-A-PRIME-ELEMENT` remains the root cut. Pinned mathlib lacks the required proof that every
nonzero prime ideal of a regular local domain contains a prime element, including the central
height-one-prime principalization and localization/descent machinery. The exact upstream candidate
at mathlib PR #39510, head `6d76bb4118837f7f8d7669c9b0b7d06bc59081c7`, remains outside the
frozen closure: it targets Lean 4.32.0-rc1 and imports seven unavailable modules. It was not fetched,
imported, replayed, or credited.

The proof item is therefore not complete. This packet records genuine partial proof progress and
does not claim master acceptance, validation, release, audit completion, or theorem completion.
