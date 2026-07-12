# Exact-statement gate: blocked

Item: `S56-M-0637-STATEMENT`

Theorem: `THM-M-0637`

Base revision: `dc2eb1390c8f2a88e7afcbdbd35f92ab43f64fb8` (tree
`25138aaafcff80ee47bf04805bccd804978e6754`).

## Decision

The exact Lean 4 target cannot yet be truthfully adopted from the accepted inputs. The statement
item remains `[ ]`. Its prerequisite intake has provisional worker state `[_]`, not
master-accepted state `[x]`; its receipt declares `accepted: false`, is not content-addressed, and
contains no accepted receipt ID. The intake deliberately leaves the canonical mathematical claim,
ordered binders, Lean expression, minimal imports, expression fingerprint, and target-environment
fingerprint open. Dependency-ordered inspection is permitted, but it cannot create an accepted
statement transition.

The repository supplies only the title Schauder fixed-point theorem, Juliusz Schauder, 1930, and
the gloss "a fixed point of a compact map on a Banach space." The intake inspected Satz II on
printed page 175 of J. Schauder, "Der Fixpunktsatz in Funktionalraeumen," *Studia Mathematica*
**2**(1) (1930), 171-180, DOI `10.4064/sm-2-1-171-180`. It identifies the candidate family: in a
`B`-space, a continuous operation maps a closed convex set `H` into itself and has compact image
`F(H)`, hence has a fixed point. But the intake expressly withholds exact adoption until a lawful
immutable source copy, incorporated definitions and conventions, proof boundary, translation,
corrections and errata, and independent review are accepted.

Material proposition choices therefore remain. The printed wording has no explicit nonemptiness
premise, while the empty-domain reading would be false; the source convention that excludes it has
not been accepted. An ambient map continuous only on `H`, a globally continuous ambient map, and a
continuous subtype self-map are not identical encodings without checked relationships. Compactness
of the literal image, compactness of its closure, and the modern condition that all bounded images
are relatively compact are also distinct. Choosing among them without an accepted source decision
would invent or substitute mathematics.

There is also an unresolved ownership collision. `THM-M-0318` separately owns the compact-domain
Schauder formulation, closer to Satz I. Its elaborated candidate assumes a nonempty compact convex
domain in an arbitrary real normed space; the present record points to a complete normed space, a
closed convex domain that need not be compact, and compactness of the particular image. No accepted
alias, distinct-root, deduplication, checked target transport, or canonical-root ownership decision
permits importing `THM-M-0318`'s statement or evidence.

Consequently there is no canonical expression whose direct imports can be certified minimal. No
expression or environment-expression fingerprint, credited alternate transport, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutation suite exists.
Those outputs are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with its three discovery imports and prints nine
adjacent APIs. It states no target and has no proof body, so its import list is not a minimal-import
certificate for an exact theorem.

For feasibility only, a temporary candidate outside the repository encoded a real Banach space, a
nonempty closed convex set, a domain-continuous invariant map, compact literal image, and an
in-domain fixed point. It elaborated with the two direct imports
`Mathlib.Analysis.Normed.Module.Basic` and `Mathlib.Analysis.Convex.Basic`; deleting either import
made a required identifier unavailable. This check shows that pinned Lean can express one familiar
candidate. It does not select that candidate, resolve source conventions or target ownership, or
earn statement, source, anchor, or proof credit.

A bounded exact-topic search of pinned mathlib and repo-local Lean found no exact terminal
compact-image Schauder declaration. The only direct Schauder target hit was the foreign
`THM-M-0318` compact-domain statement. This is discovery-only evidence, not the downstream
immutable anchor audit or an exhaustive absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone or fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0637` | 0 | rank 1054; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| target manifest, rev-5.6 blueprint and skill, intake, source crosswalk, and duplicate-scope inspection | 0 | the Satz II family was located, but the canonical target remains null and its relationship with `THM-M-0318` remains unresolved |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0637/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated and printed; stdout SHA-256 `9f769abc...34430`; no target theorem or proof body was declared |
| temporary candidate plus `cd Formalizations/Lean && lake env lean /tmp/THM_M_0637_Candidate.lean` | 0 | prospective compact-image target elaborated with two direct imports; feasibility only and no repository artifact or canonical-target credit |
| `lake env lean /tmp/THM_M_0637_NoBasic.lean` | 1 (expected) | deleting `Normed.Module.Basic` made `NormedAddCommGroup` unavailable |
| `lake env lean /tmp/THM_M_0637_NoConvex.lean` | 1 (expected) | deleting `Convex.Basic` made `Convex` unavailable |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | 0 | only the intake probe and foreign compact-domain target matched direct Schauder names; discovery only |
| `python3 -B Stage1_Instances/THM-M-0637/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while the integrated DAG now records `[_]`; this phase records rather than rewrites prior evidence |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| JSON, scoped invariant, newline, trailing-whitespace, and `git diff --check` checks | 0 | the structured blocker parsed and the two new owned artifacts passed scoped consistency and whitespace validation |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must master-accept the intake and issue an accepted identity and
canonical-root ownership decision for `THM-M-0637` versus `THM-M-0318`. Accountable reviewers must
preserve and hash a lawful complete source edition, crosswalk every incorporated definition,
ordered binder, assumption, conclusion, proof boundary, translation, correction, erratum, and
boundary case, and decide nonemptiness, continuity scope, map encoding, and image-compactness
meaning.

A fresh statement run can then encode precisely that approved claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, proof credit, or
master acceptance is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
