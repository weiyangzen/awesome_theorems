# Exact-statement gate: blocked

Item: `S56-M-0947-STATEMENT`

Theorem: `THM-M-0947`

Base revision: `d849f42c82f9da2e07c481c7beaeba6d92f86e19` (tree
`874c7795eb7b2cc49d6c8479c316b09b039e9786`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0947-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this
dependency-ordered investigation, but the intake receipt declares `accepted: false`, contains no
accepted receipt ID, and deliberately leaves the canonical mathematical statement and Lean target
null. Master acceptance remains necessary before any future statement transition can be accepted.

Independently, the exact-statement gate cannot pass from the received repository claim. The catalog
supplies only the Roth-theorem name, Klaus Roth/1953 attribution, and the slogan "integer sets
contain a three-term arithmetic progression." It gives no density or cardinality premise. Read as
an ordinary universal assertion, the slogan is false: empty and singleton integer sets contain no
nonconstant three-term progression. The catalog also does not choose a finite, asymptotic, or
infinite formulation; define its ambient integer domain or interval; order its binders; specify its
density convention; encode the progression; exclude zero common difference; or cite a theorem
passage and correction history. Its `verified` label is untrusted under rev-5.6.

The matching primary bibliographic lead is K. F. Roth, *On Certain Sets of Integers*, *Journal of
the London Mathematical Society* s1-28(1) (1953), 104-109, DOI
`10.1112/jlms/s1-28.1.104`. No paper body or exact theorem passage is admitted in the dossier. A
fresh publisher-PDF access check returned HTTP 403 with a Cloudflare challenge, while current
OpenAlex and Semantic Scholar records classify the article as closed and expose no repository PDF.
Consequently no exact theorem, incorporated definition, premise, proof boundary, correction, or
erratum has been transcribed and independently approved.

The proposition-changing choices therefore remain open: a quantitative finite-density theorem
versus `r_3(N) = o(N)` versus an infinite positive-density theorem; `Nat`, positive integers,
`Int`, or a finite abelian group; `[0, N)` versus `[1, N]`; the exact density inequality and
coercions; ordered quantifiers; endpoint equality versus zero-step nondegeneracy; and all small,
sparse, zero-density, and torsion boundary cases. Choosing a familiar variant would repair or
substitute the source claim rather than elaborate it exactly.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical expression for which minimal imports, checked transports, or
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
can be certified. All four mutation classes are undefined, not passed. No `Statement.lean`, proof
body, weakened special case, broadened interface, or circular assumption was added. The root
remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain with the single direct
import `Mathlib.Combinatorics.Additive.Corner.Roth`. It exposes three materially different
candidates:

- `roth_3ap_theorem`, an explicit finite-density theorem for sufficiently large finite abelian
  groups;
- `roth_3ap_theorem_nat`, an explicit finite-density theorem for `A` contained in
  `Finset.range n`, with a `cornersTheoremBound (epsilon / 3)` threshold; and
- `rothNumberNat_isLittleO_id`, the asymptotic extremal little-o formulation.

All candidate signatures elaborate. Each candidate axiom report is
`[propext, Classical.choice, Quot.sound]`, and the probe output has SHA-256
`0d20ca0ebb96b39c8269124da9cd7b6f1b1f8e235381eea82e2d42468eafb2b8`.
The import is the direct source module for these candidates, but it cannot be certified as the
minimal import for an absent canonical target. `Mathlib.Combinatorics.Additive.AP.Three.Defs`
supplies `ThreeAPFree` and `rothNumberNat`, not the three Roth theorem declarations.

A bounded search over pinned mathlib and repository-local Lean located these exact-family
declarations, adjacent Behrend and Ruzsa-Szemeredi work, and legacy uses. This is discovery-only
evidence, not the downstream anchor/provenance audit or a source-identity result.

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
| `python3 scripts/stage1_target.py show THM-M-0947` | 0 | rank 1486; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, guidelines, intake, source-availability, and pinned-source inspection | 0 | confirmed the false premise-free slogan, null canonical target, unavailable paper body, and unresolved formulation decisions |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0947/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]`; integration has advanced it provisionally to `[_]`; the stale intake validator was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0947/IntakeProbe.lean` | 0 | six exact-family interfaces elaborated; three candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout hash recorded above |
| bounded Roth/three-AP search in pinned mathlib and repository-local Lean | 0 | located direct candidates and adjacent work; discovery only |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable primary or approved authoritative source edition, adopt
and independently approve one exact theorem passage, and map every incorporated definition,
ordered binder, premise, conclusion, proof boundary, correction, erratum, interval convention,
density convention, progression encoding, nondegeneracy condition, and boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
