# THM-M-0412 statement recheck at `f9c6966c4`: blocked

Item: `S56-M-0412-STATEMENT`

Assigned rev-5.6 phase: `statement`. This target-scoped handoff records a fresh source-boundary
decision and pinned Lean surface replay. It adds no mathematical statement or proof content.

Base revision: `f9c6966c4a9f779a85442d309d9a4e6d4bbfe36b` (tree
`153efbfdf2465303d2ee3999dfbd92ee883d6220`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in the Stage1 rev-5.6 slot57 worker clone.

## Decision

The requested deliverable, "Elaborate the exact Lean 4 target with the minimal pinned imports," is
blocked at `exact_source_statement_identity`. The repository still identifies the target only by
the Chinese label `皮尔斯猜想` ("Pierce conjecture"), attribution to Trygve Nagell, year 1948,
and the gloss `某些三次曲线的整数点` ("integer points on certain cubic curves"). It provides no
original-language title, immutable primary publication, theorem/page locator, equation or curve
family, point and parameter domains, ordered binders, hypotheses, conclusion, proof boundary,
correction history, or degenerate cases.

The prerequisite intake remains provisional `[_]`, not master-accepted `[x]`. Rev-5.6 permits
provisional successor preparation, so that is not the first content failure, but it independently
prevents dependency-legal master acceptance. The missing proposition itself makes positive
statement work impossible without inventing mathematics.

No target-semantic input changed after the latest integrated THM-M-0412 handoff at
`cf0d919f2dfc00f3f777e9319188dec0f644d159`. The target manifest, source catalog, Stage0 entry,
intake dossier, execution skill, blueprint guidelines, legacy Lean module, toolchain, dependency
lock, and statement probe are byte-for-byte unchanged. Later commits affect unrelated target
artifacts and scheduler projections only.

The legacy `S1_M_021.lean` module remains ineligible. Its `NagellLutzBranchData` stores the curve
equation, torsion predicate, and conclusions as arbitrary `Prop` fields, while `StatementShape`
assumes source-resolution and audit predicates. It therefore states no concrete arithmetic claim.
Selecting Nagell-Lutz, the Ramanujan-Nagell equation, Markov's equation, Siegel finiteness, a
Pierce-Birkhoff result, or an arbitrary cubic would substitute a different theorem.

Accordingly the canonical human claim, canonical Lean expression, minimal imports, expression and
environment fingerprints, checked transports, and the four required statement mutations remain
undefined. Lifecycle remains `planned`, the provisional intake vector remains `H5 / M4 / R4`, and
the node remains `[ ]`. No statement receipt, worker `[_]`, proof credit, debt change, audit
completion, theorem completion, or master acceptance is claimed.

## Source Boundary

Prior evidence records J. W. S. Cassels, "Trygve Nagell," *Acta Arithmetica* 55 (1990), 109-112,
DOI `10.4064/aa-55-2-109-112`, page 111. It distinguishes Nagell's 1935 finite-order theorem for
`x^3 - A*x - B = y^2` from his 1948 p-adic solution of `x^2 + 7 = 2^n`. The former resembles the
vague cubic gloss but conflicts with the year; the latter matches the year but is not a cubic-curve
claim. Neither is identified as a Pierce conjecture.

A fresh bounded bibliographic recheck used Crossref exact-title/author-year queries, the OpenAlex
author record, and zbMATH author data. Crossref returned unrelated Pierce-Birkhoff results and no
record selecting a Nagell 1948 cubic theorem. The OpenAlex author record lists no 1948 work. zbMATH
reconfirmed the 1935 Nagell-Lutz and 1948 Ramanujan-Nagell distinction but did not select the
catalog identity. Semantic Scholar was rate-limited and general web endpoints timed out. These are
incomplete negative discovery observations, not an absence proof, and receive no source or
statement credit.

## Pinned Lean Surface Replay

`StatementProbe.lean` remains explicitly limited to adjacent Weierstrass-curve APIs. From
`Formalizations/Lean`, this command succeeded against the existing pinned artifacts:

```text
LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean
```

It elaborated six APIs. Stdout was 618 bytes with SHA-256
`52574dd9f0f5feda16279f9af5344d9218c0c6089ce238abe2bcc0c9f2628cbb`; stderr was empty with
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. This proves only
that the adjacent pinned interface is usable; it establishes no target, import minimality,
transport, mutation result, or proof.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and the clean mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink was
reused read-only. No dependency update, build, clone, fetch, or `.lake` mutation was performed.

## Commands And Results

Commands ran from the worker root unless another working directory is stated.

| Command or check | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identities match this report |
| scoped diff from latest target commit `cf0d919f2` through HEAD | 0 | no target-semantic, intake, skill, source, legacy Lean, toolchain, dependency-lock, or probe change |
| independent repository/source inspection plus bounded Crossref, OpenAlex, and zbMATH queries | mixed | no exact source proposition was identified; rate limits/timeouts are preserved and no negative search is treated as exhaustive |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 0 | six adjacent APIs elaborated with the stream sizes and hashes above; no canonical target or proof body |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake identities match those above |
| mathlib package `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean at the immutable revision and tree above |

The companion JSON records the structured results and final invariant, prohibited-construct,
whitespace, scope, and self-test-absence checks. Its recheck format has no published strict schema
or independent validator, so parsing it does not create a node-specific receipt.

## Retry Condition And Status Boundary

Retry after accountable reviewers preserve and hash an immutable primary or approved authoritative
source, reconcile the label, author, and date, and independently approve one exact claim with every
incorporated definition, ordered binder, hypothesis, conclusion, correction, proof boundary, and
degenerate case. A later statement worker can then encode exactly that claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations.

This is current-base target-scoped blocker evidence, not completion of the statement node. Because
the positive deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent.
