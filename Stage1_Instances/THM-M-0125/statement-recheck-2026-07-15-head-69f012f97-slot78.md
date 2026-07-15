# THM-M-0125 statement recheck: blocked

Item: `S56-M-0125-STATEMENT`

Base revision: `69f012f979c7114db1ee4a877c5742d4742cadba` (tree
`a4415d1a7f473d7540904dd4fd84d17ac0f99820`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 78.

## Decision

The exact-statement gate remains blocked. The repository catalog supplies only the name
"Gross-Zagier formula" and the gloss "elliptic-curve derivative formula." The provisional intake
records a theorem family but deliberately leaves the source variant and normalization unresolved.
It has state `[_]`, not master-accepted `[x]`.

A fresh source check recovered the author-hosted scan of Gross and Zagier, *Heegner points and
derivatives of L-series*, Inventiones Mathematicae 84 (1986), 225-320. The 96-page,
4,395,679-byte PDF has SHA-256
`8afee839cdc0e2056c6dcbe348e39c0a6aa27344125d8c3b80dd735f2e6d9521`. It confirms that the
metadata does not identify one proposition. At least three materially different candidates fit the
gloss:

| Candidate | Source locator | Material distinction |
|---|---|---|
| General Rankin formula | Chapter I, Theorem (6.3), journal page 230 | A normalized weight-two newform and class-group character; the Rankin derivative is related to the canonical height of an isotypical Heegner-divisor component in a Jacobian |
| Elliptic application | Chapter I, Theorem (7.3), journal page 231 | For a modular elliptic curve with `L(E, 1) = 0`, there is a rational point whose height gives `L'(E, 1)` up to a real period and a nonzero rational factor |
| Elliptic base-change identity | Chapter V, Theorem (2.1), journal page 311 | An explicit formula for `L'(E/K, 1)` involving a modular parametrization, differential norm, Heegner-point height, unit index, and discriminant |

These candidates have different binders, hypotheses, objects, conclusions, and constants. The
source also explicitly corrects the earlier announcement's omitted Euler factors at primes dividing
the level. Selecting one candidate, or silently translating among completed and imprimitive
L-series, Jacobian and elliptic-curve heights, or rational and explicit factors, would therefore
invent proposition-changing mathematics. The scan is ephemeral audit input; it was not added to
the repository and does not itself authorize target selection.

No authoritative target input has changed since the integrated historical blocker. The manifest,
catalog, Stage0 and legacy Stage1 records, execution skill and guidelines, intake dossier, legacy
Lean module, toolchain, and dependency lock are unchanged. Intervening rev-5.6 blueprint and DAG
changes affect unrelated items; the `THM-M-0125` projections are unchanged.

Consequently there is no truthful canonical Lean expression whose imports can be minimized or
whose expression and environment can be fingerprinted. No alternate form can receive a checked
transport. The required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined, not passed. The first failed gate remains
`exact_source_variant_and_normalization_selection`.

Lifecycle remains `planned`, the root vector remains `H1 / M4 / R3`, and this statement node
remains `[ ]`. No statement receipt, proof evidence, debt change, audit completion, theorem
completion, or master acceptance is claimed.

## Pinned Lean Boundary

The historical module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_044.lean` was freshly replayed with the existing
pinned Lake artifacts. It elaborates, but its main formula uses caller-supplied complex derivative,
height, and normalization values plus caller-supplied propositions. It does not construct the
source's Rankin or elliptic-curve L-series, Heegner point or divisor, canonical height, or selected
constant. Successful replay is negative boundary evidence only, not exact-target or minimal-import
evidence.

A bounded spelling search over the pinned mathlib and `flt-regular` Lean sources found no
Gross-Zagier, Heegner-point, Neron-Tate, Hasse-Weil, or Rankin-L target API. Mathlib's only
`Heegner` spelling is a prose reference to Heegner numbers in the Chudnovsky-pi development. This
is a narrow local search, not the downstream anchor audit.

Replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both dependency worktrees were clean. The
automation-provided `.lake` symlink was reused without mutation. No update, build, clone, or fetch
was performed.

## Validation Record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0125` | 0 | rank 44; planned; legacy slot `S1-M-044`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree match this record |
| scoped inspection of the standard, skill, manifest, sources, intake, legacy module, and historical blocker | 0 | the intake still leaves the exact source variant and normalization unresolved |
| scoped comparison from blocker-integration revision `00e1e30f...` to HEAD | 0 | target inputs are unchanged; the expected no-match projection check found no `THM-M-0125` blueprint or DAG change |
| `curl -L --fail --max-time 120` on the author-hosted `fulltext.pdf`, then `sha256sum`, `pdfinfo`, and `pdftotext -layout` | 0 | recovered and inspected a 96-page, 4,395,679-byte source scan at SHA-256 `8afee839...d9521`; distinct Theorems I.6.3, I.7.3, and V.2.1 and the announcement correction were located |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_044.lean` | 0 | empty stdout and stderr; the abstract legacy interface elaborated but received no target credit |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| pinned mathlib and `flt-regular` status plus revision/tree checks | 0 | both package worktrees were clean at the pinned identities above |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` Lean sources | 1, expected no match | no relevant target API; a separate broad `Heegner` search found only the unrelated prose occurrence |
| prohibited-construct scan over owned and legacy Lean sources | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` construct matched |
| `python3 -m json.tool` plus scoped invariants on the companion recheck JSON | 0 | blocked identity, unchanged vector, null target fields, four undefined mutations, two-file scope, and absent self-test agreed |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; no-index exit 1 was only each expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement deliverable failed |

## Retry Condition And Boundary

Retry only after the intake is master-accepted and an accountable reviewer selects one exact
primary-source theorem or corollary. The selection must preserve an immutable edition and hash,
pin the theorem/page and incorporated definitions, transcribe every ordered binder and assumption,
freeze the L-series, central point, height, parametrization, period and local-factor conventions,
dispose of corrections and errata, and receive independent source review. A fresh worker can then
encode only that approved claim, minimize its pinned imports, serialize the elaborated expression
and environment fingerprints, compile every credited transport, and run all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence only. Because the positive statement
deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker `[_]`
or master acceptance is requested.
