# Exact-statement gate: blocked

Item: `S56-M-0228-STATEMENT`

Theorem: `THM-M-0228`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0228-INTAKE` is only a provisional
`[_]` projection: its receipt has `accepted=false`, is not content-addressed, and has no accepted
receipt ID. Independently, the intake deliberately leaves the canonical human statement, Lean
module, expression, expression hash, ordered binders, and hypotheses null. The exact target cannot
therefore be elaborated without making proposition-changing choices that the received source does
not settle.

The catalog supplies only the gloss "a nonconstant entire function takes all complex values with
at most one exception." It contains no bibliography, formula, definition chain, binder order,
proof boundary, correction history, or independent review. The inspected Encyclopedia of
Mathematics revision `48178` is a useful secondary statement and points to Picard's 1879 article,
but the intake admits it only as a source lead: the primary theorem and definition passage was not
inspected or preserved, and no definition-chain, errata, translation, or independent review was
accepted.

The unresolved choices include:

- entire as `Differentiable Complex f` versus `AnalyticOnNhd Complex f Set.univ`;
- nonconstant as absence of `Function.const`, pairwise nonconstancy, or a distinct-value witness;
- at most one exception as a subsingleton range complement, `encard <= 1`, pairwise equality of
  omitted values, or an exceptional-value witness that may itself be attained;
- binder order, fixed options, namespaces, and the treatment of surjective functions; and
- which alternate encodings receive checked transports and under which classical principles.

Selecting the familiar candidate
`forall f : Complex -> Complex, Differentiable Complex f -> Nonconstant f ->
((Set.range f)ᶜ).Subsingleton` would choose rather than recover those missing decisions. Demanding an
actually omitted exceptional value would strengthen the surjective case; Big Picard, a multiplicity
claim, or a polynomial/exponential special case would substitute a different theorem.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint
hard blockers. Consequently there is no canonical expression for which import minimality, checked
alternate transports, or the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. Those mutations are undefined, not passed. The root
remains `[H1, M4, R3]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. Its
four direct imports check differentiability, analyticity, range, subsingleton/cardinality,
Liouville, open mapping, first-main-theorem value-distribution infrastructure, and the exponential
sharpness example. It declares no Little Picard target, transport, or proof body. A bounded search
of repo-local Lean and pinned mathlib found no exact Little Picard terminal declaration. The probe
therefore cannot establish a minimal import for a source-selected target that does not yet exist.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only; the pinned mathlib worktree remained clean. No update, build, clone, fetch, or dependency
mutation ran.

## Validation Record

Commands ran in this isolated worker checkout on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0228` | 0 | rank 1240; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit); `git rev-parse HEAD 'HEAD^{tree}'` | 0 each | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| `git blame -L 1647,1652 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 each | pinned mathlib revision and tree above; package status output empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0228/IntakeProbe.lean` | 0 | fourteen adjacent APIs elaborated; complete stdout SHA-256 `0a16d17c238cd28c98a13924b5e7793527138b5c1bdbbebb7f90fea21f241bdf`; no target theorem declared |
| bounded exact-topic `rg` search recorded in `statement-blocker.json` | 0 | only the intake disclaimer and unrelated subsingleton infrastructure matched; no exact pinned Little Picard declaration was found; discovery only |
| `python3 -B Stage1_Instances/THM-M-0228/check_intake.py` before blocker creation | 0 | planned H1/M4/R3 intake, null formal target, hashed intake inventory, and six open tasks agreed in public replay mode |
| the same historical intake checker after blocker creation | 1 | expected artifact-inventory freshness failure because its closed intake-only file set does not include this statement blocker; the intake checker was not broadened or represented as statement validation |
| `python3 -m json.tool Stage1_Instances/THM-M-0228/statement-blocker.json`; scoped invariant query | 0 each | identity, null target and imports, four undefined mutations, unchanged vector, false completion flags, and no-self-test boundary passed |
| prohibited-declaration scan over owned Lean files | 1 | expected no match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace checks recorded in the JSON | 0 / 1 each | no whitespace diagnostics; each no-index exit 1 is only the expected added-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is historical intake replay only. Its pre-edit success confirmed that the formal
target was null. After these required owned statement-blocker artifacts exist, its closed
intake-only inventory fails as designed. Rewriting the prior phase's validator is outside this item
and would not cure the source-identity blocker.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before an accepted statement transition.
Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
transcribe and independently approve its exact theorem and every incorporated definition, ordered
binder, hypothesis, conclusion, proof boundary, translation, correction, erratum, transport, and
boundary case. A later statement worker can then encode only that claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
The root remains `[H1, M4, R3]`; `audit_complete` and `theorem_complete` remain false, and no debt
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json`, node receipt, worker `[_]`, proof credit, or master-acceptance claim
is emitted.
