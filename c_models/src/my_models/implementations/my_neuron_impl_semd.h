#ifndef _NEURON_IMPL_SEMD_H_
#define _NEURON_IMPL_SEMD_H_

#include <neuron/implementations/neuron_impl.h>

// Includes for model parts used in this implementation
#include <neuron/models/neuron_model_lif_impl.h>
#include <neuron/threshold_types/threshold_type_static.h>
#include <neuron/synapse_types/synapse_types_exponential_impl.h>

#include <neuron/current_sources/current_source_impl.h>
#include <neuron/current_sources/current_source.h>

// Further includes
#include <debug.h>

#define V_RECORDING_INDEX 0
#define GSYN_EXC_RECORDING_INDEX 1
#define GSYN_INH_RECORDING_INDEX 2
#define N_RECORDED_VARS 3

#define SPIKE_RECORDING_BITFIELD 0
#define N_BITFIELD_VARS 1

#include <neuron/neuron_recording.h>

typedef struct input_current_semd_receptor {
    // my_multiplicator
    REAL my_multiplicator;

    // previous input value
    REAL my_inh_input_previous;
} semd_receptor;

typedef struct input_type_current_semd_t {
    // receptors for inh inputs
    semd_receptor receptor[NUM_INHIBITORY_RECEPTORS];
} input_type_current_semd_t;

#define SCALING_FACTOR 40.0k

static input_type_current_semd_t *input_type_array;

//! Array of neuron states
static neuron_t *neuron_array;

//! Threshold states array
static threshold_type_t *threshold_type_array;

// The synapse shaping parameters
static synapse_types_t *neuron_synapse_shaping_params;

// The number of steps per timestep to run over
static uint32_t n_steps_per_timestep;

SOMETIMES_UNUSED // Marked unused as only used sometimes
static bool neuron_impl_initialise(uint32_t n_neurons) {
    // Allocate DTCM for neuron array
    neuron_array = spin1_malloc(n_neurons * sizeof(neuron_t));
    if (neuron_array == NULL) {
        log_error("Unable to allocate neuron array - Out of DTCM");
        return false;
    }

    // Allocate DTCM for input type array and copy block of data
    input_type_array =
            spin1_malloc(n_neurons * sizeof(input_type_current_semd_t));
    if (input_type_array == NULL) {
        log_error("Unable to allocate input type array - Out of DTCM");
        return false;
    }

    // Allocate DTCM for threshold type array and copy block of data
    threshold_type_array = spin1_malloc(n_neurons * sizeof(threshold_type_t));
    if (threshold_type_array == NULL) {
        log_error("Unable to allocate threshold type array - Out of DTCM");
        return false;
    }

    // Allocate DTCM for synapse shaping parameters
    neuron_synapse_shaping_params =
            spin1_malloc(n_neurons * sizeof(synapse_types_t));
    if (neuron_synapse_shaping_params == NULL) {
        log_error("Unable to allocate synapse parameters array"
            " - Out of DTCM");
        return false;
    }

    return true;
}

SOMETIMES_UNUSED // Marked unused as only used sometimes
static void neuron_impl_add_inputs(
        index_t synapse_type_index, index_t neuron_index,
        input_t weights_this_timestep) {
    // simple wrapper to synapse type input function
    synapse_types_t *parameters = &neuron_synapse_shaping_params[neuron_index];
    synapse_types_add_neuron_input(synapse_type_index,
            parameters, weights_this_timestep);
}


//! \brief The number of _words_ required to hold an object of given size
//! \param[in] size: The size of object
//! \return Number of words needed to hold the object (not bytes!)
static uint32_t n_words_needed(size_t size) {
    return (size + (sizeof(uint32_t) - 1)) / sizeof(uint32_t);
}

