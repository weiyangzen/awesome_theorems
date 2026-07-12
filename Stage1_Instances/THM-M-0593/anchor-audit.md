# Formal-anchor audit receipt

Item: `S56-M-0593-ANCHOR_AUDIT`  
Theorem: `THM-M-0593`  
Base revision: `e7131e388baf04f670101e508b8ac8b33a896a49`  
Audit date: `2026-07-12` (Asia/Shanghai)

## Frozen inventory and method

This audit compares candidates with the already elaborated canonical expression
`Stage1Instances.THMM0593.SardTarget` in `Statement.lean`. The target quantifies over every pair of
Euclidean dimensions `m,n`, every smooth map on an open region, and concludes that the image of all
points whose Fréchet derivative is nonsurjective has codomain `volume` zero.

Inventory version `AA-0593-v1` contains the three distinct formal candidates found by the ordered
search below. Aliases and documentation mentions are not additional candidates. Searches used the
aliases `Sard`, `Sard theorem`, `Sard lemma`, `Morse-Sard`, `critical value(s)`, `critical point(s)`,
`nonsurjective derivative`, and `det_fderiv`; source inspection also followed the Sard TODO in
Whitney embedding. The cutoff was `2026-07-12`. Public GitHub API and Sourcegraph were accessible
without credentials; GitHub code search returned HTTP 401 and grep.app returned HTTP 503, so the
external negative result is bounded rather than an exhaustive-discovery claim.

## Ordered search ledger

1. **Repo-local.** `rg` over repository Lean/Markdown/JSON found no proof body or wrapper for the
   canonical target. `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_255.lean` only records missing
   Sard/Hausdorff infrastructure for Whitney embedding. The present `Statement.lean` defines a
   proposition and supplies no proof.
2. **Pinned mathlib.** The immutable local checkout is `leanprover-community/mathlib4` commit
   `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
   `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, Lean `4.29.0`. Searches found two substantive
   candidate families, classified below. `Mathlib/Geometry/Manifold/WhitneyEmbedding.lean:20-24`
   explicitly says the needed Sard result is still a TODO.
3. **Official/primary formalization project.** GitHub repository search found
   `fpvandoorn/sard`, whose description is work toward a general Lean 4 Sard theorem. Its immutable
   audited revision is `77da83ff581fc9bf8af67e18ba8949cf555cc41c`, tree
   `92b2949f7985451dd2c9f6f8656641a185370a5d`, dated `2024-10-07`, Apache-2.0, Lean `4.12.0`,
   mathlib `809c3fb3b5c8f5d7dace56e200b426187516535a`.
4. **Other public Lean repositories.** GitHub repository search for `Sard theorem Lean
   language:Lean` returned only `fpvandoorn/sard`. Sourcegraph global Lean search for the exact
   phrase `Sard theorem` returned zero matches. GitHub unauthenticated code search and grep.app were
   unavailable as noted above. No additional candidate was identified.
5. **Statement collections and historical backends.** No repo-local Lean statement collection adds
   a proof candidate. Other proof assistants were not searched because they cannot close the
   requested Lean 4 backend and no exact Lean candidate survived the earlier stages.

## Candidate classification

### C1: pinned mathlib equal-dimensional Sard lemma

- Origin: `Mathlib/MeasureTheory/Function/Jacobian.lean:650`, declaration
  `MeasureTheory.addHaar_image_eq_zero_of_det_fderivWithin_eq_zero`; source SHA-256
  `8ef05ea1f035e9281c768c453536cfeb9e6bdc205657563628ebc81ee6de6c33`.
- Checked type: for one finite-dimensional real normed space `E`, differentiability of `f : E -> E`
  on `s` plus `(f' x).det = 0` implies `mu (f '' s) = 0` for an add-Haar measure `mu`.
- Trust: the pinned declaration elaborates and `#print axioms` reports `[propext, Classical.choice,
  Quot.sound]`; its visible proof body contains no `sorry`, bodyless declaration, `unsafe`, or
  oracle boundary.
