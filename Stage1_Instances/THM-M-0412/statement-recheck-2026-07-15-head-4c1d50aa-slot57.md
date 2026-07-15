# THM-M-0412 statement recheck at `4c1d50aa`: blocked

Item: `S56-M-0412-STATEMENT`

Assigned rev-5.6 phase: `statement`. This run performs only the source audit needed to decide that
phase and adds no proof content.

Base revision: `4c1d50aa6552eb6ec56338a663a5dff79a4ae2e3` (tree
`e38ee217e0bb768c5c915905d1d0b04fc89e25f2`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in the Stage1 rev-5.6 slot57 worker clone.

## Decision

The requested deliverable, "Elaborate the exact Lean 4 target with the minimal pinned imports," is
blocked at the first substantive statement gate, `exact_source_statement_identity`. The repository
supplies only the label `皮尔斯猜想` ("Pierce conjecture"), attribution to Trygve Nagell, year
1948, and the gloss `某些三次曲线的整数点` ("integer points on certain cubic curves"). It
supplies no original-language title, immutable primary publication, theorem/page locator, equation
or curve family, domains, parameters, ordered binders, hypotheses, conclusion, correction history,
proof boundary, or degenerate cases.

The intake dependency is in provisional state `[_]`, not master-accepted state `[x]`. This is not
by itself the worker-level blocker: rev-5.6 section 10.2 and the scheduler permit provisional
successor preparation from a self-tested predecessor. It does prevent master acceptance of this
node until dependency order is closed. This worker used that permission to recheck the statement
surface; the independent source-identity failure is what makes the requested artifact impossible.

Since the preceding recheck base `d44ed2b11fb201a761afad9b133caa8bc97fd710`, the target manifest,
catalog, Stage0 entry, execution skill, intake dossier, legacy Lean module, toolchain, dependency
lock, and statement probe are unchanged. Blueprint and execution-DAG edits concern four unrelated
target states. The only new THM-M-0412 inputs are the integrated preceding recheck artifacts, which
preserve rather than resolve the missing proposition.

The legacy `S1_M_021.lean` module cannot fill the gap. Its `NagellLutzBranchData` stores the
equation, hypotheses, and conclusions as abstract propositions, while `StatementShape` assumes
source-resolution and audit predicates. It does not encode a concrete arithmetic claim. Choosing
Nagell-Lutz, the Ramanujan-Nagell equation, Markov's equation, Siegel finiteness, an arbitrary cubic,
or another Nagell paper would substitute proposition-changing mathematics.

Accordingly the canonical human claim, Lean expression, minimal imports, expression hash,
environment fingerprint, checked transports, and all four mutation classes remain undefined. The
item stays `[ ]`, lifecycle stays `planned`, and the provisional intake projection stays
`H5 / M4 / R4`. No statement receipt, worker `[_]`, proof, audit completion, theorem completion,
debt change, or master acceptance is claimed.

## Bibliographic Recheck

A current-run publisher scan gives stronger evidence that the catalog metadata conflates different
Nagell results, but it does not tell us which proposition this target was intended to denote. J. W.
S. Cassels, "Trygve Nagell," *Acta Arithmetica* 55 (1990), 109-112, DOI
`10.4064/aa-55-2-109-112`, distinguishes on page 111:

- a 1935 result for `x^3 - A*x - B = y^2`: a finite-order rational point `(a,b)` has integral
  coordinates and either `b = 0` or `b^2` divides `4*A^3 - 27*B^2`; and
- Nagell's 1948 p-adic solution of `x^2 + 7 = 2^n`, now called the Ramanujan-Nagell equation.

Thus the first result fits the vague cubic gloss but not the year, while the second fits the year
but not the cubic gloss. Neither is called a Pierce conjecture there. The publisher PDF was fetched
only for this bounded source audit; its 723084-byte content had SHA-256
`11a7d9597383ab3e024bd04bbca03aebdb84ae1955a8eccbced274ccd2dff0dc` and was not retained or
added as a dependency.

OpenAlex's quoted `"Pierce conjecture"` search returned seven unrelated works, and the exact
Crossref author/year query returned no Trygve Nagell record for 1948. A related record is Trygve
Nagell, "Über die Anzahl der Lösungen gewisser diophantischer Gleichungen dritten Grades,"
*Mathematische Zeitschrift* 52 (1950), 750-757, DOI `10.1007/BF02230731`. Its date conflicts with
1948, it does not explain the "Pierce" label, and the queried metadata exposes no exact theorem,
equation, quantifier structure, or hypotheses. It too is only a discovery lead.

No exact theorem or equation satisfying all repository fields was recovered. Search incompleteness
is preserved: these negative query results are not an absence proof and receive no source-fidelity
or statement credit.

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
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and the clean
mathlib package revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

## Commands And Results

| Command or check | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21; planned; legacy slot `S1-M-021`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identities matched this record |
| exact scoped `git diff --name-status` commands recorded in the companion JSON | 0 | no target manifest, catalog, Stage0, skill, intake, legacy Lean, toolchain, dependency-lock, or probe change; blueprint/DAG changes were unrelated; the preceding recheck pair was integrated |
| exact scoped `rg ... | sha256sum` command recorded in the companion JSON | 0 | matches remained sparse metadata, blocker records, or the rejected legacy correction; no exact proposition was found; output SHA-256 `fa4c9e5327f2a21aa4bec8fd8f1d60441efb203919602b8b5ed2b43db3891db4` |
| exact `curl`/`pdftoppm` command recorded in the companion JSON | 0 | publisher PDF page 111 separates a 1935 cubic/torsion theorem from the 1948 Ramanujan-Nagell equation; PDF SHA-256 `11a7d959...f0dc`, rendered-page SHA-256 `2e076ddb...ed3f` |
| exact OpenAlex and Crossref `curl`/`jq` commands recorded in the companion JSON | 0 | the quoted search yielded no relevant result and the exact author/year query yielded no 1948 Nagell record; the 1950 cubic-equation paper remains an unselected lead |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 0 | six adjacent APIs elaborated; stream sizes and hashes are recorded above; no canonical target, transport, or proof body |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake identities recorded above |
| mathlib package status and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package clean at the recorded immutable revision and tree |
| JSON parse and target-scoped invariant assertions for the companion recheck | 0 | blocked/open state, current base, null target fields, unchanged vector, exact two-file scope, and absent self-test agreed |
| prohibited-construct scan of owned Lean files | 1 (expected) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` match |
| scoped whitespace checks and `test ! -e .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; completion self-test intentionally absent |

The companion JSON records the structured command results. The recheck format has no published
strict repository schema or independent validator; JSON parsing and local assertions do not turn
this blocker into a node-specific receipt.

## Retry Condition And Status Boundary

Retry after accountable reviewers preserve and hash an immutable primary or approved authoritative
source, reconcile the label, author, and date, and independently approve one exact claim with every
incorporated definition, binder, hypothesis, conclusion, correction, proof boundary, and degenerate
case. A statement worker can then encode that same claim, minimize its pinned imports, serialize and
hash the elaborated expression and environment, compile every credited transport, and run the
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.

This is a current-HEAD target-scoped blocker handoff, not a completed statement node. Because the
positive deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent and no
worker `[_]` state is requested.
