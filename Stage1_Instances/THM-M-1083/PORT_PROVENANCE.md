# THM-M-1083 vendored proof provenance

The terminal theorem `ProbabilityTheory.exists_modification_holder` is vendored from
`RemyDegenne/brownian-motion` at immutable commit
`91885e6172648ea7f9c6a16b3a7069f92c88e023`. Its source is
`BrownianMotion/Continuity/KolmogorovChentsov.lean`; the upstream file has SHA-256
`ce2b9dc8fc18f083d3ebe86c5ef68bd3e8d4e2c1f1587d4fa7c6e503144578a9`.

Upstream used Lean `v4.30.0-rc1` and mathlib
`f23306121184717ace04f3ac514be974e3224c8b`. This proof phase checks the complete 15-file closure
against pinned Lean 4.29.0 and mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The upstream
archive SHA-256 is `74e42a88acbe271a34cba8668ea8bcba8afe38c0818c1de28e42bcd6d53cf20e`;
the upstream `lake-manifest.json` SHA-256 is
`23013991c467cf8f58cba624039478aaf6fdaef2bfcbe2697a3ca56eef907e02`.

## Adaptation

Eight files are byte-identical. Seven files add the standardized local notice and qualify each
internal `BrownianMotion.*` import with
`«Stage1_Instances».«THM-M-1083».Vendor.`. No declaration or proof body changes. Removing that
notice and prefix reconstructs every upstream source byte-for-byte. `check_proof.py` performs the
inverse transformation and checks every digest below.

The upstream closure manifest is the SHA-256 of sorted lines `sha256  BrownianMotion/relative-path`:
`baeba6af6f09aad37899666edf987cba2f75f0ad4dd1740314c2357293f1210c`. The corresponding adapted
manifest is `f43079ae9b6ae2745f57dc63cf07e9508a4532691a99b885bbaf26d33cc9b2aa`.

| Source | Upstream SHA-256 | Adapted SHA-256 |
|---|---|---|
| `Auxiliary/Algebra.lean` | `9bc0dcd6055139822821505897555ae5a501feea0d3a249aa7022b7e6c5b34f3` | `9bc0dcd6055139822821505897555ae5a501feea0d3a249aa7022b7e6c5b34f3` |
| `Auxiliary/ENNReal.lean` | `108c7c5320e163d18e1c250d83a7170e1b80b5b631983f87298df5787c569af6` | `108c7c5320e163d18e1c250d83a7170e1b80b5b631983f87298df5787c569af6` |
| `Auxiliary/FiniteInf.lean` | `042fae3af08e14c603c4cf85742162488d6a7ccc42f74d29ae70854ee38f3f4a` | `042fae3af08e14c603c4cf85742162488d6a7ccc42f74d29ae70854ee38f3f4a` |
| `Auxiliary/MeanInequalities.lean` | `67995c387870e772e8882dea0c7a45168946489d6ffb30c2ba870a2c8b23c50d` | `67995c387870e772e8882dea0c7a45168946489d6ffb30c2ba870a2c8b23c50d` |
| `Auxiliary/MeasureTheory.lean` | `e6637d648b5782dad84bd3fe114e731a31cb2911534f04e2ef27012b8e1ac7a0` | `3df7b5faa5795bda61419b864048349d2ae32d8381a4376bac0a337089b383e6` |
| `Auxiliary/Metric.lean` | `13f5040961175788f8631ba4551a00ef4671a0c172ba85f145c57b025f7b7d9e` | `13f5040961175788f8631ba4551a00ef4671a0c172ba85f145c57b025f7b7d9e` |
| `Auxiliary/Nat.lean` | `43ea36f4a153fd31e5d3f329d094a672270d3bed31728bb2f63d543d994177ae` | `43ea36f4a153fd31e5d3f329d094a672270d3bed31728bb2f63d543d994177ae` |
| `Auxiliary/Topology.lean` | `ce23e4180f97416196f30f05f52756ecc46c99737ec9bb674c9ed3f16014e2b6` | `ce23e4180f97416196f30f05f52756ecc46c99737ec9bb674c9ed3f16014e2b6` |
| `Continuity/Chaining.lean` | `dbb3f80c0e56d708c4dfcd1a30cd7420f280af2f50cdf2785fa2f2ad34cc7b19` | `75e88c2b7800ebf9f0f3b3f52538444e3323a30f0cbfd603847d2874e3db87bc` |
| `Continuity/CoveringNumber.lean` | `89829da52abf33125f18c30f82f2b76d89516682483c1a5cc3caa65d3a649f9d` | `1d4cad9147985c271cd58fc90bc60a8697933258db6b8228a85a0e2f125f543b` |
| `Continuity/HasBoundedInternalCoveringNumber.lean` | `8166a60c831bf60262171d94f53298908e7372ebfb76a136e9e7de6cd4725f03` | `688b05f9a645d3d87f8e5cab131b3d2b1723cac32b44703c8b54d92d45cd29e8` |
| `Continuity/IsKolmogorovProcess.lean` | `e54c594363a9cd15f60faeba19b643e972507d5af568f90ee277ec655ea78dcc` | `62f9ae5b726aba8f36db7a0cb92f9b446ba62e5b583804707aa2ae18b3378a02` |
| `Continuity/KolmogorovChentsov.lean` | `ce2b9dc8fc18f083d3ebe86c5ef68bd3e8d4e2c1f1587d4fa7c6e503144578a9` | `8c60d137ebb5918ebde96e5158867ff5a7e25b9711ef68cbcb9cb4626df9360b` |
| `Continuity/KolmogorovChentsovInequality.lean` | `502061001bd4c2244e3e69d7610aace1e759c0d26f78ada78ccb26e35a6fda51` | `0d8fd8b5bcd66770c79337fbc2ba9dcac7a888c9703f40ac665cef1504a30576` |
| `Gaussian/StochasticProcesses.lean` | `c5fc98b72eb3044fe49add5b47ce10ec8a9aeb1e47aa11aa32a91a2e0c393f81` | `c5fc98b72eb3044fe49add5b47ce10ec8a9aeb1e47aa11aa32a91a2e0c393f81` |

The copied Apache-2.0 `LICENSE` has SHA-256
`c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`.
