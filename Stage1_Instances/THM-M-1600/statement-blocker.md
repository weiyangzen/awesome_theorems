# Exact-statement gate: blocked

Item: `S56-M-1600-STATEMENT`

Theorem: `THM-M-1600`

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30` (tree
`3f567e7f76b189432b73444354070c0ff75925b9`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the title `零知识证明`, the Goldwasser/Micali/Rackoff attribution, the year 1985,
and the gloss `不泄露信息的证明` (a proof that leaks no information). It contains no cited proposition,
definition chain, ordered binders, hypotheses, conclusion, proof boundary, correction history, or
boundary cases. Stage0 explicitly leaves the exact definitions and premises, proof route,
alternate forms, axioms, formal status, and artifacts open. The catalog's `已验证` label is untrusted
metadata under rev-5.6.

The primary source family confirms rather than resolves the ambiguity. The inspected 1989 journal
version of Goldwasser, Micali, and Rackoff's *The Knowledge Complexity of Interactive Proof
Systems* contains materially different possible roots:

- Section 3.3 defines perfect, statistical, and computational zero knowledge and zero-knowledge
  proof systems;
- Theorem 1 states that the displayed quadratic-residuosity protocol is perfectly zero knowledge;
- Theorem 2 states that the displayed quadratic-nonresiduosity protocol is statistically zero
  knowledge; and
- the paper discusses a later assumption-dependent all-NP result, whose exact GMW statement is a
  separate source and catalog boundary.

The repository selects none of these. It also leaves open the language or relation, protocol and
interaction model, honest or malicious verifier, auxiliary input, simulated view, simulator and
adversary classes, perfect/statistical/computational comparison, security and complexity
parameters, completeness and soundness contract, quantifier order, and every malformed, empty,
zero-round, probability-endpoint, and number-theory case. These choices yield inequivalent
propositions. Selecting a familiar definition, QR or QNR theorem, GMW theorem, toy protocol, or
modern zero-knowledge result would invent, narrow, broaden, or substitute mathematics rather than
elaborate the exact received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake therefore correctly leaves the canonical statement, Lean
module and expression, and canonical-target expression/environment fingerprints null at
`[H5, M4, R4]`. Without one source-selected proposition, no import set can be certified minimal,
no alternate encoding can receive a checked transport, and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than
passed. No `Statement.lean`, axiom, placeholder, assumed security property, weakened special case,
or broadened theorem was introduced.

The prerequisite `S56-M-1600-INTAKE` currently has provisional worker state `[_]`, not
master-accepted state `[x]`. Its receipt is non-content-addressed, declares `accepted: false`, and
has no accepted receipt ID. Rev-5.6 section 10.2 permits this dependency-ordered statement attempt,
but dependency acceptance remains necessary before any future statement transition can be master
accepted. Independently, the first substantive failure is the absent exact source-statement and
definition-versus-theorem selection.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment. Its four
direct imports expose six generic formal-language, deterministic polynomial-time, probability-mass,
and superpolynomial-decay interfaces. All checks pass. The probe defines no interactive
probabilistic machine, protocol, verifier view, simulator, distribution-indistinguishability
relation, zero-knowledge predicate, canonical target, checked transport, or proof body. Its imports
therefore cannot be certified minimal for an absent target and receive no statement, anchor, or
proof credit.

A bounded lexical search of pinned mathlib and repository-local Lean found no declaration matching
zero knowledge, knowledge complexity, interactive protocol, or computational indistinguishability
under the recorded terms. This is discovery-only feasibility evidence, not the downstream immutable
anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` link to the canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1600` | 0 | rank 1220; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided untracked `.lake` link existed; the base revision and tree are recorded above |
| source, Stage0, intake dossier, and inspected GMR source-family review | 0 | confirmed the slogan is not one proposition, the source family contains inequivalent definitions and results, and no approved root was selected |
| `sha256sum` over authority, source, intake, probe, toolchain, manifest, and pinned mathlib inputs | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1600/IntakeProbe.lean` | 0 | six generic APIs elaborated; complete stdout SHA-256 `bd87c72a...dba5`; no canonical target or proof body |
| bounded zero-knowledge search in pinned mathlib and repo-local Lean | 1 | expected no-match exit; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-1600/check_intake.py` | 1 | historical intake replay stops at its stale pre-integration blueprint hash; its original nine-file inventory is also historical after this phase |
| prohibited-construct scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The historical intake checker freezes its original authority hashes and nine-file intake inventory.
Integration subsequently changed the generated blueprint and execution DAG. Adding these statement
artifacts also makes that intake-only inventory historical. This run records the limitation instead
of rewriting the intake checker, intake receipt, instance, task DAG, generated blueprint, or
authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
preserve and hash one immutable primary or approved authoritative source, select and independently
approve one exact truth-valued zero-knowledge result, distinguish definition from theorem, and
transcribe every incorporated definition, convention, ordered binder, hypothesis, conclusion,
proof boundary, correction, erratum, and degenerate case while preserving neighboring-target
boundaries.

A fresh statement worker can then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the vector remains `[H5, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
