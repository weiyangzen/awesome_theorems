# Exact-statement gate: blocked

Item: `S56-M-0949-STATEMENT`

Theorem: `THM-M-0949`

Base revision: `f23ca64267b6746e12a641dcc66cc4dbaf1e2191` (tree
`d1872d3251ef6a9c395116467608691849d80496`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0949-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this
dependency-ordered investigation, but the intake receipt declares `accepted: false`, contains no
accepted receipt ID, and requires independent source and formal review before dependent statement
work. Master acceptance remains necessary before a future statement transition can be accepted.

Independently, the exact-statement gate cannot pass. The repository record supplies only the title
"density Hales-Jewett theorem," the 1991 Hales/Jewett/Furstenberg/Katznelson attribution, and the
gloss "existence of a combinatorial line." It omits the density premise and every binder,
hypothesis, definition, conclusion, proof boundary, correction, and boundary convention. Its
`verified` label is untrusted under rev-5.6.

The intake identifies D. H. J. Polymath, *A new proof of the density Hales-Jewett theorem*, Annals
of Mathematics 175 (2012), Theorem 1.4 on page 1285, as an exact published candidate
restatement. That result says that for every positive integer `k` and positive real `delta`, every
sufficiently high-dimensional subset of `[k]^n` having density at least `delta` contains a
nondegenerate combinatorial line. It is not an accepted canonical root: the repository does not
cite or adopt it, the original Furstenberg-Katznelson 1991 source and correction history have not
been fully audited, and no independent reviewer has approved the source-to-statement crosswalk.

The proposition-changing Lean choices are also explicitly open: `Fin k` versus an arbitrary
finite alphabet; `Fin n -> Fin k` and the natural threshold convention; `Finset` versus finite
`Set`; real cardinal density versus a checked cast of `Finset.dens`; line containment and proper
wildcard semantics; binder order; and the cases `k = 0`, `k = 1`, `delta <= 0`, `delta > 1`,
`n = 0`, empty subsets, threshold equality, and singleton-alphabet lines. Promoting the existing
`CandidateTargetShape` would contradict its discovery-only contract and manufacture source
acceptance.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical expression for which a minimal import set, checked alternate
transport, or the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. All four mutation classes are undefined, not passed.
No `Statement.lean`, proof body, weakened special case, broadened interface, or circular assumption
was added. The root remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain. Its three direct imports
expose the line representation, ordinary coloring Hales-Jewett theorem, finite-set density, and a
source-shaped proposition-valued definition. All checks pass. The ordinary theorem has no density
premise, and the candidate shape is neither canonical nor proved. These imports therefore cannot
be certified minimal for an absent accepted target.

A bounded exact-topic search over pinned mathlib and repository-local Lean found no density
Hales-Jewett or `DHJ` declaration. This is discovery-only evidence, not the downstream immutable
anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0949` | 0 | rank 1010; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, guidelines, and intake inspection | 0 | confirmed the sparse catalog claim, candidate source, explicit null canonical target, and open source/encoding decisions |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0949/check_intake.py` | 1 | historical intake replay rejects the current regenerated blueprint hash; the intake receipt is provisional and stale after integration, so this statement run records rather than rewrites it |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0949/IntakeProbe.lean` | 0 | seven adjacent APIs and the candidate proposition shape elaborated; stdout SHA-256 `aec890922f9787194b647e55861b8daf878e883e8eb480d1bbc92d2bcb808c2e`; no canonical target or proof body |
| bounded search for density Hales-Jewett or `DHJ` in pinned mathlib and repo-local Lean | 1 | expected no-match result; discovery-only evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash a lawful immutable source edition, inspect the original-proof and correction
history, adopt and independently approve one exact proposition, and map every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, and boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
