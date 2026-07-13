# THM-M-0914 Anchor-Audit Validation

Item: `S56-M-0914-ANCHOR_AUDIT`

Base revision: `a1c9974d7fb28cd680e6494b968544bf801a93a2`

Base tree: `1fa287bc821355aca2ca9e3ce107830a3eb58e64`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Fintype.exists_ne_map_eq_of_card_lt` specializes exactly to the frozen claim about every
`Fin (n + 1) -> Fin n` placement. The audit adapter preserves the ordered binders, distinctness,
collision conclusion, and the vacuous `n = 0` case. Its substantive terminal body is
`Finset.exists_ne_map_eq_of_card_lt_of_maps_to`, not the shallow `Fintype` wrapper.

Lean reports the mathlib wrapper, terminal theorem, and audit adapter sorry-free. It reports only
`propext`, `Classical.choice`, and `Quot.sound`. A transitive environment scan covers 3,623
declarations in 117 modules and finds no bodyless nonaxiom or unsafe declaration. This establishes
an exact prospective `M0-W` route, but the dirty provisional worker check is below accepted `E1`;
the current and accepted machine classification remains `M3`.

The bounded external audit also found an independent exact-family source theorem in ZeroToQED and
an instructional duplicate wrapper in FormalBook, both at immutable revisions. ZeroToQED is pinned
to Lean 4.30 and a different mathlib revision and was source-inspected, not built in its own closure.
FormalBook delegates to the same mathlib wrapper. Neither receives machine-proof credit here.

## Commands And Results

All local validation used the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, installation, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0914` | 0 | rank 1456; planned; L0/rework-required; theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base `a1c9974d...a93a2`, tree `1fa287bc...8e64` |
| `git status --short` before editing | 0 | only pre-existing automation-provided `Formalizations/Lean/.lake` was untracked |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; dependency worktree clean |
| bounded `rg` over repository Lean and all materialized manifest packages | 0 | no repo-local exact body outside the target; only pinned mathlib supplied relevant local declarations |
| Sourcegraph exact-declaration query, archived/forks included | 0 | completed across 10 repositories with 37 matches and no skipped shards; response SHA-256 `48a864b...a70` |
| two anonymous GitHub repository queries | HTTP 200 | both returned zero complete repository-metadata results; response SHA-256 `4af480b...a5f` |
| GitHub code query | HTTP 403 | API rate limit; access limitation, not negative evidence; response SHA-256 `1db366a...86e` |
| grep.app exact declaration query | HTTP 429 | security checkpoint; access limitation, not negative evidence; response SHA-256 `f839964...944` |
| immutable ZeroToQED archive/source/lock/toolchain/license inspection at `877c7cc5...aeaf` | 0 | exact-family independent source body recorded; archive SHA-256 `936fbb7b...60e`; no upstream build claimed |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --stdin` over the immutable ZeroToQED pigeonhole source | 0 | local 4.29 compatibility elaboration passed with empty stdout; this is not an upstream 4.30 build or E2 evidence |
| immutable FormalBook archive/source/lock/toolchain/license inspection at `701731c7...bdc` | 0 | explicit-box wrapper delegates to mathlib; archive SHA-256 `8e93c92a...f43`; no upstream build claimed |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0914/Statement.lean` | 0 | frozen statement replay passed; stdout SHA-256 `718818ab...b64` |
| `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0914/check_statement.py` after adding anchor artifacts | 1 (known predecessor limitation) | reports `owned statement artifact inventory changed`; it hard-codes the pre-anchor 14-file inventory, so the anchor checker now owns statement-input and canonical-composition replay |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0914/AnchorAudit.lean` | 0 | exact wrapper/terminal bodies printed; three sorry-free reports; expected axioms and clean closure; stdout SHA-256 `e1b4eed9...da4` |
| `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0914/check_anchor_audit.py` | 0 | identities, pins, hashes, source markers, candidates, exact target, receipt, packet, Lean replay, and validator-only composition with the actual canonical declaration matched |
| `python3 -m json.tool` on the protocol, audit, receipt, and worker packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` and visible pinned wrapper/terminal source | 1 (expected no match) | no placeholder, declared axiom, unsafe/opaque declaration, oracle, external-code marker, or generated proof shortcut |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0914-anchor-pycache python3 -m py_compile Stage1_Instances/THM-M-0914/check_anchor_audit.py` | 0 | checker syntax passed without writing into the owned path |
| `git diff --check -- Stage1_Instances/THM-M-0914 .stage1-worker-selftest.json` plus added-file no-index checks | 0 / 1 expected | no whitespace diagnostics; no-index exits 1 only because each file is new |

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending dependency-ordered master
acceptance. It does not accept `M0-W` or `E1`, integrate the external source, freeze the obligation
registry, supply canonical proof-phase composition, close H0/R0, perform release-grade TCB or
hermetic independent validation, finish `AUDIT-Z`, or complete the theorem.
