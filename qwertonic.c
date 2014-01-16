#include <fluidsynth.h>

int main(int argc, char** argv) 
{
    fluid_settings_t* settings;
    fluid_synth_t* synth;
    settings = new_fluid_settings();
    synth = new_fluid_synth(settings);

    /* Do useful things here */

    delete_fluid_synth(synth);
    delete_fluid_settings(settings);
    return 0;
}

void init() 
{
    fluid_settings_t* settings;
    fluid_synth_t* synth;
    fluid_audio_driver_t* adriver;
    settings = new_fluid_settings();

    /* Set the synthesizer settings, if necessary */
    synth = new_fluid_synth(settings);

    fluid_settings_setstr(settings, "audio.driver", "jack");
    adriver = new_fluid_audio_driver(settings, synth);
}
