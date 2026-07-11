# Source-statement crosswalk

| Claim component | Repository source anchor | Lean discovery candidate | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/Stage1_Targets_rev-5.6.json`, rank 302, `THM-M-0453` | none exact | identity and lane are fixed; mathematical proposition is not |
| Human wording | `Docs/Stage0_Blueprint.md`: `椭圆曲线的塞尔默群`, attributed to Ernst Selmer | none exact | names an object but supplies no theorem, binders, hypotheses, or conclusion |
| Descent parameter | absent | multiplication-by-`n`, `p`-Selmer, and isogeny-Selmer formulations are possible | selecting one would add information absent from the source |
| Base and local data | absent | global field, its places/completions, Galois cohomology, and Kummer maps would be required | no exact formal target can yet be elaborated |
| Potential conclusion | absent | definition/kernel characterization, exact descent sequence, finiteness, and rank bounds are distinct candidates | none is credited or treated as canonical |

The metadata label `已验证` is explicitly untrusted under rev-5.6 and is not a primary mathematical
source. A source audit must first identify a specific published theorem by edition, theorem/page,
assumptions, and errata, then map each premise and conclusion to a concrete Lean expression. It must
also determine whether the intended object is an `n`-Selmer group, a `p`-Selmer group, or the Selmer
group attached to an isogeny.

The intake repository search used `rg -n -i "selmer"` over the available mathlib tree and local
Stage1 instances. It found contextual prose in other dossiers but no Lean declaration suitable as
an exact root. This is discovery evidence only, not an exhaustive immutable anchor audit. Until the
human proposition is selected, transports and mutation tests would test an invented statement. No
`H0`, machine closure, or theorem-completion claim is made.