- Scope comparison: useful only when domain and codomain are the same space. It uses determinant
  zero, not arbitrary rectangular nonsurjectivity, and therefore does not establish the canonical
  all-`m,n` target. Classification: **partial anchor, E1 for its exact narrower statement; M4 for
  the canonical root**.

### C2: pinned mathlib dimension/image family

- Origin: `Mathlib/Topology/MetricSpace/HausdorffDimension.lean:547,564`, declarations
  `ContDiffOn.dimH_image_le` and `ContDiffOn.dense_compl_image_of_dimH_lt_finrank`; source SHA-256
  `162211066ffe08483b097d6fbc6217883ead50dd0e0ba0593ae9bca8c4abb9ab`.
- Checked type: a `C^1` map on a **convex** set does not increase Hausdorff dimension; under a strict
  dimension inequality this yields density of the complement of an image.
- Trust: both declarations elaborate; `#print axioms` reports `[propext, Classical.choice,
  Quot.sound]`. Their visible bodies contain no placeholder or unsafe/oracle boundary.
- Scope comparison: this helps the `m < n` whole-image branch, but density is weaker than volume
  nullity and the convex hypothesis does not match an arbitrary open region. It says nothing about
  the critical locus in the hard `m >= n` branch. Classification: **supporting partial anchors, E1
  for their exact statements; M4 for the canonical root**.

### C3: external `fpvandoorn/sard`

- Origin: `Sard/MainTheorem.lean`, blob
  `e5dc4c238f203331cc59d01bc61c1f7bdfaf5783`, at the immutable revision above. The repository
  metadata/tree API response hashes were respectively
  `90d4c1c34e43861bffe2db8e1010be67c49e30b3f17a6a705bd3b3be24814806` and
  `011610550ff9542fcb1617497c339e3a47ee2f6d9eeaa88c2f3c741e4fb9ad31`.
- Candidate declarations: `sard_local`, `sard_boundaryless`, and `sard` have relevant conclusions,
  but their terminal bodies contain `sorry`. In particular `sard_local` leaves the entire
  `m >= n` branch as `sorry`; `sard_boundaryless` depends on it and contains further sorries; `sard`
  ends directly in `sorry`. The README truthfully says the hard case is open/not started.
- Compatibility: it targets manifolds and a custom `MeasureZero`, uses Lean 4.12/mathlib 4.12, and
  is neither a dependency nor vendored source in this repository. Fetching/building it was
  deliberately not attempted because worker rules forbid dependency mutation and its source audit
  already rules out proof credit. Classification: **M3 statement/architecture anchor only, with
  placeholder-contaminated terminal bodies; not E2 and not repo-local closure**.

## Decision and status boundary

All `3/3` members of inventory `AA-0593-v1` are classified, but discovery saturation is not claimed
because two public code-search services were unavailable. No candidate proves the exact canonical
root. The strongest local results cover equal dimension or dimension-increase support only; the
external project explicitly leaves the hard branch unfinished. Consequently the root remains
`M4` (exact local proposition exists, no exact formal closure located), with formalization debt in
the `m >= n` critical-value argument. There is no `M1` integration task because no complete exact
external theorem was found. This receipt completes only the bounded anchor-audit phase; it does not
claim `H0`, obligation-tree closure, proof closure, `M0`, audit completion, or theorem completion.

## Validation

All Lean commands used the existing pinned `.lake` tree and did not fetch or mutate dependencies.

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0593/AnchorAuditCheck.lean` | exit 0; all three declarations checked; each axiom report was `[propext, Classical.choice, Quot.sound]` |
| pinned-mathlib `rg` search for the recorded aliases | exit 0; candidates and Whitney TODO above |
| repo-local `rg` search for the recorded aliases | exit 0; no canonical proof/wrapper |
| GitHub repository API search and immutable commit/tree/raw-file requests | exit 0; one project, revision/tree and candidate bodies recorded above |
| GitHub code-search API | HTTP 401; authentication required |
| grep.app API | HTTP 503 |
| Sourcegraph global exact-phrase Lean search | exit 0; zero matches |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; structural standard consistent |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0593` | exit 0; rank 633, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0593 .stage1-worker-selftest.json` | exit 0; no whitespace errors |
