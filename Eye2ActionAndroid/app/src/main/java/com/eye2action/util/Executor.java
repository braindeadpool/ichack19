package com.eye2action.util;

public class Executor {

    private final TextToSpeech textToSpeech;

    private Language language;
    private String currentWord;
    private Parser parser;

    public Executor(Language language, TextToSpeech textToSpeech) {
        this.textToSpeech = textToSpeech;
        this.textToSpeech.setLanguage(language);
        this.language = language;
        this.parser = new Parser(language);
    }

    public boolean execute(String sequence) throws Exception {
        if (currentWord != null) {
            Character character = parser.parseSequenceAlphabetMode(sequence);

            if (character != null) {
                currentWord += character;
                return true;
            }
            else {
                return false;
            }
        } else {
            return execute(parser.parseSequence(sequence));
        }
    }

    private boolean execute(Action action) throws Exception {
        if (action != null) {
            switch (action.getType()) {
                case START_STOP:
                    if (currentWord != null) {
                        textToSpeech.speak(currentWord);
                    }
                    currentWord = null;
                    break;

                case START_TYPING:
                    currentWord = "";
                    break;

                default:
                    textToSpeech.speak(action.getText(language));
                    break;
            }

            return true;
        } else {
            return false;
        }
    }

    public TextToSpeech getTextToSpeech() {
        return textToSpeech;
    }

    public void setLanguage(Language language) {
        this.language = language;
        textToSpeech.setLanguage(language);
        parser.setLanguage(language);
    }
}
