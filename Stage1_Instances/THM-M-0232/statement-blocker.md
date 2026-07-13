# THM-M-0232 exact-statement gate: blocked

Item: `S56-M-0232-STATEMENT`

Base revision: `f294137feee7840fd105a4d3f6073d5cf45508ea` (tree
`234b8f273d252c2c42ce6860315ed973049c871a`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the title `鲁歇定理`, Eugène Rouché, 1862, and the gloss
`全纯函数零点个数比较` ("comparison of the numbers of zeros of holomorphic functions"). It
supplies no source locator, formula, incorporated definitions, ordered binders, hypotheses,
conclusion, proof boundary, corrections, or boundary cases. Stage0 explicitly leaves precise
definitions and premises, the proof route, alternate forms, axioms, machine status, and artifacts
open. The catalog's `已验证` label is untrusted metadata under rev-5.6.

These omissions are proposition-changing. A faithful statement must select a circle and disk,
Jordan domain, bounded open set, simple closed curve, or another exact contour-region pair; its
interior, boundary, orientation, and connectedness conventions; exact regularity conditions; and
one strict inequality with fixed function roles. It must also define a finite interior zero count,
count analytic multiplicities, handle boundary and identically-zero cases, and freeze every
universe, binder, hypothesis, conclusion, transport, and degenerate case. The familiar
perturbation form `|g| < |f|` comparing `f` with `f + g` and the difference form
`|f - g| < |f|` comparing `f` with `g` are related candidates, but neither is selected by an
accepted source crosswalk.

The repository separately schedules `THM-M-0234` as `儒歇定理`, with the same Rouché attribution
and 1862 date and the gloss "stability of the number of zeros of functions." The two Chinese names
are alternate transliterations. No accepted record says whether these IDs are aliases, an
accidental duplicate, or distinct variants, and no canonical-root or evidence-ownership decision
exists. Copying a future `THM-M-0234` target or assigning convenient variants between the IDs would
be an unauthorized substitution.

The intake records two source leads. A MacTutor biography quotes a familiar closed-contour
perturbation formulation, but it is a secondary source and supplies no original theorem page,
incorporated definitions, multiplicity wording, proof passage, corrections, errata, or independent
review. BnF catalog records identify a 31-page 1866 printing of *Mémoire sur la série de Lagrange*,
but not the exact theorem passage, its relation to the catalog's 1862 date, or any of the missing
source-review inputs. These leads support H1 discovery, not an exact H0 statement.

The intake consequently leaves the canonical statement, Lean module and expression, expression
hash, canonical-target environment fingerprint, ordered binders, and hypotheses null or empty at
`[H1, M4, R4]`. Without a canonical expression, no imports can be certified minimal, no alternate
encoding can receive a checked transport, and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. No
`Statement.lean`, declaration, placeholder, weakened special case, or broadened theorem was
introduced.

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt declares `accepted: false`, is not content-addressed, and contains no accepted receipt ID.
Rev-5.6 permits a provisional later-node attempt, but dependency acceptance remains necessary
before a future statement transition can be accepted. The first substantive failure is the
missing exact source proposition and duplicate-root ownership decision.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with its three direct imports:

- `Mathlib.Analysis.Analytic.Order`
- `Mathlib.Analysis.Complex.CauchyIntegral`
- `Mathlib.Analysis.Meromorphic.Divisor`

It checks eight adjacent vanishing-order, divisor, and circle-integral interfaces. All checks pass,
but the probe defines no domain, contour, zero count, Rouché proposition, checked transport, or
proof body. Its imports are discovery-only and cannot be certified minimal for an absent canonical
target. A bounded exact-topic search over repo-local Lean and pinned mathlib found no Rouché-named
or equal-zero-count terminal declaration. This is narrow feasibility evidence, not the downstream
immutable anchor audit and not a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0232` | 0 | rank 1244; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided untracked `.lake` symlink existed; base revision and tree appear above |
| `git blame -L 1675,1694 -- Docs/researches/math_theorems.md` | 0 | both adjacent Rouché catalog entries originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, probe, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0232/check_intake.py` | 1 | the historical intake checker expects the intake DAG node to remain open, while integration has advanced it to provisional `[_]`; this phase records rather than rewrites historical intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0232/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `4a13a2dcbb18c343e2779399e9dabef98228ba2707d0755858e16aef9fd44461`; empty stderr; no target declaration |
| bounded Rouché and equal-zero-count search over repo-local and pinned-mathlib Lean roots | 0 | only the owned probe comment and unrelated phrases matched; no terminal target was located |
| prohibited Lean declaration scan over the owned target | 0 wrapper, inner `rg` 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0232/statement-blocker.json` and scoped `jq` assertions | 0 | valid JSON; identity, blocked state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and exact two-file scope agree |
| `git diff --check -- Stage1_Instances/THM-M-0232` plus per-file `git diff --no-index --check` | 0; 1 expected difference | no whitespace diagnostics in the two blocker artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is intentionally not repaired by this statement-only assignment. It
freezes intake-time authoritative state and artifact inputs. This run records that historical
evidence boundary instead of changing the intake checker, receipt, instance, task DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must then lawfully preserve and hash one complete primary or approved authoritative source, select
and independently approve one exact proposition, reconcile the 1862/1866 source history, and
reconcile `THM-M-0232` with `THM-M-0234` by assigning canonical-root and evidence ownership. They
must map every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
translation, correction, erratum, and exceptional case, including the domain, contour, boundary,
orientation, regularity, strict inequality, dominant function, finite zero count, and analytic
multiplicity conventions.

A fresh statement worker may then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; the root remains `[H1, M4, R4]`, with `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
