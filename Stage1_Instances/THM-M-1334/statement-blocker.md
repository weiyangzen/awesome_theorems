# Exact-statement gate: blocked

Item: `S56-M-1334-STATEMENT`

Theorem: `THM-M-1334`

Base revision: `8bbb7ffdbb5e6e8e3e1ffaba9955137f6b68c76c`

Verdict: `blocked`

## Decision

The exact Lean 4 target cannot be selected or elaborated truthfully from the
accepted repository material. The complete catalogue claim is only
`解析ODE的解析解` ("an analytic solution of an analytic ODE"). It does not fix
one theorem's state space, dimension, scalar field, domain, autonomy,
analyticity predicate, solution carrier, local interval, uniqueness class, or
boundary cases. Each choice changes the proposition rather than merely its
notation.

There is also an unresolved source-identity conflict. The name and year point
toward Sophie von Kowalevsky's 1875 PDE work, while the repository category and
gloss explicitly select an ODE. The intake identifies Kepley and Zhang's modern
ODE Theorems 1 and 11 as a strong candidate, but deliberately marks that
candidate uncredited pending an approved ODE/PDE decision, incorporated
definitions, errata review, and independent source review. Substituting that
candidate now would overrule the intake and invent the missing catalogue-to-
source mapping.

The first failed substantive gate is therefore exact source-statement and
scope identity under rev-5.6 sections 5 and 5.1. The intake dependency is also
only provisional `[_]`: its receipt has `accepted: false`, so master acceptance
would remain dependency-blocked even if the intrinsic ambiguity were resolved.

## Source boundary

`Docs/researches/math_theorems.md:9733-9738` supplies only the name,
Cauchy/Kovalevskaya attribution, year 1875, ODE gloss, importance, and an
untrusted `已验证` label. `Docs/Stage0_Blueprint.md:36291-36316` explicitly
leaves the exact definitions, premises, proof route, equivalent forms, axioms,
and formal artifact open.

The inspected immutable modern lead is Shane Kepley and Tianhao Zhang,
*A constructive proof of the Cauchy-Kovalevskaya theorem for ordinary
differential equations*, arXiv:`1912.03836v3`, PDF SHA-256
`f5edbddab5f7a1da7591a82dca7c5a1038b5ca0fe96e8f326a2c4d3ddf4a9b36`.
Theorem 1 on PDF page 2 states that an analytic autonomous vector field
`f : V -> R^n` on an open `V`, with `x0` in `V`, gives the initial-value
problem `x' = f(x)`, `x(0) = x0` a unique solution analytic on some open
interval containing zero. Theorem 11 on PDF page 20 restates the named result
after the paper's construction. This is a precise candidate, not accepted
authority for the uncited catalogue row.

The historical lead, Sophie von Kowalevsky, *Zur Theorie der partiellen
Differentialgleichung*, Crelle issue 80 (1875), pages 1-32, DOI
`10.1515/crll.1875.80.1`, is a PDE source. Its primary text was not available
to the intake worker and it cannot silently identify this ODE target.

The unresolved proposition-level choices include:

- ODE versus PDE scope and the relationship to the historical namesake;
- autonomous versus time-dependent dynamics and real versus complex scalars;
- positive dimension versus all `n : Nat`, including dimension zero;
- the exact source definition of analytic vector field and its checked map to
  mathlib's `AnalyticOnNhd` or another predicate;
- a partial curve on an interval, a total curve restricted to an interval, or
  a local germ, and the associated derivative predicate;
- open, symmetric, or source-selected local intervals and whether a positive
  radius is explicit;
- uniqueness on one fixed interval, after shrinking two intervals, as a germ,
  or among differentiable versus analytic solutions;
- empty/disconnected domains, trivial vector fields, and other boundary cases.

## Lean boundary

The pinned Lean environment is usable. The existing `IntakeProbe.lean`
successfully elaborates generic `IsIntegralCurveAt`, `AnalyticAt`,
`AnalyticOnNhd`, Picard-Lindelof existence, regularity, and Euclidean-space
interfaces. It is an intake feasibility probe with four imports, not a
canonical target or a minimal-import certificate.

The pinned `Mathlib.Analysis.ODE.PicardLindelof` module proves local existence
and finite/`C-infinity` regularity infrastructure, but its analytic regularity
lemma contains the explicit TODO `Extend to the analytic n = top case`.
Picard-Lindelof without the analytic conclusion would be a weaker substituted
theorem. Conversely, writing a proposition around `AnalyticOnNhd` and
`IsIntegralCurveOn` would still decide the source-to-mathlib analytic
transport, total-function interval encoding, and unequal-domain uniqueness
policy without authority.

Consequently no `Statement.lean`, canonical declaration, minimal target import
set, elaborated expression hash, alternate transport, or removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutation suite is created.
The passing probe receives no statement or proof credit.

## Validation record

Commands ran in this isolated worker clone on 2026-07-13
(`Asia/Shanghai`). The automation-provided canonical `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1334` | 0 | rank 945; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git rev-parse HEAD HEAD^{tree}` | 0 | commit `8bbb7ffdbb5e6e8e3e1ffaba9955137f6b68c76c`; tree `ade61913e5912b1160e25afe096df7f5b3b0cfed` |
| `git status --short --untracked-files=all` before this report | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target `x86_64-unknown-linux-gnu` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` with Lean 4.29.0 |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1334/IntakeProbe.lean` | 0 | hashes `651c8acc...b1d2`, `321626c8...2d81`, and `b0a7645a...bd2` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1334/IntakeProbe.lean)` | 0 | all eight discovery-only API types elaborated and printed |
| bounded exact-name `rg` search in repo-local Lean and pinned mathlib | 1 | expected no-match exit; no Cauchy-Kovalevskaya-named Lean declaration was found in the searched trees; this is not an exhaustive anchor audit |
| `python3 -B Stage1_Instances/THM-M-1334/check_intake.py` | 1 | historical intake invariant fails because it freezes the intake DAG state as `[ ]`, while the current authority projects provisional `[_]`; this statement worker does not rewrite prior intake evidence |
| scoped prohibited-declaration `rg` scan over the target's Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1334/statement-blocker.json` | 0 | finalized structured blocker is valid JSON |
| per-file `git diff --no-index --check /dev/null` for both blocker files | 1 each | expected new-file difference exits with no diagnostic; no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | the ineligible statement self-test manifest is absent |

The historical intake-validator failure is authority drift in a validator that
freezes the earlier intake state; it is not repaired here because doing so
would rewrite another phase's receipt and artifact hashes. The current target
manifest and rev-5.6 standard validators both pass.

## Retry condition

First obtain master acceptance of the intake. Then preserve and hash an
immutable primary source, approve whether the canonical root is the catalogue's
ODE reading or a documented correction, transcribe the exact theorem and all
incorporated definitions, audit errata, and obtain independent approval of the
source crosswalk. Freeze every domain, ordered binder, hypothesis, conclusion,
solution/interval/uniqueness convention, and boundary case.

A fresh statement attempt can then encode that same claim, establish any
needed source-to-Lean transports, minimize its pinned imports, serialize and
hash the elaborated expression and environment, and execute all four mutation
classes. The dossier remains `planned` at `[H1, M4, R3]`; audit and theorem
completion remain false. Because this assigned statement phase did not pass
its completion gate, root `.stage1-worker-selftest.json` is deliberately
absent.
