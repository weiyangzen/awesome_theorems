# Intake validation

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

Validation is limited to repository/manifest consistency, dossier structure, scoped invariants,
and whitespace. The legacy Lean file was inspected but is not modified or credited. No canonical
Lean target has been frozen, so no kernel closure is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0612` | exit 0; rank 256, L0/rework_required, planned, theorem_complete false |

| `python3 -m json.tool Stage1_Instances/THM-M-0612/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0612/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0612` | exit 0; no output |

At intake time, exact primary-source inspection, exact local-embedding Lean elaboration, fresh anchor
audit, frozen obligation graphs, proof, hermetic replay, and independent review remained open. The
statement-phase evidence below resolves only local-embedding target elaboration; all the other gates
remain open and prevent theorem completion.

## Statement-phase validation (S56-M-0612-STATEMENT)

Base revision: `45ecc126e04773079f94f7b6f73d4f4c9a6da900`.

Pinned environment: Lean `4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The canonical statement source has SHA-256
`2de623b53340de741e2b691d81a0e1a9f0a6f74bbdeb133f7ebcc5a20d97f919`.

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0612/Statement.lean` | exit 0; no output |
| append `#print Stage1.THM_M_0612.StatementShape` to the source stream and run `lake env lean /dev/stdin` | exit 0; printed the universe-polymorphic target with `Fintype Q`, `i : Q`, positive radii, local symplectic embedding, `MapsTo`, and conclusion `r <= R` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0612` | exit 0; rank 256, L0/rework_required, planned, theorem_complete false |
| scoped `rg` checks for the single import and all target clauses | exit 0; every required clause found |
| scoped scan for `sorry`, `axiom`, `placeholder`, and `fake result` in `Statement.lean` | exit 0; clean |
| `git diff --check -- Stage1_Instances/THM-M-0612` | exit 0; no output |

This validates statement elaboration only. It does not prove `StatementShape`, establish `H0`, close
any proof obligation, or satisfy hermetic/independent release gates. The primary-source pinpoint and
errata review is still assigned to downstream source audit; the statement is the exact canonical
formalization of the already frozen intake claim, not evidence that the historical source has been
independently certified.

## Anchor-audit validation (S56-M-0612-ANCHOR_AUDIT)

Base revision: `ef4b7fa8a178497a72e8409648876ceefeb811f8`.

The audit used the existing pinned package closure only. External candidates were downloaded as
immutable commit archives to `/tmp` for inspection and were neither cloned into nor installed in
the repository. No `.lake` update, dependency fetch, or build was performed.

| Command | Result |
|---|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned `rg` scan of `Mathlib/**/*.lean` for nonsqueezing, Gromov width, symplectic, and pseudoholomorphic terms | exit 0; only finite symplectic-matrix support and the nonterminal Hofer lemma; no terminal theorem/capacity API |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0612/AnchorAudit.lean` | exit 0; all seven pinned supporting declarations checked |
| immutable archive scan of `hrmacbeth/symplectic@acc509702046aaae6a3c9be4546d5735ad7450cf` | exit 0; archive SHA-256 matched; `gromovNonsqueezing` terminal body is `sorry`; 12 total `sorry` occurrences |
| immutable archive scans of `krystophny/geomnum@8b72abbfd96111237a55ea411069ebb395bc4c00` and `BenFrohman/NS_Millennium_Proof@44ca45c347d6a08d89a31844f83d40dbb66e08d1` | exit 0; archive SHA-256 values matched receipt; no terminal search-term hits |
| `python3 -m json.tool Stage1_Instances/THM-M-0612/anchor-audit-receipt.json` | exit 0; valid JSON |
| scoped prohibited-token scan of worker-authored Lean | exit 0; clean (the admitted external candidate is documented only in Markdown/JSON) |
| `git diff --check -- Stage1_Instances/THM-M-0612 .stage1-worker-selftest.json` | exit 0; no output |

This self-tests the assigned anchor inventory, not the theorem. The audit found no terminal proof;
the root remains `[H2, M3, R4]`, and audit completion and theorem completion remain false.
