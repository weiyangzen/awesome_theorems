# Exact-statement gate: blocked

Item: `S56-M-0089-STATEMENT`

Theorem: `THM-M-0089`

Base revision: `cea7a197878ce23e819b006b2780b0bb1702fbbe` (tree
`079dc70c0b48278054700d1b4d45efee14a3bd04`).

## Decision

The statement item remains `[ ]`. The prerequisite `S56-M-0089-INTAKE` is provisional `[_]`, not
master-accepted `[x]`; its receipt is explicitly unaccepted and non-content-addressed. More
strictly, that receipt requires independent source, formal, and representation-theory review before
any dependent statement work. No such review is recorded. Rev-5.6 section 10.2's general permission
to prepare provisional later nodes does not override that target-specific policy. This attempt is
therefore limited to validating and recording the blocker; it adds no statement candidate or other
substantive downstream artifact.

Independently of that dependency state, the exact-statement gate cannot pass. The repository gives
only the Peter-Weyl name and the gloss "completeness of representations of compact groups." The
intake records that this denotes a family, not one proposition. It does not select the 1927 paper's
Parseval-type result, uniform approximation theorem, class-function approximation, or separation
consequences, nor a modern compact-Hausdorff `L2` or regular-representation formulation.

These choices change the theorem's domains, hypotheses, and conclusion. They also change the Lean
objects needed to state it. Selecting a familiar or convenient formulation would broaden or
substitute mathematics absent from the received claim. Rev-5.6 sections 5 and 5.1 make unresolved
statement identity a hard blocker. There is therefore no honest canonical target whose direct
imports can be minimized, no expression or canonical-environment fingerprint to preserve, and no
target against which the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can run. The root vector remains `[H1, M4, R4]`.

## Source Boundary

The catalog supplies no bibliography or proposition. The intake located F. Peter and H. Weyl,
*Die Vollstandigkeit der primitiven Darstellungen einer geschlossenen kontinuierlichen Gruppe*,
*Mathematische Annalen* 97 (1927), 737-755, DOI `10.1007/BF01447892`, and inspected the GDZ scan.
It identifies a Parseval-type `Fundamentalsatz` on page 752, a uniform `Approximationssatz` on page
753, and class-function approximation and separation consequences on page 754. Those pinpoints
confirm the ambiguity; the catalog does not choose one of them.

No lawful immutable source edition with a complete definition, assumption, conclusion, and proof-
boundary map has been admitted. Translation, correction and errata review, the paper's original
matrix/Lie domain versus a modern compact-Hausdorff domain, and independent source review are also
open. The source classification consequently remains `H1`, not `H0`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain. It checks adjacent
`Representation`, `FDRep`, Haar-measure, continuous-to-`Lp` density, and `HilbertBasis` interfaces.
A bounded exact-topic search found no Peter-Weyl or representation matrix-coefficient completeness
declaration in repo-local Lean or pinned mathlib. This is feasibility and discovery evidence only,
not a downstream anchor audit, a proof of global absence, or a canonical statement.

Those APIs do not select or define the intended coefficient family, continuity and unitarity
model, irreducible index, Haar normalization, closure topology, or regular action. The probe's four
direct imports therefore cannot be certified minimal for an absent target. No `Statement.lean`,
statement receipt, expression fingerprint, checked transport, proof body, or proof credit is
emitted.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or other dependency mutation ran.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0089` | 0 | rank 1106; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identifiers appear above |
| exact `sha256sum` command recorded in `statement-blocker.json` | 0 | authority, source, intake, toolchain, dependency lock, and relevant pinned mathlib source hashes were captured |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0089/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `5f9a1809738f808556e51d3e67345f31046d542098544b774649eca4218c2ab7`; no target declaration or proof body |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 (expected no match) | no Peter-Weyl or representation matrix-coefficient completeness target found; bounded discovery only |
| `python3 -B Stage1_Instances/THM-M-0089/check_intake.py` | 1 | historical intake checker expects its frozen authoritative intake state `[ ]` and rejects the integration-updated `[_]`; it was not modified and is not statement evidence |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration found |
| exact JSON parse and inline scoped assertion commands recorded in `statement-blocker.json` | 0 | identity, base, blocked open state, null target/import/hash, unchanged vector, four unrunnable mutations, exact two-file change scope, and absent self-test agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 wrapper result | no whitespace diagnostics; raw no-index commands returned only expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact target did not elaborate |

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
then independently approve one exact Peter-Weyl proposition with every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, translation, correction, erratum, and
boundary case. They must fix the compact-group domain, representation and coefficient model, Haar
normalization, topology and completeness conclusion, irreducible indexing, multiplicities, scalar
and conjugation conventions, and every required transport. Master acceptance of refreshed intake
evidence is also required before an accepted statement transition.

A later statement run can then encode exactly that claim, minimize its pinned imports, serialize
the elaborated expression and environment, compile every credited transport, and execute all four
required mutation classes.

This is the assigned phase's truthful blocker result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
node receipt, worker `[_]`, accepted state, statement fingerprint, or proof credit is claimed.
