# THM-M-1235 proof-phase recheck at current base

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `2aab68338c370228923a5f7aba2a10b328902eab`

Base tree: `cb6f7e43b6cb5a6b852dea13a3a42cc992176213`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target. The
tracked placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

kernel-checks again at trust level zero. In the frozen encoding, the fields
`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` have type `Prop`; they are
not proofs of predicates constraining the five motion functions. Thus record
update can replace any alleged unique motion's `velocityX` by `velocityX + 1`
without violating the structure type. The uniqueness conclusion would equate
the two velocity functions, and evaluation at `(0, 0), 0` gives a
contradiction. The concrete `counterexampleData` satisfies every explicit
premise of the frozen target.

This refutes only the current formal encoding, not Wolibner's mathematical
theorem. A corrected, weaker, or conditional proposition cannot be substituted
during this proof item. `M1235-T-ASSEMBLE` is still only a checked conditional
composition from unproved existence and uniqueness packages. The item remains
`[ ]`; no positive proof body, receipt, provisional state, audit completion,
theorem completion, release, or master acceptance is claimed.

## Failed Gate And Retry

The first failed gate is exact-target consistency. Reopen
`S56-M-1235-STATEMENT`, express conditions `(I)` through `(VIII)` as predicates
of the five functions, and require proofs of those predicates in `Motion`.
Then re-audit the source formulation and issue a versioned re-freeze of the
canonical expression fingerprint, crosswalk, obligation registry, typed
graphs, and dependent evidence before another proof run.

## Validation

All checks ran in this worker clone using the existing pinned Lake closure. No
update, build, fetch, clone, or dependency mutation was performed. The
automation-provided untracked `Formalizations/Lean/.lake` symlink makes this
nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | rank 159; planned lifecycle; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; the frozen projection remains root-open M3 |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and both refutation declarations elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-blocker.json` | 0 | the tracked structured blocker is valid JSON |
| `git diff --check --no-index /dev/null Stage1_Instances/THM-M-1235/proof-recheck-2026-07-14-head-2aab6833.md` | 1 | expected added-file result from `--no-index`; it emitted no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
tmp=$(mktemp -d ./.thm-m-1235-root.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-1235/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-1235/Proof.lean "$tmp/Proof.lean"
LEAN_PATH_BASE=$(lake env printenv LEAN_PATH)
timeout 300 lake env lean --trust=0 -t0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$LEAN_PATH_BASE" \
  timeout 300 lake env lean --trust=0 -t0 "$tmp/Proof.lean"
```

Input SHA-256 values were unchanged: statement
`e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`,
refutation body
`f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`,
registry `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`,
typed graphs
`a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`,
and anchor audit
`e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`.

No `.stage1-worker-selftest.json` is written because the assigned positive
proof deliverable is blocked rather than genuinely self-tested as complete.
