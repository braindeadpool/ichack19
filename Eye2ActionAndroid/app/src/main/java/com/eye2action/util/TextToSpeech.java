package com.eye2action.util;

import java.util.Set;

public interface TextToSpeech {
  void speak(String text) throws Exception;
  void setLanguage(Language language);
  String getVoice();
  Set<String> getVoices();
  void setVoice(String voice);
}