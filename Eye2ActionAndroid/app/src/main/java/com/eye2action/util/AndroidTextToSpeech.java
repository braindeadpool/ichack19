package com.eye2action.util;

import android.content.Context;

import java.util.Set;

public class AndroidTextToSpeech implements TextToSpeech {

    private final android.speech.tts.TextToSpeech textToSpeech;

    public AndroidTextToSpeech(Context context, android.speech.tts.TextToSpeech.OnInitListener listener) {
        this.textToSpeech = new android.speech.tts.TextToSpeech(context, listener);
    }

    @Override
    public void speak(String text) throws Exception {
        this.textToSpeech.speak(text, android.speech.tts.TextToSpeech.QUEUE_FLUSH, null);
    }

    @Override
    public void setLanguage(Language language) {

    }

    @Override
    public String getVoice() {
        return null;
    }

    @Override
    public Set<String> getVoices() {
        return null;
    }

    @Override
    public void setVoice(String voice) {

    }
}
