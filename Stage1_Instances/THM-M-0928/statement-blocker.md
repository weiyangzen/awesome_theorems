# THM-M-0928 exact-statement gate: blocked

- Item: `S56-M-0928-STATEMENT`
- Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a`
- Base tree: `cc5285432a02107fadffb68c698690d1b98ac5f2`
- Attempt date: 2026-07-13 (`Asia/Shanghai`)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies the title `波利亚计数定理` (Polya enumeration theorem), George Polya's name,
the year 1937, and only the gloss `考虑对称性的计数` (counting while accounting for symmetry).
It contains no formula, definition, source locator, ordered binder, hypothesis, conclusion, proof
boundary, correction history, or boundary convention. The catalog's `已验证` label is untrusted
metadata under rev-5.6.

The title denotes a theorem family, not one proposition. In particular, it does not select among:

- the total number of orbits of unrestricted `q`-colorings;
- a prescribed-color-inventory coefficient formula;
- a cycle-index substitution identity; or
- a weighted figure-inventory formulation over a specified coefficient semiring or ring.

Those variants have different inputs and conclusions. The record also does not fix a finite
permutation group versus a general action, the finite position and color types, the induced action
on colorings, faithfulness, the cycle statistic and treatment of one-cycles, the coefficient and
division domains, or any degenerate case. Selecting the familiar average of `q` to the number of
cycles, or choosing a cycle-index polynomial because it is convenient to formalize, would narrow,
broaden, or substitute proposition-changing mathematics rather than elaborate the received claim.

The intake identified the matching primary bibliographic lead:

G. Polya, *Kombinatorische Anzahlbestimmungen fuer Gruppen, Graphen und chemische Verbindungen*,
Acta Mathematica 68 (1937), 145-254, DOI `10.1007/BF02546665`.

Neither the intake nor this run admitted the article text, a pinpoint proposition and incorporated
definitions, a translation, correction or errata disposition, or independent review. Current
Project Euclid requests again returned short access-control HTML rather than the article PDF, and
the Springer PDF URL resolved to an article-access HTML page. Those mutable responses receive no
source-text credit. A bibliographic match does not authorize choosing one textbook variant.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake therefore correctly leaves `canonical_statement`,
`canonical_claim`, the Lean module and expression, minimal imports, the elaborated-expression hash,
the canonical-target environment fingerprint, binders, hypotheses, and credited transports null
or empty at `[H1, M3, R4]`. Without one approved proposition, the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. No
`Statement.lean`, declaration, proof body, substituted Burnside root, or assumed Pólya identity was
introduced.

The prerequisite `S56-M-0928-INTAKE` is only provisional `[_]`, not master-accepted `[x]`. Its
receipt is unsigned, non-content-addressed, declares `accepted: false`, and supplies no accepted
receipt ID. Section 10.2 permits this dependency-ordered blocker preparation while concurrent work
is enabled, but the unfinished dependency independently prevents statement acceptance.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates under the pinned environment. Its two
direct imports authenticate generic orbit-counting and permutation-cycle interfaces:

- `MulAction.orbitRel` and `MulAction.fixedBy`;
- `MulAction.sigmaFixedByEquivOrbitsProdGroup`;
- `MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group`;
- `Equiv.Perm.cycleType`; and
- `Equiv.Perm.card_fixedPoints`.

The probe's complete stdout has SHA-256
`d404282e866bb7b628a3086bd3a8870c599d4bbbd4f8ba9366b25fe468c0fefb`; stderr is empty. Its three
candidate axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`. The probe
defines no coloring action, fixed-coloring cycle formula, cycle index, canonical target, checked
source transport, or proof body. Burnside's lemma is separately owned by `THM-M-0929`. Therefore
the probe imports cannot be certified minimal for an absent Pólya target and receive no statement
or proof credit.

A bounded exact-topic search over repository-local Lean, pinned mathlib, and this target found no
declaration named for Pólya enumeration, cycle index, inventory polynomial, or figure inventory.
This is discovery-only feasibility evidence, not the downstream immutable anchor audit and not a
global absence theorem.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone or fetch,
or other `.lake` mutation was run; the pinned mathlib package worktree remained clean.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all other commands ran from the repository root unless noted. Exact
arguments, exits, result summaries, and current input fingerprints are recorded in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and exactly 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0928` | 0 | rank 1467; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base identifiers are recorded above |
| current `sha256sum` over named authority, intake, probe, toolchain, lockfile, and relevant pinned mathlib inputs | 0 | exact digests are recorded in the structured blocker |
| `python3 -B Stage1_Instances/THM-M-0928/check_intake.py` | 1 | historical intake replay stops at stale receipt input hash `Docs/Stage1_Blueprint_rev-5.6.md`; the prior receipt and checker were not rewritten |
| pinned Lean, Lake, mathlib revision/tree, and package-status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib worktree passed |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0928/IntakeProbe.lean` | 0 | six adjacent interfaces and three axiom reports elaborated; stdout 1367 bytes with the hash above; no target or proof body |
| bounded exact-topic `rg` search | 1 (expected no match) | no named target under the recorded terms; no absence or anchor-audit claim is inferred |
| Project Euclid and Springer source-access checks | 0 HTTP responses | access-control/article HTML, not the paper PDF; no source-text credit |
| prohibited-construct scan over owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse, scoped blocker invariants, and whitespace checks | 0 | blocker identity, null target/imports, unchanged vector, false completion fields, two-file scope, and absent self-test agree |

The intake checker is historical evidence bound to an earlier shared-authority snapshot and the
original intake artifact inventory. This statement attempt records its exact freshness failure
rather than editing the intake receipt, checker, instance, target-local task DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first revalidate and master-accept the intake. Accountable reviewers
must then lawfully preserve and hash an immutable primary or approved authoritative source, select
one exact Pólya proposition or an explicit finite multi-root package, and independently approve
every incorporated definition and proof boundary. The selection must fix the group and position
action, color model and inventory, induced coloring action, cycle convention, coefficient and
division domains, ordered binders, hypotheses, exact conclusion, corrections, errata, transports,
and every degenerate case.

A fresh statement attempt can then encode precisely that approved claim, minimize its pinned direct
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the root remains `[H1, M3, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
