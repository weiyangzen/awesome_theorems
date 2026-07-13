# THM-M-0487 statement validation

Item: `S56-M-0487-STATEMENT`

Base revision: `561d83df037004ceb2259292d7c63be930b40391` (tree
`6eb02475bf5a70139d60615c924b31c930efc2bb`). Validation date: 2026-07-13
(Asia/Shanghai).

## Frozen target

`Stage1Instances.THM_M_0487.WeakGoldbachTarget` says that every `n : Nat` satisfying
`5 < n` and `Odd n` equals `p + q + r` for three natural primes. The witnesses are selected after
the input and hypotheses; they need not be distinct or ordered, and the even prime `2` is allowed.

The source states an integer input, but `n > 5` makes every qualifying integer positive, so the
natural encoding is an exact restriction rather than a weakened or broadened theorem. The two
narrow direct imports are `Mathlib.Algebra.Ring.Int.Parity` and `Mathlib.Data.Nat.Prime.Defs`;
deleting either makes the module fail. Both the literal integer-domain and equality-reversed
presentations have checked `Iff` transports.

## Commands and results

All commands ran inside this worker clone. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or `.lake` mutation ran; this dirty run
is nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and the 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0487` | 0 | rank 1366, planned, no legacy slot, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib revision `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0487/Statement.lean)` | 0 | target, two transports, four expected mutation type rejections, seven boundary declarations, axiom reports, and explicit expression elaborated |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0487/check_statement.py)` | 0 | expression SHA-256 `29ac94dd...e703`; all mutations distinct; both imports necessary; pins agree |
| `python3 -B Stage1_Instances/THM-M-0487/check_intake.py` | 0 | expanded dossier preserves the planned lifecycle, historical intake evidence, six open tasks, H1/M3/R3 projection, and empty accepted state |
| `python3 -B Stage1_Instances/THM-M-0487/check_statement_artifacts.py --worker-packet .stage1-worker-selftest.json` | 0 | statement records, receipt, authority identity, fingerprints, boundaries, and worker packet agree |
| `python3 -m json.tool` on finalized structured artifacts | 0 | all JSON parsed successfully |
| scoped prohibited-construct scan of `Statement.lean` | 1 (expected no match) | no prohibited declaration, proof escape, TODO, FIXME, or placeholder marker |
| scoped `git diff --check` plus no-index checks for new files | 0 | no whitespace diagnostics |

## Mutations and boundaries

The removed-hypothesis mutation drops oddness; the domain mutation restricts inputs to `Fin 8` and
therefore collapses to the proved `n = 7` case;
the scope mutation chooses three witnesses before the represented number; the boundary mutation
replaces `5 < n` with `5 <= n`, incorrectly including odd `5`. Lean rejects every mutation as the canonical target, and the checker
confirms their fully explicit expressions differ.

Separate kernel checks exclude `5`, include odd `7`, exhibit `7 = 2 + 2 + 3`, and exclude even
`8`. The equality transport reports `propext`; the integer/natural transport reports `propext`,
`Classical.choice`, and `Quot.sound`. These are statement-level observations, not a proof-body or
transitive trust audit.

## Status boundary

This is provisional statement evidence pending master acceptance. It supplies no proof of weak
Goldbach. Full source and computation review, anchor and provenance audit, obligation registry,
proof and composition, readable reconstruction, hermetic replay, deterministic evidence,
independent verification, release, audit completion, and theorem completion remain open.
