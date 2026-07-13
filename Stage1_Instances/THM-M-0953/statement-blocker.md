# Exact-statement gate: blocked

Item: `S56-M-0953-STATEMENT`

Theorem: `THM-M-0953`

Base revision: `d66b6e80968b53d5b99774584721ae8976f303a5` (tree
`aaa82721074fccea81033a9a18d21652af89f8e4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0953-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
investigation, but the intake receipt declares `accepted: false`, contains no accepted receipt ID,
and deliberately leaves the canonical mathematical statement and Lean target null. Its frozen
blueprint and execution-DAG hashes are also stale after integration. Master acceptance remains
necessary before a future statement transition can be accepted.

Independently, the exact-statement gate cannot pass from the received repository claim. The
catalog supplies only the title `Solymosi定理`, the József Solymosi/2009 attribution, and the gloss
`和集与积集的下界改进` ("an improved lower bound for sumsets and product sets"). It gives no
bibliography, numbered result, formula, domain, binders, hypotheses, constants, logarithm
convention, proof boundary, corrections, or boundary cases. Its `已验证` label is untrusted under
rev-5.6.

The immutable `arXiv:0806.1040v3` source is a strong primary candidate, not an admitted canonical
root. Its Theorem 2.1 states, for a finite set `A` of positive reals,
`|AA| |A+A|^2 >= |A|^4 / (4 ceil(log |A|))`. Its Corollary 2.2 instead gives a derived lower bound
for `max{|A+A|, |AA|}` with exponent `4/3` and a cube-root logarithmic loss. The paper also contains
an asymmetric two-set extension and a higher-sumset theorem. The catalog does not cite this paper
or select among those inequivalent claims, and no independent source reviewer has approved an
edition, numbered result, incorporated definitions, proof boundary, corrections, or errata.

The source does not specify the base of `log`. More seriously, the displayed denominator is zero
for a singleton under the usual logarithm conventions; the cleared-denominator form is false for
a singleton. Adding `1 < A.card`, choosing base-two `Nat.clog`, or imposing a sufficiently-large
condition would be a proposition-changing repair unless an accountable source review authorizes
it. The remaining formal choices also change the proposition: finite `Set` versus `Finset`, the
strict positivity predicate, pointwise sum/product conventions, natural or real cardinal powers,
division versus a cleared inequality, casts, binder order, and empty/small-cardinality behavior.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical expression for which minimal imports, checked transports, or
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
can be certified. All four mutation classes are undefined, not passed. No `Statement.lean`, proof
body, weakened special case, broadened interface, or circular assumption was added. The intake
boundary remains `[H1, M3, R4]`; its `M3` records only an explicitly uncredited proposition-shaped
probe and adjacent interfaces, not a canonical target.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain. Its three direct imports
expose finite real sumsets, product sets, multiplicative energy, and `Nat.clog`, and it elaborates
one explicitly uncredited repaired proposition shape. All checks pass, but none selects or proves
the Solymosi root. The probe imports therefore cannot be certified minimal for an absent canonical
target.

A bounded exact-topic search over pinned mathlib and repository-local Lean found no Solymosi or
source-identical sum-product declaration. This is discovery-only evidence, not the downstream
immutable anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-0953` | 0 | rank 1488; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, guidelines, intake, and immutable source inspection | 0 | confirmed the family-only catalog claim, inequivalent primary-source candidates, null canonical target, unspecified log base, and singleton defect |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0953/check_intake.py` | 1 | historical provisional intake replay rejects the current regenerated blueprint hash; this statement run records rather than rewrites the stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0953/IntakeProbe.lean` | 0 | eight adjacent interfaces and one explicitly uncredited guarded candidate `Prop` elaborated; stdout SHA-256 `62ba16ac6e208a21dad742e210fe85f8d925bd734f9dd8e17cdb96e3a3b230ec` |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 | expected no-match result; discovery-only evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and independently approve one immutable source edition and exact numbered
result, map every incorporated definition and assumption, audit corrections and errata, and make
an explicit decision about the logarithm convention and singleton defect without a silent repair.
They must freeze the domain, positivity, set encoding, ordered binders, constants, casts,
inequality form, alternate encodings, and every degenerate case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
