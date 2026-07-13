# Exact-statement gate: blocked

Item: `S56-M-0199-STATEMENT`

Theorem: `THM-M-0199`

Base revision: `27400857bccc93638c97e9c65859ddf5d5b5f4da` (tree
`3762537e0e5ae46cd70b086da49a69e2fd7b275c`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0199-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt is explicitly unaccepted and contains no
accepted receipt ID. Rev-5.6 section 10.2 permits this dependency-ordered statement attempt, but
master closure remains dependency ordered.

Independently, the exact-statement gate fails before Lean target elaboration. The repository gives
only the title `梅涅劳斯定理` (Menelaus's theorem) and the gloss `共线点的比例关系` ("the ratio
relation of collinear points"). It supplies no bibliography, exact formula, definitions, ordered
binders, hypotheses, direction, proof boundary, correction history, or boundary convention. Its
`已验证` label is untrusted metadata.

The intake's inspected modern lead, McConnell's *A Six-Point Ceva-Menelaus Theorem*, confirms a
familiar variant but does not resolve the catalog ambiguity. On printed pages 1-2, Theorem 2 puts
`D`, `E`, and `F` on the extended side lines opposite `A`, `B`, and `C`, defines signed ratios
`d = BD/DC`, `e = CE/EA`, and `f = AF/FB` using orientations along `AB`, `BC`, and `CA`, and states
that the three points are collinear if and only if `d * e * f = -1`. Its footnote also assigns
values to zero denominators and points at infinity. The catalog does not cite or select this
secondary source, it has not received independent approval for the root, and the retrieved PDF's
server `v1` name disagrees with its 2018 printed date. The dossier therefore binds only the
inspected bytes by SHA-256
`ba8ff135a0bb270547f94e3344b59b35de8c107265638f95537812c0e36a3b77`.

An exact proposition must still freeze:

- the ordered nondegenerate triangle, ambient affine or projective space, scalar domain,
  characteristic, universes, and typeclass context;
- the correspondence between `D`, `E`, `F` and `BC`, `CA`, `AB`, including whether points range
  over complete affine lines, segments, or a projective completion;
- finite directed ratios versus the source lead's zero, infinite, and ideal-point conventions;
- the orientation, numerator/denominator order, product order, displayed sign, and all denominator
  conditions;
- collinearity implying the ratio identity, the converse, or the full equivalence; and
- repeated or collinear triangle vertices, side points equal to vertices, coincident side points,
  a transversal equal to a side, points beyond segments, and characteristic-two behavior.

Silently choosing the finite coordinate proposition from the discovered `lean-genius` file would
not solve this gate. That candidate specializes to `Real x Real`, assumes three affine parameters
are not one and the base determinant is nonzero, and omits the source lead's ideal-point semantics.
It is neither a pinned repository dependency nor an independently approved transport from the
catalog claim. Conversely, adding projective points or the source lead's extended arithmetic would
broaden the finite candidate. Selecting either one here would invent, narrow, or broaden the
received theorem rather than elaborate its exact target.

Consequently there is no honest canonical declaration whose imports can be certified minimal. No
`Statement.lean`, canonical expression, checked alternate transport, expression fingerprint, or
mutation suite was created. The mandated removed-hypothesis, changed-domain, changed-binder-scope,
and boundary-case mutations are undefined rather than passed. The provisional `[H1, M4, R4]`
classification remains unchanged.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment. Its direct imports
expose affine triangles, line interpolation, line membership, collinearity, and a neighboring Ceva
theorem. All eleven interface checks pass. Ceva concerns concurrence of vertex lines, not
collinearity of side-line points, and is explicitly not a substitute for Menelaus. The probe
declares no target, transport, or proof body; its imports cannot be certified minimal for the
absent canonical target and receive no statement or proof credit.

A bounded name search over repository-local Lean and pinned mathlib found no Menelaus-named
declaration. The external coordinate candidate remains discovery evidence only. These observations
are not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused without running an update, build, clone, fetch, or
other dependency-mutation command. The pinned mathlib Git worktree was clean after validation.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0199` | 0 | rank 1531; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before edits | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base revision and tree appear above |
| scoped inspection and SHA-256 over authority, source, intake, probe, toolchain, lock, and imported mathlib sources | 0 | the current inputs and the intake receipt's older frozen inputs are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree match the values above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0199/IntakeProbe.lean` | 0 | eleven adjacent APIs elaborated; stdout was 2,714 bytes with SHA-256 `eae1118a6a36635eb8081636cae497bf279922ef628e34b2ecadfef89fd267a2`; no target declaration or proof body |
| bounded `rg` search in pinned mathlib and repository-local Lean | 1 (expected no match) | no Menelaus-named target declaration matched the recorded terms |
| `python3 -B Stage1_Instances/THM-M-0199/check_intake.py` | 1 | historical intake replay stops at its frozen base revision (`5fe11f4b...`) rather than current HEAD (`27400857...`); its captured authority hashes and intake-only artifact inventory also predate this phase |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0199/statement-blocker.json` and scoped blocker assertions | 0 | identity, base, null target, unchanged vector, four undefined mutations, false completion fields, exact changed paths, and absent self-test agree |
| scoped `git diff --check` plus new-file no-index whitespace checks | 0 aggregate | no whitespace diagnostics; no-index exit 1 values were only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker validates a historical provisional receipt. Its receipt binds an earlier base,
earlier blueprint and execution-DAG hashes, and the original intake-only file inventory. This
statement worker did not rewrite the intake receipt, checker, instance, target task DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before it can accept a statement
transition. Accountable reviewers must preserve and hash one lawful immutable primary or
authoritative source, select and independently approve one exact proposition and proof boundary,
and transcribe every incorporated definition, ordered binder, hypothesis, conclusion, correction,
erratum, and boundary case. The decision must reconcile finite affine ratios with any zero,
infinite, or projective-point convention and fix the ratio orientations and theorem direction.

A fresh statement attempt can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
