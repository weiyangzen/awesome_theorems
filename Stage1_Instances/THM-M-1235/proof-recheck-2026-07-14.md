# THM-M-1235 proof-phase recheck

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `67b1bf1758649d2be86775230c7d4bfe117ade2b`

Base tree: `5f872831428a9d9805e61aad3868be443c29cef2`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target. The
tracked placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

kernel-checks again at trust level zero. In the frozen encoding, each of
`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` is freely chosen data of
type `Prop`; none is a proof of a predicate constraining the five functions.
Consequently, record update can replace any alleged unique motion's
`velocityX` by `velocityX + 1` without violating the structure type. Equality
of the two velocity functions at `(0, 0), 0` is contradictory. The concrete
`counterexampleData` also satisfies every explicit premise of the target.

This refutes only the frozen formal encoding, not Wolibner's mathematical
theorem. A proof of a corrected, weaker, or conditional proposition cannot be
substituted during this proof item. `M1235-T-ASSEMBLE` remains merely a checked
conditional composition from unproved existence and uniqueness packages; the
refutation shows that its uniqueness premise is impossible for this interface.
The item remains `[ ]`, with no proof receipt, accepted obligation, audit
completion, or theorem completion claimed.

## Failed Gate And Retry

The first failed gate is exact-target consistency. Reopen
`S56-M-1235-STATEMENT`, express conditions `(I)`--`(VIII)` as predicates of the
five functions, and require proofs of those predicates in `Motion`. Then
re-audit the source formulation and issue a versioned re-freeze of the
canonical expression fingerprint, crosswalk, obligation registry, typed
graphs, and dependent evidence before another proof run.

## Validation

All checks used the existing pinned Lake closure. No update, build, fetch,
clone, or dependency mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | rank 159, planned lifecycle, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; frozen projection remains root-open M3 |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement and both refutation declarations elaborated; axiom reports are `[propext, Classical.choice, Quot.sound]` |
| first isolated direct-`lean` probe without `LEAN_PATH` | 1 | rejected before elaboration with `unknown module prefix 'Mathlib'`; corrected by invoking the recorded `lake env lean` recipe |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-blocker.json` | 0 | tracked structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1235` | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
tmp=$(mktemp -d ./.thm-m-1235-final-recheck.XXXXXX)
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
