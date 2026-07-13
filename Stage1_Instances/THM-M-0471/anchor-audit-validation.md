# THM-M-0471 anchor-audit validation

Item: `S56-M-0471-ANCHOR_AUDIT`

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`

Base tree: `fdfff18dea4c6798c5b322b6088dfe556109c134`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains an exact
candidate route in `Mathlib.Data.Nat.Factors`. `AnchorAudit.lean` independently repeats the frozen
expanded target, chooses `n.primeFactorsList`, proves it nonempty from `1 < n`, proves its members
prime and its product equal to `n`, and applies `Nat.primeFactorsList_unique` to every alternative
prime list. The checker compares the fully explicit target expression to the statement phase's
fingerprinted expression, so the adapter does not substitute an exponent map, sorted-list equality,
integer theorem, or weakened boundary.

The pinned uniqueness body invokes `perm_of_prod_eq_prod` in `Mathlib.Data.List.Prime`; the audit
records both immutable source blobs and exact source-slice hashes. Lean reports `propext`,
`Classical.choice`, and `Quot.sound` for the four supporting theorems, the generic permutation
terminal, and the exact wrapper. `#print sorries` reports all six declarations sorry-free. Scoped
comment-aware checks find no proof gap, bodyless declaration, unsafe/opaque body, external code, or
oracle marker in the wrapper or two direct source modules. Full transitive declaration, compiled
artifact, executable TCB, supply-chain, and release trust closure remain downstream gates.

The exponent-map family in `Mathlib.Data.Nat.Factorization.Defs` is recorded separately but receives
no root credit without a checked representation transport. Bounded public discovery also found
`cymcymcymcym/Unique_Factorization_Lean4` at immutable commit
`f64a9056ce28ebe5c3946d6c522a1a79e56f835d`. Its existence and uniqueness theorems use a custom
`WellOrderedRing`, Lean 4.12.0-rc1, and a different mathlib pin. No checked Nat instance, exact root
adapter, or license was identified, so it is classified `M5`, not integrated. A historical Lean 3
xena uniqueness component is research provenance only.

Sourcegraph completed the three recorded queries without skipped results. GitHub repository search
found the custom-ring project; later code and metadata calls hit an HTTP 403 rate limit, and
grep.app hit an HTTP 429 checkpoint. Those lanes are explicit access failures, not negative
evidence. No global saturation claim is made.

The exact pinned route is therefore an unaccepted `M0-W` candidate with
`E3_plus_direct_kernel_probe_nonrelease` evidence. Release-grade `E1` has not been established. The authoritative
planned root remains `[H1, M3, R4]`: this node does not install proof-phase state, accept a receipt,
or complete the obligation, source, readability, hermetic, independent, or release gates.
`AUDIT-Z` and theorem completion remain false.

## Commands and exact outcomes

Lean used the existing manifest-pinned shared Lake artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0471` | 0 | rank 1353; planned; no legacy slot; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib revision `8a1783...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned dependency source tree clean |
| `lake env lean ../../Stage1_Instances/THM-M-0471/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact wrapper and pinned family elaborated; six axiom reports matched; six declarations were sorry-free; stdout SHA-256 `e7e41f7b...890f` |
| `lake env lean ../../Stage1_Instances/THM-M-0471/Statement.lean` from `Formalizations/Lean` | 0 | frozen target and statement-boundary fixtures re-elaborated |
| `python3 ../../Stage1_Instances/THM-M-0471/check_statement.py` from `Formalizations/Lean` | 0 | frozen statement expression, import, source, output, mutation, and boundary fingerprints matched |
| `python3 -B Stage1_Instances/THM-M-0471/check_intake.py` | 1 | historical predecessor checker reported stale `authoritative_blueprint_sha256` after the integration base changed shared authority files; no target mismatch occurred and no predecessor evidence was rewritten |
| `python3 -B Stage1_Instances/THM-M-0471/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | current manifest/DAG identity, exact target equivalence, immutable pins and source hashes, four candidates, trust boundary, receipt, packet, and narrow Lean replay agreed |
| repository-local and pinned-mathlib `rg` plus immutable Git inspection | 0 | exact mathlib family and its terminal body located; no second repo-local exact body found |
| three Sourcegraph streaming queries recorded in the ledger | 0 | complete bounded responses: 9, 0, and 3 matches with `skipped=[]` |
| GitHub repository search and immutable raw inspection | 0 | one external custom-ring project resolved to a full commit/tree and classified without cloning or integrating it |
| GitHub code/metadata follow-up | 403 HTTP | rate-limit access failure recorded; no negative-result claim |
| grep.app query | 429 HTTP | security checkpoint recorded; no search-result claim |
| `python3 -m json.tool` on every new JSON artifact and `.stage1-worker-selftest.json` | 0 | every structured artifact parsed |
| comment-aware prohibited-construct checks | 0 | no prohibited declaration or placeholder in the local wrapper and direct pinned sources; external source scan boundary recorded |
| `git diff --check -- Stage1_Instances/THM-M-0471 .stage1-worker-selftest.json` plus no-index checks for new files | 0 | no whitespace diagnostics |

## Boundary

This self-test supports only the provisional anchor-audit node pending dependency-ordered master
acceptance. The exact candidate still requires a frozen obligation registry, proof-phase adoption
and composition, complete provenance/trust and TCB closure, primary-source and readable
reconstruction review, hermetic replay, independent verification, and deterministic release
evidence. The pre-existing `.lake` symlink makes this a warm, dirty, nonrelease worker run. It
supplies no accepted proof state, audit-completion receipt, or theorem-completion receipt.
