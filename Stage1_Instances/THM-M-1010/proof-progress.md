# Proof-phase progress and blocker

Item: `S56-M-1010-PROOF`. Base revision:
`240ce7cf9937f5d92636d86bdc3c05b9224b27b0`.

`Proof.lean` adds a kernel-checked proof of the constant-law boundary case in
the exact frozen `Representation` language.  It uses `S` itself as the common
sample space, the probability measure `mu`, and the identity map for every
random variable.  Thus the prescribed laws and pointwise (hence almost
everywhere) convergence are proved without a placeholder or an additional
premise.

This is substantive proof progress on `M1010-S-BOUNDARY`, but it does not
close the assigned proof phase.  In particular, it neither declares nor
proves `Target S` for an arbitrary weakly convergent, nonconstant sequence.
The frozen root cut set remains the construction of refining null-boundary
partitions, a compatible common-space coupling, measurability and exact-law
proofs for its representatives, and a.e. stabilization implying full-sequence
topological convergence.  The pinned dependency search recorded by the
anchor audit found no theorem that supplies that construction.  The nearby
`Measure.exists_measurable_map_eq` in
`Mathlib.Probability.Kernel.Representation` realizes one measure at a time;
it does not couple the entire sequence so that its representatives converge.

Consequently the phase is blocked at `M1010-N-PARTITIONS` and
`M1010-C-COUPLING`, the exact root remains `M3`, and no
`.stage1-worker-selftest.json` is emitted.  The integration lane must not
promote the proof item based on this boundary lemma.

## Validation

Commands ran on 2026-07-12 inside the worker clone.  Lean commands ran from
`Formalizations/Lean`, reused the canonical pinned `.lake` symlink, and did
not update, build, fetch, or otherwise mutate dependencies.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 schema and 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | ordered target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | rank 290, hard anchor/wrapper lane, and L0 rework baseline confirmed |
| temporary `Statement.olean` and `ObligationTree.olean` compilation followed by `LEAN_PATH="$tmp" lake env lean ../../Stage1_Instances/THM-M-1010/Proof.lean` | 0 | both new declarations elaborated; their axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n '\bsorry\b|\badmit\b|\baxiom\b|sorryAx' Stage1_Instances/THM-M-1010 --glob '*.lean'` | 1 expected | no forbidden Lean construct in target Lean sources |
| `git diff --check -- Stage1_Instances/THM-M-1010` | 0 | no whitespace errors |

The temporary compilation recipe creates its objects under `mktemp -d` and
removes that directory after elaboration; it writes no object into the target
directory or `.lake`.
