# THM-M-0938 exact-statement gate: blocked

- Item: `S56-M-0938-STATEMENT`
- Base revision: `d66b6e80968b53d5b99774584721ae8976f303a5`
- Base tree: `aaa82721074fccea81033a9a18d21652af89f8e4`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only Kneser's name, Martin Kneser, the year 1953, and the gloss "the structure
of sumsets over abelian groups." It supplies no bibliography, truth-valued proposition, ambient
group, subset model, invariant, binders, hypotheses, conclusion, boundary policy, correction
history, or independent review. Stage0 explicitly leaves the precise definitions and premises,
proof route, equivalent forms, logical principles, machine status, and artifacts open. The
catalog's `verified` label is untrusted inventory metadata under rev-5.6.

The inspected primary sources make the ambiguity concrete:

1. The date-matched 1953 paper treats lower finite/asymptotic density for sets of rational integers
   and gives a density/periodicity dichotomy.
2. The volume-61 paper treats finite subsets of an arbitrary abelian group. Its Satz 1 gives an
   existential subgroup `H` with `A + B + H = A + B` and
   `|A + B| >= |A| + |B| - |H|`.
3. The 1956 paper treats nonempty integrable subsets of locally compact abelian groups using Haar
   measure and inner measure for a sumset that need not itself be measurable.

These are not alternate spellings of one binder-complete proposition. They change the domain,
subset semantics, invariant, assumptions, conclusion, and required Lean infrastructure. Even the
finite-cardinality family leaves proposition-changing choices between finite ambient groups and
finite subsets of arbitrary groups, empty versus nonempty inputs, an existential period subgroup
and the greatest sumset stabilizer, the weak cardinal bound and a stronger coset-saturated bound,
`Set` and `Finset`, and natural subtraction versus an integer-valued inequality.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake therefore correctly leaves the canonical human
statement, Lean module/expression, minimal imports, expression hash, and canonical-target
environment fingerprint null at `[H1, M4, R4]`. The required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. Selecting the
familiar finite formulation would invent, narrow, broaden, or substitute mathematics.

The prerequisite `S56-M-0938-INTAKE` is only provisional worker state `[_]`. Its receipt declares
`accepted: false`, is neither content-addressed nor signed, supplies no accepted receipt ID, and
leaves the canonical target null. That independently prevents an accepted statement transition.
No `Statement.lean`, assumed theorem, proof body, weakened special case, or broadened package was
introduced.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` directly imports
`Mathlib.Combinatorics.Additive.CauchyDavenport` and
`Mathlib.Combinatorics.Additive.VerySmallDoubling`. A fresh narrow replay elaborated nine adjacent
interfaces: pointwise `Finset.add`, finite cardinality, five `AddAction.stabilizer` interfaces,
`cauchy_davenport_minOrder_add`, and `Finset.vadd_stabilizer_of_no_doubling`.

The probe defines no THM-M-0938 target, checked source transport, or proof body. Its imports are
candidate-interface imports, not a certified minimal import set for an absent canonical target.
A bounded exact-name search over pinned mathlib found one `Kneser` occurrence: a Freiman-Kneser
reference URL in `VerySmallDoubling.lean`. It is not a classical Kneser theorem declaration or
proof. This is discovery evidence only, not the downstream exhaustive anchor or terminal-body
audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was reused read-only. No dependency
update, build, clone, fetch, or other `.lake` mutation was run; the mathlib package worktree was
clean.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless another working directory is shown. Exact arguments and structured results are also in
`statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0938` | 0 | rank 1477; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base identifiers appear above |
| current `sha256sum` over authority, source, intake, toolchain, lockfile, and pinned additive-combinatorics inputs | 0 | hashes agree with the structured blocker |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions agree with the pinned environment above |
| mathlib revision, tree, and status checks | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b`, clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0938/IntakeProbe.lean` | 0 | nine adjacent interfaces elaborated; 1361 output bytes; SHA-256 `97d06690d2cf4d4b43266ca1f6dd79efea0c78ec1a725e605e62ef3cc34f5f7b` |
| bounded `Kneser` search over pinned mathlib Lean | 0 | one reference URL only; 201 output bytes; SHA-256 `0dd08c2d254f6ea23a862907b0be96eca61f029d3437969bfb2a072ea0820305` |
| `python3 -B Stage1_Instances/THM-M-0938/check_intake.py` | 1 | historical intake replay stops at `stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md`; the historical evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-0938/statement-blocker.json` and scoped blocker assertions | 0 | valid JSON; identity, null target/imports, four undefined mutations, unchanged vector, false completion fields, two-file scope, and blocked state agree |
| token-anchored prohibited-declaration scan over owned Lean | 1 (expected no match) | no proof escape or bodyless/unsafe declaration was found |
| scoped tracked and new-file whitespace checks | 0 aggregate | no whitespace diagnostic in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test packet intentionally absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. It binds earlier shared-input hashes, base
revision, and an intake-only artifact inventory. This statement attempt records its exact replay
limitation instead of rewriting the intake dossier or generated authority files to manufacture
agreement. A passing API probe or blocker-structure check is not a statement-node self-test.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
lawfully preserve and hash one complete primary or approved authoritative edition, reconcile the
catalog's 1953 date with the selected proposition, transcribe every incorporated definition,
binder, premise, conclusion, proof boundary, correction, erratum, translation, and degenerate
case, and independently approve the source crosswalk. They must explicitly choose the density,
finite-cardinality, or Haar-measure root and approve every source-to-Lean generalization and
transport.

A fresh statement attempt may then encode exactly that accepted claim, minimize its pinned imports,
serialize the elaborated expression and environment, compile checked alternate transports, and run
all four required mutation classes.

This is a fail-closed statement-blocker report. Lifecycle remains `planned`; the root vector remains
`[H1, M4, R4]`; `audit_complete` and `theorem_complete` remain false. No statement receipt, worker
`[_]`, proof credit, anchor audit, audit completion, theorem completion, or master acceptance is
claimed. Because the assigned exact-statement phase did not pass, `.stage1-worker-selftest.json`
remains absent.
