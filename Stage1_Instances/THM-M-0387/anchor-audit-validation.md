# THM-M-0387 anchor-audit validation

Item: `S56-M-0387-ANCHOR_AUDIT`  
Base revision: `7723e96072c1d3996a280b874d09cfd02a847417`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The pinned mathlib and `flt-regular` anchors elaborate at their manifest
revisions and their audited endpoints report only `propext`,
`Classical.choice`, and `Quot.sound`. They close exponent `3`, exponent `4`,
the regular-prime family, and a conditional odd-prime-to-root assembly edge.
None supplies the open general odd-prime premise.

The fresh external audit resolves `ImperialCollegeLondon/FLT` main to immutable
revision `8884a744090a0e7f5a6ba0fa7ba1019403f3ca78`. Its exact `flt` declaration
still transitively uses `B4_proof`, whose body is `sorry`, at lines 98-99 of
`FLT/Proof.lean`. It is therefore `M5`, not an integration candidate. Its Lean
`4.32.0-rc1` and mathlib `0098dd...9b` pins also differ from this repository.

The exact root remains `M2` and is not kernel-closed. This completes candidate
classification for this anchor-audit phase only; it makes no theorem-completion
claim.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure passed: 15 groups, 41 legacy rows, 300 slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0387` | 0 | rank 1, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 0 | `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` |
| `git -C .../mathlib status --short` and `git -C .../flt-regular status --short` | 0 | both produced empty output |
| `git ls-remote https://github.com/ImperialCollegeLondon/FLT.git refs/heads/main` | 0 | resolved `8884a744090a0e7f5a6ba0fa7ba1019403f3ca78` |
| immutable GitHub raw-file inspection for `FLT/Proof.lean`, `lean-toolchain`, and `lake-manifest.json` | 0 | exact root located; direct proof gap at `B4_proof`; Lean and mathlib pins recorded |
| `lake env lean ../../Stage1_Instances/THM-M-0387/AnchorAudit.lean` from `Formalizations/Lean` | 1 | expected cache blocker: the canonical shared `.lake` has no pinned mathlib root/FLT oleans, so Lean reports unknown module prefix `Mathlib`; no dependency mutation was attempted |
| `lake env lean ../../Stage1_Instances/THM-M-0387/Statement.lean` from `Formalizations/Lean` | 0 | the exact canonical target and statement-identity probe elaborated with `Init` |
| `python3 Stage1_Instances/THM-M-0387/check_anchor_audit.py` | 0 | local package revisions/worktree cleanliness and exact source declarations matched; immutable Imperial root and direct proof gap matched; root classification remained `M2` |
| `python3 -m json.tool Stage1_Instances/THM-M-0387/anchor-audit.json` | 0 | structured ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0387 .stage1-worker-selftest.json` | 0 | no whitespace errors |

`AnchorAudit.lean` is retained as the exact narrow probe for retry after the
pinned mathlib oleans are materialized by the canonical dependency builder.
The source-level verifier supplies the available audit gate now, but it does
not upgrade its declarations to fresh kernel evidence. No `lake update`,
dependency clone/fetch, or mutation of `.lake` was performed.
