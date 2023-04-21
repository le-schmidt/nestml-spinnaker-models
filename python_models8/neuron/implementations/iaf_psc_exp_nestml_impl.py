#
#  iaf_psc_exp_nestml_impl.py
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
#  Generated from NESTML at time: 2023-04-20 14:18:51.159530

from data_specification.enums.data_type import DataType
from spinn_front_end_common.utilities.constants import BYTES_PER_WORD
from spynnaker.pyNN.utilities.struct import Struct
from spynnaker.pyNN.models.neuron.implementations import (
    AbstractNeuronImpl, RangedDictVertexSlice)

from spinn_utilities.overrides import overrides


# TODO: Find way to generate the variable units



class iaf_psc_exp_nestmlImpl(AbstractNeuronImpl):

    def __init__(self,
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
                 # spike input ports:
                 exc_spikes,
                 inh_spikes,
                 # internals:
                 RefractoryCounts,
                 __h,
                 __P__V_m__V_m,
                 __P__V_m__I_kernel_exc__X__exc_spikes,
                 __P__V_m__I_kernel_inh__X__inh_spikes,
                 __P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes,
                 __P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes,
                ):

        # state:
        self._r = r
        self._V_m = V_m
        self._I_kernel_exc__X__exc_spikes = I_kernel_exc__X__exc_spikes
        self._I_kernel_inh__X__inh_spikes = I_kernel_inh__X__inh_spikes
        # parameters:
        self._C_m = C_m
        self._tau_m = tau_m
        self._tau_syn_inh = tau_syn_inh
        self._tau_syn_exc = tau_syn_exc
        self._t_ref = t_ref
        self._E_L = E_L
        self._V_reset = V_reset
        self._V_th = V_th
        self._I_e = I_e
        # spike input ports:
        self._exc_spikes = exc_spikes
        self._inh_spikes = inh_spikes
        # internals:
        self._RefractoryCounts = RefractoryCounts
        self.___h = __h
        self.___P__V_m__V_m = __P__V_m__V_m
        self.___P__V_m__I_kernel_exc__X__exc_spikes = __P__V_m__I_kernel_exc__X__exc_spikes
        self.___P__V_m__I_kernel_inh__X__inh_spikes = __P__V_m__I_kernel_inh__X__inh_spikes
        self.___P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes = __P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes
        self.___P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes = __P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes

        self._struct = Struct([
                 # state:
            (DataType.S1615,   "r"),
            (DataType.S1615,   "V_m"),
            (DataType.S1615,   "I_kernel_exc__X__exc_spikes"),
            (DataType.S1615,   "I_kernel_inh__X__inh_spikes"),
                 # parameters:
            (DataType.S1615,   "C_m"),
            (DataType.S1615,   "tau_m"),
            (DataType.S1615,   "tau_syn_inh"),
            (DataType.S1615,   "tau_syn_exc"),
            (DataType.S1615,   "t_ref"),
            (DataType.S1615,   "E_L"),
            (DataType.S1615,   "V_reset"),
            (DataType.S1615,   "V_th"),
            (DataType.S1615,   "I_e"),
                 # spike input ports:
            (DataType.S1615,   "exc_spikes"),
            (DataType.S1615,   "inh_spikes"),
                 # internals:
            (DataType.S1615,   "RefractoryCounts"),
            (DataType.S1615,   "__h"),
            (DataType.S1615,   "__P__V_m__V_m"),
            (DataType.S1615,   "__P__V_m__I_kernel_exc__X__exc_spikes"),
            (DataType.S1615,   "__P__V_m__I_kernel_inh__X__inh_spikes"),
            (DataType.S1615,   "__P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes"),
            (DataType.S1615,   "__P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes"),
            ])

    @property
    @overrides(AbstractNeuronImpl.structs)
    def structs(self):
        return [self._struct]

    @property
    def model_name(self):
        return "iaf_psc_exp_nestmlImpl"

    @property
    def binary_name(self):
        return "iaf_psc_exp_nestml_impl.aplx"

    def get_global_weight_scale(self):
        # TODO: Update if a weight scale is required
        return 1.

    def get_n_synapse_types(self):
        return 0 \
                + 1 \
                + 1 \
                + 0

    def get_synapse_id_by_target(self, target):
        if target == "exc_spikes":
            return 0
        if target == "inh_spikes":
            return 1
        raise ValueError("Unknown target {}".format(target))

    def get_synapse_targets(self):
        return [
            "exc_spikes",
            "inh_spikes",
               ]
    @overrides(AbstractNeuronImpl.get_recordable_variables)
    def get_recordable_variables(self):
        return [
            "r",
            "V_m",
            "I_kernel_exc__X__exc_spikes",
            "I_kernel_inh__X__inh_spikes", 
        ]

    def get_recordable_data_types(self):
        return {
            "r": DataType.S1615,
            "V_m": DataType.S1615,
            "I_kernel_exc__X__exc_spikes": DataType.S1615,
            "I_kernel_inh__X__inh_spikes": DataType.S1615,
            }

    def get_recordable_units(self, variable):
    # TODO: Find way to print units not datatypes
        if variable == "r":
            return "integer"
        if variable == "V_m":
            return "mV"
        if variable == "I_kernel_exc__X__exc_spikes":
            return "real"
        if variable == "I_kernel_inh__X__inh_spikes":
            return "real"
        raise ValueError("Unknown variable {}".format(variable))

    def get_recordable_variable_index(self, variable):
        if variable == "r":
            return 0
        if variable == "V_m":
            return 1
        if variable == "I_kernel_exc__X__exc_spikes":
            return 2
        if variable == "I_kernel_inh__X__inh_spikes":
            return 3

        raise ValueError("Unknown variable {}".format(variable))

    def is_recordable(self, variable):
        return variable in [
        "r",
        "V_m",
        "I_kernel_exc__X__exc_spikes",
        "I_kernel_inh__X__inh_spikes",
                           ]

    def add_parameters(self, parameters):
        parameters["C_m"] = self._C_m
        parameters["tau_m"] = self._tau_m
        parameters["tau_syn_inh"] = self._tau_syn_inh
        parameters["tau_syn_exc"] = self._tau_syn_exc
        parameters["t_ref"] = self._t_ref
        parameters["E_L"] = self._E_L
        parameters["V_reset"] = self._V_reset
        parameters["V_th"] = self._V_th
        parameters["I_e"] = self._I_e

    def add_state_variables(self, state_variables):
        state_variables["r"] = self._r
        state_variables["V_m"] = self._V_m
        state_variables["I_kernel_exc__X__exc_spikes"] = self._I_kernel_exc__X__exc_spikes
        state_variables["I_kernel_inh__X__inh_spikes"] = self._I_kernel_inh__X__inh_spikes

    def get_units(self, variable):
    #TODO: Find way to print units instead of data types
        # state:
        if variable == "r":
            return "integer"
        if variable == "V_m":
            return "mV"
        if variable == "I_kernel_exc__X__exc_spikes":
            return "real"
        if variable == "I_kernel_inh__X__inh_spikes":
            return "real"
        # parameters:
        if variable == "C_m":
            return "pF"
        if variable == "tau_m":
            return "ms"
        if variable == "tau_syn_inh":
            return "ms"
        if variable == "tau_syn_exc":
            return "ms"
        if variable == "t_ref":
            return "ms"
        if variable == "E_L":
            return "mV"
        if variable == "V_reset":
            return "mV"
        if variable == "V_th":
            return "mV"
        if variable == "I_e":
            return "pA"
        # spike input ports:
        if variable == "exc_spikes":
            return "pA buffer"
        if variable == "inh_spikes":
            return "pA buffer"
        # internal parameters:
        if variable == "RefractoryCounts":
            return "integer"
        if variable == "__h":
            return "ms"
        if variable == "__P__V_m__V_m":
            return "real"
        if variable == "__P__V_m__I_kernel_exc__X__exc_spikes":
            return "real"
        if variable == "__P__V_m__I_kernel_inh__X__inh_spikes":
            return "real"
        if variable == "__P__I_kernel_exc__X__exc_spikes__I_kernel_exc__X__exc_spikes":
            return "real"
        if variable == "__P__I_kernel_inh__X__inh_spikes__I_kernel_inh__X__inh_spikes":
            return "real"

        raise ValueError("Unknown variable {}".format(variable))

    @property
    def is_conductance_based(self):
        # TODO: Update if uses conductance
        return False