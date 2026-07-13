# Exact-statement gate: blocked

Item: `S56-M-0288-STATEMENT`

Theorem: `THM-M-0288` (Vitali covering theorem)

Base revision: `67d32ab26aba14b674ae8a1b919e6935812190c3` (tree
`8a1d264cf3331992fbbc3a4fffca285af0b88929`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the family name "Vitali covering theorem," Giuseppe Vitali, the year
1908, and the compound gloss "covering lemma and differentiation theorem." It cites no proposition
or explicit two-node bundle and supplies no incorporated definitions, ordered binders, hypotheses,
conclusion, composition edge, proof boundary, translation, correction history, or boundary cases.
The catalog's verified label is untrusted metadata under rev-5.6.

The intake predecessor has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt declares `accepted: false`, is not content-addressed, and contains no accepted receipt ID.
This permits a dependency-ordered inspection, but master acceptance remains independently required
before a future statement transition can be accepted. More importantly, the intake deliberately
leaves the canonical claim, Lean module and expression, expression hash, and canonical-target
environment fingerprint null.

The repository gloss does not decide whether the root is one covering result, one differentiation
result, or a bundle in which covering supports differentiation. Each interpretation still has
proposition-changing choices:

- Euclidean, metric, or pseudo-metric ambient space, dimension, topology, measurable structure,
  measure assumptions, and local finiteness or doubling;
- intervals, balls, arbitrary closed or measurable sets, their index type, centers and radii,
  boundedness or fineness, and an enlargement constant;
- finite or countable selection, the disjointness convention, coverage of input sets, centers, or a
  target set, and literal versus almost-everywhere coverage;
- differentiation of a measure, density, or a scalar- or vector-valued function, its regularity,
  the limiting filter, exceptional set, and exact limit; and
- empty families and sets, nonpositive radii, zero or infinite measures, zero-measure averages,
  non-doubling spaces, and failures of second countability, Borel compatibility, or local finiteness.

The inspected 1904 scan does not select this modern compound root. A contemporary JFM record
identifies the 1908 Torino article and reports an interval-family theorem used for integral-function
results, but the primary text was not obtained. Encyclopedia of Mathematics revision `55740`
states a modern measurable variant while conflicting with JFM on pagination. There is no accepted
primary-source passage, incorporated-definition map, exact translation, proof boundary,
correction/errata disposition, or independent source review. Selecting a familiar classical
formulation or the nearest pinned declaration would therefore invent, narrow, broaden, or
substitute mathematics.

Consequently there is no honest canonical expression whose imports can be certified minimal. No
alternate encoding or covering-to-differentiation edge can receive a checked witness, and the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined rather than passed. No `Statement.lean`, axiom, placeholder, assumed conclusion, proxy
predicate, weakened special case, or broadened theorem was introduced. The root remains
`[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with these direct imports:

- `Mathlib.MeasureTheory.Covering.Vitali`
- `Mathlib.MeasureTheory.Covering.Differentiation`

It exposes materially different exact-topic interfaces. The closed-ball theorem selects a
pairwise-disjoint subfamily in a pseudo-metric space and covers each input ball by a selected ball
dilated by `tau > 3`. The measurable theorem assumes second countability, local finiteness, closed
sets with nonempty interiors, a proportional measure estimate, and fineness, and returns a
countable disjoint family covering a target almost everywhere. `Vitali.vitaliFamily` instead builds
an abstract Vitali family from a small-scale doubling condition, while
`VitaliFamily.FineSubfamilyOn.exists_disjoint_covering_ae` restates covering data already carried by
that abstraction.

The differentiation interfaces have different roots and conclusions:
`VitaliFamily.ae_tendsto_rnDeriv` concerns ratios of locally finite measures,
`VitaliFamily.ae_tendsto_measure_inter_div` concerns density, and
`VitaliFamily.ae_tendsto_average_norm_sub` and `VitaliFamily.ae_tendsto_average` concern locally
integrable functions. None is expression-identical to a source-selected root because no such
selection exists. The probe reports `[propext, Classical.choice, Quot.sound]` for five representative
candidates but declares no canonical target, transport, composition, or proof body. Its imports
are minimal only for that discovery probe, not for an absent target or bundle.

A bounded search of repo-local Lean and the pinned covering modules found these inequivalent
covering and differentiation families. Other repo-local `Vitali` matches concern convergence or
approximation and are expressly different theorem families. This is bounded discovery evidence,
not the downstream immutable anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-0288` | 0 | rank 1294; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided untracked `.lake` link existed; base revision and tree appear above |
| catalog, Stage0, source-boundary, and intake inspection | 0 | the catalog remains a compound family gloss; the intake explicitly leaves the source root or bundle and canonical target null |
| authority, intake, toolchain, manifest, and pinned-source SHA-256 checks | 0 | exact input hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | revision and tree above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0288/IntakeProbe.lean` | 0 | ten distinct pinned APIs elaborated; five axiom reports were `[propext, Classical.choice, Quot.sound]`; output 5418 bytes, SHA-256 `c7cb70922146dc629842ee69d6d66b791359a44af65ef59093b09e2170ae5ce3`; no target or proof body |
| bounded exact-topic `rg` search in repo-local Lean, the owned probe, and three pinned covering modules | 0 | 194 lines, 26230 bytes, SHA-256 `4272f7943c0e57f01fda98f8dbfd5ea35e084be10d6adcab31a85d04df16f9d8`; multiple inequivalent candidates, discovery only |
| `python3 -B Stage1_Instances/THM-M-0288/check_intake.py` | 1 | historical intake replay stops at line 154 because it freezes authority state `[ ]` while the current DAG records provisional `[_]`; this phase records rather than rewrites historical evidence |
| `rg -n --glob '*.lean' '(^|[[:space:]])(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)([[:space:]]|$)' Stage1_Instances/THM-M-0288` | 1 | expected no-match exit; no prohibited declaration token was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0288/statement-blocker.json`; scoped Python blocker assertions | 0 | structured blocker parsed; identity, current base, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0288` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0288/statement-blocker.json` and the corresponding command for `statement-blocker.md` | 1 each | expected new-file difference exits with empty diagnostic output; exact Python byte-hygiene command and result are recorded in the JSON companion |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority state and nine-file intake
inventory. Integration subsequently promoted the intake worker evidence to provisional `[_]`, so
the checker already fails before its inventory assertion. Adding these two statement artifacts also
makes that intake-only inventory historical. This run records the limitation instead of rewriting
the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative execution
DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
lawfully preserve and hash one complete primary or approved authoritative source, select and
independently approve one exact covering proposition, differentiation proposition, or explicit
bundle, and transcribe every incorporated definition, ordered binder, hypothesis, conclusion,
composition edge, translation, correction, erratum, proof boundary, and degenerate case.

A later statement worker can encode precisely that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport and
bundle wrapper, and execute all four mutation classes.

This is a blocked-attempt record, not completion of the assigned node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt change
is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, node receipt, worker `[_]`, proof credit, or master acceptance is
claimed.
