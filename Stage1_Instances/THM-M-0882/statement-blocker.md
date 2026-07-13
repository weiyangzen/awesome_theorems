# THM-M-0882 exact-statement gate: blocked

- Item: `S56-M-0882-STATEMENT`
- Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`
- Base tree: `018557070da18ea1733a82de81a238750c59aa84`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete authoritative repository wording is the family label `Margulis构造` (Margulis
construction), the 1973 attribution, and the gloss `扩展图的显式构造`, literally "explicit
construction of expander graphs." This does not determine one proposition with fixed definitions,
ordered binders, hypotheses, and conclusion.

The strongest intake lead is G. A. Margulis, "Explicit constructions of concentrators,"
*Problemy Peredachi Informatsii* 9(4) (1973), 71-80, translated in *Problems of Information
Transmission* 9 (1973), 325-332. It is a bibliographic discovery lead only: the catalog does not
cite it, no immutable edition or exact theorem locator is admitted, and the definitions, theorem
text, translation comparison, proof boundary, corrections, errata, and independent source review
remain open. The source's concentrator result cannot silently be replaced by a familiar later
expander formulation.

In particular, the record does not select among these inequivalent roots:

- the original 1973 explicit bounded-concentrator construction;
- a degree-eight undirected Margulis graph on `(ZMod n) x (ZMod n)`;
- a Margulis-Gabber-Galil family with uniform vertex or edge expansion; or
- a conductance or spectral-gap theorem for a named graph family.

It also fixes no graph or network category, carrier and modulus restrictions, affine generators and
their inverses, loop or parallel-edge convention, regularity degree, expansion or concentration
predicate, normalization and constant, subset range, family quantifiers, explicitness guarantee,
or boundary cases. Choosing any of these would invent or substitute proposition-changing
mathematics. The 1982 Margulis short-cycle construction and the neighboring targets
`THM-M-0881`, `THM-M-0883`, `THM-M-0884`, `THM-M-0885`, and `THM-M-0886` are explicitly separate
and transfer no statement credit.

Rev-5.6 permits this provisional later-node attempt, but its prerequisite intake remains worker
state `[_]`: its receipt declares `accepted: false`, is not content-addressed, and has no accepted
receipt ID. That independently prevents accepted closure. The first failed statement gate is exact
source-statement identity and definition freeze. Intake deliberately keeps the canonical human
claim, Lean module and expression, expression hash, target-environment fingerprint, binders,
hypotheses, and alternate encodings null or empty. Sections 5 and 5.1 make that ambiguity and the
missing expression fingerprint hard blockers.

With no canonical target, minimal imports and the removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than failed Lean tests. No
`Statement.lean`, proof body, weakened special case, broadened theorem, or circular predicate was
added. The lifecycle stays `planned` and the vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` re-elaborates with the direct imports
`Mathlib.Combinatorics.SimpleGraph.AdjMatrix` and `Mathlib.Data.ZMod.Basic`. It checks nine adjacent
simple-graph, neighborhood, regularity, adjacency-matrix, and modular-arithmetic interfaces. All
nine elaborate in the pinned environment; the complete output is 749 bytes with SHA-256
`55cab969a7e67bc850ca79447645580452dcf6808fc6429ff0783c9c3f7592c9`.

This is real adjacent-substrate validation, but the probe defines no source-selected Margulis graph,
concentrator or expansion predicate, canonical target, checked source transport, or proof body. Its
imports therefore cannot be certified as minimal for an absent target and receive no statement or
proof credit. A bounded exact-topic search found no Margulis, graph-expander, concentrator, or named
expansion target in pinned mathlib or repository-local Lean. This is discovery-only evidence, not
the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Exact executable
validation arguments and results and current input hashes are preserved in
`statement-blocker.json`; its scoped inspection and hashing entries explicitly enumerate their
input paths. That JSON is a worker blocker report, not a node receipt or accepted state.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0882` | 0 | rank 1434; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, guidelines, manifest, catalog, Stage0 record, execution DAG, and complete intake dossier | 0 | confirmed provisional dependency state, null target, inequivalent candidate roots, and unresolved proposition-defining inputs |
| recorded `sha256sum` over authority, source, intake, toolchain, lockfile, and directly imported mathlib sources | 0 | current digests are recorded in the structured blocker |
| `python3 -B Stage1_Instances/THM-M-0882/check_intake.py` | 1 | historical intake replay stopped at line 140 because the integrated authority now records intake `[_]` while the worker-time checker froze `[ ]`; this phase did not rewrite historical evidence |
| pinned Lean, Lake, and mathlib revision/tree/status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib revision and tree |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0882/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; output SHA-256 `55cab969...92c9`; no target or proof body was declared |
| bounded Margulis/concentrator/expander search in pinned mathlib and repo-local Lean | 1 | expected no-match result; discovery-only evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0882/statement-blocker.json` and scoped `jq -e` invariants | 0 | blocker JSON parses; identity, dependency, null target, unchanged vector, four undefined mutations, false completion fields, exact two-file change scope, and remaining cut set agree |
| scoped `git diff --check`; per-new-file `git diff --no-index --check /dev/null <path>` | 0 / 1 expected differences | tracked check passed; each no-index check exited 1 only because the new file differs from `/dev/null`, with zero diagnostic bytes |
| absence checks for `.stage1-worker-selftest.json` and `statement-receipt.json` | 0 | neither artifact exists because the exact-statement completion gate failed |

The intake validator is historical evidence from the earlier intake attempt. Integration changed
the authoritative intake state and authority-file hashes, and adding this blocker also extends the
target directory beyond its original nine-file inventory. This phase records that freshness
boundary rather than modifying the intake checker, receipt, instance, local task DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable primary or approved authoritative source, select and
independently approve one exact Margulis proposition, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and boundary case.
They must freeze the construction or network model, carrier, parameters, generators, multiplicity
and loop policy, regularity, expansion or concentration predicate and constant, family and
explicitness quantifiers, and any checked concentrator-to-expander transport while preserving
neighboring-target ownership.

A fresh statement attempt can then encode precisely that approved source claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt change is proposed.
Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement
receipt, worker `[_]`, or master acceptance is claimed.
