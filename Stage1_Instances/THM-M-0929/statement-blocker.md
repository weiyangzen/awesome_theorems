# THM-M-0929 exact-statement gate: blocked

- Item: `S56-M-0929-STATEMENT`
- Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d`
- Base tree: `0d6c1fdf06d1573c256af331c6b198e5a787af43`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog claim is only the title `Burnside引理` (Burnside's lemma), William Burnside's
name, the year 1897, and the gloss `群作用下的轨道计数` (orbit counting under a group action).
It supplies no formula, source locator, definitions, ordered binders, hypotheses, conclusion,
proof boundary, correction, erratum, or boundary convention. Stage0 explicitly leaves the precise
definitions and premises open, and the catalog's `已验证` label is untrusted under rev-5.6.

The title and gloss identify the classical Burnside orbit-counting family, but they do not select
one proposition. In particular, the evidence does not decide among:

- the natural-number identity saying that the sum of fixed-point counts equals the orbit count
  times the group cardinality;
- an average or division formula over `Nat`, `Rat`, or another exact arithmetic carrier; or
- the structural equivalence between the sigma type of fixed pairs and the product of the orbit
  quotient with the group.

Nor does it fix a finite group acting on a finite carrier versus mathlib's more general separate
finiteness assumptions for the group, each fixed-point subtype, and the orbit quotient. Fixed-point
and same-orbit conventions, quotient representation, universes, explicit and implicit binders,
multiplicative versus additive form, and every degenerate case are likewise unresolved. These are
proposition-changing choices: natural-number division hides exact divisibility, and whole-carrier
finiteness is not the same formal binder surface as componentwise finiteness.

The intake identified William Burnside's 1897 *Theory of Groups of Finite Order* as a matching
bibliographic lead, but no book text, immutable edition, theorem/section/page locator, incorporated
definition chain, assumption map, proof boundary, attribution analysis, correction or errata audit,
or independent review was admitted. A bibliography entry does not authorize choosing one familiar
modern formulation.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake therefore correctly leaves `canonical_statement`,
`canonical_claim`, the Lean module and expression, minimal imports, the expression hash, the
canonical-target environment fingerprint, binders, hypotheses, alternate encodings, and excluded
cases null or empty at `[H1, M3, R4]`. Without an approved proposition, the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not
passed. No `Statement.lean`, theorem declaration, assumed identity, weakened consequence, or
broadened package was introduced.

The prerequisite `S56-M-0929-INTAKE` is also only provisional worker state `[_]`. Its receipt says
`accepted: false`, is unsigned and not content-addressed, and supplies no accepted receipt ID.
The historical intake checker additionally expects the former root worker packet, now absent after
integration. Rev-5.6 section 10.2 permits this later-node blocker investigation, but accepted
closure remains dependency ordered. The prior intake artifacts were preserved rather than rewritten
to manufacture freshness.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` directly imports
`Mathlib.GroupTheory.GroupAction.Quotient`. A fresh narrow replay elaborated:

```lean
MulAction.fixedBy
MulAction.orbitRel
MulAction.orbitRel.Quotient
MulAction.sigmaFixedByEquivOrbitsProdGroup
MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group
AddAction.sigmaFixedByEquivOrbitsProdAddGroup
AddAction.sum_card_fixedBy_eq_card_orbits_mul_card_addGroup
```

The multiplication candidate has the pinned surface

```lean
(α : Type u) (β : Type v) [Group α] [MulAction α β]
[Fintype α] [(a : α) -> Fintype (MulAction.fixedBy β a)]
[Fintype (Quotient (MulAction.orbitRel α β))] :
  (∑ a, Fintype.card (MulAction.fixedBy β a)) =
    Fintype.card (Quotient (MulAction.orbitRel α β)) * Fintype.card α
```

The three candidate axiom diagnostics each report `propext`, `Classical.choice`, and `Quot.sound`.
Complete probe stdout is 1780 bytes on 17 lines with SHA-256
`d4600c9b607f48ce306916f715bd7d59c7022d34ed87642f177880b16a994874`; stderr is empty. The probe
declares no canonical THM-M-0929 target, checked source transport, or proof body. Its import is
therefore a direct candidate-module import, not a minimal-import certificate for an absent target,
and it grants no statement or proof credit.

A scoped search found the expected probe references and pinned declarations and no repository-local
canonical target. This is discovery-only feasibility evidence, not the downstream immutable anchor
or terminal proof-body audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was run; the pinned mathlib package worktree remained clean.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless another working directory is shown. Exact arguments, exits, result summaries, and current
input hashes are also recorded in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, exactly 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0929` | 0 | rank 1468; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base identifiers appear above |
| scoped authority, catalog, Stage0, and complete intake inspection and hashing | 0 | sparse family gloss, provisional dependency, null target, H1/M3/R4 boundary, and current input hashes agreed |
| `python3 -B Stage1_Instances/THM-M-0929/check_intake.py` | 1 | historical replay stops at missing `.stage1-worker-selftest.json`; prior intake evidence was not rewritten |
| pinned Lean, Lake, mathlib revision/tree, and package-status checks | 0 | Lean 4.29.0, Lake 5.0.0, expected mathlib revision/tree, and clean package worktree passed |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0929/IntakeProbe.lean` | 0 | seven interfaces and three axiom diagnostics elaborated with the stdout hash above; no canonical target or proof body |
| scoped candidate search | 0 | only the probe and pinned mathlib declarations were located; no root identity is inferred |
| prohibited-construct scan over owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, opaque declaration, or unsafe declaration |
| final JSON parse, scoped blocker invariants, standard/manifest replay, and whitespace checks | 0 | blocker identity, null target/imports, four undefined mutations, false completion fields, exact two-file scope, and clean formatting agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test packet intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must refresh, revalidate, and master-accept the intake. Accountable reviewers
must lawfully preserve and hash an immutable primary or approved authoritative source, select one
exact Burnside proposition or an explicit source-defined package, and independently approve every
incorporated definition, domain, ordered binder, hypothesis, conclusion, proof boundary,
attribution issue, correction, erratum, transport, and boundary case. They must fix the group and
action domains, finiteness surface, fixed-point and orbit quotient conventions, arithmetic carrier,
and relationship among multiplication, average, structural, multiplicative, and additive forms.

A fresh statement worker can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; the root remains `[H1, M3, R4]`; `audit_complete: false` and
`theorem_complete: false`; no debt change is proposed. Because the assigned phase did not pass,
no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
