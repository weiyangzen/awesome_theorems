# Anchor-audit validation record

Item: `S56-M-1228-ANCHOR_AUDIT`  
Base revision: `be286e95464895d6966301556151584a57536a1b`

## Result

The exact repo-local artifact is the proposition definition
`Stage1Instances.THMM1228.CaffarelliKohnNirenbergTarget`, not a theorem body.
Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95`
provides distributions, test functions, smoothness, Lp spaces, and ambient-metric
Hausdorff measure. The nine probes elaborate, but none supplies suitable weak
Navier-Stokes solutions, the parabolic Hausdorff construction, or CKN partial
regularity. Ambient Euclidean/product-metric Hausdorff measure is not accepted
as a substitute for the source theorem's parabolic geometry.

Four related external Lean repositories were audited at full 40-character
commits through complete, non-truncated Git tree responses. They contain Clay
Navier-Stokes statement scaffolding, Serrin/global-regularity work, a numerical
certificate pipeline, or vortex-stretching inequalities. None has an exact CKN
terminal theorem. The latter three also have proof/trust boundaries recorded by
the repo-local historical source inspection, so they cannot receive root proof
credit. The tree-response hashes bind this pass's immutable discovery evidence;
they are not proof receipts.

The root therefore remains `M4`. This completes the bounded anchor audit only;
it does not assert that no Lean proof exists globally, and it supplies no human
source classification, obligation tree, proof, or theorem-completion evidence.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Existing pinned `.lake`
artifacts were reused. No update, build, dependency clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1228/AnchorAudit.lean` | 0 | Nine adjacent mathlib declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1228/Statement.lean` | 0 | Canonical statement and definitional expansion re-elaborated |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | M4 boundary, probe inventory, manifest pin, installed mathlib HEAD, and four immutable tree receipts agreed |
| `rg -n -i 'Caffarelli.Kohn.Nirenberg\|NavierStokes\|Navier.Stokes\|suitable weak solution\|local energy inequality\|partial regularity\|parabolic Hausdorff\|epsilon regularity' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No terminal-name match in pinned mathlib source; exit 1 is the expected no-match result |
| `curl ... /repos/lean-dojo/LeanMillenniumPrizeProblems/git/trees/540da948...?recursive=1` | 0 | Complete 71-entry tree; SHA-256 `55efcc7d06fd49b41cb09b73118716c52e6512f10fda2811046056d07265906f` |
| `curl ... /repos/motanova84/3D-Navier-Stokes/git/trees/7fbbcb26...?recursive=1` | 0 | Complete 952-entry tree; SHA-256 `0539d74764d9fa2c48642b01347e0e0eb1fe8f5f256fac3fcbf29e292c490895` |
| `curl ... /repos/Bitumenmachina/ns-lean4-pipeline/git/trees/4cfc7bfd...?recursive=1` | 0 | Complete 81-entry tree; SHA-256 `3e243e851cfaccddab505efe598bb81f637977469d6b3360d217be8ba94f05eb` |
| `curl ... /repos/MohamedMoawadHassan/GIGD-Formalization/git/trees/1d04458c...?recursive=1` | 0 | Complete 7-entry tree; SHA-256 `a9f801dc25488ffb4a942f8a45689a2be7f9a52b52a6fe7f96ae17316c697f3a` |

## Open integration gate

Reopen only for a repository URL, immutable revision, compatible toolchain,
module, declaration, exact-type transport, terminal proof-body provenance,
license, and successful local wrapper check. Until then, no exact machine
closure or theorem-completion credit is valid.
