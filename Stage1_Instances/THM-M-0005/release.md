# THM-M-0005 release reconciliation

Item: `S56-M-0005-RELEASE`

Base revision: `229ca98e7478d389ccf8de8173c94e0e7c8fe670`

Decision date: `2026-07-15` (`Asia/Shanghai`)

## Exact verdict

The release verdict is `blocked`. Lifecycle remains `planned`; the accepted root vector stays
`[H1, M3, R3]`; `audit_complete=false`; and `theorem_complete=false`. No receipt or frozen
obligation is accepted.

The first gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. `S56-M-0005-VALIDATION` is only
worker-provisional `[_]`; its receipt is `accepted=false`, `release_grade=false`, `verdict=blocked`,
and not master accepted. The validation recipe is also stale on the current snapshot: its checker
is bound to ancestor revision `63a9ed9c` and exits before replay, while its recorded blueprint and
execution-DAG hashes differ from current authority.

## Evidence reconciliation

The exact frozen `KunnethFormula` statement elaborates with pinned Lean 4.29.0 and the existing
mathlib revision. Prior provisional validation observed 22 partial or conditional declarations as
sorry-free with only `propext`, `Classical.choice`, and `Quot.sound`. That is useful negative and
partial-progress evidence, not exact-root closure or release evidence.

No premise-free `NaturalKunnethSequence` is recorded or validated in the reconciled snapshot.
`root_compose` and
`kunnethFormula_of_fields` explicitly consume the missing Kunneth construction, exactness, and
naturality premises. The authoritative graph has zero closed obligations, `root_closed=false`, and
the following root cut:

```text
M0005-CHAIN-FREE
M0005-EZ-MAP
M0005-EZ-EQUIV
M0005-EZ-NAT
M0005-ALG-MAPS
M0005-ALG-ZERO
M0005-ALG-EXACT
M0005-ALG-NAT
M0005-DIRECT-SUM
M0005-COMPONENTS
M0005-TOP-NAT
```

`AUDIT-Z` is independently blocked by the unresolved exact source and splitting boundary, H1
pinpoint review, R3 reconstruction, trust/source-boundary classification, and evidence
reconciliation. `THEOREM-Z` additionally lacks exact-root M0 closure, complete provenance and TCB,
immutable clean input, empty-cache cold build, offline restoration, complete SBOM/license archive,
distinct signed runners, an independent minimal verifier, protected adversarial CI, and a
deterministic release bundle.

## Commands and results

Commands ran in the worker clone on 2026-07-15. The automation-provided pinned `.lake` symlink was
reused without intentional mutation. No `lake update`, `lake build`, dependency clone/fetch, or
checkout was performed.

The receipt contains a path-sorted SHA-256 ledger for every non-self-referential untracked input,
including a hash of the `.lake` symlink target without publishing its absolute value. The receipt
cannot embed its own final hash; that recursion boundary is explicit and requires the integration
lane to content-address the completed receipt before acceptance.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | The standard, skill, and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets at ranks 1 through 1,546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Rank 100 remains planned and theorem-incomplete. |
| `python3 -B Stage1_Instances/THM-M-0005/check_obligation_tree.py` | 0 | 18 obligations and 51 typed edges passed; root remains open M3 with zero closure credit. |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 180s lake env lean --trust=0 ../../Stage1_Instances/THM-M-0005/KunnethStatement.lean` | 0 | Exact statement elaborated; four unused-variable linter warnings; no proof/root closure checked. |
| `python3 -I -B Stage1_Instances/THM-M-0005/check_validation.py --probe` | 1 | Stale validation checker rejected current HEAD at its ancestor base-revision assertion before Lean. |
| `python3 -I -B Stage1_Instances/THM-M-0005/check_release.py` | 0 | Inputs reconciled, statement re-elaborated, and the blocked H1/M3/R3 decision passed. |
| `python3 -m json.tool` over the release JSON artifacts and worker packet | 0 | All JSON parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0005-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0005/check_release.py` | 0 | Checker syntax compiled outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0005 .stage1-worker-selftest.json` | 0 | No tracked whitespace diagnostics; `check_release.py` separately byte-checks every untracked release path. |

Status boundary: this is a self-tested negative release decision proposed as worker `[_]` for
integration review. It is not an accepted receipt, H0, M0, E0/E1, R0, `AUDIT-Z`, `THEOREM-Z`,
release, theorem completion, or master acceptance.
