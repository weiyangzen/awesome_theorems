# Exact-statement gate: blocked

Item: `S56-M-0211-STATEMENT`

Theorem: `THM-M-0211`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0211-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; the intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered attempt, but the statement node cannot be accepted before its prerequisite.

Independently, the exact-statement gate fails. The repository supplies only the title `帕斯卡定理`
(Pascal's theorem), its 1640 attribution, and the gloss `圆锥曲线内接六边形的共线性质`: the
collinearity property of a hexagon inscribed in a conic. It supplies no bibliography, projective
model, field, conic definition, ordered binders, hypotheses, exact conclusion, proof boundary,
correction history, or boundary convention. Its `已验证` label is untrusted metadata.

The two versioned modern source leads preserved by intake confirm that these omissions change the
proposition:

- Caminata and Schaffler, arXiv `1903.00460v2`, state that six points `a,...,f` in `P^2` on a
  conic imply that `ab ∩ de`, `af ∩ dc`, and `ef ∩ bc` are aligned. They then explicitly use
  "Pascal's Theorem" for both that implication and the Braikenridge-Maclaurin converse, allowing a
  possibly degenerate conic.
- Wiese, arXiv `2408.00020v1`, Theorem 1, works in the real projective plane. It permits repeated
  vertices by interpreting repeated adjacent points as tangents, provided each paired pair of
  opposite lines is not identical.

The catalog cites neither source and selects neither convention. An exact proposition must still
freeze:

- a synthetic projective plane, `P(K^3)`, or another model, together with the scalar field and
  characteristic hypotheses;
- a smooth irreducible conic, a possibly reducible quadratic zero locus, or another exact conic
  representation;
- the cyclic order and distinctness of the six vertices, plus any general-position hypotheses;
- whether repeated vertices are excluded or create tangent sides, and how tangents are defined;
- the exact opposite-side pairs and the hypotheses under which each intersection is well-defined;
- projective collinearity as dependence, containment in a line, or a determinant equation, with
  checked transports for any alternate encoding;
- forward Pascal only, the converse, or an equivalence; and
- affine parallel cases, coincident sides, repeated intersections, reducible conics,
  characteristic two, and every other degenerate boundary.

Choosing the real tangent-inclusive theorem, a distinct-point theorem over an arbitrary field, a
smooth-conic theorem, or the forward-and-converse equivalence would invent, narrow, broaden, or
substitute mathematics rather than elaborate the exact received target. Rev-5.6 sections 5 and 5.1
make this ambiguity and the missing elaborated-expression fingerprint hard blockers.

Consequently there is no honest canonical declaration whose imports can be certified minimal. No
`Statement.lean`, exact expression, checked transport, or mutation suite was created. The required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. The provisional vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with these four pinned imports:

```lean
import Mathlib.LinearAlgebra.Projectivization.Constructions
import Mathlib.LinearAlgebra.Projectivization.Subspace
import Mathlib.LinearAlgebra.QuadraticForm.Basic
import Mathlib.LinearAlgebra.AffineSpace.FiniteDimensional
```

All ten adjacent APIs pass. This is real environment evidence, but not target elaboration.
`Projectivization.cross` deliberately totalizes the equal-point case as `cross v v = v`, so
distinctness and line-intersection hypotheses are semantic requirements, not optional polish.
Pinned `Projectivization.Independence` defines dependence, but its own future-work list says that
projective collinearity remains to be defined. The checked affine `Collinear` predicate is a
different model. The probe therefore defines no source-selected conic, projective collinearity
predicate, canonical target, transport, or proof body, and its imports cannot be certified minimal
for the absent target.

A bounded exact-topic search found no Pascal-theorem, mystic-hexagon, conic-hexagon, or Pascal-line
Lean declaration in pinned mathlib or repository-local Lean outside this dossier. The two broad
mathlib `Pascal` hits concern Pascal's triangle. This is discovery-only feasibility evidence, not
the downstream immutable anchor audit or a global absence claim.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0211` | 0 | rank 1227; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| repository source, Stage0, intake dossier, and the two preserved versioned source PDFs | 0 | confirmed the sparse gloss, null canonical target, and material field, degeneracy, tangent, and converse differences |
| `sha256sum` over authorities, intake artifacts, toolchain, dependency lock, imported mathlib sources, and source PDFs | 0 | exact digests are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0211/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout was 1,407 bytes with SHA-256 `e4d504be5e973b226c4b71516643646ad92f03b8b395e9e91fec7b4883228c49`; no target or proof body |
| bounded exact-topic `rg` search over pinned mathlib and repository-local Lean | 1 (expected no match) | no target-specific declaration matched; broad Pascal hits were Pascal's triangle only |
| `python3 -B Stage1_Instances/THM-M-0211/check_intake.py` | 1 | the historical checker expects its original authoritative intake row `[ ]` with zero attempts, while the current DAG records provisional `[_]` with one attempt; this worker did not rewrite intake evidence |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0211/statement-blocker.json` and scoped blocker-invariant validation | 0 | identity, base, null target, unchanged vector, four undefined mutations, false completion fields, exact changed paths, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. Its expected authoritative row predates the
integration lane's provisional DAG update, and it freezes the intake-only artifact inventory. This
statement worker records that exact limitation rather than rewriting the intake receipt, checker,
instance, target task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before a future statement can be
accepted. Accountable reviewers must preserve and hash one lawful immutable primary or
authoritative source, select and independently approve one exact proposition and proof boundary,
and transcribe every incorporated definition, ordered binder, hypothesis, conclusion, correction,
erratum, side pairing, and boundary case. The decision must resolve the projective model, field,
conic and degeneracy policy, repeated-point tangents, intersection contracts, collinearity
encoding, and converse boundary without silently changing the catalog claim.

A fresh statement attempt can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
