from spinn_utilities.overrides import overrides
from data_specification.enums import DataType
from spinn_front_end_common.utilities.constants import BYTES_PER_WORD
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence import (
    AbstractTimingDependence)
from spynnaker.pyNN.models.neuron.plasticity.stdp.synapse_structure import (
    SynapseStructureWeightOnly)


class MyTimingDependence(AbstractTimingDependence):
    __slots__ = [
        "_a_minus",
        "_a_plus",
        "_my_depression_parameter",
        "_my_potentiation_parameter",
        "_synapse_structure"]

    NUM_PARAMETERS = 2

    # noinspection PyPep8Naming
    def __init__(
            self,

            # TODO: update parameters
            my_potentiation_parameter,
            my_depression_parameter,

            A_plus=0.01, A_minus=0.01):

        # TODO: Store any parameters
        self._my_potentiation_parameter = my_potentiation_parameter
        self._my_depression_parameter = my_depression_parameter

        # TODO: Update to match the synapse structure in the C code
        self._synapse_structure = SynapseStructureWeightOnly()

        # Are these in the c code?
        self._a_plus = A_plus
        self._a_minus = A_minus

    # TODO: Add getters and setters for parameters

    @property
    def my_potentiation_parameter(self):
        return self._my_potentiation_parameter

    @my_potentiation_parameter.setter
    def my_potentiation_parameter(self, my_potentiation_parameter):
        self._my_potentiation_parameter = my_potentiation_parameter

    @property
    def my_depression_parameter(self):
        return self._my_depression_parameter

    @my_depression_parameter.setter
    def my_depression_parameter(self, my_depression_parameter):
        self._my_depression_parameter = my_depression_parameter

    @overrides(AbstractTimingDependence.is_same_as)
    def is_same_as(self, timing_dependence):
        # TODO: Update with the correct class name
        if not isinstance(timing_dependence, MyTimingDependence):
            return False

        # TODO: update to check parameters are equal
        return (
            (self._my_potentiation_parameter ==
                timing_dependence.my_potentiation_parameter) and
            (self._my_depression_parameter ==
                timing_dependence.my_depression_parameter))

    @property
    def vertex_executable_suffix(self):
        """ The suffix to be appended to the vertex executable for this rule
        """
        # TODO: Add the extension to be added to the binary executable name
        # to indicate that it is compiled with this timing dependence
        # Note: The expected format of the binary name is:
        #    <neuron_model>_stdp[_mad|]_<timing_dependence>_<weight_dependence>
        return "my_timing"

    @property
    def pre_trace_n_bytes(self):
        """ The number of bytes used by the pre-trace of the rule per neuron
        """
        # TODO: update to match the number of bytes in the pre_trace_t data
        # structure in the C code
        return 0

    @overrides(AbstractTimingDependence.get_parameters_sdram_usage_in_bytes)
    def get_parameters_sdram_usage_in_bytes(self):
        # TODO: update to match the number of bytes used by the parameters
        return self.NUM_PARAMETERS * BYTES_PER_WORD

    @property
    def n_weight_terms(self):
        """ The number of weight terms expected by this timing rule
        """
        # TODO: update to match the number of weight terms expected in the
        # weight rule according to the C code
        return 1

    @overrides(AbstractTimingDependence.write_parameters)
    def write_parameters(
            self, spec, global_weight_scale, synapse_weight_scales):
        # TODO: update to write the parameters
        spec.write_value(
            self._my_potentiation_parameter, data_type=DataType.S1615)
        spec.write_value(
            self._my_depression_parameter, data_type=DataType.S1615)

    @overrides(AbstractTimingDependence.get_parameter_names)
    def get_parameter_names(self):
        return ['my_potentiation_parameter', 'my_depression_parameter']

    @property
    def synaptic_structure(self):
        """ Get the synaptic structure of the plastic part of the rows
        """
        return self._synapse_structure

    @property
    def A_plus(self):
        return self._a_plus

    @A_plus.setter
    def A_plus(self, new_value):
        self._a_plus = new_value

    @property
    def A_minus(self):
        return self._a_minus

    @A_minus.setter
    def A_minus(self, new_value):
        self._a_minus = new_value