SOMETIMES_UNUSED // Marked unused as only used sometimes
static void neuron_impl_load_neuron_parameters(
        address_t address, uint32_t next, uint32_t n_neurons,
        address_t save_initial_state) {
    log_debug("writing parameters, next is %u, n_neurons is %u ",
            next, n_neurons);
    n_steps_per_timestep = address[next];
    next += 1;

    neuron_params_t *neuron_params = (neuron_params_t *) &address[next];
    for (uint32_t i = 0; i < n_neurons; i++) {
        neuron_model_initialise(&neuron_array[i], &neuron_params[i], n_steps_per_timestep);
    }
    next += n_words_needed(n_neurons * sizeof(neuron_params_t));

    input_type_current_semd_t *input_type_params =
            (input_type_current_semd_t *) &address[next];
    for (uint32_t i = 0; i < n_neurons; i++) {
        input_type_array[i] = input_type_params[i];
    }
    next += n_words_needed(n_neurons * sizeof(input_type_current_semd_t));

    threshold_type_params_t *threshold_params = (threshold_type_params_t *) &address[next];
    for (uint32_t i = 0; i < n_neurons; i++) {
        threshold_type_initialise(&threshold_type_array[i], &threshold_params[i],
                n_steps_per_timestep);
    }
    next += n_words_needed(n_neurons * sizeof(threshold_type_params_t));

    synapse_types_params_t *synapse_params = (synapse_types_params_t *) &address[next];
    for (uint32_t i = 0; i < n_neurons; i++) {
        synapse_types_initialise(&neuron_synapse_shaping_params[i], &synapse_params[i],
                n_steps_per_timestep);
    }
    next += n_words_needed(n_neurons * sizeof(synapse_types_params_t));

    // If we are to save the initial state, copy the whole of the parameters
    // to the initial state
    if (save_initial_state) {
        spin1_memcpy(save_initial_state, address, next * sizeof(uint32_t));
    }
}

SOMETIMES_UNUSED // Marked unused as only used sometimes
static void neuron_impl_do_timestep_update(
        uint32_t timer_count, uint32_t time, uint32_t n_neurons) {

    for (uint32_t neuron_index = 0; neuron_index < n_neurons; neuron_index++) {
        // Get the neuron itself
        neuron_t *neuron = &neuron_array[neuron_index];

        // Get the input_type parameters and voltage for this neuron
        input_type_current_semd_t *input_type = &input_type_array[neuron_index];

        // Get threshold synapse parameters for this neuron
        threshold_type_t *threshold_type =
                &threshold_type_array[neuron_index];
        synapse_types_t *synapse_type =
                &neuron_synapse_shaping_params[neuron_index];

        bool spike = false;
        for (uint32_t i = n_steps_per_timestep; i > 0; i--) {

            // Get the voltage
            state_t voltage = neuron_model_get_membrane_voltage(neuron);

            // Get the exc and inh values from the synapses
            input_t exc_values[NUM_EXCITATORY_RECEPTORS];
            input_t* exc_input_values =
                    synapse_types_get_excitatory_input(exc_values, synapse_type);
            input_t inh_values[NUM_INHIBITORY_RECEPTORS];
            input_t* inh_input_values =
                    synapse_types_get_inhibitory_input(inh_values, synapse_type);

            // Set the inhibitory my_multiplicator value
            for (int i = 0; i < NUM_INHIBITORY_RECEPTORS; i++) {
                if ((inh_input_values[i] >= 0.01k) &&
                        (input_type->receptor[i].my_multiplicator == ZERO) &&
                        (input_type->receptor[i].my_inh_input_previous == ZERO)) {
                    input_type->receptor[i].my_multiplicator = exc_input_values[i];
                } else if (inh_input_values[i] < 0.01k) {
                    input_type->receptor[i].my_multiplicator = ZERO;
                }
                input_type->receptor[i].my_inh_input_previous = inh_input_values[i];
            }

            // Sum g_syn contributions from all receptors for recording
            REAL total_exc = ZERO;
            REAL total_inh = ZERO;

            for (int i = 0; i < NUM_EXCITATORY_RECEPTORS; i++) {
                total_exc += exc_input_values[i];
            }
            for (int i = 0; i < NUM_INHIBITORY_RECEPTORS; i++) {
                total_inh += inh_input_values[i];
            }

            // Do recording if on first step
            if (i == n_steps_per_timestep) {
                neuron_recording_record_accum(V_RECORDING_INDEX, neuron_index, voltage);
                neuron_recording_record_accum(GSYN_EXC_RECORDING_INDEX, neuron_index, total_exc);
                neuron_recording_record_accum(GSYN_INH_RECORDING_INDEX, neuron_index, total_inh);
            }

            // This changes inhibitory to excitatory input
            for (int i = 0; i < NUM_INHIBITORY_RECEPTORS; i++) {
                inh_input_values[i] = -inh_input_values[i] * SCALING_FACTOR
                        * input_type->receptor[i].my_multiplicator;
            }

            // Get any input from an injected current source
            REAL current_offset = current_source_get_offset(time, neuron_index);

            // update neuron parameters
            state_t result = neuron_model_state_update(
                    NUM_EXCITATORY_RECEPTORS, exc_input_values,
                    NUM_INHIBITORY_RECEPTORS, inh_input_values, 0, current_offset, neuron);

            // determine if a spike should occur
            bool spike_now = threshold_type_is_above_threshold(result, threshold_type);

            // If spike occurs, communicate to relevant parts of model
            if (spike_now) {
                // Call relevant model-based functions
                // Tell the neuron model
                spike = true;
                neuron_model_has_spiked(neuron);
                send_spike(timer_count, time, neuron_index);
            }

            // Shape the existing input according to the included rule
            synapse_types_shape_input(synapse_type);
        }

        if (spike) {
            neuron_recording_record_bit(SPIKE_RECORDING_BITFIELD, neuron_index);
        }
    }
}

