# THM-M-0115 Anchor-Audit Validation

Item: `S56-M-0115-ANCHOR_AUDIT`

Base revision: `c4715a2babbead02e04d70708c3ebc58c75a1942`

## Validated Decision

The frozen nine-row inventory contains no valid Lean 4 proof anchor for the
exact target. Pinned mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies adjacent object-model
support only. `AnchorAudit.lean` directly checks the scheme, over-base,
proper, smooth, quasi-affine, sheaf-module, quasi-coherent, sheaf-cohomology,
derived-category, and generic monoid group-completion surfaces in that pin.
The probe axiom-prints one support wrapper as
`[propext, Classical.choice, Quot.sound]`; no terminal GRR declaration exists
in mathlib to credit.

The only immutable public Lean 4 GRR declaration found is
`GRR.grothendieck_riemann_roch` in
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`.
The checker replays the content-addressed immutable-source observation, whose
acquisition used the recorded immutable URL, and verifies SHA-256
`2ade6a4b32dd2b2960bf6a9993921308591b9fe95aec61407f9f89bea554f450`,
and requires the direct body `by sorry` and the downstream dependency from
`grr_trivial_todd`. It also verifies that Atlas uses the same Lean and mathlib
pins. This is an `M5` blocker, not proof or integration evidence. Three
broader Riemann-Roch repositories are recorded as graph, curve, or function-
field statement mismatches.

The root therefore stays `H4 / M3 / R4`. The node is self-tested worker
evidence pending dependency-ordered master acceptance. It is not exhaustive
discovery, `H0`, `R0`, a proof, `AUDIT-Z`, or theorem completion.

## Commands And Results

All commands ran in this worker clone. Lean used the existing automation-
provided `.lake` symlink read-only. No update, build, dependency clone/fetch,
checkout, or dependency mutation ran.

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection passed |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and uniform L0/rework baseline passed |
| repository root | `python3 scripts/stage1_target.py show THM-M-0115` | 0 | Rank 23, planned, legacy artifacts unaccepted, theorem incomplete |
| `Formalizations/Lean` | `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0115/AnchorAudit.lean` | 0 | Pinned support declarations and wrappers elaborated; support axiom set printed |
| repository root | `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0115/check_anchor_audit.py` | 0 | Base, DAG, statement fingerprint, pins, mathlib blobs, 9/9 inventory, immutable Atlas placeholder, and root boundary agreed |
| repository root | `python3 -m json.tool` on the protocol, audit, external snapshot, receipt, and worker self-test | 0 | All structured artifacts parsed |
| repository root | prohibited-token scan over `AnchorAudit.lean` | 1 | Expected no-match exit; the checker enforces the same scan |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0115 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics |

The Lean probe output SHA-256 is
`4a166e22906e3059fd89413de98c7f1d75ea4e58088f19ffe504dfff7f5b93ad`.
The structured-checker output SHA-256 is
`132b2bdfa878e485aaf4b77747cc1484010a947f3563264292f4a183fe78d31e`.
The provisional receipt records source and output identities while deliberately
omitting its own hash, this validation record's hash, and the root handoff's
hash. It also treats network refresh as a new discovery version: the ordinary
self-test replays the content-addressed external snapshot offline rather than
depending on transient network availability. The integration lane must
content-address the final integrated packet.

## Access Limits

Sourcegraph's bounded exact-declaration query completed and found only Atlas.
GitHub repository queries completed before the shared anonymous core limit was
exhausted; later code search returned HTTP 403. grep.app returned HTTP 429.
These failures are recorded, not converted into global negative evidence.

## Reopen Condition

Reopen integration when a concrete immutable Lean 4 candidate supplies a
placeholder-free exact theorem or checked transport, terminal proof-body and
transitive trust provenance, complete pins, compatible licensing, and a
successful repo-local check. Until those conditions hold, `M1` and `M0` are
invalid.
