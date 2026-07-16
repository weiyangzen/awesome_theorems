# THM-M-0390 anchor-audit scheduler blocker

Item: `S56-M-0390-ANCHOR_AUDIT`

Worker base: `6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049` (tree
`28c148dbd84fbd549c749f060c92c9a3f00b16d0`)

Claim order: `(v2 rank 4, phase layer 2, S56-M-0390-ANCHOR_AUDIT)`

Verdict: `blocked`; authoritative state remains `[_]`;
`phase_accepted=false`

## First failed gate

`G05-AUTHORITY-REPLAY.immutable_HEAD_validator_is_stale_for_worker_base`

The HEAD anchor-audit contract declares two scheduler-owned candidates. Exactly
one exists: `Stage1_Instances/THM-M-0390/check_anchor_audit.py`, SHA-256
`36b8d075f9a09ecd598ad0a69696265644dee6b984c83b87a0c89537126bad08`,
Git blob `50c2541e90f0f01795bb51b18b25a13bf9660137`. This worker did not
change it or add the absent `check_anchor.py` candidate.

The exact authority-selected argv is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py
```

It exits `1`, writes nothing to stderr, and emits exactly one 463-byte
`stage1-validator-semantic-result/1.0` JSON object on stdout (SHA-256
`e737f1c1abc68113dc377db8293ce83a978ff3bca827fa90e80206a7cb518abe`).
The result reports `verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, and `message="repository revision drift"`.
The protected validator pins base `c5037228...`, tree `78b2627e...`, theorem
DAG `fb17743f...`, and the historical target artifact hashes. Current values
are `6cff7bae...`, `28c148db...`, and
`80cf05109d5b3776b7defe95fdb591b216894a57ecbb7180a59f315a67d487d5`.

The scheduler's HEAD recipe selector still resolves this one unchanged
candidate successfully for the current base. The semantic replay, not
candidate selection, fails. The existing `anchor-audit-receipt.json` is not a
current replacement: it records base `c5037228...` and tree `78b2627e...`.
The exact HEAD role resolver rejects it with `phase receipt base_revision
disagrees with worker base`; its receipt-bound rows additionally use fields
outside the closed binding schema. Rewriting the sole receipt without a
passing unchanged validator would manufacture a false self-test.

`G02-TOPOLOGY` also remains pending: `S56-M-0390-STATEMENT` is `[_]`, not
master-accepted `[x]`. Provisional anchor observations may be audited, but the
master cannot accept this phase before its predecessor.

## Dependency and reuse audit

The supplied direct/transitive hard-parent inspection order is exactly empty.
That complete empty closure was traversed once, in order, before any possible
proof work. No proof work was performed. There are no hard edges or reuse
hints.

The sole nonblocking group, `SHARED-MODULE-32f9c9eb1b52d871`, was re-inspected
through `THM-M-0133`: its current seven phases are all `[_]`; its anchor audit,
exact statement, conditional proof body, and validation receipt retain SHA-256
values `98dd1ebb...a72ca`, `01ea9240...960e1`, `edf99220...43a6d`, and
`c8f42b62...2d2f9`. Its target is Fermat's Last Theorem, its root is open, and
none of its declarations proves `CatalanStatement`. `Polynomial.flt_catalan`
is a theorem over field polynomials concluding constant degrees. The correct
decision remains `not_applicable`; no declaration, receipt, checkbox,
acceptance, or proof credit transfers.

The tracked `stage1-dependency-reuse-ledger/1.1` records the stable context
`a615cea5c684a96055d1d5bb30bdcfccbc499a62f7fcfac3490551cb836c1598`,
the empty closure, the weak-group decision, and no unresolved compatibility
obligation. It is nevertheless stale on graph digest and repository revision.
Refreshing only that ledger would violate the protected validator's pinned
ledger hash and cannot create a valid phase packet, so this blocked attempt
does not manufacture a partial ledger/receipt pair.

## Bounded anchor result

The current immutable observations preserve the negative result without root
proof credit:

- repo-local files contain exact statement shapes, transports, finite checks,
  and open proof architecture, but no terminal `CatalanStatement` body;
- pinned mathlib revision
  `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`) has documentation row
  `Q174955` without a `decl`/`decls` anchor;
- the current read-only cache contains `Polynomial.olean`, and a trust-zero
  import probe elaborates `Polynomial.flt_catalan` at its materially
  incompatible field-polynomial type; this corrects the historical cache
  observation but gives no Catalan root credit;
- Formal Conjectures revision
  `7871d8fc7a8164a1ac16c3765b40c25ce015b681` remains content-bound by the
  recorded source digest and its near statement ends in `by sorry`; and
- public discovery remains bounded and access-limited rather than saturated;
  the primary human publication is identified, but exact locator,
  assumptions, errata, and independent H0 review remain open.

The strongest boundary remains `M3/E4` formalization debt: no exact
placeholder-free terminal candidate, no accepted reuse, no H0/R0, no
`AUDIT-Z`, and no theorem completion.

## Validation

No `lake update`, `lake build`, clone, fetch, or dependency mutation was run.
The automation-provided `.lake` symlink and pinned package worktrees were used
read-only.

| Command | Exit | Result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py` | 1 | exactly one typed negative JSON object; `repair_required`, `repository revision drift` |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0390/Statement.lean` | 0 | exact statement and mutation surfaces elaborated |
| `cd Formalizations/Lean && lake env lean --trust=0 /tmp/thm_m_0390_polynomial_import_probe.lean` | 0 | pinned `Polynomial.flt_catalan` type elaborated without dependency mutation |
| `python3 Docs/tools/check_stage1_standard.py` | 0 before the new blocker; 1 after | pre-edit rev-5.6 authorities passed; post-edit failure is the expected derived evidence-inventory drift from these blocker files |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 before the new blocker; 1 after | pre-edit graph passed; post-edit deterministic generation sees these new target-owned blocker files and awaits scheduler regeneration |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, twenty-three source references |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranked uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0390` | 0 | rank 4, planned, rework required, theorem incomplete |
| HEAD role-map probe | 0 | current base rejected solely because the sole phase receipt records the obsolete base |
| HEAD validator-recipe probe | 0 | exactly one unchanged protected candidate selected with the argv above |

Adding this target-owned blocker changes the theorem DAG's derived evidence
inventory. This worker does not edit that forbidden projection; scheduler
integration must regenerate and validate it transactionally.

## Retry condition

The scheduler or authority-maintenance lane must publish one coherent base
containing a corrected declared validator plus refreshed target ledger,
inventory, discovery evidence, validation record, and sole phase receipt. It
must bind the current graph/base, use complete path/SHA-256/Git-blob role rows,
and correct the materialized-olean and historical Git-blob observations while
preserving the negative candidate classifications and zero root proof credit.
A fresh worker claim must start from a base already containing that unchanged
validator, replay it successfully, and emit the required self-test packet.
Master acceptance still waits for the statement predecessor to become `[x]`.

This is current-base, target-scoped blocker evidence only. It does not satisfy
the phase, refresh the sole receipt or dependency ledger, transfer acceptance,
claim proof credit, change H/M/R debt, claim `AUDIT-Z` or `THEOREM-Z`, change
task state, or claim master acceptance. Because the phase is not genuinely
self-tested, `.stage1-worker-selftest.json` is deliberately absent.
