# THM-M-1383 statement-phase blocker

- Item: `S56-M-1383-STATEMENT`
- Base revision: `d3cbfa8941a8bcaafa3b8a690d1333f9643288ad`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the frozen intake boundary. The repository catalog supplies only the topic
label "boundary-value problems," a collective twentieth-century attribution, and the gloss "the
theory of two-point boundary-value problems." It gives no cited proposition, formula, ordered
binders, hypotheses, conclusion, proof boundary, or correction history. Stage0 likewise leaves the
target formal system, exact definitions and premises, proof route, alternate forms, axioms, and
machine artifact open. The catalog's verified label is explicitly untrusted under rev-5.6.

A two-point boundary-value problem is a class of inputs, not a truth-valued theorem. An exact claim
would have to select at least:

- an independent-variable interval and endpoint convention, including endpoint order;
- a scalar or state space, differential equation or operator, coefficients, forcing, parameters,
  and regularity;
- a classical, weak, integral, Sobolev, or another source-defined solution concept;
- separated or coupled boundary operators and homogeneous or inhomogeneous endpoint data;
- existence, uniqueness, nonexistence, multiplicity, solvability, representation, estimates,
  spectral structure, or numerical convergence as the conclusion; and
- compatibility, nonresonance, compactness, Lipschitz, coercivity, sign, and degeneracy conditions
  appropriate to that conclusion.

Those choices produce inequivalent propositions. In particular, universal existence or uniqueness
is false without substantial assumptions. Selecting a familiar theorem would invent or substitute
mathematics rather than elaborate the exact received target.

The Teschl textbook section recorded by intake was admitted only as a source-family discriminator.
It moves from one fixed-endpoint wave equation to a Sturm-Liouville eigenvalue problem and then
separates multiple conclusions. The catalog does not cite this book or select one of those results.
The neighboring records `THM-M-1384` through `THM-M-1394` separately own Sturm-Liouville,
comparison, separation, oscillation, eigenvalue, asymptotic, variational, Green-function, Fredholm,
and shooting-method topics. None can be imported as this root without an approved target correction.

The authoritative intake task is provisional `[_]`. Its worker receipt is unsigned, has
`accepted: false`, and contains no accepted receipt ID. A dependency-ordered attempt is permitted,
but no accepted statement transition can precede master acceptance. Independently, intake freezes
the canonical statement, binders, formal module, declaration or expression, expression hash, and
environment fingerprint as absent at `[H5, M4, R4]`. Exact source-statement identity is therefore
the first substantive statement gate failure.

Consequently there is no canonical expression to elaborate and no honest minimal-import set.
Checked transports and the removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutation classes are not runnable before a canonical proposition exists. The root vector remains
`[H5, M4, R4]`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated against the pinned environment. Its three direct
imports expose interval, integral-curve, Picard-Lindelof local initial-value existence, and
Gronwall initial-value uniqueness APIs. All six checks passed. The probe defines no differential
equation, second-endpoint condition, boundary operator, solution predicate, canonical target, or
proof body. Initial-value existence or uniqueness does not imply that a prescribed second endpoint
can be attained. The probe's imports therefore cannot be certified minimal for an unidentified
target and receive no statement or proof credit.

A bounded search found no two-point boundary-value occurrence in pinned mathlib or the repo-local
Lean modules. Generic repo-local boundary-value hits concerned unrelated topology, PDE, conformal,
obstacle, and complex-analysis material. These are discovery observations, not an exhaustive anchor
audit or a global absence claim.

The environment was Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink and canonical
pinned artifacts were used read-only. No `lake update`, `lake build`, dependency clone or fetch, or
other `.lake` mutation was run.

## Commands and exact results

Commands ran in this worker clone unless a working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups, `41` legacy rows, `300` legacy slots, and `1546` uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets, ranks `1..1546`, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1383` | 0 | rank `993`; `planned`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `d3cbfa8941a8bcaafa3b8a690d1333f9643288ad`; tree `e912a107150c6f9c3fc096901412fce0337c7c01` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; mathlib worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1383/IntakeProbe.lean` | 0 | all six adjacent APIs elaborated; stdout SHA-256 `0016ea42d29bd81f5f8355ac238bcdd0e5426ee3cd4d424907c6308d7da03f5e`; no target declaration or proof body |
| bounded two-point boundary-value `rg` over pinned mathlib, repo-local Lean, and the owned intake probe | 0 | only the intake probe's disclaimer matched; no formal target occurrence |
| bounded generic boundary-value `rg` over pinned mathlib | 1 | expected no-match result; bounded discovery only |
| bounded generic boundary-value `rg` over repo-local Lean | 0 | unrelated topology, PDE, conformal, obstacle, and complex-analysis hits only; none credited |
| `python3 -B Stage1_Instances/THM-M-1383/check_intake.py` (pre-edit) | 0 | frozen intake invariants passed at `planned`, `H5/M4/R4`, with six open tasks |
| `python3 -m json.tool Stage1_Instances/THM-M-1383/statement-blocker.json` | 0 | blocker is valid JSON |
| scoped Python blocker-invariant check | 0 | identity, base, null target fields, unchanged debt vector, false completion fields, four unrunnable mutations, owned paths, and absent self-test agree |
| prohibited declaration scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace checks | 0 | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent as required for a blocked phase |

The intake checker intentionally freezes the intake-only inventory. After these statement-blocker
artifacts are added, it is historical intake evidence rather than the statement validator and is
not rewritten to accept a later phase's files.

## Unblocking condition

An accountable source owner must preserve and hash one lawful complete source edition, select and
independently approve one exact proposition and proof boundary as the `THM-M-1383` root, audit its
corrections, and resolve ownership relative to the neighboring targets. Every incorporated
definition, ordered binder, hypothesis, conclusion, endpoint convention, and boundary case must
then be frozen. A later statement run can encode that same claim, establish minimal pinned imports,
serialize its elaborated expression and environment, check each credited alternate encoding, and
run all four mutation classes.

Until those prerequisites hold, no exact statement, proof, audit completion, or theorem completion
is claimed. Because the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
