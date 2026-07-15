# THM-M-0890 proof-phase validation

## Implemented proof

`Proof.lean` closes the exact frozen `HoffmanRatioBoundTarget`. It proves that the final entry of
the descending Hermitian adjacency spectrum is least, derives strict negativity from positive
regular degree, and therefore proves the exact denominator positive. It then diagonalizes
`A - lambda_min I` to prove positive semidefiniteness, evaluates its quadratic form on the centered
characteristic vector of a maximum independent set, rearranges the resulting scalar inequality,
and invokes the checked quotient transport from `ObligationTree.lean`.

The file contains sixteen local proof declarations. The terminal declaration
`Stage1Instances.THM_M_0890_Proof.hoffmanRatioBound_proof` has exactly the canonical proposition
type. Lean `--trust=0` reports the declarations sorry-free and reports only `propext`,
`Classical.choice`, and `Quot.sound` in every axiom closure. No statement, obligation registry, or
master state was changed.

## Commands and results

Commands ran at repository revision `20808d65f53d8801e78f061504b93bb7efd49489`, tree
`a5bf33a278a7a285878c89177838ae1a0dcc9990`, on 2026-07-15. The pre-existing canonical `.lake`
symlink was used read-only; no update, build, clone, fetch, checkout, or dependency mutation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4
  targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1..1546; all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0890
  exit 0: rank 1440, planned, L0/rework_required, theorem_complete=false

python3 -B Stage1_Instances/THM-M-0890/check_obligation_tree.py
  exit 1: the immutable predecessor checker pins its historical base revision
  6ac589f0d8c5a9eeb726a1a05def7f9467ea2e2d and stops when the current proof base differs.
  The authoritative predecessor state is [_]; this is a stale replay limitation, not a proof error.

python3 -B Stage1_Instances/THM-M-0890/check_proof.py
  exit 0: exact input hashes, proof-node identity, frozen graph boundary, receipt, worker packet,
  proof declarations, prohibited-token scan, changed paths, and file hygiene passed

python3 -B Stage1_Instances/THM-M-0890/check_proof.py --run-lean
  exit 0: isolated Statement.olean, ObligationTree.olean, and Proof.olean elaborated under
  --trust=0; sixteen clean axiom reports; output SHA-256
  1feb46c6727f181724eb22479f0345d5a36682b795841eb89c07983539cd9d59

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0890-proof-pycache python3 -m py_compile
  Stage1_Instances/THM-M-0890/check_proof.py
  exit 0: checker compiled outside the repository tree

python3 -m json.tool Stage1_Instances/THM-M-0890/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both JSON artifacts parsed

scoped prohibited Lean construct scan over Stage1_Instances/THM-M-0890/Proof.lean
  exit 1 as expected: no prohibited construct matched after comments and audit commands were removed

git diff --check -- Stage1_Instances/THM-M-0890 .stage1-worker-selftest.json
  plus no-index checks for the five new files
  exit 0: no whitespace diagnostics; `git diff --no-index` exit 1 means new content only and is
  accepted only when its output contains no whitespace diagnostics
```

## Status boundary

This is provisional proof-node worker evidence. It proposes local `M0-L` kernel closure of the
exact root but is not acceptance or theorem completion. The proof uses a shifted-adjacency
centered-vector route rather than the frozen registry's deeper Hoffman-matrix/principal-submatrix
decomposition. Consequently the ten internal decomposition plans receive no individual closure
credit until master architecture reconciliation and versioned binding. The accepted vector remains
`H1/M3/R4`. H0, R0, downstream independent validation, hermetic cold/offline replay, release
evidence, `AUDIT-Z`, `THEOREM-Z`, and theorem completion remain open.
