# THM-M-0414 Anchor Audit Validation

## Result

The frozen target has exact component closures in pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The instance
`Ideal.uniqueFactorizationMonoid` closes the uniqueness conjunct, and
`Ideal.finprod_heightOneSpectrum_factorization` literally closes the finite-product conjunct for
every nonzero ideal. `AnchorAudit.lean` transcribes the frozen proposition and composes those two
anchors without strengthening or weakening it. In particular, the unit ideal stays in scope and
the zero ideal stays excluded.

The audit records exact modules, declarations, source hashes, terminal-body provenance, license,
toolchain, dependency feasibility, and the shared immutable tree. The historical repository
wrapper is classified as a duplicate of these bodies, not independent proof credit. The pinned
non-mathlib dependency scan found only downstream Dedekind-domain users. Bounded GitHub repository
queries found no additional project; authenticated code search was unavailable and grep.app was
rate limited, so no global nonexistence claim is made.

## Validation

Commands were run on 2026-07-12 from repository base
`1ec654c416270f261b365f46f5f2409b65d3f839`. The Lean command ran from
`Formalizations/Lean`; all other commands ran from the workspace root.

```text
lake env lean ../../Stage1_Instances/THM-M-0414/AnchorAudit.lean
  exit 0: exact adapter elaborated; both terminal anchors and the adapter report only
  [propext, Classical.choice, Quot.sound]
python3 Stage1_Instances/THM-M-0414/check_anchor_audit.py
  exit 0: 3 candidates classified; 2 immutable mathlib terminal anchors and exact adapter verified
python3 -m json.tool Stage1_Instances/THM-M-0414/anchor-audit.json
  exit 0: valid JSON
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0414
  exit 0: rank 69; planned; L0/rework_required; theorem_complete=false
git diff --check -- Stage1_Instances/THM-M-0414
  exit 0: no whitespace errors
```

No update, build, clone, fetch, or other `.lake` mutation was performed. The anchor-audit node is
self-tested pending master acceptance. This is not acceptance of the later proof node: obligation
architecture, full transitive provenance, human-source H0 review, hermetic replay, independent
validation, and theorem completion remain outside this phase.
