# THM-M-0125 statement recheck: blocked at current HEAD

Item: `S56-M-0125-STATEMENT`

Base revision: `49a36d838ccc3bf57666cf2281303ef09a1ef3e3` (tree
`6c9052ea5f96f6ab899d2d4fc26c762d8f6e540a`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 78.

## Decision

The exact-statement gate remains blocked. The authoritative repository inputs still identify only
the Gross-Zagier theorem family and the gloss "elliptic-curve derivative formula." They do not
select one mathematical proposition. The predecessor `S56-M-0125-INTAKE` also remains provisional
`[_]`, not master-accepted `[x]`.

The author-hosted scan of Gross and Zagier, *Heegner points and derivatives of L-series*, was
downloaded afresh to `/tmp` and inspected. The 96-page, 4,395,679-byte file again has SHA-256
`8afee839cdc0e2056c6dcbe348e39c0a6aa27344125d8c3b80dd735f2e6d9521`. It contains at least three
materially different candidates consistent with the repository gloss:

| Candidate | Source locator | Material distinction |
|---|---|---|
| General Rankin formula | Chapter I, Theorem (6.3), journal page 230 | A normalized weight-two newform and a class-group character; the Rankin derivative is related to the canonical height of an isotypical Heegner-divisor component in a Jacobian, with explicit Petersson, class-number, unit-index, and discriminant factors |
| Elliptic application | Chapter I, Theorem (7.3), journal page 231 | A modular elliptic curve with `L(E, 1) = 0`; existence of a rational point whose height gives `L'(E, 1)` up to a real period and a nonzero rational factor |
| Elliptic base-change identity | Chapter V, Theorem (2.1), journal page 311 | An explicit formula for `L'(E/K, 1)` using a modular parametrization, differential norm, traced Heegner point, canonical height, unit index, and discriminant |

The source also states after Chapter I equation (5.3), journal page 229, that its earlier
announcement failed to remove Euler factors at primes dividing the level. Thus choosing a candidate
or silently translating between its L-series, Heegner, height, or normalization conventions would
change the proposition. The source scan is ephemeral audit input; it is not stored in the repository
and does not supply the missing accountable selection or independent review.

The integrated prior recheck was based on revision `69f012f979c7114db1ee4a877c5742d4742cadba`.
Since then, the target manifest, source records, intake dossier, execution skill, guidelines, legacy
Lean module, toolchain, dependency lock, and every substantive `THM-M-0125` input remain unchanged.
Blueprint and DAG edits concern other targets; filtering those diffs for this theorem found no
match. The only new target-local inputs are the prior recheck files themselves.

Consequently there is still no truthful canonical human statement or Lean expression whose direct
imports can be minimized and whose elaborated expression and environment can be fingerprinted. No
alternate encoding can receive a checked transport. The required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations remain undefined rather than
passed. The first failed gate is `exact_source_variant_and_normalization_selection`.

Lifecycle remains `planned`; the root vector remains `H1 / M4 / R3`; the statement item remains
`[ ]`. No statement receipt, proof evidence, debt change, audit completion, theorem completion, or
master acceptance is claimed.

## Pinned Lean boundary

The historical module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_044.lean` was freshly replayed through the
existing pinned Lake environment. It elaborates, but its formula interfaces accept caller-supplied
complex derivative, height, normalization, and proposition fields. It constructs neither a selected
arithmetic L-series nor a Heegner point/divisor, canonical height, or source normalization. This is
negative boundary evidence only, not exact-target or minimal-import evidence.

A bounded search over the pinned mathlib and `flt-regular` Lean sources again found no Gross-Zagier,
Heegner-point, Neron-Tate, Hasse-Weil, or Rankin-L target spelling. The only broad `Heegner` match is
unrelated prose about Heegner numbers in mathlib's Chudnovsky-pi development. This is a local
statement-boundary check, not a downstream anchor audit.

Replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both dependency worktrees were clean. The
automation-provided `.lake` symlink was reused without mutation. No update, build, clone, or fetch
was performed.

## Validation record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0125` | 0 | rank 44; planned; legacy slot `S1-M-044`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; revision and tree match this record |
| scoped current-input hashes and diff from `69f012f9...` to HEAD | 0 | no substantive authoritative target input changed; the expected target-projection filter returned no match |
| fresh `curl`, `sha256sum`, `wc`, `pdfinfo`, and `pdftotext -layout` on the author-hosted scan | 0 | 96 pages, 4,395,679 bytes, SHA-256 `8afee839...d9521`; Theorems I.6.3, I.7.3, V.2.1 and the correction after I.(5.3) were rechecked |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_044.lean` | 0 | empty stdout/stderr; the abstract legacy boundary elaborated without exact-target credit |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| pinned mathlib and `flt-regular` status and revision/tree checks | 0 | both package worktrees were clean at the recorded identities |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` Lean sources | 1, expected no match | no relevant target spelling; the separate broad search found only unrelated prose |
| prohibited-construct scan over owned and legacy Lean sources | 1, expected no match | no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe path, or native-decision construct matched |

The structured companion records the remaining artifact checks. No
`.stage1-worker-selftest.json` is emitted because the assigned statement deliverable did not pass.

## Retry condition

After intake master acceptance, an accountable owner must select exactly one theorem or corollary
from an immutable primary-source edition and obtain independent review. Its theorem/page,
incorporated definitions, ordered binders, hypotheses, conclusion, L-series and central-point
convention, Heegner construction, height and parametrization conventions, every period/local
factor, corrections, errata, and degenerate cases must be frozen. Only then can concrete pinned Lean
objects encode that approved claim, imports be minimized, expression/environment fingerprints be
serialized, transports be checked, and all four mutation classes be executed.
