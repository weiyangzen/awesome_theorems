# Statement validation

Base revision: `12d69b6951899a8e7de7ade1dfc86ce524d34a6e`.

The canonical target uses the repository wording, elementary equivalence, while the additional
`#M <= kappa` bound makes "arbitrarily large" explicitly upward. The single direct import is
`Mathlib.ModelTheory.Satisfiability`. The elementary-extension presentation is credited only in
the checked implication direction. This phase claims statement elaboration, not theorem proof.

| Command | Result |
|---|---|
| `lake env lean ../../Stage1_Instances/THM-M-0646/Statement.lean` from `Formalizations/Lean` | exit 0; target and both checked implication witnesses elaborated; explicit universe expression printed |
| `lake env lean ../../Stage1_Instances/THM-M-0646/StatementMutations.lean` from `Formalizations/Lean` | exit 1 as required; removed `Infinite M`, changed cardinal domain, invalid binder scope, and finite-cardinal boundary were all rejected |
| mutation output assertions for `Infinite M`, `Unknown identifier M`, and `aleph_0 = 0` | exit 0; expected independent failure signatures found |
| `python3 -m json.tool` on `instance.json` and `statement-receipt.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0646` | exit 0; rank 692, L0/rework_required, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-0646 .stage1-worker-selftest.json` | exit 0 |

Expression evidence is the exact `#print` output in `statement-elaboration.txt`, SHA-256
`60759741f71ff69531857f6ed68ac5b989f60dec9d4d7faed08564cce2b16dfc`.

Known failures outside this node: source pinpoint review/H0, anchor audit, frozen obligation graphs,
proof and provenance closure, hermetic replay, release checks, and independent validation remain
open. No audit or theorem completion is claimed.
