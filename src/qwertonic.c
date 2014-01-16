#include <fluidsynth.h>

// Example 1
int main(int argc, char** argv) 
{
    fluid_settings_t* settings;
    fluid_synth_t* synth;
    fluid_audio_driver_t* adriver;

    settings = new_fluid_settings();
    synth = new_fluid_synth(settings);
    fluid_settings_setstr(settings, "audio.driver", "coreaudio");
    adriver = new_fluid_audio_driver(settings, synth);

	fluid_synth_noteon(synth, 0, 60, 100);
	// we should wait here
	// not currently sure how
	fluid_synth_noteoff(synth, 0, 60);

	delete_fluid_audio_driver(adriver);
    delete_fluid_synth(synth);
    delete_fluid_settings(settings);
    return 0;
}
