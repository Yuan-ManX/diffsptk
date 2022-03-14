diffsptk
========
*diffsptk* is a differentiable version of [SPTK](https://github.com/sp-nitech/SPTK) based on the PyTorch framework.

[![](http://img.shields.io/badge/license-Apache%202.0-green.svg)](https://github.com/sp-nitech/diffsptk/blob/master/LICENSE)


Requirements
------------
- PyTorch 1.8.0+


Installation
------------
```sh
git clone https://github.com/sp-nitech/diffsptk.git
pip install -e diffsptk
```


Examples
--------
### Mel-cepstral analysis
```python
import diffsptk
import torch

x = torch.randn(100)

# Compute STFT of x.
stft = diffsptk.STFT(frame_legnth=12, frame_period=10, fft_length=16)
y = stft(x)
```


License
-------
This software is released under the Apache License 2.0.
