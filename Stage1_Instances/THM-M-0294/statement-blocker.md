# Exact-statement gate: blocked

Item: `S56-M-0294-STATEMENT`

Theorem: `THM-M-0294`

Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4` (tree
`61214aa2a03c032134ddc4958b1df63df3430a85`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is only the title `普朗歇尔定理` (Plancherel theorem) and the
gloss `L^2函数的傅里叶变换等距性` ("isometry of the Fourier transform for `L^2` functions"),
with Michel Plancherel and 1910 as uncited metadata. It gives no binder-complete formula, exact
source theorem, spatial domain and dual, scalar or Hilbert value space, Fourier character and sign,
`2 * pi` and measure normalization, `L^2` carrier, extension route, ordered binders, exact
conclusion, or boundary cases. Stage0 leaves the precise definitions and premises open, and
rev-5.6 treats the catalog's `已验证` value as untrusted.

Those choices distinguish materially different propositions. Norm preservation, inner-product
preservation, existence of a linear isometry, unitary equivalence, inversion, and surjectivity are
not interchangeable roots. A theorem on `R`, `R^n`, arbitrary finite-dimensional real
inner-product spaces, or locally compact abelian groups also fixes different binders and
normalizations. The catalog separately retains `THM-M-0342` with the same name and a nearly
identical gloss, but no accepted reviewer decision establishes whether the records are aliases,
distinct formulations, or which target owns any terminal proof body. Selecting the familiar
Euclidean norm theorem, copying the sibling, or conjoining variants would invent, narrow, broaden,
or substitute mathematics.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and canonical expression and environment fingerprints null at `[H1, M3, R4]`.
Without one canonical target, checked transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than
passed. No `Statement.lean`, axiom, placeholder, assumed isometry, weakened special case, or
broadened theorem was introduced.

## Source boundary

The intake identifies Michel Plancherel's 1910 article *Contribution a l'etude de la
representation d'une fonction arbitraire par des integrales definies*, Rendiconti del Circolo
Matematico di Palermo 30, pages 289-335, DOI `10.1007/BF03014877`, as a primary-work metadata lead.
The publisher endpoint returned HTML rather than the article, and Crossref anomalously listed an
additional author. No immutable article text, exact theorem and definition locators, normalization
crosswalk, proof boundary, corrections or errata disposition, translation decision, or independent
review was admitted. This remains `H1` discovery, not a source-authorized statement.

The duplicate record at `Docs/researches/math_theorems.md:2493-2498` and the sibling
`Stage1_Instances/THM-M-0342` dossier are useful collision evidence only. Their selected target,
wrappers, receipts, debt, and state cannot be transferred into this owned path without an accepted
identity and proof-ownership decision.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with its single direct import,
`Mathlib.Analysis.Fourier.LpSpace`. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, it checks:

- `MeasureTheory.Lp.fourierTransformₗᵢ`, a complex linear isometry equivalence on `L^2`;
- `MeasureTheory.Lp.norm_fourier_eq`, the norm-preservation interface;
- `MeasureTheory.Lp.inner_fourier_eq`, the inner-product interface;
- the complex scalar specialization on `EuclideanSpace Real (Fin n)`.

All interfaces elaborate, but they do not decide which source proposition belongs to
`THM-M-0294`. The successful probe therefore supplies feasibility evidence only. Its import cannot
be certified minimal for an absent canonical target, and it receives no statement, transport,
anchor, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link points to canonical pinned artifacts and was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0294` | 0 | rank 1298, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped blueprint, skill, catalog, Stage0, manifest, intake, crosswalk, scope, duplicate, and pinned-candidate inspection | 0 | only the theorem family and gloss are authoritative; all proposition-changing choices and the duplicate identity remain open |
| `sha256sum` over authority, intake, toolchain, lockfile, sibling, and pinned Fourier inputs | 0 | current hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0294/IntakeProbe.lean` | 0 | three exact-topic interfaces and the Euclidean scalar specialization elaborated; stdout SHA-256 `7281909edded52829aec9eab57d00f09018134be03e7942ad90228ffa52f9862`; no canonical target or proof body was declared |
| bounded repo-local and pinned-mathlib Lean search | 0 | direct mathlib candidates, the sibling target, and an unrelated legacy infrastructure wrapper were found; discovery only |
| `python3 -B Stage1_Instances/THM-M-0294/check_intake.py` before adding the blocker artifacts | 0 | planned intake invariants were consistent at `[H1, M3, R4]` with six open tasks |
| the same intake replay after adding the blocker artifacts | 1 | expected historical-evidence failure: the intake checker freezes its exact original nine-file inventory and rejects the two later statement files; it was not rewritten |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-0294` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0294/statement-blocker.json` | 0 | the structured blocker parsed as JSON |
| scoped statement-blocker invariant assertions | 0 | item identity, open state, null target and imports, four undefined mutations, unchanged debt, false completion flags, exact two-file change scope, and absent self-test agree |
| scoped whitespace checks for both blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test exists because the exact-statement deliverable did not pass |

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`; its
receipt declares `accepted: false` and is not content-addressed. Rev-5.6 permits this
dependency-ordered attempt, but dependency acceptance independently remains necessary before any
future statement transition can be accepted. The first substantive failure is the missing exact
source proposition and duplicate-identity decision.

## Retry condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must preserve and hash one lawful complete primary or authoritative source edition, select and
transcribe one exact theorem and every incorporated definition with pinpoint locators, audit its
normalization, translation, corrections, errata, and proof boundary, and independently approve the
mapping. They must resolve the identity, deduplication, and proof-ownership relationship with
`THM-M-0342`, then freeze the spatial domain and dual, value space, `L^2` construction, measures,
Fourier kernel and constants, extension route, ordered binders, exact conclusion, and every
boundary case.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M3, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
