#!/usr/bin/env python3

import torch


def permutation_heuristics(pd_mat, k):
    return None


def block_jacobi(pd_mat, k, pi=None):
    from ..lazy import BlockJacobiLazyTensor

    if pi is not None:
        pd_mat = pd_mat[pi, :]
        pd_mat = pd_mat[:, pi]

    n = pd_mat.size(-1)

    num_blocks = n // k
    # last_block_size = n - k * num_blocks

    batched_blocks = torch.zeros(
        num_blocks, k, k,
        device=pd_mat.device,
        dtype=pd_mat.dtype,
    )

    # TODO: Vectorize the for loop
    # for i in range(num_blocks):
    #     batched_blocks[i] = pd_mat[i * k: (i + 1) * k, i * k: (i + 1) * k]
    #     error += 0.
    tmp = pd_mat[:num_blocks * k, :num_blocks * k].view(num_blocks, k, num_blocks * k)
    tmp = tmp.transpose(-2, -1)
    tmp = tmp.view(num_blocks, num_blocks, k, k)
    idx = torch.arange(num_blocks, dtype=torch.long, device=pd_mat.device)
    batched_blocks = tmp[idx, idx, :, :]

    last_block = pd_mat[num_blocks * k:, num_blocks * k:]

    # batched_chol = torch.linalg.cholesky(batched_blocks)
    # last_chol = torch.linalg.cholesky(last_block)

    # tmp = tmp.clone()
    # tmp[idx, idx, :, :] = 0.
    # error = tmp.square().sum() + pd_mat[num_blocks * k:, 0:num_blocks * k].square().sum() * 2
    # print("fro norm diff {:f}".format(error.sqrt().item()))
    # return batched_chol, last_chol, pi

    return BlockJacobiLazyTensor(batched_blocks, last_block)
