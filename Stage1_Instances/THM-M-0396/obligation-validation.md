# THM-M-0396 obligation-tree validation

Item: `S56-M-0396-OBLIGATION_TREE`  
Base revision: `d1dfa89886e694f1978fa8ee3a7509babd6864b8`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The frozen registry contains 15 unique semantic obligations. Fourteen are
machine-required; the primary-source policy boundary is explicitly machine
`not_applicable` while remaining human-source and readability required. The
registry denominator SHA-256 is
`a4b1dbec5ed8621aa5ddca701659bf926d52a87c57be115432db11d628e37bc2`.

The structural validator checked required registry and node fields, statement
and anchor-audit hashes, one-to-one node coverage, the denominator hash, seven
typed graph families, reciprocal proof/composition edges, proof acyclicity,
validation-recipe references, forbidden Lean mechanisms, and the honest open
root boundary. The Lean check elaborated the statement, the binder-level
`CoreEstimate` equivalence, and conditional `root_compose`. Its axiom report was
`[propext, Classical.choice, Quot.sound]`, inherited from the definitions and
mathlib environment; no new axiom declaration was introduced.

Only the checked statement-layer obligations `M0396-S2` and `M0396-S3` are
`M0-L`. The canonical root stays `M3`; all substantive Baker-Matveev estimate
obligations are `M4`, and `M0396-T` is the remaining root cut.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0396` | 0 | rank 9, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0396/build_obligation_artifacts.py` | 0 | deterministically generated the registry, graph bundle, and validation specs |
| `python3 Stage1_Instances/THM-M-0396/check_obligation_tree.py` | 0 | `PASS THM-M-0396 obligation tree: 15 obligations, 9 proof requirements; root M3/open` |
| `tmp=$(mktemp -d ./.m0396-obligation.XXXXXX); trap 'rm -rf "$tmp"' EXIT; cp ../../Stage1_Instances/THM-M-0396/Statement.lean ../../Stage1_Instances/THM-M-0396/ObligationTree.lean "$tmp/"; lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean" && LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean "$tmp/ObligationTree.lean"` from `Formalizations/Lean` | 0 | statement and conditional composition elaborated; `root_compose` axiom report printed |
| `jq empty` on the three generated JSON artifacts | 0 | all structured artifacts parsed |
| forbidden-token `rg` on `ObligationTree.lean` | 1 | expected no-match result: no `sorry`, `admit`, axiom declaration, `sorryAx`, placeholder, or unsafe mechanism |
| `git diff --check -- Stage1_Instances/THM-M-0396 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Generated artifact hashes:

```text
d63c20b7d77043e656fd5e295e68171a5b3d4dabea527dd6c6d1a15c90ff97f3  obligation-registry.json
b0090e4f7389f2c9d26f350719b88ef2e40f49c530b561a896c909bd1a7ad942  typed-graphs.json
2cfda44f9edd2f9a20f87de801ddb8a8fdd4b9179ffe86e2c706f9735eb6e986  validation-specs.json
93551393a7489d5705b063a632952da8018d97285b32d4d2b25fdb2642dee81b  ObligationTree.lean
```

The pre-existing untracked `Formalizations/Lean/.lake` canonical link was
reused without mutation. No update, broad build, clone, or fetch ran.

## Status boundary

This self-test covers only the obligation-tree phase. Planned signatures are
not declarations or proof evidence. The conditional composition requires the
entire analytic estimate as a premise. Human-source pinpointing, readable
reconstruction, terminal proof, trust closure, hermetic replay, independent
verification, audit completion, theorem completion, and master acceptance all
remain open.
