# Statement validation record

Item: `S56-M-0508-STATEMENT`. Base revision:
`aa55669bb59986e08ea8a0d1d77a1e40343d8142`.

`Statement.lean` freezes the exact natural-number reading of the repository claim and compiles a
checked equivalence to its eventual-filter presentation. The four named mutations deliberately
change the canonical proposition; they are separately elaborated so their differences remain
reviewable and cannot accidentally receive proof credit. The canonical declaration itself is
only a `Prop` definition, not a theorem proof.

The imports were selected by API ownership: `Prime.Basic` supplies `Nat.Prime` and parity, while
`AtTopBot.CountablyGenerated` supplies the `eventually_atTop` characterization used by the checked
transport. The canonical pinned `.lake` artifacts were used read-only. No update, build, clone, or
fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure passed: 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | manifest passed: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0508` | 0 | rank 882, planned, L0/rework-required, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0508/Statement.lean)` | 0 | exact target, checked eventual transport, four mutation expressions, and boundary lemma elaborated |
| `python3 Stage1_Instances/THM-M-0508/check_statement.py` | 0 | canonical expression hash `54ddaa6f...c1ac5fb`; all four structural mutations killed |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum /tmp/thm-m-0508-statement.out Stage1_Instances/THM-M-0508/Statement.lean` | 0 | explicit print `dc51d7...a19791`; source `e27734...7080da` |

Known failures are downstream rather than statement failures: historical pinpoint-source review,
anchor and provenance audit, obligation freeze, theorem proof, trust/composition closure, readable
reconstruction, hermetic replay, independent validation, and master acceptance remain open. This
record supports only worker self-test state `[_]` for the assigned statement node.
