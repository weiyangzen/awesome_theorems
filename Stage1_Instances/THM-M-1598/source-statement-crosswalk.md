# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:11770-11775` contains the full originating record: the Chinese
title, Diffie/Hellman attribution, year 1976, gloss `公钥密码学的开创`, importance `高`, and
formalization label `已验证`. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md` repeats the gloss but
explicitly leaves definitions, assumptions, proof path, axioms, and formal artifacts open. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

The gloss says that the work inaugurated public-key cryptography. That is historical assessment,
not a proposition that Lean can elaborate. It does not say whether the target is agreement,
correctness, hardness, security, authentication, or implementation refinement.

## Primary source lead, not credited

Whitfield Diffie and Martin E. Hellman, *New Directions in Cryptography*, IEEE Transactions on
Information Theory 22(6), November 1976, pages 644-654, DOI
`10.1109/TIT.1976.1055638`, is a strong author/year/topic match. Crossref metadata confirms the
bibliography. An 11-page author-hosted scan from
`https://ee.stanford.edu/~hellman/publications/24.pdf` was inspected with SHA-256
`68e2895c270c8c35f423530fcbce7d9ef7111fd891c542c7299c11081a676e15`.

The abstract and introduction distinguish the public-key cryptosystem and public-key distribution
problems. Section III presents public-key cryptography and the discrete-exponentiation distribution
method; later sections discuss one-wayness and computational infeasibility. The article supplies a
protocol/result family, not a modern formal security game selected by the catalog. The scan is an
external discovery input, not a repository-owned source or durable accepted archive. No exact
passage, source-faithful proposition, full incorporated-definition mapping, errata decision, or
independent review is accepted, so this is not H0 evidence.

A modern standards lead, NIST SP 800-56A Rev. 3 (2018), DOI
`10.6028/NIST.SP.800-56Ar3`, Section 5.7.1.1, specifies an FFC DH primitive including domain
parameters, private/public inputs, computation, rejected shared values, byte encoding, and error
output. It demonstrates why protocol correctness is materially richer than a bare exponent law. It
is not attributed by the catalog and is not selected as the canonical target.

## Phrase-to-statement crosswalk

| Repository/source phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `Diffie-Hellman密钥交换` | protocol/result family | exact roles, parameters, transcript, outputs, and claim | family identified; root open |
| `公钥密码学的开创` | historical significance | no truth-valued theorem follows | rejected as statement identity |
| public-key distribution | parties establish a common secret over a public channel | protocol state and honest-output relation | source lead only |
| discrete exponentiation | exponentiation in a finite cyclic group | domain, generator, exponent range, and power operation | generic substrate elaborates |
| common key | algebraic or serialized/derived equality | exact output equality plus success conditions | theorem form open |
| computationally infeasible for an eavesdropper | security/hardness claim | experiment, adversary, advantage, parameters, assumption | absent from catalog; modern form open |
| `已验证` | untrusted inventory label | no statement or proof credit | explicitly rejected |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`IntakeProbe.lean` checks cyclic-group and exponentiation declarations including `IsCyclic`,
`IsCyclic.exists_generator`, `pow_mul`, and `pow_mul'`. A bounded name/content search found no
Diffie-Hellman or key-agreement declaration in pinned mathlib or repository-local Lean. These APIs
can support a later encoding but do not identify the catalog statement or establish protocol
correctness/security. The search is intake discovery, not a global absence claim or the required
anchor audit.
