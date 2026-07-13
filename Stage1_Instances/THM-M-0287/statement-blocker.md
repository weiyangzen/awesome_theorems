# Exact-statement gate: blocked

Item: `S56-M-0287-STATEMENT`

Theorem: `THM-M-0287`

Base revision: `a75b2f3ac5b8b7d34eb73435734edfeecc41bd40` (tree
`66a22e1dc2e1c14c27bd01396a99826ab2536bf1`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the family name "Lusin's theorem," Nikolai Luzin, the year 1912, and the
gloss "the relationship between measurable functions and continuous functions." It gives no
citation, formula, incorporated definitions, ordered binders, hypotheses, conclusion, proof
boundary, correction history, or boundary cases. Stage0 explicitly leaves the precise definitions
and premises, proof route, alternate forms, axiom profile, machine status, and artifact links open.
The catalog's verified label is untrusted metadata under rev-5.6.

The intake predecessor has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt declares `accepted: false`, is not content-addressed, and contains no accepted receipt ID.
This permits a dependency-ordered inspection, but master acceptance remains independently required
before a future statement transition can be accepted. More importantly, the intake deliberately
leaves the canonical claim, Lean module and expression, expression hash, and canonical-target
environment fingerprint null. Rev-5.6 makes statement ambiguity and a missing expression
fingerprint hard blockers.

The intake found a strong primary-source lead: N. Lusin, "Sur les proprietes des fonctions
mesurables," *Comptes rendus hebdomadaires des seances de l'Academie des sciences* 154 (1912),
1688-1690, with the relevant passage on printed page 1689. Its visual inspection reports, in
substance, a measurable function on `[0,1]`, an arbitrarily small positive epsilon, and a perfect
nowhere-dense subset of measure greater than `1 - epsilon` on which the function is relatively
continuous. This remains `H1`, not an accepted source root. The catalog does not cite that passage,
and the historical definitions, exact translation, measure normalization, proof boundary,
corrections or errata, and independent review have not been admitted.

Materially different modern statements share the same family name: a finite-measure theorem
producing a large closed set, a finite Radon-measure theorem producing a large compact set, a
metric-valued or almost-everywhere measurable form, and a globally continuous representative
agreeing away from a small exceptional set. They differ in domain and topology, measure and
finiteness, codomain, measurability, epsilon type and strictness, large-set predicate, relative
continuity versus global equality, binder order, and degenerate cases. Selecting the historical
interval result or any modern variant without an accepted source decision would invent, broaden,
strengthen, weaken, or substitute mathematics.

Consequently there is no honest canonical expression whose imports can be certified minimal. No
alternate encoding can receive a checked transport, and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than
passed. No `Statement.lean`, axiom, placeholder, assumed conclusion, proxy predicate, weakened
special case, or broadened theorem was introduced. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with these three direct imports:

- `Mathlib.MeasureTheory.Constructions.Polish.Basic`
- `Mathlib.MeasureTheory.Function.AEEqFun`
- `Mathlib.MeasureTheory.Measure.RegularityCompacts`

It checks six adjacent interfaces: `ContinuousOn`, `Continuous.measurable`,
`MeasurableSet.exists_isCompact_diff_lt`,
`MeasureTheory.innerRegular_isCompact_isClosed_measurableSet_of_finite`,
`Measurable.exists_continuous`, and `ContinuousMap.toAEEqFun`. All elaborate. They provide generic
relative-continuity, measurability, compact-regularity, topology-refinement, and a.e.-function
infrastructure only. In particular, `Measurable.exists_continuous` changes to a finer Polish
topology, while compact inner regularity supplies no continuity conclusion. The probe states no
canonical Lusin proposition, source transport, or proof body, so its imports cannot be certified
minimal for an absent target.

A bounded exact-topic search of repo-local Lean and pinned mathlib found the distinct Lusin
separation and Lusin-Souslin theorems plus adjacent continuous-on-compact and measurability
infrastructure, but no accepted usual large-measure continuous-restriction declaration. This is
narrow discovery evidence, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository
root unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0287` | 0 | rank 1293; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided untracked `.lake` link existed; base revision and tree appear above |
| authority, catalog, Stage0, source-lead, and intake inspection | 0 | the catalog remains a family gloss; the intake and H1 lead explicitly leave the canonical proposition and Lean target null |
| `sha256sum` over authority, source, intake, probe, toolchain, manifest, and pinned mathlib sources | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, target `x86_64-unknown-linux-gnu`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`, Lean 4.29.0 |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0287/IntakeProbe.lean` | 0 | six adjacent pinned APIs elaborated; no target or proof body declared; stdout SHA-256 `c3532189de5c770680d83f72305b0d8bece4f3297925bcb84436fbed0d0d4aaf` |
| bounded repo-local and pinned-mathlib Lean `rg` searches for the target relation | 0 | only distinct Lusin-name theorems and adjacent generic interfaces were found; discovery only |
| `python3 -B Stage1_Instances/THM-M-0287/check_intake.py` | 1 | historical intake replay stops at line 144 because it freezes authority state `[ ]` while the current DAG records provisional `[_]`; this phase records rather than rewrites historical evidence |
| prohibited Lean declaration scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0287/statement-blocker.json`; scoped Python blocker assertions | 0 | structured blocker parsed; identity, current base, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| scoped newline/trailing-whitespace checks plus `git diff --check -- Stage1_Instances/THM-M-0287` | 0 | no whitespace diagnostics in either new file |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority state and nine-file intake
inventory. Integration subsequently promoted the intake worker evidence to provisional `[_]`, so
the checker already fails before its inventory assertion. Adding these two statement artifacts also
makes that intake-only inventory historical. This run records the limitation instead of rewriting
the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative execution
DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
lawfully preserve and hash one complete primary or authoritative source, select and independently
approve one exact proposition and every incorporated definition, and reconcile translation,
corrections and errata. They must freeze the historical-versus-modern variant; domain, topology,
measure, and normalization; codomain and measurability; perfect/nowhere-dense, closed, or compact
large-set predicate; relative-continuity or global-agreement conclusion; ordered binders; epsilon
convention; foundation profile; and every exceptional and degenerate case.

A later statement worker can encode precisely that source claim, minimize pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four mutation classes.

This is a blocked-attempt record, not completion of the assigned node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt change
is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, node receipt, worker `[_]`, proof credit, or master acceptance is
claimed.
