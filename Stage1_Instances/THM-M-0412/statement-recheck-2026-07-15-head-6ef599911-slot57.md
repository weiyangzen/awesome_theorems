# THM-M-0412 statement recheck at `6ef599911`: blocked

Item: `S56-M-0412-STATEMENT`

Assigned rev-5.6 phase: `statement`. This run performs only the source audit needed to decide that
phase and adds no proof content.

Base revision: `6ef59991169993a9ea46509b541072535d616672` (tree
`cd0f8bdbb4fe4928c5fd30a3a8fd59df3d30d58e`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in the Stage1 rev-5.6 slot57 worker clone.

## Decision

The requested deliverable, "Elaborate the exact Lean 4 target with the minimal pinned imports," is
blocked at the first substantive statement gate, `exact_source_statement_identity`. The repository
supplies only the label `皮尔斯猜想` ("Pierce conjecture"), attribution to Trygve Nagell, year
1948, and the gloss `某些三次曲线的整数点` ("integer points on certain cubic curves"). It
supplies no original-language title, immutable primary publication, theorem/page locator, equation
or curve family, domains, parameters, ordered binders, hypotheses, conclusion, correction history,
proof boundary, or degenerate cases.

The intake dependency is provisional `[_]`, not master-accepted `[x]`. Rev-5.6 section 10.2 permits
successor preparation from a self-tested predecessor, so this is not the first worker-level failure.
It does prevent master acceptance until dependency order closes. The independent source-identity
failure makes the requested statement artifact impossible now.

Since the preceding slot57 recheck base `6c6ba6a88ba8abb210744f39722c3aaa0b689925`, the target
manifest, catalog, Stage0 entry, execution skill, intake dossier, legacy Lean module, toolchain,
dependency lock, and statement probe are unchanged. The blueprint and DAG changed only to promote
three unrelated provisional items. The sole new THM-M-0412 input is that preceding recheck pair,
which preserves rather than resolves the missing proposition.

The legacy `S1_M_021.lean` module cannot fill the gap. Its `NagellLutzBranchData` stores the
equation, hypotheses, and conclusions as abstract propositions, while `StatementShape` assumes
source-resolution and audit predicates. It does not encode a concrete arithmetic claim. Choosing
Nagell-Lutz, the Ramanujan-Nagell equation, Markov's equation, Siegel finiteness, an arbitrary
cubic, or another Nagell paper would substitute proposition-changing mathematics.

Accordingly the canonical human claim, Lean expression, minimal imports, expression hash,
environment fingerprint, checked transports, and all four mutation classes remain undefined. The
item stays `[ ]`, lifecycle stays `planned`, and the provisional intake projection stays
`H5 / M4 / R4`. No statement receipt, worker `[_]`, proof, audit completion, theorem completion,
debt change, or master acceptance is claimed.

## Source Boundary

The prior bounded audit records J. W. S. Cassels, "Trygve Nagell," *Acta Arithmetica* 55 (1990),
109-112, DOI `10.4064/aa-55-2-109-112`, page 111. Cassels distinguishes a 1935 finite-order result
for `x^3 - A*x - B = y^2` from Nagell's 1948 p-adic solution of `x^2 + 7 = 2^n`. The former fits
the vague cubic gloss but not the year; the latter fits the year but not the gloss. Neither is
identified there as a Pierce conjecture. The related 1950 Nagell cubic paper recorded by the prior
audit likewise does not reconcile the name and date or expose an exact target claim.

Current repository inspection and an independent worker probe found no new identity. A bounded
Crossref exact-topic check likewise returned no matching Nagell claim; unrelated Pierce-Birkhoff
records receive no credit. These are incomplete negative discovery observations, not an absence
proof. No external file was retained or added as a dependency.

## Pinned Lean Surface Replay

`StatementProbe.lean` remains only an adjacent-interface probe. From `Formalizations/Lean`, this
command succeeded against the existing pinned artifacts:

```text
LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean
```

It elaborated six `WeierstrassCurve` APIs. Stdout was 618 bytes with SHA-256
`52574dd9f0f5feda16279f9af5344d9218c0c6089ce238abe2bcc0c9f2628cbb`; stderr was empty with
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. This confirms only
that the pinned environment is usable. It receives no canonical-target, import-minimality,
transport, anchor-audit, or proof credit.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and the clean mathlib
package revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

## Commands And Results

| Command or check | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21; planned; legacy slot `S1-M-021`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identities matched this record |
| scoped `git diff --name-status 6c6ba6a88ba8abb210744f39722c3aaa0b689925..HEAD` | 0 | no target-semantic or Lean-environment input changed; three unrelated scheduler states and the preceding target recheck pair were integrated |
| exact-topic repository/source inspection by the main worker and an independent worker | 0 | sparse metadata and the ineligible abstract legacy candidate were confirmed; no exact proposition was found |
| bounded Crossref exact-topic and Nagell 1947-1949 queries; attempted OpenAlex and Wikipedia API checks | mixed | Crossref returned generic or unrelated records and only a 1949 Nagell paper on indefinite binary quadratic forms; OpenAlex rate-limited and Wikipedia timed out; no result received statement credit |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 0 | six adjacent APIs elaborated; stream sizes and hashes are recorded above; no canonical target, transport, or proof body |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake identities recorded above |
| mathlib package status and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package clean at the recorded immutable revision and tree |
| JSON parse and target-scoped invariant assertions for the companion recheck | 0 | blocked/open state, current base, null target fields, unchanged vector, exact two-file scope, and absent self-test agreed |
| prohibited-construct scan of owned Lean files | 1 (expected) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` match |
| scoped whitespace checks and `test ! -e .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; completion self-test intentionally absent |

The companion JSON records structured results. The recheck format has no published strict repository
schema or independent validator; JSON parsing and local assertions do not turn this blocker into a
node-specific receipt.

## Retry Condition And Status Boundary

Retry after accountable reviewers preserve and hash an immutable primary or approved authoritative
source, reconcile the label, author, and date, and independently approve one exact claim with every
incorporated definition, binder, hypothesis, conclusion, correction, proof boundary, and degenerate
case. A statement worker can then encode that same claim, minimize its pinned imports, serialize and
hash its elaborated expression and environment, compile every credited transport, and run the
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.

This is a current-HEAD target-scoped blocker handoff, not a completed statement node. Because the
positive deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent and no
worker `[_]` state is requested.
