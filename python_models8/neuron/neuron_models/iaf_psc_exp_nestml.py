#
#  iaf_psc_exp_nestml.py
#
#  This file is part of NEST.
#
#  Copyright (C) 2004 The NEST Initiative
#
#  NEST is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  NEST is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with NEST.  If not, see <http://www.gnu.org/licenses/>.
#
#  Generated from NESTML at time: 2023-04-13 08:44:02.151455

from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModel
from spynnaker.pyNN.models.defaults import default_parameters
from python_models8.neuron.implementations.iaf_psc_exp_nestml_impl import iaf_psc_exp_nestmlImpl


class iaf_psc_exp_nestml(AbstractPyNNNeuronModel):

    def __init__(self,
# XXX: need to print default values here?
                 r,
                 V_m,
                 I_kernel_exc__X__exc_spikes,
                 I_kernel_inh__X__inh_spikes,
                 C_m,
                 tau_m,
                 tau_syn_inh,
                 tau_syn_exc,
                 t_ref,
                 E_L,
                 V_reset,
                 V_th,
                 I_e,
                 exc_spikes,
                 inh_spikes,
                ):

        # compute propagators and other internal parameters
        self.V_.RefractoryCounts = steps(self.P_.t_ref, self._timestep)  # type: integer
        self.V_.__h = self._timestep  # type: ms
        self.V_.__P__V_m__V_m = exp((-self.V_.__h) / self.P_.tau_m)  # type: real
        self.V_.__P__V_m__I_kernel_exc__X__exc_spikes = self.P_.tau_m * self.P_.tau_syn_exc * ((-exp(self.V_.__h / self.P_.tau_m)) + exp(self.V_.__h / self.P_.tau_syn_exc)) * exp((-self.V_.__h) * (self.P_.tau_m + self.P_.tau_syn_exc) / (self.P_.tau_m * self.P_.tau_syn_exc)) / (self.P_.C_m * (self.P_.tau_m - self.P_.tau_syn_exc))  # type: real
        self.V_.__P__V_m__I_kernel_inh__X__inh_spikes = self.P_.tau_m * self.P_.tau_syn_inh * (exp(self.V_.__h / self.P_.tau_m) - exp(self.V_.__h / self.P_.tau_syn_inh)) * exp((-self.V_.__h) * (self.P_.tau_m + self.P_.tau_syn_inh) / (self.P_.tau_m * self.P_.tau_syn_inh)) / (self.P_.C_m * (self.P_.tau_m - self.P_.tau_syn_inh))  # type: real
        self.V_.__P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes = exp((-self.V_.__h) / self.P_.tau_syn_exc)  # type: real
        self.V_.__P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes = exp((-self.V_.__h) / self.P_.tau_syn_inh)  # type: real

        super().__init__(iaf_psc_exp_nestmlImpl(
                 # state:
                 r,
                 V_m,
                 I_kernel_exc__X__exc_spikes,
                 I_kernel_inh__X__inh_spikes,

                 # parameters:
                 C_m,
                 tau_m,
                 tau_syn_inh,
                 tau_syn_exc,
                 t_ref,
                 E_L,
                 V_reset,
                 V_th,
                 I_e,

                 # input ports:
                 exc_spikes,
                 inh_spikes,

                 # internal variables:
                 RefractoryCounts,
                 __h,
                 __P__V_m__V_m,
                 __P__V_m__I_kernel_exc__X__exc_spikes,
                 __P__V_m__I_kernel_inh__X__inh_spikes,
                 __P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes,
                 __P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes,
                                           ))