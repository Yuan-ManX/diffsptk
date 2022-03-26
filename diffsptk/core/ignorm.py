# ------------------------------------------------------------------------ #
# Copyright 2022 SPTK Working Group                                        #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
# ------------------------------------------------------------------------ #

import warnings

import torch
import torch.nn as nn


class GeneralizedCepstrumInverseGainNormalization(nn.Module):
    """See `this page <https://sp-nitech.github.io/sptk/latest/main/ignorm.html>`_
    for details.

    Parameters
    ----------
    gamma : float [-1 <= gamma <= 1]
        Gamma.

    c : int >= 1
        Inverse gamma.

    """

    def __init__(self, gamma=0, c=None):
        super(GeneralizedCepstrumInverseGainNormalization, self).__init__()

        if c is None:
            self.gamma = gamma
        else:
            if gamma != 0:
                warnings.warn("gamma is given, but not used")
            self.gamma = 1 / c

    def forward(self, y):
        """Perform cepstrum inverse gain normalization.

        Parameters
        ----------
        y : Tensor [shape=(..., M+1)]
            Normalized generalized cepstrum.

        Returns
        -------
        x : Tensor [shape=(..., M+1)]
            Generalized cepstrum

        Examples
        --------
        >>> x = diffsptk.ramp(1, 4)
        >>> gnorm = diffsptk.GeneralizedCepstrumGainNormalization(c=2)
        >>> ignorm = diffsptk.GeneralizedCepstrumInverseGainNormalization(c=2)
        >>> x2 = ignorm(gnorm(x))
        >>> x2
        tensor([1., 2., 3., 4.])

        """
        K = y[..., :1]
        y = y[..., 1:]
        if self.gamma == 0:
            x0 = torch.log(K)
            x1 = y
        else:
            z = torch.pow(K, self.gamma)
            x0 = (z - 1) / self.gamma
            x1 = y * z

        x = torch.cat((x0, x1), dim=-1)
        return x
