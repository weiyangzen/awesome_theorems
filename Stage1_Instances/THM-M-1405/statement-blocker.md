# Exact-statement gate: blocked

Item: `S56-M-1405-STATEMENT`

Theorem: `THM-M-1405`

Base revision: `1f79a3f74a8e206d44c27513f4016a26dd7050e3`

## Decision

The exact Lean 4 target cannot be truthfully frozen or elaborated from the authoritative repository
record. Its complete mathematical wording is the title `Sinai theorem`, the attribution Yakov
Sinai (1959), and the gloss `measure entropy's generator` (`测度熵的生成子`). Stage0 leaves the
precise definitions, premises, equivalent statements, axioms, and formal artifacts open. The
catalogue status `已验证` is explicitly untrusted under rev-5.6.

The accepted intake identifies the Kolmogorov-Sinai generator theorem as the leading
interpretation, but deliberately does not accept it as the canonical claim. Sinai's author-written
Scholarpedia article, fixed revision 91407, gives the candidate statement: for a finite generating
partition `xi` of a discrete-time probability-preserving dynamical system, `h(T) = h(T, xi)`.
Retrieval of that revision succeeded and its response has SHA-256
`802d75051330ce87b16ac41b7eff75932ba485f3220d9a0adb78d10106ef783f`. This remains an
author-written secondary statement anchor. It neither supplies an independently reviewed
immutable edition of the cited 1959 primary proof nor resolves the exact source scope and
conventions required by the intake dependency.

Material choices remain open:

- an arbitrary probability space versus a standard or Lebesgue probability space;
- an invertible measure-preserving automorphism versus a one-sided endomorphism, and integer
  versus natural iterates;
- finite versus countable partitions and any finite-entropy requirement;
- literal sigma-algebra generation versus generation after completion modulo null sets;
- the definitions and codomains of partition entropy, entropy rate, and system entropy, including
  logarithm and infinite-value conventions;
- whether ergodicity is assumed and how null atoms, trivial partitions, zero entropy, and infinite
  entropy are treated.

These choices change the domains, ordered binders, hypotheses, conclusion, and boundary cases.
Selecting conventional answers, or merely copying the Scholarpedia formula while leaving its
incorporated definitions abstract, would broaden or substitute the unidentified repository target.
Encoding entropy or generation as unconstrained proposition-valued inputs would instead be a
placeholder. Both are forbidden.

Consequently the statement gate fails at exact source-statement identity. There is no canonical
human proposition from which to derive a minimal direct import, fixed Lean universes and binders,
a normalized expression fingerprint, checked alternate transports, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Machine debt
remains `M4`; no statement or theorem completion is claimed.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports
`Mathlib.Dynamics.Ergodic.Ergodic`,
`Mathlib.MeasureTheory.MeasurableSpace.MeasurablyGenerated`, and
`Mathlib.Order.Partition.Finpartition`. It elaborates six adjacent APIs for measure preservation,
ergodicity, probability measures, generated and pulled-back measurable spaces, and finite lattice
partitions. These interfaces are feasibility evidence only. They define neither
measure-theoretic entropy nor the generator theorem, so their imports cannot be certified as the
minimal import set for an unknown canonical target.

A bounded search of the pinned mathlib source found no target-specific occurrence matching Sinai,
Kolmogorov-Sinai, measure-theoretic or metric entropy, generating partition, or partition entropy.
The only entropy file families found by filename were binary entropy and topological entropy.
This negative search is not an anchor audit and does not establish that no differently named
external formalization exists.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The pre-existing
`Formalizations/Lean/.lake` link targets the canonical checkout's pinned artifacts and was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1405` | 0 | rank 904, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short && git rev-parse HEAD && git rev-parse HEAD^{tree} && readlink Formalizations/Lean/.lake` | 0 | before statement edits, only the pre-existing `.lake` link was untracked; base revision above, tree `5024086eeb6994ff53242ac82b32b2d9af8b2462`, and link destination recorded |
| `rg -n 'Sinai定理\|测度熵的生成子\|Yakov Sinai' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | found only the terse catalogue gloss and Stage0 fields that leave the exact proposition open |
| `curl -L --fail --silent --show-error 'http://www.scholarpedia.org/w/index.php?title=Kolmogorov-Sinai_entropy&oldid=91407' \| sha256sum` | 0 | retrieved fixed revision 91407; response SHA-256 recorded above |
| `cd Formalizations/Lean && lake env lean --version && lake --version && sha256sum lean-toolchain lake-manifest.json && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | Lean, Lake, toolchain hash `651c8acc...b1d2`, manifest hash `321626c8...2d81`, and mathlib revision recorded |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1405/IntakeProbe.lean` | 0 | all six adjacent APIs elaborated; no entropy or generator target asserted |
| `rg -n -i '\b(sinai\|kolmogorov.?sinai\|measure.?theoretic entropy\|metric entropy\|generating partition\|entropy of.*partition\|partition entropy)\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match exit in the bounded pinned source search |
| `python3 -m json.tool Stage1_Instances/THM-M-1405/statement-blocker.json >/dev/null` | 0 | structured blocker is valid JSON |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-1405 --glob '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or bodyless axiom in target Lean source |
| per-file `git diff --no-index --check -- /dev/null <new statement-blocker file>`, accepting exit 1 as the normal added-content difference and rejecting exit greater than 1 | 0 | both new owned-path artifacts passed direct whitespace checks |
| `git diff --check -- Stage1_Instances/THM-M-1405 && test ! -e .stage1-worker-selftest.json` | 0 | no tracked whitespace error; required worker self-test manifest is absent because the node is blocked |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable primary edition or an accepted
translation, identify the exact theorem passage and incorporated definitions with pinpoint
locators, audit translation fidelity and errata, and independently approve the source-statement
crosswalk. That review must freeze every system, partition, iteration, null-set, entropy, binder,
hypothesis, conclusion, and boundary convention listed above. A later statement worker can then
encode that same claim with real Lean definitions, minimize its pinned imports, serialize and hash
the elaborated expression and environment, compile credited transports, and run all four required
mutation classes.

This is the first failed gate, not completion of the statement node or any downstream node. The
provisional root remains `[H1, M4, R3]`, with `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. The assigned phase is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
