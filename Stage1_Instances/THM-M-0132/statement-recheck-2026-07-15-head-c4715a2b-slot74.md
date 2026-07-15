# THM-M-0132 statement recheck: blocked

Item: `S56-M-0132-STATEMENT`

Base revision: `c4715a2babbead02e04d70708c3ebc58c75a1942` (tree
`28cd40da86c57dea61aed02b4965f80699894bd3`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 74.

## Decision

The exact-statement gate remains blocked. The intake identifies the human root as BCDT Theorem A:
every elliptic curve over `Q` is modular. The pinned Lean closure can express a rational
Weierstrass curve, its nonsingularity, analytic cusp forms, and congruence subgroups. It cannot
express the source-faithful conclusion: it has no elliptic-curve conductor, normalized weight-two
newform or eigenform, conductor-level equality, or concrete compatibility connecting the curve to
a form through L-series, Frobenius traces, or Galois representations.

The legacy `AwesomeTheorems.Stage1.S1_M_049.StatementShape` does not repair this gap. Its witness
chooses an arbitrary positive natural number, arbitrary subgroup, arbitrary cusp form, and three
freely supplied propositions, only one of which must be inhabited. It therefore omits exactly the
mathematics needed to mean modularity. Reusing it, introducing an uninterpreted `IsModular`
predicate, or asserting existence of an unrelated cusp form would weaken and substitute BCDT
Theorem A. The semistable Wiles/Taylor-Wiles branch likewise cannot replace the unrestricted root.

The predecessor `S56-M-0132-INTAKE` is provisional `[_]`, not master-accepted `[x]`. No target input
changed after the integrated blocker at `de9509a9b807a45e9fb1511465a7b957788afc54`: the manifest,
source records, dossier, legacy Lean module, toolchain, and dependency lock are unchanged. The
rev-5.6 blueprint and DAG changed for unrelated integrations, but their `THM-M-0132` projections
are identical.

Consequently there is no truthful canonical Lean target, target-minimal import set, elaborated
expression hash, canonical-target environment fingerprint, checked alternate transport, or
meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutation suite.
The first failed statement gate is `exact_source_faithful_modularity_relation_unavailable`.
Lifecycle remains `planned`, debt remains `H1 / M3 / R3`, and the statement node remains `[ ]`.
No proof, receipt, debt change, audit completion, theorem completion, or master acceptance is
claimed.

## Pinned Lean Boundary

Fresh elaboration of `StatementInfrastructure.lean` emitted the three expected API types, 207
bytes, at SHA-256
`f0c8f435355cda30057d64773163f7294fdb9749f52e99b30d87a33b19042a22`; stderr was empty. The
probe declares no canonical target or proof body. Deleting its Weierstrass import or
`ModularForms.Basic` import makes the probe fail. Deleting its explicit `CongruenceSubgroups`
import succeeds because the current `ModularForms.Basic` closure already exposes `Gamma0`. This
corrects the earlier implication that all three probe imports were minimal; it does not make
canonical-target minimality assessable.

Fresh elaboration of the legacy module returned exit 0 with empty output. A bounded pinned-source
search returned one line, solely an expository Wiles citation in
`Mathlib/NumberTheory/FLT/Basic.lean`, at SHA-256
`bd7d21b7628a98883926bd705a975b38aafb5d608df1dfb3f2841709a817f2ae`. No relevant Lean declaration
was located. These are boundary checks, not a downstream exhaustive anchor audit.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both dependency worktrees were clean. The
automation-provided canonical `.lake` symlink was reused read-only. No update, build, clone, fetch,
or other dependency mutation was performed.

## Validation Record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0132` | 0 | rank 49; planned; legacy slot `S1-M-049`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree match this record |
| scoped standard, source, dossier, legacy-module, infrastructure, and prior-blocker inspection | 0 | the human root is identified, but its source-faithful Lean conclusion remains unavailable; the prior blocker remains substantively correct |
| target-input diff and exact `THM-M-0132` JSON/Markdown projection comparison since `de9509a9b` | 0 | target sources, dossier, legacy Lean, toolchain, and lock are unchanged; target blueprint/DAG projections compare equal |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0132/StatementInfrastructure.lean` | 0 | three adjacent API types elaborated; no canonical target or proof body was declared |
| import-deletion elaboration on temporary copies of the infrastructure probe | 0 aggregate | deleting Weierstrass or `ModularForms.Basic` failed as expected; deleting explicit `CongruenceSubgroups` succeeded through the Basic import closure |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_049.lean` | 0 | legacy abstract compatibility boundary elaborated with empty output; no exact-target credit applies |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| mathlib and `flt-regular` status plus revision/tree checks | 0 | both dependency worktrees were clean at the pinned revisions and trees above |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` Lean sources | 0 | one expository Wiles citation and no relevant declaration; not a completed anchor audit |
| declaration-position prohibited-construct scan over the owned probe and legacy module | 1, expected no match | no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe declaration, or backend replacement occurrence; legacy `native_decide` planning proofs receive no target proof credit |

## Retry Condition And Boundary

Retry after the intake is dependency-ordered and master-accepted and source-faithful conductor,
normalized weight-two newform, level-matching, and arithmetic compatibility interfaces are
implemented or pinned. The selected interfaces and curve-representation transports must be
reviewed against the BCDT source. A fresh worker can then elaborate only the approved universal
claim, minimize its imports, fingerprint the expression and environment, compile every credited
transport, and execute all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence only. Because the positive statement
deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker
`[_]` or master acceptance is requested.
