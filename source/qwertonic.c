#include <fluidsynth.h>

// Example 1
int main(int argc, char** argv) 
{
    fluid_settings_t* settings;
    fluid_synth_t* synth;
    settings = new_fluid_settings();
    fluid_audio_driver_t* adriver;
    synth = new_fluid_synth(settings);
    fluid_settings_setstr(settings, "audio.driver", "coreaudio");
    adriver = new_fluid_audio_driver(settings, synth);

    /* Do useful things here */

    delete_fluid_synth(synth);
    delete_fluid_settings(settings);
    return 0;
}

// Example 3
class SoundButton : public SomeButton
{
public: 

    SoundButton() : SomeButton() {
        if (!_synth) {
            initSynth();
        }
    }

    static void initSynth() {
        _settings = new_fluid_settings();
        _synth = new_fluid_synth(_settings);
        _adriver = new_fluid_audio_driver(_settings, _synth);
    }

    /* ... */

    virtual int handleMouseDown(int x, int y) {
        /* Play a note on key 60 with velocity 100 on MIDI channel 0 */
        fluid_synth_noteon(_synth, 0, 60, 100);
    }

    virtual int handleMouseUp(int x, int y) {
        /* Release the note on key 60 */
        fluid_synth_noteoff(_synth, 0, 60);
    }

protected:

    static fluid_settings_t* _settings;
    static fluid_synth_t* _synth;
    static fluid_audio_driver_t* _adriver;
};
