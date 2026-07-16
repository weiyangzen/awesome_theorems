# THM-M-0426 anchor-audit scheduler blocker

Item: `S56-M-0426-ANCHOR_AUDIT`  
Worker base: `fe1ec5161fd86894fef54d2a1860437053d9e8d7`  
Verdict: `blocked`; authoritative state remains `[ ]`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The mandatory HEAD contract declares only these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0426/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0426/check_anchor.py`

Neither path exists in the worker-base commit or worktree. The worker may not create, refresh,
rename, replace, or delete either candidate. Therefore there is no lawful validator argv and no
typed `stage1-validator-semantic-result/1.0` output to bind in the required phase receipt. Exit zero
from another command or an undeclared adapter cannot replace scheduler-owned replay.

The independent topology gate is also closed: `S56-M-0426-STATEMENT` is authoritatively `[_]`, not
master-accepted `[x]`. Its receipt says `accepted=false`, `verdict=blocked`, and contains no canonical
statement fingerprint. That evidence remains useful discovery guidance but cannot define the exact
statement-normalization boundary required for anchor classification.

## Dependency and reuse boundary

The exact claim tuple is `(306, 2, S56-M-0426-ANCHOR_AUDIT)`. The current theorem-DAG SHA-256 is
`6d0668e741eb7f886c28ad37c524f11eb902f5be610ea4e69a68badb80075b39`, and the target context
digest is `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The complete parent inspection order and all direct-parent, transitive-ancestor, hard-edge,
reuse-hint, and shared-group lists are empty. That empty closure was traversed exactly once before
any proof work. No proof work was performed, and no provider declaration, body, receipt, copy,
transport, checkbox state, acceptance, or proof credit was consumed.

The existing schema-1.1 dependency ledger correctly records the empty context, but binds an older
repository revision and graph digest and is an exact input of the predecessor receipt. It is not
rewritten in this blocked claim: changing those bytes would invalidate prior evidence while neither
creating the missing scheduler validator nor making this phase self-testable. A fresh eligible
anchor run must refresh it before proof work or a phase handoff.

## Bounded observations

- The historical `S1_M_080.lean` artifact is `M5`: its character type, completed function,
  conductor factor, root number, center, dual, primitivity predicate, and functional-equation field
  are caller supplied. It is an abstract/circular shape, not a terminal Hecke theorem.
- Pinned mathlib at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies generic
  `WeakFEPair`/`StrongFEPair` equations, a primitive Dirichlet-character special case, and
  number-field/Adele/product-formula substrate. The bounded pinned-tree topic scan found no
  Hecke-character or Hecke-L terminal declaration. These adjacent interfaces are `M3`, not an exact
  root candidate.
- The remaining official-project, public-project, statement-only, other-prover, and primary-source
  lanes lack a precommitted response packet. Network is denied, and the exact target is not frozen;
  they remain `M4` access/unresolved boundaries rather than false global-negative claims.

These observations are not a complete seven-lane anchor inventory. They grant no H0, M0, proof,
AUDIT-Z, THEOREM-Z, or theorem-completion credit.

The pre-edit structural, DAG, phase-contract, target-list, and target-show checks all passed, and the
existing `Statement.lean` interface probe elaborated under `lake env lean --trust=0`. After these
two blocker files were added, the deterministic DAG check reports expected evidence-inventory
drift. The worker does not edit that forbidden generated authority; scheduler integration must
regenerate it.

## Retry condition

The scheduler must publish exactly one declared anchor validator and launch a fresh worker from a
base containing the identical blob. The statement predecessor must separately become `[x]` with an
exact source-selected statement and fingerprints. The fresh worker must refresh the empty ledger,
precommit and execute all seven discovery lanes, bind every immutable result or access failure,
normalize and classify the complete frozen inventory, emit exactly one phase receipt, and replay
the unchanged validator.

No `anchor-audit.json`, discovery packet, phase receipt, `AnchorAudit.lean`, or
`.stage1-worker-selftest.json` is produced. This target-scoped blocker changes no task state and
claims no phase acceptance, proof credit, audit completion, theorem completion, or master acceptance.
