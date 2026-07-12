# Exact-statement gate: blocked

Item: `S56-M-0642-STATEMENT`

Theorem: `THM-M-0642`

Base revision: `ec27eb0336c89f0aed87200fc7cbf03a09996597` (tree
`3fe77e381bf94ce1ed347bed17c94af25de8d543`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0642-INTAKE` has provisional state `[_]`
in the execution DAG, but its worker receipt is not master accepted. Rev-5.6 section 10.2 permits
this dependency-ordered attempt while acceptance remains pending. Independently, the exact Lean 4
target cannot be truthfully elaborated from the authoritative repository record.

The complete claim-bearing catalog record gives the Nielsen fixed-point family name, Jakob
Nielsen, 1921, and only the gloss "the theory of fixed-point classes." It supplies no cited
proposition or page, incorporated definitions, ordered binders, hypotheses, conclusion, proof
boundary, corrections, or errata. Stage0 explicitly leaves precise definitions and premises open,
and the catalog's verified-status label is untrusted under rev-5.6.

The gloss names a theory rather than selecting one of its materially different claims:

- construction of fixed-point classes by paths and homotopies or by lifts and Reidemeister
  classes;
- an index for each class, essentiality, and the definition or finiteness of the Nielsen number;
- homotopy invariance of the Nielsen number;
- the lower bound on fixed points among maps homotopic to a given map; or
- a surface or other minimum-realization theorem, which may instead belong to neighboring Wecken
  target `THM-M-0643`.

Nor does the record select a space category, dimension or boundary conditions, a self-map and
homotopy category, an index convention, a cardinality representation, quantifier order, or any
degenerate case. These decisions produce different propositions. Choosing a familiar formulation,
narrowing to a convenient finite type or interval, or substituting Wecken, Lefschetz, Brouwer, or
Nielsen-Schreier would invent, narrow, broaden, or replace the received target.

The historical Nielsen papers and Jiang monograph recorded by intake remain discovery leads. No
immutable theorem-level transcription, definition chain, assumption map, proof boundary,
translation, date or edition resolution, correction and errata review, or independent statement
approval has been accepted. Section 5.1 therefore fails at exact source-statement identity before
proof evidence may be inspected.

There is no canonical expression on which to certify minimal imports, serialize an expression and
environment fingerprint, compile alternate transports, or execute removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations. Those tests are undefined, not
passed. The root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports
`Mathlib.Dynamics.FixedPoints.Topology` and `Mathlib.Topology.Homotopy.Basic`. It re-elaborates
eight generic fixed-point, closedness, continuous-map, homotopy, and relative-homotopy interfaces.
It defines neither a Nielsen class nor a target theorem. Its imports are discovery candidates and
cannot be called minimal for an absent canonical target.

A bounded exact-topic search in repo-local Lean and pinned mathlib found no Nielsen fixed-point,
fixed-point-class, Nielsen-number, or Reidemeister-class declaration. A broader search finds the
unrelated Nielsen-Schreier theorem and Reidemeister knot-move prose. This is narrow feasibility
evidence, not the downstream immutable anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` link to canonical
pinned artifacts was used read-only. No update, build, clone, fetch, or dependency mutation was
run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all other commands ran from the repository root unless noted otherwise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0642` | 0 | rank 1059, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` before edits | 0 | only the pre-existing automation `.lake` link was untracked; base revision and tree are recorded above |
| scoped catalog, Stage0, manifest, DAG, blueprint, skill, and intake-dossier inspection | 0 | only a topic gloss is claim-bearing; the canonical statement, binders, hypotheses, conclusion, Lean expression, imports, expression hash, and target environment fingerprint are null |
| SHA-256 over authority, source, intake, toolchain, lockfile, probe, and pinned adjacent mathlib inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; the package worktree is clean |
| `lake env lean ../../Stage1_Instances/THM-M-0642/IntakeProbe.lean` | 0 | all eight adjacent APIs elaborated; no canonical target or proof body was declared; stdout SHA-256 `728b8fb2758e036a7824571cce0947a9866eb5ed101d9c46037ab74ac2f1ee35` |
| bounded exact-topic search in repo-local and pinned-mathlib Lean sources | 1 | expected no-match result; discovery evidence only |
| `python3 -B Stage1_Instances/THM-M-0642/check_intake.py` | 1 | historical intake-only checker expects intake authority state `[ ]`, while current authority records provisional `[_]`; this statement phase does not rewrite intake evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0642/statement-blocker.json` and scoped blocker assertions | 0 | identity, open blocked state, null target/imports, four undefined mutations, unchanged vector, false completion flags, structured probe recipe, and absent self-test agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace and final-newline checks | 0 | both added blocker artifacts passed |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable is blocked |

The intake checker also owns a closed nine-file intake inventory. Adding later phase artifacts makes
that inventory historical; this statement run does not change the intake manifest, receipt,
checker, task DAG, generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must accept the intake dependency through a valid receipt. Accountable
reviewers must preserve and hash one immutable primary or authoritative source, select one exact
proposition with a page or section locator, transcribe every incorporated definition, ordered
binder, hypothesis, conclusion, proof boundary, correction, erratum, translation, and boundary
case, and independently approve the mapping. They must resolve the class/index/invariance/lower-
bound/realization choice and its ownership boundary with Wecken.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
