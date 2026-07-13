# THM-M-0943 exact-statement gate: blocked

Item: `S56-M-0943-STATEMENT`

Base revision: `b56df790fc94c5366cf919a6fe5411d06b427c59` (tree
`18ba629d4c00333f6e17018905f4fbd30558bb4c`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0943-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt is explicitly unaccepted and
non-content-addressed, lists no accepted receipt ID, and binds an older repository revision and
older blueprint and execution-DAG hashes. Rev-5.6 section 10.2 permits this dependency-ordered
investigation, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete catalog record
provides only the Plunnecke-Ruzsa inequality name, a combined Helmut Plunnecke/Imre Ruzsa
attribution, the year 1970, and the slogan "growth of sumsets." It supplies no formula, source
locator, incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary,
correction history, or reviewer. Stage0 explicitly leaves precise definitions and premises open,
and the catalog's `verified` label is untrusted under rev-5.6.

The inspected Petridis source lead distinguishes two materially different roots. Theorem 1.1 is
Plunnecke's subset-growth result: under a small first-sumset premise, it produces a subset `X` of
`A` whose higher sumsets grow at the prescribed rate. Theorem 1.2 is Ruzsa's extension: for
finite `A` and `B` in an abelian group, `|A + B| <= alpha |A|` implies
`|kB - lB| <= alpha^(k+l) |A|` when `k+l > 1`. The catalog cites and selects neither result. The
source was only a temporary intake lead; it has not been admitted as immutable source authority,
fully crosswalked, or independently approved.

The proposition-changing decisions therefore remain open: Plunnecke subset growth versus Ruzsa
sum-and-difference growth; the ambient group and finite-set encoding; which sets are nonempty; a
free parameter `alpha` or `K` versus an exact cardinality ratio; `A+B` versus `A-B`; one or two
indices; the cardinality codomain and coercions; pointwise subtraction; binder order; and all
zero- and low-index cases. In particular, the close pinned mathlib theorem quantifies over every
`m n : Nat`, while the displayed Petridis Theorem 1.2 assumes `m+n > 1`. Silently choosing the
mathlib strengthening, a special case, or a package of variants would invent, broaden, narrow, or
substitute mathematics rather than elaborate the exact received target.

Sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint hard
blockers. There is consequently no canonical Lean expression whose imports can be certified
minimal, no checked alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. All four mutation classes are undefined, not
passed. No `Statement.lean`, theorem declaration, proof body, weakened special case, broadened
interface, axiom, or placeholder was added. The root remains `[H1, M3, R4]`: `M3` records a close
pinned candidate interface, not an accepted root or proof.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` has one direct import:

- `Mathlib.Combinatorics.Additive.PluenneckeRuzsa`

It re-elaborates the Petridis bridge, the two `A+B`/`A-B` two-index variants, and the two one-index
variants. The closest interface is
`Finset.pluennecke_ruzsa_inequality_nsmul_sub_nsmul_add`, which, for nonempty finite `A` and finite
`B` in an additive commutative group, bounds the pointwise difference of the `m`-fold and `n`-fold
sums of `B` in nonnegative rationals by
`(|A+B| / |A|)^(m+n) |A|`. Lean reports axioms `[propext, Classical.choice, Quot.sound]` for the two
representative imported candidates. These checks authenticate pinned API feasibility only. They
do not select the catalog root, establish a source transport, certify import minimality for an
absent target, or supply target proof credit.

A bounded exact-topic search located this pinned module and two mathlib importers but no
repository-local target declaration. That is discovery-only evidence, not the downstream
immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0943` | 0 | rank 1482; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, manifest, execution-DAG, intake, and source-crosswalk inspection | 0 | confirmed the sparse family slogan, intake `[_]`, statement `[ ]`, null canonical claim and target, H1/M3/R4 boundary, and unresolved source/result selection |
| `git blame -L 6889,6894 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over authority, intake, source, toolchain, lockfile, probe, and pinned module inputs | 0 | exact current hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0943/check_intake.py` | 1 | historical intake replay stops at line 129 because it expects authoritative intake state `[ ]`, while integration now records `[_]`; this statement phase records rather than rewrites historical evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0943/IntakeProbe.lean` | 0 | five candidate interfaces elaborated; two axiom reports were `[propext, Classical.choice, Quot.sound]`; 1467 output bytes; SHA-256 `9876c9208b5e0bf30a36237968ba3f227145c67aac7cb44e9e07787c57268a52` |
| bounded exact-topic Lean search | 0 | pinned target module and two importers located; output SHA-256 `608119c979cddee2b1156c3682b19eecf268704453528bd6428a05d156ccfbda`; no repository-local target declaration |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The finalized JSON parse, scoped invariants, whitespace checks, change-scope check, standard replay,
and absent-self-test check are recorded in the structured blocker beside this report. The
historical intake checker freezes intake-time authority state and its original artifact inventory;
this phase does not rewrite it, the intake receipt, the generated blueprint, or the authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first revalidate and master-accept refreshed intake evidence.
Accountable reviewers must then lawfully preserve and independently approve one immutable primary
or approved authoritative source, select Plunnecke's subset-growth theorem, Ruzsa's two-index
extension, or one explicit reviewed package, and map every incorporated definition, binder,
hypothesis, conclusion, attribution, low-index case, proof boundary, correction, and erratum. They
must freeze the ambient group, finite-set representation, nonemptiness, ratio or parameter premise,
cardinality codomain, pointwise operations, alternate forms, and all degenerate cases.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
