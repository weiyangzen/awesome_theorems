# Exact-statement gate: blocked

Item: `S56-M-0027-STATEMENT`

Theorem: `THM-M-0027` (Wedderburn-Artin theorem)

Base revision: `dc2eb1390c8f2a88e7afcbdbd35f92ab43f64fb8` (tree
`25138aaafcff80ee47bf04805bccd804978e6754`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0027-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 permits
this dependency-ordered inspection, but the intake receipt is non-content-addressed, declares
`accepted: false`, and has no accepted receipt ID. Master acceptance remains necessary before any
future statement transition can be accepted.

Independently, the exact-statement gate cannot pass from the received claim. The repository gives
only the title "Wedderburn-Artin theorem" and the gloss "the structure theorem for semisimple
rings." It gives no source proposition, definitions, ordered binders, hypotheses, conclusion,
proof boundary, correction history, or boundary-case convention. In particular, it does not say
whether the root is:

- the forward decomposition of a semisimple ring into a finite product of full matrix rings over
  division rings;
- an existence biconditional characterizing semisimple rings;
- a uniqueness-enhanced classification of the factors and matrix sizes;
- the endomorphism-ring-opposite presentation of the factors; or
- a simple Artinian, algebra, finite-dimensional, or central-simple-algebra specialization.

Those readings are materially different. Ring identity and zero-ring conventions, left or right
semisimplicity, the factor universes, positive matrix sizes, the empty product, and uniqueness up to
permutation and division-ring isomorphism are also unstated. The intake's Wedderburn 1908 and Artin
1927 references are bibliographic discovery leads only: no immutable pinpoint passage,
incorporated-definition map, premise map, chronology and errata disposition, or independent source
review has been accepted. The separately owned `THM-M-0036` central-simple-algebra classification
also lacks an accepted identity or overlap decision with this target.

Selecting the familiar forward theorem, the iff theorem, or a uniqueness form from convention
would therefore invent, narrow, broaden, or substitute mathematics rather than elaborate the exact
received target. Sections 5 and 5.1 of the rev-5.6 blueprint make this ambiguity and the missing
expression fingerprint hard blockers. There is no canonical expression whose imports can honestly
be certified minimal, no credited alternate encoding to transport, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. Those four
tests are undefined rather than passed. The vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

Pinned mathlib does contain strong members of the theorem family in
`Mathlib.RingTheory.SimpleModule.WedderburnArtin`. The existing `IntakeProbe.lean` re-elaborated
five adjacent declarations:

- `IsSemisimpleRing.exists_ringEquiv_pi_matrix_divisionRing` is the forward form. It requires
  `[Ring R]` and `[IsSemisimpleRing R]`, explicitly requires `NeZero (d i)` for every matrix size,
  and returns a finite-product ring equivalence.
- `isSemisimpleRing_iff_pi_matrix_divisionRing` is an iff form. Its existential encoding does not
  explicitly require `NeZero (d i)`, so it is not expression-identical to the forward result with
  its positivity data.
- The probe also checks the endomorphism-opposite presentation, a simple Artinian single-factor
  form, and a finite algebra form.

The forward and iff axiom reports are both `[propext, Classical.choice, Quot.sound]`. This is real
API and environment validation, but no candidate is identified with the underspecified source
claim. The probe's direct import therefore cannot be certified minimal for an absent canonical
target and receives no statement or proof credit. The foreign `THM-M-0424` wrapper in
`AwesomeTheorems.Stage1.S1_M_078` covers only a finite-dimensional central simple algebra and
cannot replace this general semisimple-ring target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
was used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0027` | 0 | rank 1072; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `sha256sum` over authority, intake, toolchain, and pinned candidate inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned mathlib package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0027/IntakeProbe.lean` | 0 | five adjacent theorem-family declarations elaborated; stdout was 1554 bytes with SHA-256 `61abf61463ec3fc8cdd7ffc97c425b085e7fa4323c68f2d4ffc60522cc6e7596`; no canonical target or proof body was declared |
| bounded Wedderburn-Artin name search in pinned mathlib and repo-local Lean | 0 | located the family module, algebraically closed specialization, and foreign central-simple-algebra wrapper; discovery evidence only |
| `python3 -B Stage1_Instances/THM-M-0027/check_intake.py` | 1 | historical intake replay stops at its stale assertion for authoritative intake state `[ ]` and attempts 0; current authority records `[_]` and attempts 1 |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | blocker identity, null target/import/hash, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0027` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0027/statement-blocker.json` and the corresponding command for `statement-blocker.md` | 1 each | expected new-file differences with empty diagnostic output; no whitespace error |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes the original execution-DAG state and intake-only file
inventory. This statement phase records its stale replay rather than rewriting `check_intake.py`,
the intake receipt, the instance record, the target-local task DAG, the generated blueprint, or the
authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

Accountable source reviewers must preserve and hash a lawful immutable primary or authoritative
source, select and independently approve one exact proposition, transcribe all incorporated
definitions, ordered binders, assumptions, conclusion, proof boundary, corrections, and boundary
cases, and issue a `THM-M-0036` identity and overlap decision. A fresh statement worker can then
encode precisely that claim, minimize pinned imports, serialize and hash the elaborated expression
and environment, compile every credited transport, and execute all four required mutation classes.
The integration lane must also revalidate and master-accept the intake dependency before accepting
that later statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
