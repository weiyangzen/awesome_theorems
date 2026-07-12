# Exact-statement gate: blocked

Item: `S56-M-0852-STATEMENT`

Theorem: `THM-M-0852`

Base revision: `5c38e670073bc890a78e61556f36d2c6b35d257d` (tree
`95a189ecdfe548d9cff4faaebc111079babceb92`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the family label `Hamilton-circle threshold`, a collective twentieth-century
attribution, and the gloss `existence of Hamiltonian cycles in random graphs`. It cites no theorem
and supplies no probability law, formula, ordered binder, hypothesis, conclusion, proof boundary,
correction, erratum, or formal artifact. Stage0 explicitly leaves the precise definitions and
premises open, and the catalog's `verified` label is untrusted under rev-5.6.

The intake identifies three bibliographic leads: Komlos and Szemeredi (1975), Komlos and Szemeredi
(1983), and Posa (1976). Those records are discovery anchors only. No immutable full text, numbered
theorem and page, incorporated definitions, assumptions, proof boundary, corrections, errata, or
independent source review has been admitted. The repository does not select any of them.

Consequently, the repository does not decide:

- whether the model is independent-edge `G(n,p)`, fixed-edge `G(n,m)`, or a coupled random graph
  process;
- whether the root is a one-sided high-probability bound, zero-one or sharp threshold, explicit
  critical-window limit law, or hitting-time equality;
- the vertex type, parameter functions, asymptotic filter, binder order, inequalities, rounding,
  or logarithm convention;
- whether minimum degree, isolated vertices, connectivity, or another event belongs to the root or
  is a proof bridge; or
- the Hamiltonicity convention and treatment of orders zero, one, and two and the endpoint
  probabilities.

These choices produce inequivalent propositions. Selecting the familiar threshold near
`(log n + log log n) / n`, a convenient `G(n,p)` zero-one statement, or any other folklore variant
would invent, weaken, strengthen, or substitute mathematics rather than elaborate the received
target. Deterministic Dirac, Ore, and Chvatal-Erdos criteria and the separately cataloged random-
graph connectivity threshold are also different roots.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves the canonical human claim, Lean module and
expression, minimal imports, and expression/environment fingerprints null at `[H5, M4, R4]`.
Without a canonical target, alternate transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. No
`Statement.lean`, axiom, placeholder, assumed probability theorem, weakened finite example, or
broadened theorem was introduced.

The prerequisite `S56-M-0852-INTAKE` is provisional worker state `[_]`, not master-accepted `[x]`.
Section 10.2 permits this dependency-ordered attempt, so that did not prevent truthful blocker
work, but master acceptance remains independently required before a future statement transition
can be accepted.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its two direct imports
expose `SimpleGraph.IsHamiltonian`, its monotonicity theorem, and the independent-edge measure
`SimpleGraph.binomialRandom` with endpoint laws. All six checks pass. The probe defines no random-
graph sequence, event probability, asymptotic threshold, canonical target, checked source
transport, or proof body. Its imports are therefore substrate imports, not a minimal import set for
an absent target, and receive no statement or proof credit.

A bounded pinned-mathlib search for declarations connecting Hamiltonicity to random graphs or a
threshold returned no match. This is discovery-only feasibility evidence, not the downstream
immutable anchor audit and not a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to the canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0852` | 0 | rank 1034, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| scoped manifest, blueprint, skill, catalog, Stage0, and intake inspection | 0 | only a broad existence gloss is authoritative; every proposition-changing choice remains open |
| `sha256sum` over authority, intake, toolchain, and pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0852/check_intake.py` | 1 | the historical intake checker freezes pre-integration state `[ ]`; current authority records intake `[_]`, and the checker also freezes the original nine-file inventory, so this phase records rather than rewrites that evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | the pinned revision and tree agree with the fingerprint; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0852/IntakeProbe.lean` | 0 | all six adjacent APIs elaborated; complete stdout SHA-256 is `107bb18968e19cd1fb9876483a5cdbf21089569c6d2e8fa88469c0f28740cc7a`; no canonical target was declared |
| bounded Hamiltonicity/random-graph search in pinned mathlib Lean sources | 1 | expected no-match result; discovery only, not an anchor audit |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | identity, open blocked state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| scoped whitespace checks | 0 | no whitespace diagnostics in the two blocker artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
preserve and hash a lawful immutable primary or authoritative source, select and independently
approve one exact proposition, and transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, and boundary case. They must freeze
the graph model, threshold strength, parameterization, asymptotic mode, event relationship, and
Hamiltonicity convention.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. `H5` classifies the supplied catalog wording as not yet one stable proposition;
it does not refute or declare open published random-graph Hamiltonicity results. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
