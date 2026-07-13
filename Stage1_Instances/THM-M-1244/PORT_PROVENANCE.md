# Gaussian Log-Sobolev Port Provenance

The Lean sources below vendor the complete import closure of
`GaussianLSI.gaussian_logSobolev_W12_pi` from:

- Repository: <https://github.com/YuanheZ/lean-stat-learning-theory>
- Revision: `7b82b1323c80f0c21ca449fd12e1c24315ae9782`
- Source tree: `SLT`
- Declared license: Apache-2.0 in every vendored source header
- Target environment: Lean 4.29.0 and mathlib
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`

The immutable archive does not contain a root `LICENSE`, `COPYING`, or `NOTICE` file even though
its source headers refer to `LICENSE`. This directory therefore supplies the standard Apache 2.0
license text in `LICENSE`; it is not represented as a byte copy from the absent upstream file.

No theorem statement, assumption, or proof argument was weakened. The closure contains 24 modules,
35 internal `SLT` import edges, 17,391 lines, and 876,559 bytes including notices. Sixteen files are
byte-identical to the immutable source. Eight files carry a two-line port notice after their
existing license header and the API-only changes listed below. The table binds every source file to
its immutable upstream bytes and to the local port bytes.

| Vendored path | Upstream SHA-256 | Vendored SHA-256 |
|---|---|---|
| `SLT/ConvergenceL1Subseq.lean` | `9c68b82984246989606811af9dc629925b7b4cf33bb93b9639038be1ab2e4236` | `9c68b82984246989606811af9dc629925b7b4cf33bb93b9639038be1ab2e4236` |
| `SLT/EfronStein.lean` | `5c1880799e993d938174138055fa2027f0cfb6cfe350be07bdfe61578759d179` | `44354c785c5ac07f7da08d21ed38f537fd1299efc9579aa1bdaffb0c435b6456` |
| `SLT/GaussianLSI/BernoulliLSI.lean` | `f7559b7951cf84623385eb47847a9c3a2dd5978282f72250ff9410b79029b984` | `36bd56b4c667ab6e8b7c9edaa5d640405cba7c1ec49636e435bb36ed7a9eda11` |
| `SLT/GaussianLSI/DualEntApp.lean` | `d2854bb651567555867f649d2feff5bfd5533d13def74a58828b6e78a3d233e6` | `d2854bb651567555867f649d2feff5bfd5533d13def74a58828b6e78a3d233e6` |
| `SLT/GaussianLSI/DualityEntropy.lean` | `8cbfae7f02a04c99e0328c5d33f1ab022e4b54269333f13124cbdb7ee30377b5` | `8cbfae7f02a04c99e0328c5d33f1ab022e4b54269333f13124cbdb7ee30377b5` |
| `SLT/GaussianLSI/Entropy.lean` | `00530d1b319448a5a668439018da08b7bd9b40be518262e108fe4ac9ffcdc6b7` | `00530d1b319448a5a668439018da08b7bd9b40be518262e108fe4ac9ffcdc6b7` |
| `SLT/GaussianLSI/OneDimGLSI.lean` | `d3e36df5fcc34c1e61be53e538f457c0a657e36929f60dea92fc90b8c661001b` | `d3e36df5fcc34c1e61be53e538f457c0a657e36929f60dea92fc90b8c661001b` |
| `SLT/GaussianLSI/OneDimGLSICompSmo.lean` | `ebe756ab83c2439881aa3805fd1de5073c5166f94fa7fbb6e641506502cc13c1` | `ebe756ab83c2439881aa3805fd1de5073c5166f94fa7fbb6e641506502cc13c1` |
| `SLT/GaussianLSI/SubAddEnt/Basic.lean` | `02c10a2452dd29d6f6cb3b69e43904a5eafeed1e932b129e0f699f43a6a24e60` | `02c10a2452dd29d6f6cb3b69e43904a5eafeed1e932b129e0f699f43a6a24e60` |
| `SLT/GaussianLSI/SubAddEnt/Decomposition.lean` | `e4e6641911c25b40ebd0047f23da951ba87fb2fd92d43740d1ab8318e737d955` | `e4e6641911c25b40ebd0047f23da951ba87fb2fd92d43740d1ab8318e737d955` |
| `SLT/GaussianLSI/SubAddEnt/Subadditivity.lean` | `56e92f6158b1ad6af070b94680777f392970c38ccce71ff1aae745bb1b6c2ac0` | `56e92f6158b1ad6af070b94680777f392970c38ccce71ff1aae745bb1b6c2ac0` |
| `SLT/GaussianLSI/TensorizedGLSI.lean` | `22eefaf07248a28de214b07154ecd953e50ed7c9432931ac9e2fe34ea9c45e29` | `22eefaf07248a28de214b07154ecd953e50ed7c9432931ac9e2fe34ea9c45e29` |
| `SLT/GaussianLSI/TwoPoint.lean` | `b74b7bd6edba94b9b64b7605865b4d4630591b785cb145e787a3aabab5ae4520` | `b74b7bd6edba94b9b64b7605865b4d4630591b785cb145e787a3aabab5ae4520` |
| `SLT/GaussianMeasure.lean` | `c679103bbd2a7e2fc652e1c13cba264d012964e6815ab50ef9546c58b3412907` | `c679103bbd2a7e2fc652e1c13cba264d012964e6815ab50ef9546c58b3412907` |
| `SLT/GaussianPoincare/EfronSteinApp.lean` | `822375e389fe964533054515c7ceb03c1c41fd27fadd31a2f09aa1916ba7e63f` | `2b5631646fc83b07d45d2fc515c407e07ae8dc219f8fe1150736bcf0f30b780d` |
| `SLT/GaussianPoincare/LevyContinuity.lean` | `c43b8d505fd646fd7340a8f29b7364ea134897f71ca8f32d1a5b5203707546c9` | `c71e1289fe5f75030ff32465ada05b1522b45009e4844b418f596ab889914d1a` |
| `SLT/GaussianPoincare/Limit.lean` | `ac574efd3fb6d67c47259760265db0565b6c93975d54a21e6d959ec7db117169` | `c6c88ea7022fa12e9cb46b4a5667a054300755793fe397416601df8bf8e0a684` |
| `SLT/GaussianPoincare/RademacherApprox.lean` | `796b6d91ff2fd1c2e8702a0e2c7a0af1197ef36c2b2f6dfccd4b69703b343f45` | `7ef64a5fc146c92729d1423390f6c99f7bb02311b1e6643c869c95db06e1453b` |
| `SLT/GaussianPoincare/TaylorBound.lean` | `f62c49a5fd5be645a97515b40bfd2a5759cfce142f47ea8935231fa14322a0b0` | `863b6903e2fa482631be039f4bef6a0e9af33bae2b4b1f69529fb41aa99aee84` |
| `SLT/GaussianSobolevDense/Cutoff.lean` | `320a4547b0fb1ad886d58451bd43aec61f4a6d01a0051966528ebe3504194dd0` | `320a4547b0fb1ad886d58451bd43aec61f4a6d01a0051966528ebe3504194dd0` |
| `SLT/GaussianSobolevDense/Defs.lean` | `a587ce9b807413eef7c49045db83187f0b1bcf23f03831522172094967f62b3a` | `a587ce9b807413eef7c49045db83187f0b1bcf23f03831522172094967f62b3a` |
| `SLT/GaussianSobolevDense/Density.lean` | `356e93dfdc51936c1ec37a25f23434ab6966acc3379a350be2ee02996e7f0374` | `356e93dfdc51936c1ec37a25f23434ab6966acc3379a350be2ee02996e7f0374` |
| `SLT/GaussianSobolevDense/Mollification.lean` | `98e65bbfe6a509332a4213121a4b30bdde001c6aba848e8a7beb2e56133792a9` | `40c30859078f52a87b724aace4d1f829941810149f74c66f1458c501d3aa54cd` |
| `SLT/MeasureInfrastructure.lean` | `21fd2a3c99695943d3b6e0d9b977d5816aedfe73a02cf522365a0ae7af6cec7a` | `21fd2a3c99695943d3b6e0d9b977d5816aedfe73a02cf522365a0ae7af6cec7a` |

## Exact Compatibility Edits

Apart from each changed file's port notice, the complete semantic diff is:

- `EfronStein.lean`: replace an intermediate `rw [MeasurableEquiv.map_symm_map]` proof with the
  current `e.map_symm_map.symm.trans (congrArg (Measure.map e.symm) h1)` equality chain.
- `BernoulliLSI.lean`: remove the obsolete explicit wildcard argument from
  `integral_fintype Integrable.of_finite`.
- `EfronSteinApp.lean` and `RademacherApprox.lean`: use the current theorem name
  `Measure.ae_ennreal_smul_measure_iff` instead of `Measure.ae_smul_measure_iff`.
- `LevyContinuity.lean`: rename its local `tendsto_iSup_of_tendsto_limsup` helper to avoid a
  current namespace collision; replace three ambiguous `zero_le'` terms with typed `bot_le` or
  `zero_le _`; use `exact integral_const_mul _ _` where `rw` no longer selects the intended side.
- `Limit.lean`: import `Mathlib.Analysis.Complex.Asymptotics`; replace an expanded proof with the
  current `Complex.tendsto_pow_exp_of_isLittleO_sub_add_div` theorem; make the real scalar action
  on complex numbers explicit before rewriting with `Complex.real_smul`.
- `TaylorBound.lean`: remove an obsolete no-progress `simp only [hone_eq] at hξ_eq` step.
- `Mollification.lean`: replace removed empty-fintype product simp lemmas with `simp`.

The compatibility checker removes exactly the notices, mechanically inverts these eight edits,
and verifies all reconstructed SHA-256 values. This makes any unrecorded source change fail closed.
