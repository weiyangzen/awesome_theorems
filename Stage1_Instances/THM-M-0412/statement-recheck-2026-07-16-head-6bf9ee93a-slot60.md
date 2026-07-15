# THM-M-0412 statement recheck: blocked

Item: `S56-M-0412-STATEMENT`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff` (tree
`24acf86e69ab2e6fca9480c6269b6429874ba295`). Rechecked on 2026-07-16
(`Asia/Shanghai`) in worker slot 60.

## Decision

The assigned deliverable, "Elaborate the exact Lean 4 target with the minimal pinned imports,"
remains blocked at `exact_source_statement_identity`. The repository identifies the item only by
the Chinese label `皮尔斯猜想` ("Pierce conjecture"), attribution to Trygve Nagell, year 1948,
and the gloss `某些三次曲线的整数点` ("integer points on certain cubic curves"). It provides no
original-language title, immutable primary publication, theorem/page locator, equation or curve
family, point and parameter domains, ordered binders, hypotheses, conclusion, proof boundary,
correction history, or degenerate cases.

The v2 theorem node has no direct hard parent, transitive hard ancestor, incoming hard edge, reuse
hint, or shared-lemma group. The new `dependency-reuse-ledger.json` records exactly that empty
closure using schema `stage1-dependency-reuse-ledger/1.1`, the supplied theorem-DAG digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`, and dependency-context
digest `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`. The repository's strict
ledger validator accepted the record. An empty dependency context does not prove independence,
identify the proposition, or confer proof or checkbox credit.

The prerequisite intake remains provisional `[_]`, not master-accepted `[x]`, and it deliberately
records unresolved source identity. Rev-5.6 permits provisional successor preparation, so this does
not precede the content failure, but it independently prevents dependency-legal master acceptance.
The missing proposition makes positive statement work impossible without inventing mathematics.

The legacy `S1_M_021.lean` module remains ineligible. It stores its curve equation, torsion
predicate, and conclusions as arbitrary `Prop` fields behind conditional source/audit premises. It
therefore states no concrete arithmetic claim. Selecting Nagell-Lutz, Ramanujan-Nagell, Markov's
equation, Siegel finiteness, Pierce-Birkhoff, or an arbitrary cubic would substitute a different
theorem.

Accordingly the canonical human claim, canonical Lean expression, minimal canonical imports,
expression and environment fingerprints, checked transports, and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations remain undefined. Lifecycle stays
`planned`, the provisional intake vector stays `H5 / M4 / R4`, and this node stays `[ ]`. No node
receipt, worker `[_]`, proof credit, audit completion, theorem completion, or master acceptance is
claimed.

## Source Boundary

A fresh exact-topic repository search found only sparse catalog/intake metadata and the rejected
legacy correction. Its 26-line, 2923-byte output has SHA-256
`ed6cdd6e5afa9075aaa05b4ae97150251c9ed9a753abaa217fab50fd495829e1`; no match supplies an exact
proposition.

Prior evidence records J. W. S. Cassels, "Trygve Nagell," *Acta Arithmetica* 55 (1990), 109-112,
DOI `10.4064/aa-55-2-109-112`, page 111. It distinguishes Nagell's 1935 finite-order theorem for
`x^3 - A*x - B = y^2` from his 1948 p-adic solution of `x^2 + 7 = 2^n`. The former resembles the
vague cubic gloss but conflicts with the year; the latter matches the year but is not the stated
topic. Neither is identified as a Pierce conjecture.

A fresh Crossref query for the exact English label plus Nagell returned Pierce-Birkhoff papers,
Ramanujan-Nagell material, and unrelated records, but no source selecting this target. OpenAlex
returned an unusable response, while general web endpoints timed out. These incomplete discovery
observations are not an absence proof and receive no source or statement credit.

## Pinned Lean Boundary

`StatementProbe.lean` remains explicitly limited to adjacent Weierstrass-curve APIs. From
`Formalizations/Lean`, the following command succeeded against the existing pinned artifacts:

```text
LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean
```

It elaborated six APIs. Stdout was 8 lines and 618 bytes with SHA-256
`52574dd9f0f5feda16279f9af5344d9218c0c6089ce238abe2bcc0c9f2628cbb`; stderr was empty with
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Its single direct
import is the narrow pinned module defining the checked affine-point group instance, but that is
only a minimality observation about this six-check probe. There is no canonical target whose
imports can be minimized.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and the clean mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake`
symlink was reused read-only. No dependency update, build, clone, fetch, or `.lake` mutation was
performed.

## Validation Record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 130 | interrupted after roughly 135 seconds while its nested execution-cron unittest suite remained silent; this is recorded as a failure, not a pass |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 legacy states preserved, 2 hard edges, 5 reuse hints, 310 shared groups, and acyclicity passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` | 1 | its nested validator reported that the checked-in theorem DAG differs from fresh generation after these target-owned evidence files appeared; this pre-integration projection mismatch made no tracked change and is not reported as a pass |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | before edits, only the automation-provided `.lake` symlink was untracked; base identities match this report |
| `python3 -m json.tool` plus `validate_dependency_reuse_ledger` on the new ledger | 0 | schema 1.1 and the exact empty closure passed against the supplied graph and base revision |
| from `Formalizations/Lean`: the `lake env lean` probe above | 0 | six adjacent APIs elaborated with the stream sizes and hashes above; no canonical target or proof body |
| from `Formalizations/Lean`: Lean/Lake versions and mathlib status/revision/tree | 0 | pinned identities match those above; mathlib is clean |

The companion JSON records these results and the final JSON, ledger, invariant,
prohibited-construct, whitespace, ownership-scope, and self-test-absence checks. The recheck format
has no published strict schema or independent validator, so parsing it does not create a
node-specific receipt.

## Retry Condition And Boundary

Retry after accountable reviewers preserve and hash an immutable primary or approved authoritative
source, reconcile the label, author, and date, and independently approve one exact claim with every
incorporated definition, ordered binder, hypothesis, conclusion, correction, proof boundary, and
degenerate case. A later statement worker can then encode exactly that claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four mutation classes.

This is current-base target-scoped blocker evidence, not completion of the statement node. Because
the positive deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent.
