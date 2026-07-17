# THM-M-0125 Statement Revalidation: Blocked

`S56-M-0125-STATEMENT` was rechecked at base
`c6ccce54afcb261a3b4c236a3eb538a1e4b829a8` (tree
`13ac09d107589b9b20956e6d2e4c0696058a0b41`) in exact claim order
`(v2 rank 278, phase layer 1, S56-M-0125-STATEMENT)`.

## Verdict

`blocked`. The HEAD statement contract selects exactly one existing validator,
`Stage1_Instances/THM-M-0125/check_statement.py`. Its SHA-256 is
`ee7b12276f34af731b38b9155c0c119ad0accc0347527533a679ded16b7eef31`
and its tracked Git blob is `ea899a7a5d8f22d9d40b5052d1bc181d5110232c`.
The candidate is scheduler-owned and was not changed or supplemented.

The declared replay exits `1`. Its standard output is exactly one typed JSON
object reporting `repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, and first failure `S01-ARTIFACTS`; its message is
`negative statement packet validation failed: repository HEAD differs from the
claimed worker base`. Standard output is 486 bytes including its final LF, with
SHA-256 `d8a3deba...1bd1df`; standard error is empty.

The validator pins base `1cc6aa61...`, tree `dc3053b5...`, theorem-DAG digest
`e8472863...`, blueprint digest `fb6cd286...`, and execution-skill digest
`5da11caa...`. Current values are respectively `c6ccce54...`, `13ac09d1...`,
`95128825...`, `d543fbc3...`, and `ee9b5fde...`. The existing sole receipt and
dependency ledger are likewise bound to the historical packet. Updating those
selected artifacts cannot make the protected historical validator accept, and
would not prove the positive statement predicate. No additional receipt or
self-test handoff was created.

## Dependency And Reuse Boundary

The supplied direct and transitive hard-parent inspection order is exactly
empty. That complete closure was traversed exactly once in the supplied order
before any possible proof work. There are no hard edges, reuse hints, or shared
groups. No proof work occurred, and no declaration, receipt, provider state, or
acceptance credit transfers.

The existing ledger has the required schema 1.1 and correctly records the
stable dependency context `068170c7...c5c`, empty inspections and reuse
decisions, and no compatibility obligations. Its graph and repository bindings
are stale at this claim base. The structured companion records the current
empty-closure audit without pretending that a partial refresh is a coherent
phase packet.

## Independent Statement Blocker

Even after scheduler freshness is repaired, `S02-EXACT-TARGET` remains false.
The repository gloss, "elliptic-curve derivative formula," does not select one
of at least three materially different Gross-Zagier formulations:

| Candidate | Source locator | Material boundary |
|---|---|---|
| General Rankin formula | I.(6.3), journal page 230 | Weight-two newform, class-group character, Rankin derivative, Heegner divisor, and normalization factors |
| Elliptic application | I.(7.3), journal page 231 | `L'(E,1)` and canonical height, up to period and rational factors |
| Elliptic base-change identity | V.(2.1), journal page 311 | `L'(E/K,1)`, modular parametrization, differential norm, traced point, height, unit index, and discriminant |

No authoritative record or independent review selects one proposition and
freezes its arithmetic objects, binders, hypotheses, L-series convention,
Heegner construction, height convention, constants, corrections, and boundary
cases. Inferring a convenient equality from the gloss or legacy abstract API
would broaden, narrow, or substitute the assigned theorem.

`Statement.lean` is explicitly a two-import substrate probe, not a canonical
Gross-Zagier declaration. Trust-zero Lean elaboration confirms only that
`WeierstrassCurve` and `HasDerivAt` are available. It supplies no target
expression, expression fingerprint, transport, mutation result, or statement
acceptance.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 before edit; 1 after edit | authority passed before adding this target evidence; afterward fresh theorem-DAG generation includes the new evidence while this worker may not edit the checked-in projection |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 before edit; 1 after edit | same expected integration boundary; master must regenerate the protected deterministic evidence inventory |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0125` | 0 | rank 44, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | 7 phases, 12 common gates, and 23 source references passed |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0125/Statement.lean` | 0 | only the two generic boundary interfaces elaborated |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0125/check_statement.py` | 1 | exactly one typed JSON result; `repair_required`, current HEAD differs from the pinned historical base |

The clone reused the canonical pinned `.lake` symlink read-only. No network
request, Lake update/build, dependency clone/fetch, or `.lake` mutation was
performed. The post-edit aggregate failures are not statement evidence; they
are the expected projection drift caused by adding these owned blocker files.

## Retry Condition

The scheduler must publish a refreshed declared validator and a coherent
current-base ledger/receipt packet, then issue a claim based on those unchanged
validator bytes. Independently, after intake master acceptance, an accountable
source owner must select and review exactly one immutable primary-source
theorem or corollary, freeze every incorporated definition and normalization,
encode only that proposition with concrete pinned Lean objects, fingerprint it,
check any transports, and execute all four required mutation classes.

This is current-base target-scoped blocker evidence only. It does not satisfy
or accept the statement phase, replace a selected artifact or protected
validator, transfer acceptance, prove a canonical statement or theorem, change
task state, or claim master acceptance. Because semantic validation failed,
`.stage1-worker-selftest.json` is deliberately absent.
