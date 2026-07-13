# Exact-statement gate: blocked

Item: `S56-M-1589-STATEMENT`

Theorem: `THM-M-1589`

Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
`a5488edccb2687c4ff0bbdccf4650e06b2e45337`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1589-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
attempt, so pending master acceptance did not prevent the investigation. The intake receipt is
non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and intentionally
leaves the canonical mathematical statement and Lean target null. Master acceptance remains
required before any eventual accepted statement transition.

Independently, the exact-statement gate cannot pass from the authoritative repository record. It
supplies only the title `线性码`, an attribution to many twentieth-century mathematicians, and the
noun phrase `线性纠错码` (linear error-correcting codes). It gives no cited truth-valued
proposition, formula, definition chain, ordered binder, hypothesis, conclusion, proof boundary,
correction history, or boundary case. Stage0 explicitly leaves the precise definitions and
premises open, and rev-5.6 treats the catalog's `已验证` label as untrusted metadata.

The inspected Guruswami coding-theory notes confirm rather than resolve the ambiguity. They
separate a linear-code definition from generator-matrix encoding, systematic form, parity-check
kernel representation, minimum distance as minimum nonzero weight, dependent-column distance,
and dual-code results. An encoder/decoder correctness or error-correction theorem would add yet
another distinct target. The catalog selects none of these.

It also fixes no scalar field; coordinate, word, or code representation; row/column matrix
orientation; block length, dimension, or rank convention; distance, duality, encoding, or decoding
surface; ordered binders; exact conclusion; or zero-size and other degenerate cases. Selecting one
familiar theorem, conjoining several, or presenting a submodule definition as a theorem would
invent, narrow, broaden, or substitute mathematics rather than elaborate the exact received
target. The neighboring Hamming, Singleton, Gilbert-Varshamov, cyclic, BCH, Reed-Solomon, and
Stage0-only duality records supply no authority or transferable proof credit.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. There is consequently no honest canonical expression for which minimal
imports, checked transports, or removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. Those mutations are undefined, not passed. The root
vector remains `[H5, M4, R4]`. No `Statement.lean`, declaration, axiom, placeholder, weakened
special case, or broadened interface was added.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment. Its two
direct imports expose eight generic Hamming-distance, Hamming-weight, submodule, matrix, and
matrix-vector interfaces. All checks pass. This is real substrate validation, but the probe defines
no finite-field linear code, source-selected proposition, canonical target, checked transport, or
proof body. Its imports therefore cannot be certified minimal for an absent target.

A bounded lexical search of pinned mathlib and repository-local Lean found generic uniquely
decodable-code prose but no source-selected linear-code declaration under the recorded terms. This
is discovery-only feasibility evidence, not the downstream immutable anchor audit or a claim of
global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1589` | 0 | rank 1210; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| catalog, Stage0, intake dossier, source lead, and neighboring-target inspection | 0 | confirmed the code-class noun phrase, inequivalent theorem families, null intake target, and absence of an approved root selection |
| `sha256sum` over authority, source, intake, probe, toolchain, and pinned mathlib inputs | 0 | exact current hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-1589/check_intake.py` | 1 | historical intake replay stops at `stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1589/IntakeProbe.lean` | 0 | eight generic APIs elaborated; stdout SHA-256 `4856b69b...9492`; no canonical target or proof body |
| bounded linear-code search in pinned mathlib and repo-local Lean | 0 | only generic uniquely decodable-code prose matched; no source-selected target declaration was located |
| prohibited-declaration scan over owned Lean files | 1 | expected no-match result; none of the prohibited declarations or proof escapes was found |

The historical intake checker freezes the pre-integration blueprint and execution-DAG hashes and
its original nine-file intake inventory. This statement run records that limitation instead of
rewriting the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before accepting a future
statement transition. Accountable reviewers must preserve and hash an immutable primary or
authoritative source, select or correct one exact truth-valued linear-code proposition, and
independently approve every incorporated definition, ordered binder, hypothesis, conclusion, proof
boundary, correction, erratum, and degenerate case while preserving neighboring-target boundaries.
They must fix the field, word and code representation, matrix convention, and the exact generator,
parity-check, dimension/cardinality, distance, systematic-form, duality, or decoder surface.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
