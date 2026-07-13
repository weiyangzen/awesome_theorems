# Exact-statement gate: blocked

Item: `S56-M-0291-STATEMENT`

Theorem: `THM-M-0291`

Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
`2c866b9d840d48c48ac839740c62d3b9440be0e5`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0291-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. It deliberately leaves the canonical
mathematical statement, Lean module and expression, expression hash, ordered binders, and
canonical-target environment fingerprint null or empty.

Independently, the exact source-statement gate fails. The repository record names Fejer's theorem,
attributes it to Lipot Fejer in 1900, and says only that the Cesaro means of a continuous function
converge uniformly. It contains no citation, definitions, binder-complete proposition, proof
boundary, translation, correction history, or reviewer. Stage0 repeats the gloss while explicitly
leaving precise definitions and premises, alternate forms, axioms, and machine artifacts open. Its
`verified` label is untrusted metadata under rev-5.6.

The intake inspected Fejer's 1903 *Untersuchungen uber Fouriersche Reihen*, pages 51-52 and 59-60,
and reports an everywhere-continuous real `2*pi`-periodic function, symmetric real sine/cosine
Fourier partial sums, the `n`-term arithmetic means through `s_(n-1)`, and uniform convergence. That
is a strong source lead, but intake explicitly withheld canonical-statement status pending
independent approval of the catalog-to-source identity, incorporated definitions and proof
boundary, translation, corrections and errata, and the roles of the 1900 note and 1903 article.
The temporary source scan is not preserved in this clone for an independent statement-phase page
and translation review.

The Lean encoding still has proposition-changing bridges. A source-faithful freeze must relate the
real-line periodic carrier to `AddCircle (2 * Real.pi)`, the source sine/cosine coefficient
normalization to mathlib's normalized complex characters, real scalars to complex coefficients and
real-part projection, the source's `n`-term indexing to a zero-based `n + 1` sequence, and uniform
convergence on intervals to the continuous-map topology. Endpoint representatives, ordered
binders, zero and constant functions, the zeroth partial sum, the first mean, and denominator
behavior must also be frozen. None of those bridges is an accepted checked transport.

`StatementCandidate.lean` makes the obstruction concrete. With only
`Mathlib.Analysis.Fourier.AddCircle`, it elaborates a real-valued fixed-`2*pi` candidate, defines
the real part of the symmetric complex Fourier sum, averages `S_0, ..., S_n`, prints the resulting
explicit target, and proves the two initial-index identities. That establishes expressibility, not
source identity. The file is deliberately namespaced `Candidate`; no canonical target, import
minimality, statement fingerprint, checked source transport, or Fejer proof is credited.

Copying `THM-M-0347` would not solve the problem. That distinct target quantifies over arbitrary
positive periods and complex-valued functions. The `THM-M-0291` intake explicitly classifies its
statement, proof, status, and receipts as discovery inputs with no evidence transfer. Using it here
would silently broaden the source-literal real fixed-period theorem.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing canonical expression
fingerprint hard blockers. Without an accepted canonical expression, no import set can be
certified minimal, no alternate encoding can receive credit, and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than passed.
The lifecycle remains `planned`, and the root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates eight adjacent APIs, including the
additive circle, normalized Haar measure, Fourier characters and coefficients, continuous maps,
and uniform convergence. It also checks two strictly different theorems:

- `hasSum_fourier_series_of_summable` assumes summable Fourier coefficients; and
- `Filter.Tendsto.cesaro_smul` assumes the unaveraged sequence already converges.

Neither may replace unrestricted Fejer convergence. The probe output has SHA-256
`5403d9ac...3b16`. The candidate output has SHA-256 `97ec84cc...27f`, and its two boundary lemmas
kernel-check. A bounded search found no Fejer-named pinned terminal theorem outside the distinct
`THM-M-0347` dossier. These are statement-feasibility observations, not the downstream anchor
audit or an absence proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository
root unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0291` | 0 | rank 1297; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| authority, source, intake, toolchain, lockfile, candidate, and pinned-source `sha256sum` commands recorded in `statement-blocker.json` | 0 | all current input fingerprints were captured; historical intake hashes were not rewritten |
| `git blame -L 2090,2095 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake identities recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree agree; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0291/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `5403d9ac...3b16`; no canonical target or proof body |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0291/StatementCandidate.lean` | 0 | fixed-period real candidate, explicit target print, and two initial-index lemmas elaborated; 79 output lines, 4504 bytes, SHA-256 `97ec84cc...27f`; candidate only |
| bounded exact-topic `rg` over repository Lean, pinned mathlib, and both Fejer dossiers | 0 | located the distinct `THM-M-0347` artifacts and adjacent Cesaro APIs; no source-identical root mapping was inferred |
| `python3 -B Stage1_Instances/THM-M-0291/check_intake.py` | 1 | historical intake checker expects its original authoritative intake row, while integration records `[_]` and attempts 1; it was not rewritten or credited as statement evidence |
| prohibited-declaration scan over owned Lean files | 1 expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0291/statement-blocker.json`; scoped Python invariant check | 0 | structured identity, null canonical target/imports, unchanged vector, four undefined mutations, false completion flags, and absent self-test agree |
| scoped `git diff --check`; per-new-file `git diff --no-index --check` | 0 / 1 expected difference | no whitespace diagnostics in the three new owned artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker freezes intake-time authority, the original execution row, and its original
nine-file inventory. Integration later recorded intake worker state `[_]`; these statement
artifacts also extend the owned inventory. This run records that historical boundary instead of
rewriting intake evidence or any state authority to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must refresh and master-accept the intake. Accountable reviewers must then
lawfully preserve and independently inspect one immutable source edition and exact theorem
passage, including incorporated definitions, proof boundary, translation, corrections, errata,
and the 1900/1903 roles. They must approve or kernel-check the real-line/AddCircle,
sine-cosine/complex-character, measure-normalization, character-sign, real-part, index, and
uniform-topology transports and freeze ordered binders and boundary cases.

A later statement worker can then promote only the reviewed expression, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No statement receipt, worker `[_]`,
proof credit, or master acceptance is claimed. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted.
