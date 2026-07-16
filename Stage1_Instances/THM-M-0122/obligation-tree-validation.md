# THM-M-0122 obligation-tree validation

Item: `S56-M-0122-OBLIGATION_TREE`

Base revision: `2dc5a410b68eff806858fd6ed0cb33d57f6209f7`

Base tree: `841bdd6114e7436cff4a3a1ff248fc1e884a9ddc`

Validation date: `2026-07-17` (`Asia/Shanghai`)

## Frozen result

Registry v1 freezes 23 canonical obligations before observing closure. The
denominator is
`fa58b3f6f5f390a8fd776a0d789158582ec5ded0f22616a94460d6eb0306a508`.
The proof, refinement, provenance, evidence, trust, documentation, and
workflow graph families contain 56 typed edges. Every proof dependency has a
reciprocal typed reverse edge, every material non-support node is reachable
from `M0122-ROOT`, and no graph assigns closure or proof credit.

The exact root and terminal composition certificates consume every one of
their direct children. The terminal certificate consumes three aggregate
packages: finite-extension normalization, Abel-Jacobi, and Mordell-Lang
finiteness. Detailed Mordell-Weil, no-positive-coset, finite-intersection, and
range-transport work is modeled as refinement of that aggregate package, not
as silently unused direct terminal premises.

## Validation

The target validator is declared by the HEAD phase contract and emits exactly
one `stage1-validator-semantic-result/1.0` JSON object. It deterministically
regenerates the three generated artifacts, verifies all registry and graph
invariants, audits the empty dependency context, checks receipt and worker
packet bindings, and performs a narrow pinned Lean replay.

The Lean replay copies only `Statement.lean` and `ObligationTree.lean` into a
temporary directory. It compiles the statement to a temporary `Statement.olean`
with `--trust=0`, then elaborates the obligation module with `--trust=0`. The
generic finiteness transport, conditional terminal composition, and exact-root
identity certificate are sorry-free and report exactly `propext`,
`Classical.choice`, and `Quot.sound`. These declarations prove only composition
from explicit package premises; they do not inhabit those premises or prove
Faltings' theorem.

Existing pinned `.lake` artifacts were reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout, or dependency mutation was
performed. The initial worker status contained only the automation-provided
untracked `Formalizations/Lean/.lake` symlink outside the owned change set.

`scripts/stage1_target.py check` passes for 1546 unique L0/rework-required
targets, and `scripts/stage1_target.py show THM-M-0122` reports rank 41,
planned lifecycle, and `theorem_complete=false`. The aggregate
`Docs/tools/check_stage1_standard.py` currently reports expected deterministic
theorem-DAG projection drift because this unintegrated worker adds target-owned
evidence files; the worker did not modify the authority-owned generated DAG.

## Status boundary

This packet self-tests the phase predicate T01-T04 only. It proposes `[_]` and
cannot perform master acceptance. No obligation is machine-closed. The finite
extension, Jacobian/Abel-Jacobi, Mordell-Weil, Mordell-Lang,
no-positive-coset, finite-intersection, source, provenance, trust, readable,
validation, release, `AUDIT-Z`, and `THEOREM-Z` boundaries remain open.
Accordingly `audit_complete=false` and `theorem_complete=false`.
