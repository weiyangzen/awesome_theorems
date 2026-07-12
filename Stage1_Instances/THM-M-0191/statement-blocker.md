# Statement gate blocker

Item: `S56-M-0191-STATEMENT`  
Theorem: `THM-M-0191`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The intake deliberately leaves the source statement and normalization open. The authoritative
metadata gives only the title "Weil conjectures" and the gloss "properties of zeta functions of
algebraic varieties." It does not identify an edition-stable theorem/page or decide the exact
meaning of variety, connectedness and purity assumptions, the point-count versus Euler-product
normalization, factor indexing and coefficient rings, the sign and powers in the functional
equation, the cohomology/comparison theory used for Betti numbers, the reciprocal-root convention,
or the treatment of empty, zero-dimensional, and disconnected schemes.

These choices change the ordered binders, hypotheses, and conclusion. Selecting a familiar modern
four-part package and filling in its constants from memory would invent missing mathematics rather
than elaborate an exact source target. A record whose fields simply assume rationality, the
functional equation, degree control, and weight bounds would likewise encode the conclusions as
premises and is not an admissible substitute. Therefore the canonical expression, expression
fingerprint, checked transports, and meaningful removed-hypothesis, changed-domain, binder-scope,
and boundary mutations required by section 5.1 cannot truthfully be produced. Machine state remains
`M4`; statement acceptance and theorem completion are false.

## Pinned Lean boundary

`StatementInfrastructure.lean` uses narrow pinned imports to check the presently available scheme,
smooth/proper morphism, finite-field-extension, and pro-etale ell-adic cohomology declarations. A
repository and pinned-mathlib search found no Hasse-Weil zeta-function or Weil-conjectures target,
and no API connecting Frobenius on these cohomology groups to point counts, rational factors,
functional equations, or weights. The probe therefore receives infrastructure evidence only and
no statement or proof credit.

The existing canonical `.lake` artifacts were used read-only. No update, build, fetch, clone, or
dependency mutation was run.

## Validation evidence

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). Exact toolchain hashes and
command outputs are recorded after the narrow checks below.

Environment fingerprint: repository base `3320329db47d2d9804ae3322159af1f5125bbcf7`;
`leanprover/lean4:v4.29.0`; Lean commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lean-toolchain` SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0191` | 0 | rank 677, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0191/StatementInfrastructure.lean` | 0 | all five exact declaration types printed and elaborated |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match the environment fingerprint above |
| repository and pinned-mathlib `rg` searches for Weil conjectures, Hasse-Weil zeta functions, point-count zeta functions, and Frobenius/cohomology bridges | 0/1 | no exact target or required bridge package found; exit 1 denotes no match in the focused search |
| `git diff --check -- Stage1_Instances/THM-M-0191` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve an immutable primary-source edition and select and
transcribe the exact assertions, incorporated definitions, hypotheses, conventions, and errata,
with an independently reviewed row-by-row crosswalk. The formal environment must then provide, or
the statement phase must define without assuming the theorem, the required point-count zeta and
cohomological/Frobenius objects. A later statement worker can encode that same claim, minimize its
imports, serialize the elaborated expression, check alternate encodings, and run all four mutation
classes.

Until those conditions hold, this is a truthful blocker rather than completion of the assigned
node. Because the phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
