# THM-M-0994 release decision handoff

## Exact verdict

`S56-M-0994-RELEASE` is `blocked`. Lifecycle remains `planned`, the accepted root vector remains
`H2/M3/R4`, and both `audit_complete` and `theorem_complete` are false. There are no accepted
receipt IDs and no theorem-completion promotion.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is `[_]`
worker evidence with `support_state=provisional_worker_selftest`, not a master-accepted receipt.
Even after dependency acceptance, section 10.6 hermetic reproduction remains unsatisfied.

## Evidence reconciliation

The exact frozen Hoeffding root and a separately written reconstruction both kernel-elaborate in
this checkout against pinned mathlib `8a178386`. They report only `propext`, `Classical.choice`, and
`Quot.sound`, and the scoped Lean files contain no `sorry`, `admit`, axiom declaration, or unsafe
marker. This is useful provisional exact-root evidence, not accepted M0 or release evidence.

The structured authorities disagree because they were produced at different phases. The intake
remains `H2/M3/R4`; the older frozen graph records `H2/M1/R3`, `root_closed=false`; and the later
validation receipt records a successful root replay but explicitly refuses completion. Without
master reconciliation, the conservative accepted vector is therefore unchanged at `H2/M3/R4`.

`AUDIT-Z` fails because exact primary-source/errata review and independent H0 acceptance remain
open, as do a complete readable reconstruction and independent R0 review. Full transitive
proof-body provenance, foundation/axiom policy, trust, and TCB acceptance are also absent.

`THEOREM-Z` independently fails release assurance. The validation used this mutable worker checkout
and the shared warm pinned `.lake` artifacts. There is no immutable clean snapshot, empty-cache
network-denied cold build, offline archive replay, SBOM/license closure, two signed independently
provisioned runners, independently implemented minimal release verifier, protected CI evidence, or
deterministic content-addressed bundle.

## Self-test

Commands ran from base revision `21b5f8a135c40b3fc4f9987beee433d2ebd8bd43` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0994
  exit 0: rank 274, planned, theorem_complete=false

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0994/Proof.lean
  exit 0: exact Hoeffding root elaborated; axioms are propext, Classical.choice, Quot.sound

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0994/Validation.lean
  exit 0: separately reconstructed exact root elaborated with the same axiom profile

python3 Stage1_Instances/THM-M-0994/check_release.py
  exit 0: upstream validation replay and fail-closed release reconciliation passed

python3 -m json.tool Stage1_Instances/THM-M-0994/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0994 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No dependency update, build, clone, fetch, or `.lake` mutation was performed. This self-tests the
negative release verdict only. It is not a release-grade receipt or a theorem-completion claim.
