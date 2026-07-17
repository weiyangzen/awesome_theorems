# THM-M-0126 anchor-audit scheduler blocker

Item: `S56-M-0126-ANCHOR_AUDIT`  
Worker base: `e19e77ec08fca6a8a9c45a003c9904020dae8382`  
Verdict: `blocked`; authoritative state remains `[ ]`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The mandatory HEAD contract declares only these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0126/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0126/check_anchor.py`

Neither path exists in the worker-base commit or worktree. The worker may not create, refresh,
rename, replace, or delete either candidate. Therefore there is no lawful validator argv and no
typed `stage1-validator-semantic-result/1.0` output to bind in the required phase receipt. Exit zero
from another command or an undeclared adapter cannot replace scheduler-owned replay.

The independent topology gate is also closed. `S56-M-0126-STATEMENT` is authoritatively `[_]`, not
master-accepted `[x]`; its receipt says `accepted=false`, `verdict=blocked`, and records neither a
canonical formal target nor statement fingerprints. Bounded discovery guidance remains observable,
but it cannot define the exact normalization boundary required for accepted anchor classification.

## Dependency and reuse boundary

The exact claim tuple is `(279, 2, S56-M-0126-ANCHOR_AUDIT)`. The current theorem-DAG SHA-256 is
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`, and the target context
digest is `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The complete parent inspection order and all direct-parent, transitive-ancestor, hard-edge,
reuse-hint, and shared-group lists are empty. That empty closure was traversed exactly once before
any proof work. No proof work was performed, and no provider declaration, body, receipt, reusable
artifact, import, copy, transport, checkbox state, acceptance, or proof credit was consumed.

The existing schema-1.1 dependency ledger correctly records the empty context, but it binds an older
repository revision and graph digest and is an exact input of the predecessor receipt. It is not
rewritten in this blocked claim: changing those bytes would invalidate prior evidence while neither
creating the missing scheduler validator nor making this phase self-testable. A fresh eligible
anchor run must refresh it before proof work or a phase handoff.

## Bounded observations

- The repo-local `S1_M_045.lean` and same-topic `S1_M_084.lean` modules elaborate generic
  quaternion, arithmetic, scheme, order/level, and moduli interfaces. Their decisive moduli and
  representability properties remain data or explicit boundaries. They are `M3` substrate, not
  source-exact terminal proof bodies; `THM-M-0435` is not a parent or reuse provider for this claim.
- Pinned mathlib at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies generic
  quaternion algebra, basis, scheme, smooth/proper, number-field, ideal, class-group, and local-field
  APIs. A bounded read-only scan found no Shimura-curve construction, quaternionic-moduli
  representability, canonical-model, or uniformization terminal declaration. This is `M3` substrate.
- Content-bound legacy evidence records `ImperialCollegeLondon/FLT` at commit
  `2f4325e3b3e647225890f143d4f2dbf1315d4ebd` as an adjacent but incompatible `M5` lead: its
  source bytes and trust closure are outside the pinned dependency closure, its pins differ, relevant
  placeholders remain, and no terminal Shimura-curve declaration was recorded.
- The remaining public-project, statement-collection, and other-prover lanes are `M4` access
  boundaries. Network is denied, and no target-owned replayable immutable response packet exists;
  these are not global negative results.
- Goro Shimura's 1967 *Annals of Mathematics* paper is an `H2` bibliographic lead only. The repo has
  no immutable source copy, exact theorem/page, complete incorporated definitions and assumptions,
  errata disposition, translation, or independent review for this target.

These observations are not a complete precommitted seven-lane inventory. Because the exact source
statement remains unselected, candidate normalization is impossible. The truthful root boundary
remains `[H4, M4, R4]`; no H0, M0, proof, `AUDIT-Z`, or `THEOREM-Z` credit is claimed.

## Validation and retry

The structural standard, theorem-DAG, phase-contract, target-list, and target-show checks passed at
the immutable base. Using the canonical pinned `.lake` symlink read-only, both
`StatementInfrastructure.lean` and `S1_M_045.lean` elaborated with
`lake env lean --trust=0`. Those narrow checks prove only that adjacent interfaces typecheck; they
cannot substitute for the absent semantic validator.

After these blocker files were added, the deterministic theorem-DAG and aggregate-standard checks
report the expected evidence-inventory drift. The worker does not edit that forbidden generated
authority; scheduler integration must regenerate the read-only projection. JSON parsing and
`git diff --check` still pass, and the required phase receipt and self-test manifest remain absent.

The scheduler must commit exactly one declared anchor validator and launch a fresh worker from a
base containing the identical blob. The statement predecessor must separately become `[x]` with an
exact source-selected statement and fingerprints. The fresh worker must refresh the empty ledger,
precommit and execute all seven discovery lanes, bind every immutable result or access failure,
normalize and classify the complete frozen inventory, emit exactly one phase receipt, and replay
the unchanged validator.

No `anchor-audit.json`, discovery packet, phase receipt, `AnchorAudit.lean`, or
`.stage1-worker-selftest.json` is produced. This target-scoped blocker changes no task state and
claims no phase acceptance, proof credit, audit completion, theorem completion, or master acceptance.
