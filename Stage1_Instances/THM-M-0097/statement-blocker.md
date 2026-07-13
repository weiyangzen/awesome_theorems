# Exact-statement gate: blocked

Item: `S56-M-0097-STATEMENT`

Theorem: `THM-M-0097`

Base revision: `ee8c1843ef3ce74178a990f4e64554c1558c51fa` (tree
`3a34df1cc2089854dc563ab4909cc0586713ad20`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0097-INTAKE`, has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is explicitly unaccepted and
non-content-addressed, has no accepted receipt ID, and requires independent source, formal, and
representation-theory review before downstream statement work. It deliberately leaves the
canonical mathematical statement and Lean target null.

Independently, the received catalog record does not identify one exact proposition. Its complete
mathematical gloss is `半单李群表示的特征标` ("characters of representations of semisimple Lie
groups"), with attribution to Harish-Chandra and the year 1951. It supplies no bibliography,
theorem locator, definitions, ordered binders, hypotheses, exact conclusion, proof boundary,
correction history, boundary policy, or independent review. The catalog's `已验证` label is
untrusted under rev-5.6.

The intake identified two important primary-source leads without treating either as the target.
The catalog year aligns with Harish-Chandra's 1951 PNAS note *Representations of Semisimple Lie
Groups: III. Characters*, but a complete statement from that paper was not admitted. Theorem 6 of
the inspected 1956 paper *The Characters of Semisimple Lie Groups* states an analyticity result for
the distribution character of a quasi-simple representation on that paper's quasi-regular set.
The catalog does not select the 1951 trace/distribution-character construction, the 1956 Theorem 6,
a later global local-integrability and regular-set analyticity result, or an explicit formula
theorem. Those are inequivalent roots.

The unresolved choices change the proposition rather than merely its notation:

- connected semisimple, reductive, real, linear, finite-center, or other group hypotheses;
- the continuity, unitarity, irreducibility, quasi-simplicity, admissibility, and Hilbert-space
  conditions on the representation;
- the Haar normalization, test-function space, integrated operator, trace/summability assumptions,
  and construction of the distribution character;
- the regular or quasi-regular locus, analyticity or local-integrability conclusion, and equality
  as distributions, pointwise, or almost everywhere;
- scalar fields, Lie-algebra complexification, centers, central and infinitesimal characters, and
  action/inverse conventions;
- ordered binders, universes, typeclass context, and all degenerate and boundary cases.

Choosing a familiar modern regularity theorem, a compact or finite-dimensional character formula,
or a structure field that stores the desired result would invent, narrow, or assume mathematics
not fixed by the repository record. Section 5 of the rev-5.6 blueprint makes statement ambiguity
and a missing elaborated-expression fingerprint hard blockers. There is consequently no canonical
expression for which minimal imports, fixed context, checked transports, or removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations can be certified. Those mutation
tests are undefined, not passed. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborated under the pinned environment. It checks eight adjacent
interfaces: semisimple Lie algebras, manifold Lie groups, algebraic representations and their
finite-dimensional trace character, Haar measure, local integrability, test functions, and
distributions on open subsets of finite-dimensional real normed spaces. These are possible
substrate only. The algebraic `Representation.character` is not the Harish-Chandra distribution
character, and the distribution API is not already global distribution theory on an arbitrary Lie
group. The probe declares no canonical target, checked transport, or proof body, so its imports
cannot be certified minimal for the absent target.

A bounded repo-local and pinned-mathlib search found no terminal Harish-Chandra character theorem.
The relevant repo-local matches are abstract fields in `THM-M-0063`; that artifact explicitly
records that no concrete Harish-Chandra API is present. These results are discovery evidence only,
not an exhaustive anchor audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink exposed the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0097` | 0 | rank 1114; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided untracked `.lake` symlink existed; base identifiers appear above |
| `git blame -L 712,717 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0097/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `3d344c016e809ef613658d30657f2fe9f710a0820a0d291c30139225abbada87`; no target or proof body declared |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 | only unrelated/abstract repo-local fields and terminology collisions matched; no terminal target located; bounded discovery only |
| `python3 -B Stage1_Instances/THM-M-0097/check_intake.py` | 1 | historical intake replay stops at its assertion that authoritative intake state is `[ ]`; integration now records provisional `[_]`; this known stale-intake failure is not statement evidence |

The finalized JSON blocker was parsed and scoped invariants checked for item identity, null target,
null imports and fingerprints, unchanged debt, four undefined mutation classes, false completion
flags, and the no-self-test boundary. A prohibited declaration scan over the owned Lean probe found
no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration. New-file and
scoped whitespace checks passed.

## Retry Condition And Status Boundary

The intake dependency must be independently reviewed, refreshed where needed, and master-accepted.
Accountable reviewers must also lawfully preserve and hash one immutable primary or authoritative
source, select and independently approve one exact proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and
boundary case. They must fix the group and representation class, distribution-character
construction, Haar and test-function conventions, trace conditions, regular locus, exact
analyticity/local-integrability conclusion, equality notion, scalars, and action conventions.

A later statement run can then encode exactly that approved source model, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, accepted state, statement fingerprint, or proof credit is claimed.
