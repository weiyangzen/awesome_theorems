# Anchor-audit authority blocker

Item: `S56-M-0445-ANCHOR_AUDIT`  
Theorem: `THM-M-0445`  
Worker base revision: `739d30014e3a21d9f0abfa3b9ae206d4c32f120c`  
Worker base tree: `2728571d64aefe781c1b17e97dafc9343fc129f4`  
Worker verdict: `blocked`  
Proposed state: `[ ]` (unchanged)  
Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`. For
`anchor_audit` it declares exactly these validator candidates:

- `Stage1_Instances/THM-M-0445/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0445/check_anchor.py`

Neither path exists in commit `739d30014e3a21d9f0abfa3b9ae206d4c32f120c`. The contract requires exactly
one candidate, requires it to exist at the worker base, and requires its HEAD blob to equal its
worker-base blob. The integration code also rejects every worker change to a declared validator
candidate. Creating either validator here would therefore be ineligible for authority replay and
would make the handoff rejectable; creating both would additionally make selection ambiguous. No
undeclared adapter, command success, prose output, or receipt can replace the missing immutable
validator.

The independent topology gate `G02-TOPOLOGY` is also closed: the sole intra-theorem predecessor,
`S56-M-0445-STATEMENT`, is worker-self-tested `[_]`, not master-accepted `[x]`. Consequently this
claim cannot support master acceptance even if its audit artifacts were otherwise complete.

## Scoped observations

The complete hard-parent inspection order, direct-parent list, transitive-ancestor list, hard-edge
list, reuse-hint list, and shared-group list are empty. No provider was inspected, reused, copied,
or credited. The authoritative theorem DAG SHA-256 is
`ccfe534e697065f0d1501abba8d092102230694e73f0335f2a6d2faa92b42876`; the target dependency-context
SHA-256 is `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The bounded audit observations available at this base do not resolve the mathematical target:

- The repository source identifies Karl Rubin and Victor Kolyvagin, the year 1991, and only the
  gloss `BSD for elliptic curves`; it supplies no edition, theorem/page locator, exact hypotheses,
  theorem branch, or precise conclusion.
- The tracked legacy discovery source
  `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_091.lean` has SHA-256
  `755068effda6d0d7c2047b5b35db9376c2851f391c3543a971aafbae80bc49e5` and Git blob
  `b5ac493d7319fdb836c56e8b69978912af795a4b`. It exposes abstract proposition fields and competing
  statement shapes, not a terminal Rubin-Kolyvagin/BSD proof. It records an access-limited public
  search and rejects `adri326/rubin-lean4` as a different Rubin theorem about topological group
  actions; no immutable external candidate bytes were admitted.
- The pinned local environment is Lean `v4.29.0`, mathlib revision
  `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
  `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Repository and dependency searches located only
  generic elliptic-curve, L-series, Selmer, Mordell-Weil substrate, or unrelated Rubin results; no
  terminal exact BSD/Kolyvagin/Rubin declaration was identified.
- The truthful provisional classifications remain: unresolved exact root and bounded/access-limited
  lanes `M4`; abstract legacy interfaces `M3`; checked but nonterminal substrate `M2`; materially
  mismatched candidates `M5`. These are discovery observations only, not a completed inventory,
  proof credit, search-saturation claim, or phase evidence.

The existing `dependency-reuse-ledger.json` predates this base and graph revision. It was not
rewritten because this claim cannot reach a lawful self-test and a new ledger alone cannot repair
the missing scheduler-owned validator.

## Retry condition

The scheduler must first commit exactly one declared anchor-audit validator at one of the two
contract candidate paths, then issue a fresh claim whose worker base contains that identical blob.
The statement predecessor must separately obtain master acceptance `[x]` before this phase can pass
`G02-TOPOLOGY`. A fresh worker can then bind a complete seven-lane inventory and discovery evidence,
refresh the empty dependency-reuse ledger to the fresh base and current graph, create exactly one
phase receipt, and replay the unchanged validator.

No `.stage1-worker-selftest.json` or anchor-audit receipt is produced. This blocker grants no state
transition, phase acceptance, H0, M0, R0, audit completion, theorem completion, or master acceptance.
