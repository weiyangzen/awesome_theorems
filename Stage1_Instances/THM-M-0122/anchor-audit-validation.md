# THM-M-0122 Anchor-Audit Validation

Item: `S56-M-0122-ANCHOR_AUDIT`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

## Validated Decision

The frozen eight-row inventory contains no valid Lean 4 proof anchor for the
exact target. Pinned mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the concrete number-field,
scheme, relative-smoothness, geometric-base-change, projective-spectrum,
closed-immersion, sheaf-module, and sheaf-cohomology interfaces used by the
statement. It also supplies generic Northcott sublevel-set finiteness and
descent to finite generation. `AnchorAudit.lean` directly elaborates these
interfaces, and its support wrapper reports no axioms. None supplies the
missing native genus comparison or concludes finiteness of all rational points.

The only direct public Lean declaration found by the bounded searches is
`faltings_theorem` in
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`.
The immutable 2,323-byte source has SHA-256
`b5aca9ae03c178c908fdf0e28d4dd8672643b16390b25e9b9771882726ed8f01`
and ends in `by sorry`. It also proves only a custom `Q`-curve statement whose
genus is stored as a natural number; there is no checked transport to the
frozen all-number-field scheme/cohomological target. Its matching Lean and
mathlib pins do not rescue the direct placeholder. Atlas is absent from the
Lake closure, has no recorded Actions run for that commit, and its restrictive
license is an additional integration concern. The candidate is rejected as
`M5`, not credited as an external proof.

The exact local target remains `M3`, not `M4`: a concrete proposition and
checked statement transports already exist, but no terminal proof body does.
The root stays `H4 / M3 / R3`. Classification is complete only for the frozen
eight-row inventory; public discovery saturation, global absence, `H0`,
`AUDIT-Z`, proof closure, and theorem completion are not claimed.

## Dependency Context

The v2 graph records no direct hard parent, transitive ancestor, incoming hard
edge, reuse hint, or shared group for `THM-M-0122`. The required
`dependency-reuse-ledger.json` binds graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`
and context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
with every inspection and decision list empty. This is a successful empty
closure audit, not a claim that the mathematical proof is independent.

The same-claim `THM-M-0395` dossier was inspected as an anchor candidate only.
Its statement uses supplied proposition fields and its proof source contains
generic finiteness transports but no Faltings theorem. Because the v2 node
admits no edge, hint, or group, it is not placed in the reuse ledger and
transfers no proof or checkbox credit.

## Commands And Results

All commands ran in this worker clone. Lean used the existing canonical pinned
`.lake` symlink read-only. No update, build, dependency clone/fetch, checkout,
or dependency mutation ran.

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 1, expected worker-artifact boundary | nested v2 validator sees target-owned unintegrated audit inventory and reports deterministic-generation mismatch; with the seven worker additions temporarily absent it exits 0, so no authoritative input is stale |
| repository root | `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1, expected worker-artifact boundary | fresh graph discovery sees unintegrated target files; a read-only replay with all seven additions temporarily absent exits 0 with 1546/10822/2/5/310 coverage |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, uniform L0/rework baseline |
| repository root | `python3 scripts/stage1_target.py show THM-M-0122` | 0 | rank 41, planned, legacy artifacts unaccepted, theorem incomplete |
| repository root | `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` | 1, expected worker-artifact boundary | fails only through the same pre-integration theorem-DAG inventory mismatch; master integration regenerates the projection after copying worker files |
| `Formalizations/Lean` | `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0122/Statement.lean` | 0 | frozen target, transports, mutations, expression, and axiom observations elaborated |
| `Formalizations/Lean` | `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0122/AnchorAudit.lean` | 0 | ten pinned support declarations elaborated; support wrapper has no axioms |
| repository root | `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0122/check_anchor_audit.py` | 0 | base, DAG, empty reuse closure, statement, pins, source digests, eight candidates, Atlas placeholder, and root boundary agreed |
| repository root | `python3 -m json.tool` on all target-owned audit JSON files | 0 | structured artifacts parsed |
| repository root | target-owned Lean prohibited-token scan | 1 expected | no proof escape or unsafe declaration in `AnchorAudit.lean` |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0122 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The Lean anchor-probe output SHA-256 is
`6ad2bd21c50e83dfed78cfad764595411316aff6a5bf463383a490b5b0263a8c`;
the unchanged statement output SHA-256 is
`82b09c5ebb5b8a560f76cc37361d67faf46d8ca8555ce1b4fe5d730f0fb7271b`;
the structured-checker output SHA-256 is
`28d0ed75c7aed200451190c2a4c420eb269fdb5eb7b575208b26c11b95ec7516`.

## Search Limits And Reopen Condition

Sourcegraph's combined archived/fork-inclusive Lean query completed and found
only the three Atlas paths classified in the snapshot. Seven GitHub repository
queries completed with zero repositories. GitHub anonymous code search returned
HTTP 401, so that lane is recorded as unavailable rather than converted into a
negative result. A later GitHub core-limit failure also does not alter an
existing immutable-tree observation. The protocol deliberately makes no
exhaustive public-search claim.

Reopen this inventory if a concrete immutable candidate supplies a
placeholder-free exact theorem or checked transport, terminal body and
transitive trust provenance, complete pins, usable licensing, and a successful
repo-local check, or if any bound statement, graph, source, toolchain, or
search-protocol input changes.

## Status Boundary

This is provisional node-specific worker evidence for a bounded immutable
formal-anchor inventory. The intake and statement prerequisites still await
master acceptance, as does this phase. It accepts no receipt, leaves the exact
root open, and does not finish the obligation tree, proof, validation,
readability/source reviews, release, `AUDIT-Z`, or the theorem.
