# THM-M-1021 proof-phase validation

Item: `S56-M-1021-PROOF`. Base revision
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`, tree
`d881fd9641fa3e5f3ebe5082b35672981e90adcf`.

## Implemented proof route

`Proof.lean` proves the forward direction locally. It identifies the frozen
integral with mathlib's real characteristic function, obtains continuity and
normalization from the pinned characteristic-function API, and writes the
finite positive-definite quadratic form as the integral of a nonnegative norm
square. For the reverse direction it derives Hermitian symmetry from the
frozen real-witness predicate, transports that predicate to the external
positive-definite structure, and applies the vendored `bochner_theorem`.

The resulting declaration is exact:

```text
AwesomeTheorems.Stage1.THM_M_1021.bochner_exact (phi : Real -> Complex) :
  AwesomeTheorems.Stage1.THM_M_1021.BochnerTarget phi
```

No premise, domain, binder, sign convention, or conclusion in the frozen
canonical target changed.

## Immutable provenance

The reverse analytic body is vendored from
`https://github.com/mrdouglasny/bochner.git` at commit
`1b56973aff9b4e6ba761a6bd8af678e38bfd8d10`, tree
`a031b68a944a46488384ba01ac386e1b17dc242d`. The upstream project is
Apache-2.0; its license is retained byte-for-byte with SHA-256
`8ebdd6164d5245aba45342f898b1a9f1c1509246a22fdf3002a66bbbe5d70089`.

| Source | Upstream SHA-256 | Local SHA-256 | Adaptation |
|---|---|---|---|
| `Bochner/PositiveDefinite.lean` | `2f5e07e86773b57551203b3556057a2ee3dd842b627474a76c3ec98c0c74bff2` | same | none |
| `Bochner/FejerPD.lean` | `503f9aaeb17becd77b5f986ebc82a3c17abcce79fd7568d3fcd66524ef352f24` | `a4bc1a1d3a6dc67f02f9afe8b09507131780fc2e4e94f9c0940170e264423a2c` | target-local import path only |
| `Bochner/Main.lean` | `5a23ba46df0866f33eae31354b659f194e5ebc1a26fd47cd92f838658b278d3b` | `9ab4cd83b1694d98059ec4b6cb7b57a56e1d6798f7609938b1939a2a0788cbd0` | two target-local imports and one nonsemantic comment correction |

The checker reconstructs all three upstream files from those documented
adaptations and requires their immutable upstream hashes. Upstream and this
repository both use Lean `4.29.0`. Upstream pins mathlib
`6ef8cc2731780be866bf243afcb7732f4da5f406`; this proof was checked against
the repository pin `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Frozen-route boundary

The frozen registry was not changed. Its reverse `M1021-C1` through
`M1021-C5` architecture describes a Riesz-Markov construction, whereas the
successful vendored body uses Fejer positivity, Gaussian regularization,
tightness, and Prokhorov compactness. `M1021-T2` therefore also lacks the
required child-to-parent certificate for the frozen route. The earlier anchor
audit and `M1021-X2` provenance overlay report that no external candidate was
found; this later bounded-audit discovery is a delta for integration review,
not a silent rewrite of predecessor evidence.

Accordingly, the exact canonical root is kernel inhabited and is an `M0-P`
candidate, but `closed_obligation_ids=[]` and
`accepted_closed_obligation_ids=[]`. No individual frozen obligation or
internal composition certificate receives proof credit. A registry v2 or an
append-only alternate-route delta is required before the frozen graph can be
declared closed.

## Commands and exact outcomes

A superseded invocation completed all Lean stages successfully, including the
fresh temporary `--trust=0` compilation and the sorry/axiom audit, but the
overall script exited `1` because `check_proof.sh` changed concurrently and the
already-running shell later observed an unbound `AUDIT_OUTPUT`. That invocation
is not credited as a passing recipe. The final stable script reruns the Lean
recipe with strict parsed axiom and sorry assertions, then checks all packet
bindings. Its final outcome is recorded in the root worker self-test manifest.
Ancillary checks recorded there include the rev-5.6 standard validator, target
manifest check, target display, frozen obligation-tree check, JSON parsing,
Python syntax, disabled-assertion rejection, prohibited-device scan, and
whitespace check. All proof replays use the existing pinned `.lake` artifacts
without running `lake update`, `lake build`, clone, fetch, or dependency
mutation.

## Status boundary

This is provisional, warm, dirty proof-phase evidence. The exact root proof is
not accepted `M0-P`, the authoritative lifecycle and root vector remain
`planned` and `[H1, M3, R3]`, and predecessor items are only provisional.
Foundation/TCB closure, the frozen-route reconciliation, H0, R0, downstream
validation and release, hermetic empty-cache/offline replay, independent
verification, master acceptance, `AUDIT-Z`, and `THEOREM-Z` remain open.
`theorem_complete=false`.
