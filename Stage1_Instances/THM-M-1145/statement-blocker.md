# Exact-statement gate: blocked

Item: `S56-M-1145-STATEMENT`  
Base revision: `b08e4eb319008c958d529196907c5f193beee335`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the repository source
record. The complete mathematical wording is only `全纯函数的导数估计` ("derivative estimates for
holomorphic functions") under the label "Cauchy estimates." This denotes a theorem family rather
than one proposition. In particular, it does not fix:

- whether the function is complex-valued or Banach-space-valued;
- an open disk, a neighborhood of a closed disk, or a general-domain formulation;
- the center and the positivity or nonzeroness condition on the radius;
- whether every derivative order or only the first derivative is asserted;
- continuity or differentiability assumptions on the closed disk;
- a boundary-circle bound, a disk supremum, or a separately quantified constant; or
- the precise factorial, radius-power, norm, and `n = 0` conventions in the conclusion.

These choices yield materially different propositions. The Stage0 entry independently marks the
precise definitions, hypotheses, proof route, equivalent statements, and machine artifact as
missing. Its untrusted `已验证` label is neither a source-statement decision nor kernel evidence.
The accepted intake therefore correctly records `H4/M4/R4` and leaves the canonical human and Lean
statements open. Selecting a convenient library theorem would broaden the source record by adding
unsourced domains and hypotheses, which the rev-5.6 exact-statement gate forbids.

## Pinned Lean discovery boundary

Pinned mathlib does contain two close candidates in
`Mathlib.Analysis.Complex.Liouville`:

- `Complex.norm_iteratedDeriv_le_of_forall_mem_sphere_norm_le` gives the order-`n` estimate
  `norm (iteratedDeriv n f c) <= n.factorial * C / R ^ n` for a complete complex normed codomain,
  positive radius, `DiffContOnCl` on the ball, and a boundary-sphere norm bound.
- `Complex.norm_deriv_le_of_forall_mem_sphere_norm_le` gives the first-derivative estimate without
  the codomain completeness assumption.

`StatementCandidateProbe.lean` elaborates both declaration references using the narrow module that
defines them. This is discovery evidence only. The repository source does not choose between these
two candidates or establish that either candidate is the intended exact theorem, so the probe is
not a canonical target, checked transport, proof, or completion receipt. Successful elaboration of
a candidate cannot establish minimal imports for an exact target whose identity remains unknown.

## Required unblock

An accountable source reviewer must select an immutable primary-source edition and exact
theorem/page, map each premise and the conclusion, settle errata and conventions, and explicitly
freeze the codomain, disk/domain, radius condition, derivative order, boundary hypothesis, bound,
and degenerate cases. A later statement execution can then encode that claim, minimize its pinned
imports, hash the elaborated expression and environment, add checked transports for any alternate
encoding, and run the required removed-hypothesis, changed-domain, binder-scope, and boundary-case
mutations.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. The existing canonical `.lake` symlink was
used read-only; no dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1145` | 0 | rank 350, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1145/StatementCandidateProbe.lean` | 0 | both pinned candidate declarations elaborated |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/Liouville.lean Stage1_Instances/THM-M-1145/StatementCandidateProbe.lean` | 0 | hashes recorded below |
| `git diff --check -- Stage1_Instances/THM-M-1145` | 0 | no whitespace errors |

SHA-256 values, in command order:

```text
651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2
321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81
de49ced84f5799222893a523667144dd01cfa0b793cf1b2deb72268b3651700d
06b93b65f0dedbb41822d18259d627391173313250085aaced6d4563db22ed23
```

First failed gate: exact source-statement identity. Known failures are the canonical Lean
declaration, exact-target minimal imports, expression fingerprint, checked transports, and semantic
mutation tests. The assigned phase is not genuinely self-tested or complete, so no
`.stage1-worker-selftest.json` is emitted. No statement acceptance, proof credit, audit completion,
or theorem completion is claimed.
