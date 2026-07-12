# Statement validation

The statement phase inspected the immutable arXiv v2 PDF of the primary paper (SHA-256
`0a432946234949c12a3e379e42d8f79fa646b9002810ffe97817d52aca184a7a`) and selected its Theorem
1.1 exactly, including the uniform permutation model, strict LIS statistic, centering `2 sqrt N`,
`N^(1/6)` scaling, every-real-threshold CDF convention, and its equations (1.4)--(1.6) definition
of `F`. The formal target is `Stage1Instances.THM_M_1108.CanonicalStatement` in `Statement.lean`.

The three direct imports are the smallest set found by deletion testing: removing any one makes
an identifier or instance used by the file unavailable. The file includes an unfolded checked
`iff` and four successful `#check_failure` mutation probes. Their type-mismatch diagnostics are
expected output; Lean exits zero.

## Validation record

Base revision: `9464c8a759b73fadf4c56c116c00b7ec96409b2a`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1108` | exit 0; rank 548, planned, L0/rework_required, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1108/Statement.lean)` | exit 0; canonical target and unfolded transport elaborated; four mutation terms rejected; transport axioms printed |
| `python3 -m json.tool Stage1_Instances/THM-M-1108/statement.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-1108 .stage1-worker-selftest.json` | exit 0; no output |

Validation is nonrelease. The clone reuses a pre-existing untracked `Formalizations/Lean/.lake`
link to canonical pinned artifacts. No Lake update, build, fetch, clone, or `.lake` mutation was
performed.

## Boundary

This is statement-node evidence only. Primary-source independent review, anchor audit, obligation
registry, proof, hermetic replay, and release validation remain open. In particular, elaborating
the proposition proves neither the existence/uniqueness encoded by `IsTracyWidomCDF` nor the BDJ
limit itself.
