# THM-M-0338 partial proof execution

Item: `S56-M-0338-PROOF`

Base revision: `b8c0a0c119a82ef435e23f9ff85bfd783db95736`

Validated: `2026-07-15T18:33:44+08:00` (`Asia/Shanghai`)

## Implemented Body

`Proof.lean` proves the exact frozen `ExtensionExists diagonal phi` interface for every state on
every star subalgebra of bounded operators. The proof does not assume purity, a basis, or the
matrix-coefficient characterization of the diagonal, so it validly strengthens the context of
`M0338-E-EXTENSION` without changing its required conclusion.

The construction restricts the state to the real vector space of self-adjoint elements in the
subalgebra, proves real-valuedness and positivity, and invokes mathlib's M. Riesz extension theorem.
Its cofinality premise is discharged by the order unit `||y|| * 1` and
`IsSelfAdjoint.neg_algebraMap_norm_le_self`. The resulting positive real functional is complexified
through real and imaginary parts, bundled with `PositiveLinearMap.mk₀`, and proved positive,
normalized, and equal to the original state on every subalgebra element.

`extension_exists_for_kadison_singer_input` retains the frozen Hilbert basis, diagonal
matrix-coefficient hypothesis, state, and purity hypothesis verbatim. It delegates to the stronger
unconditional theorem and is only a contextual wrapper, so the packet counts one terminal proof
body rather than two.

This packet provisionally proposes closure of `M0338-E-EXTENSION` against its frozen planned
fingerprint, pending master reconciliation. Accepted closure remains empty. Uniqueness is the
substantive Kadison-Singer theorem and remains open through the paving, Weaver, MSS, interlacing,
real-root, and finite-to-infinite branches. Consequently the root remains open M3 and
`theorem_complete=false`.

## Validation

The automation-provided `Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout, network operation, or `.lake` mutation was run.
The Lean replay used fresh temporary sources and oleans, `--trust=0`, one thread, and the pinned
Lake environment. It is narrow warm-cache nonrelease evidence, not hermetic or independent release
evidence.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework-required

python3 scripts/stage1_target.py show THM-M-0338
  exit 0: rank 831, lifecycle planned, theorem_complete=false

python3 Stage1_Instances/THM-M-0338/check_statement.py
  exit 0: canonical expression hash c0c479c8...7868 and all four structural mutations killed

python3 Stage1_Instances/THM-M-0338/check_obligation_tree.py
  exit 0: 16 obligations, 70 typed edges, denominator e53a0b15...cca6e; root open M3

python3 Stage1_Instances/THM-M-0338/check_anchor_audit.py
  exit 0: exact statement-only boundary, eight pinned probes, mathlib revision, and bounded
  no-candidate source scan agree

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release

bash Stage1_Instances/THM-M-0338/check_proof.sh
  exit 0: fresh Statement, ObligationTree, and Proof elaboration passed at trust zero;
  extension_exists_for_state and its exact-input wrapper are sorry-free and each report exactly
  [propext, Classical.choice, Quot.sound]

rg --pcre2 token-anchored prohibited constructs over Proof.lean
  exit 1 with empty output: expected pass; no prohibited construct found

python3 -m json.tool proof-receipt.json proof-blocker.json .stage1-worker-selftest.json
  each exit 0 after individual invocation: valid JSON

python3 -B Stage1_Instances/THM-M-0338/check_proof.py
  exit 0: proof source, exact target binding, frozen hashes, pins, receipt, blocker, packet,
  changed-path scope, and open-root boundary passed

git diff --check -- Stage1_Instances/THM-M-0338 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

The proof source SHA-256 is
`e01e94a10cd5ce14e8ed6a9db278613dc36db450bd6321b6b7b024d5b745ce63`.
Lean is pinned at 4.29.0 and mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with clean tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The first failed machine boundary remains the planned `M0338-S-ENCODING` interface together with
the unimplemented uniqueness route. H0, R0, foundation/provenance closure, cold hermetic replay,
independent verification, validation, release, `AUDIT-Z`, `THEOREM-Z`, and master acceptance remain
open.
