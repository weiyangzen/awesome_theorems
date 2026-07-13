# THM-M-0934 exact-statement gate: blocked

- Item: `S56-M-0934-STATEMENT`
- Base revision: `d66b6e80968b53d5b99774584721ae8976f303a5`
- Base tree: `aaa82721074fccea81033a9a18d21652af89f8e4`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog input is the name Erdős-Heilbronn conjecture, the Paul Erdős/Hans Heilbronn
attribution, the year 1964, and the gloss `子集和的大小下界` (a lower bound for the size of subset
sums). It gives no bibliography or binder-complete proposition, and Stage0 explicitly leaves the
definitions and premises open. The catalog's `已验证` label is untrusted inventory metadata under
rev-5.6.

The intake established that the gloss has several proposition-changing readings:

1. all sums of all subsets of one finite set;
2. the conventional restricted self-sumset of two distinct elements of one set in `ZMod p`;
3. the later restricted two-set theorem, with `a ∈ A`, `b ∈ B`, and `a ≠ b`; and
4. the general fixed-cardinality `h`-fold Dias da Silva-Hamidoune theorem.

These statements have different binders, domains, hypotheses, bounds, endpoint conventions, and
proof ownership. Even the conventional self-sum candidate still requires decisions about prime
and positivity premises, `Finset` versus finite `Set`, the encoding of distinct pairs, natural
subtraction at cardinalities zero and one, the modulus cap, and every degenerate case. The
neighboring target `THM-M-0935` separately owns the Dias da Silva-Hamidoune proof/generalization,
so this phase may not silently merge their roots or receipts.

The immutable secondary survey inspected at intake distinguishes the one-set result from the later
two-set theorem and says that the conjecture did not occur in the catalog-associated 1964 paper.
That is useful source discrimination, not an independently approved primary statement. Selecting
the familiar formula `min(p, 2 * |A| - 3)` now would therefore invent missing source identity and
scope rather than elaborate the exact received theorem.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake correctly leaves the canonical human statement,
Lean module and expression, minimal target import set, expression hash, and canonical-target
environment fingerprint null at `[H1, M4, R4]`. Checked alternate transports and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined
rather than passed. No `Statement.lean`, assumed proposition, weakened special case, broadened
generalization, axiom, placeholder, or proof body was introduced.

The prerequisite `S56-M-0934-INTAKE` is only provisional worker state `[_]`. Its receipt declares
`accepted: false`, is not content-addressed, supplies no accepted receipt ID, and leaves the target
null. That independently prevents an accepted statement transition.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was freshly replayed against the pinned environment. It
imports `Mathlib.Combinatorics.Additive.SubsetSum` and
`Mathlib.Combinatorics.Additive.CauchyDavenport` and elaborates:

- `Finset.subsetSum` and `Finset.mem_subsetSum_iff`, which concern sums of all subsets;
- generic `Finset.product`, `filter`, `image`, and `image₂` encoding infrastructure; and
- `ZMod.cauchy_davenport` and `cauchy_davenport_minOrder_add`, which concern unrestricted sumsets.

The printed axiom set for the neighboring `ZMod.cauchy_davenport` theorem is `propext`,
`Classical.choice`, and `Quot.sound`. None of these declarations states the restricted-sumset
target, and the probe defines no THM-M-0934 statement, checked source transport, or proof body. Its
two direct imports are candidate-interface imports, not certified minimal imports for an absent
canonical target. A bounded exact-topic search over pinned mathlib and shared repo-local Lean found
no obvious Erdős-Heilbronn, Dias da Silva-Hamidoune, or restricted-sumset declaration; this is
narrow discovery evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No dependency
update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless another working directory is shown. Exact arguments, exits, and input hashes are also
preserved in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0934` | 0 | rank 1473; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree appear above |
| current `sha256sum` over authority, source, intake, toolchain, lockfile, and pinned additive-combinatorics inputs | 0 | hashes agree with the structured blocker |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| mathlib revision, tree, and status checks | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b`, clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0934/IntakeProbe.lean` | 0 | eight adjacent APIs and one axiom diagnostic elaborated; output 1,209 bytes on 13 lines; SHA-256 `bc7531f36eabfcdc2abbe6f70ff91456074739c0cb44a86cc84d4e483d60f2f3` |
| bounded exact-topic `rg` in pinned mathlib and shared repo-local Lean | 1 (expected no match) | no obvious exact declaration was located; no target identity or global absence is inferred |
| `python3 -B Stage1_Instances/THM-M-0934/check_intake.py` | 1 | historical intake checker stops because it hardcodes authoritative intake state `[ ]` while integration now records provisional `[_]`; intake history was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-0934/statement-blocker.json` plus scoped blocker assertions | 0 | valid JSON; identity, null target/imports, four undefined mutations, unchanged vector, false completion fields, two-file scope, and blocked state agree |
| token-anchored prohibited-declaration scan over owned Lean | 1 (expected no match) | no prohibited proof escape or bodyless/unsafe declaration was found |
| scoped tracked and new-file whitespace checks | 0 for diagnostics | no whitespace error in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test packet intentionally absent because the exact-statement deliverable did not pass |

A blocked-run artifact check is not a statement-node self-test. The passing Lean probe confirms only
the neighboring pinned API surface described above.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable source and
additive-combinatorics reviewers must then preserve and hash an immutable exact primary or approved
authoritative statement, identify its historical and proof-source roles, independently approve the
complete definition, premise, conclusion, correction, erratum, and proof-boundary crosswalk, and
resolve ownership with `THM-M-0935`. They must select all-subset versus restricted addition,
one-set versus two-set versus `h`-fold scope, the ambient carrier, set and distinctness encoding,
arithmetic convention, ordered binders, sharpness boundary, and every degenerate case.

A fresh statement worker can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master
acceptance is claimed.
