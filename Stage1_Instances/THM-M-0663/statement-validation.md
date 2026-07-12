# Statement validation

Validation date: 2026-07-12 (Asia/Shanghai). Base revision:
`a74bf62e5952864a45901ffdf9160b000ba3fd01`.

The existing untracked `Formalizations/Lean/.lake` link/artifact was used read-only. No dependency
update, build, clone, or fetch command was run. Lean elaboration used the repository toolchain and
the already pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0663` | exit 0; rank 707, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0663/check_statement.py` | exit 0; `statement invariant check: ok` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0663/Statement.lean` | exit 0; canonical target, definitional transport, mutations, and empty-domain boundary elaborate |
| remove each direct import in turn and rerun the preceding Lean command | the three retained imports each fail when removed; `Mathlib.Order.Interval.Set.Basic` remained removable and was deleted |
| `python3 -m json.tool Stage1_Instances/THM-M-0663/statement.json` | exit 0 |
| scoped forbidden-token scan over statement artifacts | exit 0; no `sorry`, `axiom`, or `admit` token |
| `git diff --check -- Stage1_Instances/THM-M-0663 .stage1-worker-selftest.json` | exit 0; no output |

Final content hashes and the full `pp.explicit` print are recorded in `statement.json` and
`statement-print.txt` respectively.

## Status boundary

This is statement-only evidence for `S56-M-0663-STATEMENT`. The broad repository gloss does not
itself supply a theorem/page citation, so exact primary-source fidelity remains an H-axis task for
the later audit. No proof of o-minimal monotonicity, formal candidate acceptance, obligation tree,
audit completion, or theorem completion is claimed.
