# flash-atten Python wheel index

This repo creates a index that links back to the releases from https://github.com/Dao-AILab/flash-attention/releases. This allows you to install `flash-atten` without building the wheel on your machine.

## Usage

If you installed PyTorch from PyPI, then install `flash-attn` with:

```bash
export TORCH=torch2.6
export CXX=cxx11abiFALSE

pip install flash-attn \
    --extra-index-url https://thomasjpfan.github.io/flash-atten-whl/cu12/$TORCH/$CXX/
```

where `TORCH` is your PyTorch version. `CXX` should be set to `cxx11abiFALSE` your PyTorch was compiled with `_GLIBCXX_USE_CXX11_ABI`.

- `CXX=cxx11abiFALSE`: If you installed PyTorch from PyPI, then you likely need `CXX=cxx11abiFALSE`
- `CXX=cxx11abiTRUE`: If you got PyTorch from a nvcr image, then you likely need `CXX=cxx11abiTRUE`

To confirm, please run [torch.compiled_with_cxx11_abi()](https://pytorch.org/docs/stable/generated/torch.compiled_with_cxx11_abi.html).
