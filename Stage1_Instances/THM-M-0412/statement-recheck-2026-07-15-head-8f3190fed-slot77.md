# THM-M-0412 statement recheck: blocked

Item: `S56-M-0412-STATEMENT`

Base revision: `8f3190fed598f6cb4547035d0d96d460ba5fc5cc` (tree
`d8ca24ac4a840d07b81dcc099a4d31023046d649`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 77.

## Decision

The exact-statement gate is still blocked. The authoritative catalog record still consists only of
the Chinese label `皮尔斯猜想`, attribution to Trygve Nagell, year 1948, and the gloss
`某些三次曲线的整数点`. It still has no original-language identity, publication or theorem/page
locator, equation or curve family, parameter and point domains, ordered binders, hypotheses,
conclusion, proof boundary, correction history, or degenerate cases. The Stage0 projection still
marks the exact definitions and premises as missing.

No authoritative target input changed after the prior blocker attempt. Between its base revision
`4d389eb47e043f6f44925a418baee0d034f764ba` and this base revision, the only changes among the
reviewed inputs are unrelated scheduler-state projections plus integration of
`StatementProbe.lean` and `statement-blocker.{json,md}` themselves. The manifest, catalog, Stage0
record, execution skill, intake dossier, legacy Lean module, toolchain, and dependency lock are
unchanged. Current repository and bibliographic searches found no new source that resolves the
identity. OpenAlex's Trygve Nagell record has no 1948 work and its nearby cubic-work record does not
select this catalog claim; search incompleteness is preserved.

The integrated legacy module remains ineligible: its `NagellLutzBranchData` packages the desired
facts as abstract propositions and its conditional `StatementShape` assumes audit and source
predicates rather than encoding a source-backed cubic theorem. Substituting Nagell-Lutz, a
Ramanujan-Nagell equation, the Markov equation, Siegel finiteness, or an arbitrary Weierstrass cubic
would change the received mathematics.

Therefore the canonical human statement, canonical Lean expression, minimal imports, expression
hash, target environment fingerprint, credited transports, and all four required structural
mutations remain undefined. The first failed gate is `exact_source_statement_identity`. Lifecycle
remains `planned`, the root vector remains `H5 / M4 / R4`, and this node remains `[ ]`. No theorem,
proof body, receipt, debt change, audit completion, or theorem completion is claimed.

## Pinned Lean Boundary

The prior source-boundary probe was replayed with the existing pinned Lake artifacts and still
elaborates using the one direct import
`Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point`. It checks six nearby Weierstrass-curve APIs
only. This confirms that the environment is usable, not that any one API is the missing target or
that this import is minimal for an absent canonical expression.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was performed.

## Validation Record

Commands ran from this isolated worker clone unless a working directory is stated otherwise.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21; planned; legacy slot S1-M-021; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `.lake` symlink; base revision and tree match this record |
| source, manifest, blueprint, skill, intake, legacy-module, and prior-blocker inspection | 0 | the source record remains incomplete; intake still says `unresolved_source_identity`; prior blocker remains substantively correct |
| `git diff 4d389eb47e043f6f44925a418baee0d034f764ba..HEAD` over authoritative target inputs | 0 | no target-source, intake, legacy Lean, toolchain, or dependency-lock changes; only unrelated DAG/checklist states and the integrated prior blocker artifacts changed |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 0 | six adjacent APIs elaborated; stdout SHA-256 `52574dd9f0f5feda16279f9af5344d9218c0c6089ce238abe2bcc0c9f2628cbb`; no canonical target, transport, or proof body |
| from `Formalizations/Lean`: `lake env lean --version && lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| mathlib package `git status --short`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean at the revision and tree above |
| repo-local exact-topic search | 0 | matches remain sparse catalog projections or the rejected legacy correction; no exact proposition was found |
| pinned mathlib `Pierce`, `Nagell`, and `Lutz` source search | 0 | only unrelated author/reference matches; no exact target was found |
| OpenAlex/Crossref/Semantic Scholar and exact web discovery queries | mixed | no result established the catalog identity or an exact proposition; Google timed out and Semantic Scholar returned no usable payload, so the bounded search is not treated as exhaustive |
| `python3 -m json.tool` on the recheck JSON | 0 | structured current-HEAD blocker record parsed |
| scoped blocker invariant script | 0 | item/base identity, blocked state, unchanged vector, null canonical fields, undefined mutations, current input hashes, two-file change scope, and self-test absence agree |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry only after accountable reviewers preserve and hash an immutable primary or approved
authoritative source, reconcile the label, author, and date, and independently approve one exact
claim with every incorporated definition, binder, hypothesis, conclusion, correction, and boundary
case. A fresh statement worker can then encode that claim, minimize imports, fingerprint the
elaborated expression and environment, check transports, and run all four mutation classes.

This is fresh current-HEAD blocker evidence only. Because the positive statement deliverable did
not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker `[_]` or master
acceptance is requested.
