# flash-attn Python wheel index

This repo creates a wheel index that links back to the releases from [github.com/Dao-AILab/flash-attention/releases](https://github.com/Dao-AILab/flash-attention/releases). This allows you to install `flash-attn` without building the wheel locally.

## Usage

If you installed PyTorch from PyPI, then install `flash-attn` with:

```bash
export TORCH=torch2.6

pip install flash-attn \
    --extra-index-url https://thomasjpfan.github.io/flash-attn-whl/cu12/$TORCH/cxx11abiFALSE
```

where `TORCH` is your PyTorch version.

### PyTorch compiled with CXX11ABI

If you got PyTorch from a nvcr image, then you likely need wheels built with `cxx11abiTRUE`:

```bash
export TORCH=torch2.6
export CXX=cxx11abiTRUE

pip install flash-attn \
    --extra-index-url https://thomasjpfan.github.io/flash-attn-whl/cu12/$TORCH/$CXX
```

To confirm, please run [torch.compiled_with_cxx11_abi()](https://pytorch.org/docs/stable/generated/torch.compiled_with_cxx11_abi.html). Overall:

- If you install PyTorch from a nvcr image, then you likely need `CXX=cxx11abiTRUE`
- If you installed PyTorch from PyPI, then you likely need `CXX=cxx11abiFALSE`

## Navigate the index

This [wheel index](https://thomasjpfan.github.io/flash-attn-whl/) is split into the variants shown in [github.com/Dao-AILab/flash-attention/releases](https://github.com/Dao-AILab/flash-attention/releases): CUDA version, PyTorch version, and `CXX11ABI`. If a release does not have any generated wheels, it will be excluded from this index.
