# THM-M-0412 statement recheck at `6c6ba6a88`: blocked

Item: `S56-M-0412-STATEMENT`

Assigned phase: `statement`. This handoff contains only the source-boundary and pinned Lean-surface
checks needed to decide that phase. It adds no mathematical statement or proof content.

Base revision: `6c6ba6a88ba8abb210744f39722c3aaa0b689925` (tree
`b9a939605d30dd3e029c1cba892d8b47439b500f`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in the rev-5.6 slot57 worker clone.

## Decision

The requested deliverable, "Elaborate the exact Lean 4 target with the minimal pinned imports," is
blocked at `exact_source_statement_identity`. The repository identifies the target only by the
Chinese label `皮尔斯猜想` ("Pierce conjecture"), Trygve Nagell, the year 1948, and the gloss
`某些三次曲线的整数点` ("integer points on certain cubic curves"). It does not provide an
original-language title, immutable primary publication, theorem/page locator, equation or curve
family, domains, parameters, ordered binders, hypotheses, conclusion, proof boundary, correction
history, or degenerate cases.

The intake dependency remains provisional `[_]`, rather than master-accepted `[x]`. Section 10.2
allows provisional preparation of a successor, so this is not the first worker-level failure, but
it prevents dependency-legal master acceptance. The missing proposition itself makes the positive
statement deliverable impossible.

Since the preceding slot57 recheck base `a1ba351e42fd9eefe315119ef09c0b958358bb8e`, the target
manifest, catalog, Stage0 entry, execution skill, intake dossier, legacy Lean module, toolchain,
dependency lock, and statement probe are unchanged. Blueprint and DAG edits concern three unrelated
target states. The only new THM-M-0412 input is the integrated preceding recheck pair, which
preserves rather than resolves the blocker.

The legacy `S1_M_021.lean` module is not a substitute. Its `NagellLutzBranchData` represents the
equation, hypotheses, and conclusions by abstract proposition fields, while `StatementShape`
assumes source-resolution and audit predicates. It therefore states no concrete arithmetic claim.
Choosing Nagell-Lutz, Ramanujan-Nagell, Markov's equation, Siegel finiteness, an arbitrary cubic, or
one selected Nagell paper would silently change the proposition.

Accordingly the canonical human statement, formal target, minimal imports, elaborated-expression
hash, environment fingerprint, checked transports, and four required mutation classes remain
undefined. The item remains `[ ]`, lifecycle remains `planned`, and the provisional intake vector
remains `H5 / M4 / R4`. No statement receipt, worker `[_]`, proof credit, audit completion, theorem
completion, debt change, or master acceptance is claimed.

## Source Boundary

The fresh bounded public recheck used exact English and Chinese Bing RSS queries, a Trygve Nagell
1947-1949 Crossref query, and a Crossref query for Pierce conjecture plus cubic. Results were
nonpertinent. Crossref returned one Nagell-authored 1949 paper on indefinite binary quadratic forms
and no 1948 Nagell record; the broader query surfaced unrelated Pierce-Birkhoff work and Selmer's
1954 conjecture on rational points on cubic curves. OpenAlex and Semantic Scholar returned rate-limit
errors, Google Books timed out, and the attempted zbMATH endpoint form returned a bad-request
response. These negative, partial, and failed searches are not an absence proof and receive no
statement or source-fidelity credit.

The prior source audit records Cassels, "Trygve Nagell," *Acta Arithmetica* 55 (1990), 109-112,
DOI `10.4064/aa-55-2-109-112`, page 111. It distinguishes a 1935 finite-order theorem for the cubic
`x^3 - A*x - B = y^2` from Nagell's 1948 p-adic solution of `x^2 + 7 = 2^n`. The former fits the
vague cubic gloss but not the year; the latter fits the year but not the gloss. Neither is identified
there as a Pierce conjecture, so neither selects the target.

## Pinned Lean Replay

`StatementProbe.lean` remains deliberately limited to adjacent Weierstrass-curve APIs. From
`Formalizations/Lean`, the following command succeeded against the existing pinned artifacts:

```text
LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean
```

It elaborated six APIs. Stdout was 618 bytes with SHA-256
`52574dd9f0f5feda16279f9af5344d9218c0c6089ce238abe2bcc0c9f2628cbb`; stderr was empty with
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
This proves only that the adjacent pinned interface is usable. It gives no canonical-target,
import-minimality, transport, anchor-audit, or proof credit.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and the clean mathlib
package revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink was reused
without dependency mutation. No update, build, clone, or fetch command ran.

## Commands And Results

| Command or check | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identities matched this record |
| scoped diff from `a1ba351e42fd9eefe315119ef09c0b958358bb8e` to HEAD | 0 | target-semantic and Lean-environment inputs were unchanged; only three unrelated blueprint/DAG states and the preceding recheck pair were added |
| exact-topic Bing RSS and Crossref inspection; attempted OpenAlex, Semantic Scholar, Google Books, and zbMATH calls | mixed | no exact proposition found; incomplete or failed services were preserved and no result received statement credit |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 0 | six adjacent APIs elaborated with stream sizes and hashes recorded above; no canonical target or proof body |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake identities recorded above |
| mathlib package status and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package clean at the immutable revision and tree recorded above |
| `python3 -m json.tool` plus target-scoped assertions for the companion record | 0 | blocked/open state, base, null target fields, vector, undefined mutations, two-file scope, and absent self-test agree |
| prohibited-construct scan of owned Lean files | 1 (expected) | no prohibited Lean declaration or proof shortcut matched |
| scoped whitespace checks and `test ! -e .stage1-worker-selftest.json` | 0 | no whitespace errors; completion self-test intentionally absent |

The companion JSON is structured blocker evidence, but no strict repository schema or independent
validator is published for its format. Parsing and local assertions do not turn it into a
node-specific completion receipt.

## Retry Condition

Retry after accountable reviewers preserve and hash an immutable primary or approved authoritative
source, reconcile the label, author, and date, and independently approve one exact claim with all
incorporated definitions, binders, hypotheses, conclusion, corrections, proof boundary, and
degenerate cases. Then encode precisely that claim, minimize its pinned imports, hash its elaborated
expression and environment, compile every credited transport, and run the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations.

This is current-HEAD target-scoped blocker evidence. Because the assigned phase was not genuinely
self-tested, `.stage1-worker-selftest.json` is intentionally absent.
