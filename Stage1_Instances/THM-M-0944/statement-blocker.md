# Exact-statement gate: blocked

Item: `S56-M-0944-STATEMENT`

Theorem: `THM-M-0944`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0944-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this
dependency-ordered investigation, but the intake receipt declares `accepted: false`, contains no
accepted receipt ID, and requires exact source adoption and independent review before the
statement can be frozen. Its replay checker is also stale after integration because it binds the
pre-integration blueprint hash. This statement run records those boundaries rather than rewriting
historical intake evidence.

Independently, the exact-statement gate cannot pass. The repository record supplies only the
Balog-Szemeredi-Gowers theorem name, the Balog/Szemeredi/Gowers attribution, the year 1994, and the
gloss "the Freiman theorem for approximate groups." The gloss is not a binder-complete BSG
proposition and conflates the energy-to-structure step with neighboring Freiman and
approximate-group structure theory. It chooses neither an energy nor a restricted-sum graph form,
one nor two inputs, an ambient group, an energy normalization, a parameter regime, quantitative
constants and exponents, a conclusion shape, nor boundary cases.

The intake identifies Balog and Szemeredi's 1994 article bibliographically, but no exact primary
theorem passage was admitted. Croot and Borenstein, arXiv `0805.3305v2`, printed page 1, Theorem 1,
is a precise secondary lead for one later Gowers refinement. That source itself says Gowers proved
more, and no accountable reviewer has approved it as the catalog's canonical root or mapped it to
the historical theorem, incorporated definitions, assumptions, proof boundary, corrections, and
errata. Encoding that convenient variant would manufacture source acceptance.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is therefore no canonical expression for which minimal imports, fixed elaboration
context, checked alternate transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. All four mutation classes are
undefined, not passed. No `Statement.lean`, theorem declaration, proof body, weakened special
case, broadened family, circular premise, or substituted neighbor theorem was added. The root
remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain. Its four direct imports
expose additive energy, doubling constants, approximate subgroups, Ruzsa covering, and two
adjacent elementary inequalities. These APIs show that nearby vocabulary is available; none
states or proves the unidentified BSG root. Their imports consequently cannot be certified
minimal for an absent canonical target.

A bounded search over pinned mathlib and repository-local Lean found no BSG-named,
source-title-named, or direct energy-to-small-doubling declaration under the recorded terms. This
is discovery-only evidence, not the downstream immutable anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-0944` | 0 | rank 1483; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, guidelines, and intake inspection | 0 | confirmed the sparse catalog gloss, null canonical target, secondary source lead, and open proposition-changing decisions |
| `sha256sum` over authority, source, intake, probe, toolchain, Lake manifest, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0944/check_intake.py` | 1 | historical provisional intake replay rejects the regenerated blueprint hash; this statement phase records rather than rewrites the stale intake receipt |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0944/IntakeProbe.lean` | 0 | six adjacent API signatures elaborated; stdout SHA-256 `a1fd840fd5b5a12d226e0530b8a1b13f93477264fb1ecbba6580fb9b1b861d5e`; no canonical target or proof body |
| bounded Balog/Gowers/source-title/energy-to-small-doubling search in pinned mathlib and repo-local Lean | 1 | expected no-match result; discovery-only evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable primary or approved authoritative source edition, adopt
and independently approve one exact BSG proposition, and map every incorporated definition,
ordered binder, hypothesis, quantitative dependency, conclusion, proof boundary, correction,
erratum, relation to Gowers's refinement, relation to Freiman/approximate-group theory, and
boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
