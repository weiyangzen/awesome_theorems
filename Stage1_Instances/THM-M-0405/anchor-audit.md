# THM-M-0405 anchor audit

## Scope and revisions

This audit compares the frozen `Stage1.THM_M_0405.Statement` with repo-local,
pinned mathlib, and discoverable external Lean 4 candidates. The dependency
lock is mathlib4 commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`
under Lean `v4.29.0`. The legacy repo artifact is inspected at its containing
commit `16d227cffb7cb7d9e8392b6c0ff8211e498e1330`. No moving dependency was fetched
or installed.

## Pinned mathlib inventory

| Candidate | Exact role | Verdict |
|---|---|---|
| `Mathlib.NumberTheory.LucasLehmer`: `LucasLehmerTest`, `lucasLehmerResidue`, `lucas_lehmer_sufficiency`, `lucas_lehmer_necessity` | A recurrence-based primality test for Mersenne numbers and its correctness directions | Nearby non-target: it neither models BHV Lucas/Lehmer pairs nor proves primitive divisors for `n > 30`. |
| `Mathlib.NumberTheory.LucasPrimality`: `lucas_primality`, `reverse_lucas_primality` | Lucas primality certificates | Nearby non-target, not a primitive-divisor existence theorem. |
| `Mathlib.Algebra.LinearRecurrence`: `LinearRecurrence` | General recurrence object model | Substrate only; no terminal BHV result or checked transport to the frozen target. |

A tracked-source search across all 8,528 files at the pinned mathlib revision
found no Lean file containing `Bilu`, `Hanrot`, `Voutier`, `Zsigmondy`, or the
phrase `primitive divisor`. `AnchorAudit.lean` elaborates the named declarations
and records their actual types through `#check`. Because none matches either
branch of the frozen conjunction, terminal proof-body provenance and an axiom
report do not exist to audit; these anchors receive zero root proof credit.

## Repo-local and external inventory

The legacy `S1_M_018.lean` contains models, adapters, a Fibonacci toy result,
and an explicit abstract wrapper whose main existence premise is supplied by
the caller. It also labels its own terminal status as lacking the BHV existence
proof. It is discovery input, not an exact candidate and not proof provenance.

On 2026-07-12, GitHub REST repository searches for
`"Bilu-Hanrot-Voutier" Lean` and `Zsigmondy Lean` each returned
`total_count: 0` and `incomplete_results: false`. These are repository metadata
searches, not exhaustive source-code searches. Attempts to search grep.app for
`Bilu-Hanrot-Voutier`, `Zsigmondy`, and `primitive divisor` returned HTTP 429,
so that surface is recorded as blocked and is not converted into negative
evidence. No external candidate was discovered, hence there is no candidate
revision that can truthfully be pinned or imported. The limitation remains
explicit rather than turning a bounded search into a universal nonexistence
claim.

## Classification

- Human mathematics: known BHV theorem; `H0` is not assigned by this machine-anchor phase.
- Machine state: `not_repo_local_closed`.
- Debt: `formalization_debt`, because no public Lean 4 terminal proof candidate was identified; this is not `repo_local_integration_debt` without an actual external closure.
- Proof credit: none. No anchor is exact, no wrapper is implemented, and no theorem completion is claimed.

## Validation receipt

Base revision: `76065c6d4727c5f002398b7e5310e0e68c872b56`.
Commands were run in this worker clone on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Returned the pinned commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `rg -l -i --glob '*.lean' 'Bilu\|Hanrot\|Voutier\|Zsigmondy\|primitive divisor' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | No tracked mathlib source match; exit 1 is ripgrep's expected no-match status. |
| `lake env lean ../../Stage1_Instances/THM-M-0405/AnchorAudit.lean` from `Formalizations/Lean` | 0 | All seven nearby declarations elaborated and their types printed. |
| `lake env lean ../../Stage1_Instances/THM-M-0405/Statement.lean` from `Formalizations/Lean` | 0 | Frozen exact target still elaborates. |
| `python3 -m json.tool Stage1_Instances/THM-M-0405/anchor-audit.json` | 0 | Structured audit parses. |
| `git diff --check -- Stage1_Instances/THM-M-0405 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Status boundary: the scoped anchor inventory and honest negative/blocker record
are self-tested worker evidence pending master acceptance. The next obligation
tree, proof, validation, release, `H0`, and theorem-completion gates remain open.