//! \brief stores neuron parameter back into sdram
//! \param[in] address: the address in sdram to start the store
SOMETIMES_UNUSED // Marked unused as only used sometimes
static void neuron_impl_store_neuron_parameters(
        address_t address, uint32_t next, uint32_t n_neurons) {
    next += 1;

    neuron_params_t *neuron_params = (neuron_params_t *) &address[next];
    for (uint32_t i = 0; i < n_neurons; i++) {
        neuron_model_save_state(&neuron_array[i], &neuron_params[i]);
    }
    next += n_words_needed(n_neurons * sizeof(neuron_t));

    input_type_current_semd_t *input_type_params =
            (input_type_current_semd_t *) &address[next];
    for (uint32_t i = 0; i < n_neurons; i++) {
        input_type_params[i] = input_type_array[i];
    }
    next += n_words_needed(n_neurons * sizeof(input_type_current_semd_t));

    threshold_type_params_t *threshold_params = (threshold_type_params_t *) &address[next];
    for (uint32_t i = 0; i < n_neurons; i++) {
        threshold_type_save_state(&threshold_type_array[i], &threshold_params[i]);
    }
    next += n_words_needed(n_neurons * sizeof(threshold_type_t));

    synapse_types_params_t *synapse_params = (synapse_types_params_t *) &address[next];
    for (uint32_t i = 0; i < n_neurons; i++) {
        synapse_types_save_state(&neuron_synapse_shaping_params[i], &synapse_params[i]);
    }
    next += n_words_needed(n_neurons * sizeof(synapse_types_t));
}

#if LOG_LEVEL >= LOG_DEBUG
SOMETIMES_UNUSED // Marked unused as only used sometimes
static void neuron_impl_print_inputs(uint32_t n_neurons) {
    bool empty = true;
    for (index_t i = 0; i < n_neurons; i++) {
        input_t exc_values[NUM_EXCITATORY_RECEPTORS];
        input_t inh_values[NUM_INHIBITORY_RECEPTORS];
        empty = empty && (0 == bitsk(
                synapse_types_get_excitatory_input(
                        exc_values, &neuron_synapse_shaping_params[i])
                - synapse_types_get_inhibitory_input(
                        inh_values, &neuron_synapse_shaping_params[i])));
    }

    if (!empty) {
        log_debug("-------------------------------------\n");

        for (index_t i = 0; i < n_neurons; i++) {
            input_t exc_values[NUM_EXCITATORY_RECEPTORS];
            input_t inh_values[NUM_INHIBITORY_RECEPTORS];
            input_t input =
                    synapse_types_get_excitatory_input(
                            exc_values, &neuron_synapse_shaping_params[i])
                    - synapse_types_get_inhibitory_input(
                            inh_values, &neuron_synapse_shaping_params[i]);
            if (bitsk(input) != 0) {
                log_debug("%3u: %12.6k (= ", i, input);
                synapse_types_print_input(&neuron_synapse_shaping_params[i]);
                log_debug(")\n");
            }
        }
        log_debug("-------------------------------------\n");
    }
}

SOMETIMES_UNUSED // Marked unused as only used sometimes
static void neuron_impl_print_synapse_parameters(uint32_t n_neurons) {
    log_debug("-------------------------------------\n");
    for (index_t n = 0; n < n_neurons; n++) {
        synapse_types_print_parameters(&neuron_synapse_shaping_params[n]);
    }
    log_debug("-------------------------------------\n");
}

SOMETIMES_UNUSED // Marked unused as only used sometimes
static const char *neuron_impl_get_synapse_type_char(uint32_t synapse_type) {
    return synapse_types_get_type_char(synapse_type);
}
#endif // LOG_LEVEL >= LOG_DEBUG

#endif // _NEURON_IMPL_SEMD_H_
