# THM-M-0125 statement recheck: blocked at current HEAD

Item: `S56-M-0125-STATEMENT`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff` (tree
`24acf86e69ab2e6fca9480c6269b6429874ba295`). Rechecked on 2026-07-16
(`Asia/Shanghai`) in worker slot 73.

## Decision

The exact-statement gate is blocked. The repository metadata identifies only the Gross-Zagier
theorem family and the gloss "elliptic-curve derivative formula." It does not select one exact
mathematical proposition. The prerequisite `S56-M-0125-INTAKE` remains provisional `[_]`, not
master-accepted `[x]`; its manifest deliberately leaves the source variant, normalization,
canonical Lean expression, and imports open.

The author-hosted scan of Gross and Zagier, *Heegner points and derivatives of L-series*, confirms
at least three materially different candidates consistent with that gloss:

| Candidate | Source locator | Material distinction |
|---|---|---|
| General Rankin formula | Chapter I, Theorem (6.3), journal page 230 | A normalized weight-two newform and class-group character; an explicit Rankin derivative formula involving the height of an isotypical Heegner-divisor component in a Jacobian and Petersson, class-number, unit-index, and discriminant factors |
| Elliptic application | Chapter I, Theorem (7.3), journal page 231 | If `L(E, 1) = 0` for a modular elliptic curve, a rational point exists whose canonical height gives `L'(E, 1)` up to a real period and a nonzero rational factor |
| Elliptic base-change identity | Chapter V, Theorem (2.1), journal page 311 | An explicit identity for `L'(E/K, 1)` using a modular parametrization, differential norm, traced Heegner point, canonical height, unit index, and discriminant |

The source also corrects its earlier announcement immediately after Chapter I equation (5.3),
journal page 229: Euler factors at primes dividing the level had not been removed. Candidate and
normalization selection therefore changes the proposition. No worker may infer one from the short
catalog gloss, and no accountable source reviewer or master decision has selected one.

No substantive target input changed after the latest integrated recheck. The current repository
adds the v2 dependency overlay and its execution gates. Under that overlay this theorem has no hard
parents or transitive ancestors, no reuse hints, no shared lemma groups, and no reusable artifact.
The target-owned `dependency-reuse-ledger.json` binds graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`, context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`, the current base revision,
and the audited empty closure. It transfers no proof or statement credit and does not assert that
the mathematical proof is independent of other theorems.

Consequently there is no truthful canonical human statement or Lean expression whose imports can
be minimized and whose elaborated expression and environment can be fingerprinted. There is no
target against which to check alternate-form transports or the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. Those mutations are
unexecutable, not passed. The first failed gate is
`exact_source_variant_and_normalization_selection`.

Lifecycle remains `planned`; the root vector remains `H1 / M4 / R3`; this statement item remains
`[ ]`. No statement receipt, proof evidence, debt change, audit completion, theorem completion, or
master acceptance is claimed.

## Pinned Lean Boundary

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_044.lean` freshly elaborates in the existing
pinned Lake environment. It is not the exact target: its interfaces accept caller-supplied complex
derivative, height, normalization, and proposition fields rather than construct a selected
arithmetic L-series, Heegner point or divisor, canonical height, and source normalization.

A bounded search of pinned mathlib and `flt-regular` found no Gross-Zagier, Heegner-point,
Neron-Tate, elliptic Hasse-Weil, or Rankin-L target declaration. Pinned mathlib has only generic
surfaces such as L-series derivatives and a Petersson integrand. The six legacy imports support only
the abstract boundary and cannot be certified as minimal for an unidentified target. These results
are negative boundary evidence only; they confer no statement, import-minimality, transport,
mutation, anchor-audit, or proof credit.

Replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both dependency worktrees were clean. The existing
automation-provided `.lake` symlink was reused without mutation. No update, build, clone, or fetch
was performed.

## Validation Record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` before writing evidence | 0 | 1546 theorems and all 10822 legacy phase states passed; graph has 2 hard edges, 5 reuse hints, 310 shared groups, and is acyclic |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0125` | 0 | rank 44; planned; legacy slot `S1-M-044`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; revision and tree match this record |
| v2 node, incoming-edge, hint, and shared-group queries | 0 | all five required context ID sets are empty; the node context digest matches this record |
| dependency-ledger schema validator | 0 | the target-owned schema-1.1 ledger matches the current graph, context, base revision, and audited empty closure |
| fresh `curl`, `sha256sum`, `wc`, `pdfinfo`, and `pdftotext -layout` on the author-hosted scan | 0 | 96 pages, 4,395,679 bytes, SHA-256 `8afee839...d9521`; Theorems I.6.3, I.7.3, V.2.1 and the correction after I.(5.3) were rechecked |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_044.lean` | 0 | empty stdout/stderr; the abstract legacy boundary elaborated without exact-target credit |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| pinned mathlib and `flt-regular` status and revision/tree checks | 0 | both package worktrees were clean at the identities above |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` Lean sources | 1, expected no match | no relevant target spelling |

The structured companion records the final artifact, hygiene, and standard-validation checks. A
post-edit v2/standard check correctly reports that the checked-in master-owned theorem DAG is stale
relative to this worker's newly added statement JSON inventory. Workers are forbidden to regenerate
or edit that DAG; the integration lane regenerates and validates it after copying a blocked artifact
batch. This expected handoff boundary is not a statement pass. No `.stage1-worker-selftest.json` is
emitted because the exact-statement deliverable did not pass.

## Retry Condition

After intake master acceptance, an accountable owner must preserve and independently review one
immutable primary-source edition and select exactly one theorem or corollary. Its theorem/page,
incorporated definitions, ordered binders, hypotheses, conclusion, L-series and central-point
convention, Heegner construction, height and parametrization conventions, every period and local
factor, corrections, errata, and degenerate cases must be frozen. Only then can concrete pinned Lean
objects encode that approved claim, imports be minimized, expression and environment fingerprints
be serialized, transports be checked, and all four mutation classes be executed.
