# Statement validation record

Item: `S56-M-0652-STATEMENT`. Base revision:
`07cc89a04d18aba80d921bc643786856d7e22ad7`.

All commands ran from the worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake`
directory was reused read-only; no dependency update, fetch, clone, or build was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0652` | 0 | rank 298, planned, `hard_statement_first_partial_verification`, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0652/Statement.lean` | 0 | Canonical target and transparent transport elaborated; three negative mutation fixtures produced their expected guarded errors; empty-language and package-projection probes elaborated; printed transport axiom closure was `[Quot.sound]` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-0652/statement.json` | 0 | Statement receipt parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0652 .stage1-worker-selftest.json` | 0 | No whitespace errors |

`Statement.lean` has SHA-256
`0688e793479810070b0d7afe2b93ffa85bb132e80f4c79840532ae5add69d793`. The full successful
Lean stdout has SHA-256 `3afe8770cdb0bd71a36ae495e57699cedb65dcee24964096c9181b75b2126958`.
The normalized expression hash in `statement.json` is computed from the exact pretty-printed
`Statement` declaration emitted with explicit arguments and universes; its four-line byte stream
has SHA-256 `31ddfe8d7d426cacfb1acb17e443bbaa59a0e975fb92fb47916a600964362c6a`.

This is statement-phase evidence, not theorem-completion evidence. The intake node is only
provisional (`[_]`) pending master acceptance, and the anchor audit, obligation registry, proof,
hermetic validation, independent validation, release, and master acceptance remain open.
