MODELS = my_full_neuron_impl \
    my_full_neuron_impl_neuron \
    iaf_psc_exp_nestml_impl

ifneq ($(SPYNNAKER_DEBUG), DEBUG)
    MODELS += my_model_curr_exp_stdp_mad_my_timing_my_weight \
              my_if_curr_exp_sEMD    
endif

all:
	for d in $(MODELS); do $(MAKE) -C $$d || exit $$?; done

clean:
	for d in $(MODELS); do $(MAKE) -C $$d clean || exit $$?; done
