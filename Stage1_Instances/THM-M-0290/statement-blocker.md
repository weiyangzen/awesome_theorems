# THM-M-0290 exact-statement gate: blocked

Item: `S56-M-0290-STATEMENT`

Base revision: `67d32ab26aba14b674ae8a1b919e6935812190c3` (tree
`8a1d264cf3331992fbbc3a4fffca285af0b88929`).

## Decision

The statement item remains `[ ]`. The catalog supplies only the family name "Carleson-Hunt
theorem" and the gloss that the Fourier series of an `L^p` function converges almost everywhere.
It does not fix the exponent range and endpoints; circle or interval domain and period; real or
complex scalar; Haar, Lebesgue, or Fourier normalization; actual function or `L^p` equivalence
class and representative; partial-sum cutoff; convergence filter and topology; ordered binders; or
boundary cases. These choices change the proposition and cannot be silently filled in by a Lean
file.

The intake identifies Richard A. Hunt's 1968 paper *On the convergence of Fourier series* only as
a primary-work lead. No exact theorem passage, incorporated definition chain, proof boundary,
correction and errata audit, catalog-identity review, or independent approval has been admitted.
Accordingly, `instance.json` deliberately leaves the canonical human claim, Lean expression,
expression fingerprint, and canonical-target environment fingerprint null. Selecting a familiar
modern statement would invent or substitute missing mathematics.

The first failed gate is exact source-statement identity and normalization selection. Without a
canonical expression there is no target-specific minimal-import result, credited alternate
transport, or meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case
mutation. Those four tests are undefined, not passed. The root remains `[H1, M4, R4]`; lifecycle
remains `planned`; `audit_complete` and `theorem_complete` remain false.

The prerequisite intake has provisional `[_]` state in the authoritative execution DAG, not
master-accepted `[x]` state. Its unsigned worker receipt says `accepted: false`, contains no
accepted receipt ID, and deliberately leaves the target null. This permits dependency-ordered
inspection, but independently prevents an accepted statement transition.

## Pinned Lean Boundary

The intake records a strong external discovery candidate at immutable commit
`fpvandoorn/carleson@80e151dff5ddce2426079ec6392616496a4ec927`:

```lean
theorem carleson_hunt {T : Real} [Fact (0 < T)] {f : AddCircle T -> Complex}
    {p : ENNReal} (hp : 1 < p) (hf : MeasureTheory.MemLp f p AddCircle.haarAddCircle) :
    forall_ae x, Filter.Tendsto (partialFourierSum' . f x) Filter.atTop (nhds (f x))
```

Here `partialFourierSum'` is the inclusive symmetric sum over frequencies from `-N` through `N`.
This source is not an installed dependency, targets Lean `4.30.0-rc2` and a different mathlib
revision, and was not imported, built, source-approved, or transitively trust-audited here. It is
therefore anchor-only discovery and cannot select the canonical proposition or receive proof
credit.

Pinned mathlib exposes adjacent interfaces through the existing sole direct probe import,
`Mathlib.Analysis.Fourier.AddCircle`: `AddCircle`, normalized Haar measure, Fourier coefficients,
`MemLp`, `Lp`, `Tendsto`, and `hasSum_fourier_series_L2`. The last theorem is convergence in the
`L^2` space, not almost-everywhere pointwise convergence. `IntakeProbe.lean` re-elaborates all nine
recorded interfaces, but declares no canonical target, transport, wrapper, or proof body. Its
import cannot be certified minimal for a target that has not been selected.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink and pinned
artifacts were used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran on 2026-07-13 in `Asia/Shanghai`; commands without a stated working directory ran at
the worker-clone root.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0290` | 0 | rank 1296; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` and pre-edit `git status --short --untracked-files=all` | 0 | base identity shown above; only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| authority, catalog, Stage0, intake, and immutable external-candidate inspection | 0 | the catalog remains a family gloss; all proposition-changing choices and the primary-source crosswalk remain open; the external declaration remains discovery-only |
| `sha256sum` over authority, source, intake, toolchain, manifest, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` and `rev-parse HEAD 'HEAD^{tree}'` | 0 | clean package status; pinned revision and tree shown above |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0290/IntakeProbe.lean)` | 0 | nine pinned APIs elaborated; stdout was 1,215 bytes with SHA-256 `3473600293b90e19c7ef56a027cc17de93479c69c2a7eb1586d4032070b1de82`; no canonical target or proof declared |
| bounded exact-name `rg` for `carleson_hunt` and `partialFourierSum` in repo-local Lean and pinned mathlib | 1 for declarations | no local declaration found; the only repository match was prose in the intake probe; discovery only |
| `python3 -B Stage1_Instances/THM-M-0290/check_intake.py --master-replay` | 1 | historical intake replay stops at the stale `Docs/Stage1_Blueprint_rev-5.6.md` receipt hash after later integration changed authority inputs; it was recorded rather than rewritten |
| prohibited Lean declaration scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0290/statement-blocker.json`; scoped blocker assertions | 0 | structured blocker parsed; identity, base, open state, null target/imports, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and absent self-test agree |
| scoped `git diff --check` and per-new-file no-index whitespace checks | 0 aggregate | no whitespace diagnostics in either new artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker is frozen to its original authority hashes and nine-file inventory. Integration
subsequently changed the blueprint and DAG cursor. Adding this statement blocker also makes that
intake-only inventory historical. This phase records the limitation instead of rewriting intake
evidence, the task DAG, the generated blueprint, or the authoritative execution DAG.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash one complete primary or authoritative source, select and independently
approve one exact theorem passage, and map every incorporated definition, assumption, conclusion,
proof boundary, correction, and erratum. They must freeze the exponent type and endpoints; domain
and period; scalar field; measure and Fourier normalizations; function or equivalence-class model;
representative semantics; partial-sum convention; convergence filter and topology; ordered binders;
foundation profile; and every exceptional and boundary case.

A later statement run can encode precisely that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This is a truthful first-gate blocker, not completion of the assigned node or any downstream node.
No `Statement.lean`, statement receipt, worker `[_]`, accepted state, statement fingerprint, proof
credit, audit completion, theorem completion, or master acceptance is claimed. Because the assigned
phase did not pass its completion gate, `.stage1-worker-selftest.json` is intentionally absent.
