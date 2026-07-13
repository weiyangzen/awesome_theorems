# Exact-statement gate: blocked

Item: `S56-M-0293-STATEMENT`

Theorem: `THM-M-0293` (Hurwitz theorem, Fourier absolute-convergence family)

Base revision: `27400857bccc93638c97e9c65859ddf5d5b5f4da` (tree
`3762537e0e5ae46cd70b086da49a69e2fd7b275c`).

## Decision

The statement item remains `[ ]`. The repository supplies only the name `赫维茨定理`, Adolf
Hurwitz, the year 1903, and the gloss `傅里叶级数的绝对收敛` (absolute convergence of Fourier
series). It gives no theorem locator, formula, definition chain, ordered binders, hypotheses,
conclusion, proof boundary, corrections, or reviewer. Stage0 repeats the gloss while explicitly
leaving the precise definitions, premises, formal system, equivalent forms, axioms, machine status,
and artifacts open. The catalog's `已验证` label is untrusted metadata under rev-5.6.

The intake identified and inspected Hurwitz's 1903 paper *Uber die Fourierschen Konstanten
integrierbarer Funktionen*, but it found several non-equivalent possible roots:

- page 436, after equation (27), states absolute convergence of a separated bilinear
  Fourier-coefficient product series;
- pages 438-440, Satz VI and VII, give an absolutely convergent trigonometric expansion of an
  indefinite integral and a termwise-differentiation bridge;
- pages 429-436 and 441-442 contain neighboring Parseval and uniqueness results; and
- pages 442-446, Satz IX, give the distinct Sturm-Hurwitz sign-change theorem.

The catalog does not select among these results. In particular, the paper does not state the blanket
claim that every integrable function's own Fourier series is absolutely convergent. Selecting the
coefficient-product claim, the indefinite-integral expansion, a later regularity criterion, or the
Sturm-Hurwitz theorem would change or correct the target rather than merely choose notation.

Even after selecting a passage, the statement must fix the real interval, periodic-function, or
`AddCircle` carrier; Riemann versus Lebesgue integrability; real sine/cosine pairs versus complex
integer-indexed coefficients; coefficient and measure normalization; endpoint and additive-constant
conventions; and whether absolute convergence means coefficient-norm summability, pointwise or
uniform absolute convergence, or absolute convergence of a bilinear product series. None of those
source-to-Lean transports has independent approval.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. There is no honest canonical expression whose imports can be certified minimal, no
alternate encoding that can receive checked credit, and no canonical target for the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those tests
are undefined, not passed. The lifecycle remains `planned`, and the vector remains `[H1, M3, R4]`.

The prerequisite intake has authoritative provisional state `[_]`, not master-accepted `[x]`. Its
receipt is unsigned, unaccepted, and non-content-addressed, and its historical checker is now stale
against the integrated execution DAG. This topologically ordered inspection does not rewrite that
evidence or manufacture dependency acceptance.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` re-elaborates with the sole direct import
`Mathlib.Analysis.Fourier.AddCircle`. It checks `AddCircle`, normalized Haar measure, Fourier
characters and coefficients, Parseval/L2 interfaces, and two summability-to-convergence interfaces.
It also checks that `fourierCoeff` specializes to period `2 * Real.pi`.

The probe's important boundary is negative: `hasSum_fourier_series_of_summable` assumes
`Summable (fourierCoeff f)` and concludes uniform convergence. It does not derive absolute
summability from source-selected Hurwitz hypotheses. Its 15 stdout lines (1427 bytes) have SHA-256
`e803388b7b79edd4efc8bb2cdbcfc9a5489cdb8c5584c74b63b2ae4afc2a0478`; stderr is empty. The two
printed candidate axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`.

A bounded search over repo-local Lean, this target, and pinned mathlib Fourier modules found adjacent
coefficient-summability interfaces and an unrelated Hurwitz-zeta string, but no source-approved
`THM-M-0293` target identity. This is discovery evidence, not the downstream anchor audit or an
absence proof. The probe declares no target, checked transport, or proof body, and its import cannot
be certified minimal for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No `lake update`, `lake build`, clone,
fetch, or other dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository
root unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0293` | 0 | rank 1543; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| `git blame -L 2104,2109 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake identities recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'`; `git status --short --untracked-files=all` | 0 | pinned revision and tree agree; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0293/IntakeProbe.lean` | 0 | eight adjacent APIs, period specialization, and two axiom reports elaborated; stdout SHA-256 `e803388b...0478`; no canonical target or proof body |
| bounded exact-topic `rg` over repo-local Lean, the owned target, and pinned mathlib Fourier modules | 0 | 8 lines, 1256 bytes, SHA-256 `e6e49978...c4e`; adjacent interfaces only; no root identity inferred |
| `python3 -B Stage1_Instances/THM-M-0293/check_intake.py --skip-probe-replay` | 1 | historical intake checker stops at its intake-time execution-DAG target-entry digest after integration recorded intake `[_]`; prior intake evidence was not rewritten |
| prohibited-declaration scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| final JSON parse, scoped blocker assertions, text-hygiene and scoped whitespace checks | 0 | identity, blocked state, unchanged vector, null target/imports, four undefined mutations, false completion and receipt fields, and exact two-file scope agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest is absent because the exact-statement deliverable did not pass |

The machine-readable blocker records exact commands, hashes, null target fields, four undefined
mutation classes, unchanged debt vector, and the no-self-test boundary.

## Retry Condition And Status Boundary

The integration lane must refresh and master-accept the intake. Accountable reviewers must lawfully
preserve and independently inspect one immutable primary or approved authoritative source, select
the page 436 product-series claim, the pages 438-440 indefinite-integral expansion, another exact
passage, or a corrected target, and approve its transcription, translation, incorporated
definitions, ordered binders, hypotheses, conclusion, proof boundary, corrections, errata, and
absolute-convergence semantics.

A later statement worker can then encode only that reviewed claim, compile every required
historical-to-modern and real-to-complex transport, minimize its pinned imports, serialize and hash
the elaborated expression and environment, and run all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. No statement receipt, worker `[_]`, proof credit, or master acceptance is claimed. Because
the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json` is emitted.
