# Exact-statement gate: blocked

Item: `S56-M-0015-STATEMENT`

Theorem: `THM-M-0015`

Base revision: `5ae439adae290d44dcf08cc6439c5fb64154fe47` (tree
`51717feef6efc7076e60ee31e7a1ca0a246fec42`).

## Decision

The statement item remains `[ ]`. Rev-5.6 section 10.2 permits this dependency-ordered attempt
while the prerequisite `S56-M-0015-INTAKE` has only provisional worker state `[_]`. The intake
receipt is not content-addressed, declares `accepted: false`, has no accepted receipt ID, and
deliberately leaves the canonical mathematical statement and formal target null. It also fails
replay at this revision because its recorded blueprint hash is stale. These conditions require
integration-lane revalidation and master acceptance before any future statement transition, but
they did not prevent this fail-closed inspection.

Independently and decisively, the exact-statement gate cannot pass from the received source record.
The repository gives only the title `阿廷互反律` (Artin reciprocity), Emil Artin, the year 1927,
and the gloss `类域论的核心定理` ("the central theorem of class field theory"). It supplies no
bibliography, formula, definition, ordered binder, hypothesis, conclusion, normalization, boundary
case, proof boundary, correction history, or accountable source review. Its `已验证` label is
explicitly untrusted under rev-5.6.

The intake's inspected modern source identifies a leading theorem family but does not authorize a
canonical root. In the number-field setup of Milne, *Class Field Theory* v4.03, Chapter V,
Theorem 5.3, the global Artin map kills principal ideles and, for every finite abelian extension
`L/K`, induces the expected norm-quotient isomorphism with `Gal(L/K)`. Milne's Theorem 5.5 is the
separate class-field existence theorem. The catalog neither cites Milne nor selects the finite-level
idelic form, the historical ideal/ray-class form, or an inverse-limit form. The Artin 1927 article
body was not inspected during intake, so it cannot supply the missing exact passage or a checked
historical-to-modern transport.

Material proposition choices remain unresolved:

- number fields only versus arbitrary global fields;
- ideal or ray-class language versus ideles and idele classes;
- existence or uniqueness of the Artin map, principal-idele kernel, finite-level norm kernel and
  quotient isomorphism, local compatibility, or a source-authorized conjunction;
- arithmetic versus geometric Frobenius and the direction or inverse of every reciprocity map;
- ramified and archimedean places, moduli, positivity, topology, connected components, and closure
  conventions;
- idelic norms versus idele-class norms and the exact quotient direction; and
- trivial extensions, positive-characteristic function fields, and all other boundary cases.

These choices produce different propositions. Selecting the familiar Milne statement, silently
adding the existence theorem, or introducing a structure whose fields assume a global Artin map or
reciprocity isomorphism would invent, broaden, or substitute mathematics. Rev-5.6 sections 5 and
5.1 make this ambiguity and the missing elaborated-expression fingerprint hard blockers. There is
therefore no honest canonical target whose imports can be certified minimal, no checked alternate
transport, and no meaningful removed-hypothesis, changed-domain, changed-binder-scope, or
boundary-case mutation. The root vector remains `[H1, M4, R3]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with four direct imports from the pinned dependency
closure. It checks eight adjacent APIs: `NumberField`, the additive number-field adele ring and
diagonal embedding, its additive principal subgroup, `ClassGroup`, `IsAbelianGalois`, and generic
quotient-group maps. The complete probe output has SHA-256
`5fa6b62838bcc702800275a704a5fa482a127400fb2209fb0577831a7df19007`.

This is real substrate validation only. The probe defines no source-faithful multiplicative idele
group or idele topology, idele-class norm, global Artin map, Frobenius normalization, reciprocity
kernel, or quotient isomorphism, and it states no target theorem. A bounded pinned-mathlib search
found no terminal Artin reciprocity declaration; the repo-local `S1_M_077.lean` file explicitly
uses an abstract statement boundary and records no terminal global theorem. Neither observation is
the downstream anchor audit, and the probe imports cannot be certified minimal for an absent
canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0015` | 0 | rank 1065; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0015/IntakeProbe.lean` | 0 | eight adjacent pinned APIs elaborated; no canonical target or proof body declared; stdout hash recorded above |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_077.lean` | 0 | legacy abstract global-CFT boundary elaborated; it supplies no exact Artin reciprocity target or proof credit |
| bounded Artin/global-reciprocity/class-field-theory search in pinned mathlib and repo-local Lean | 0 | no terminal pinned-mathlib declaration; repo-local matches are nonterminal discovery boundaries only |
| `python3 Stage1_Instances/THM-M-0015/check_intake.py` | 1 | historical intake replay stops at `stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md` |
| `python3 -m json.tool Stage1_Instances/THM-M-0015/statement-blocker.json` plus scoped `jq -e` invariants | 0 | valid JSON; identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, and blocked state agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0015` | 1 | expected no-match result; no prohibited Lean declaration or proof escape |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0015/statement-blocker.md`; same for `statement-blocker.json` | 1 each | expected new-file difference status with no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0015` | 0 | no tracked whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake receipt recorded blueprint SHA-256 `bcbce90f...1c1d72` and execution-DAG SHA-256
`0f01e506...23bfcd0`; current authority is `a4fbaf9f...110170a` and
`0422c3e1...ab3034`. This statement run records that stale predecessor evidence rather than
rewriting the intake receipt, instance manifest, task DAG, generated checklist, or authoritative
execution DAG.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
select and independently approve one exact Artin reciprocity proposition, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, normalization, proof boundary,
correction, erratum, historical transport, and boundary case. They must also decide its boundary
against the separately cataloged global class field theory target `THM-M-0422`. A fresh statement
worker can then encode exactly that source model with concrete Lean interfaces, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes. The integration lane must revalidate and
master-accept the intake before accepting that future statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
