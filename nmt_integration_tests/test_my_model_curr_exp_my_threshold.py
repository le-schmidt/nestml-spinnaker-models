# Copyright (c) 2017-2023 The University of Manchester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyNN.spiNNaker as sim
from .nwt_testbase import NwtTestBase
from python_models8.neuron.builds.my_model_curr_exp_my_threshold import (
    MyModelCurrExpMyThreshold)

# Set the run time of the execution
run_time = 1000


class TestMyModelCurrExpMyThreshold(NwtTestBase):

    def do_run(self):
        sim.setup(timestep=1.0)
        input_pop = sim.Population(
            1, sim.SpikeSourceArray(range(0, run_time, 100)), label="input")
        test_pop = sim.Population(
            1, MyModelCurrExpMyThreshold(
                my_neuron_parameter=-70.0, i_offset=0.0,
                threshold_value=-10.0, my_threshold_parameter=0.4),
            label="my_model_threshold_pop")
        test_pop.record(['spikes', 'v'])
        sim.Projection(
            input_pop, test_pop, sim.AllToAllConnector(),
            receptor_type='excitatory',
            synapse_type=sim.StaticSynapse(weight=2.0))
        sim.run(run_time)
        neo = test_pop.get_data('all')
        sim.end()
        self.check_results(
            neo, [404, 901])

    def test_do_run(self):
        self.runsafe(self.do_run)
