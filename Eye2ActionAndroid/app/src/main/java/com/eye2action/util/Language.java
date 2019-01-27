package com.eye2action.util;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public class Language {

    public enum Name {
        ENGLISH
    }

    private final static int CUSTOM_COMMANDS_NUMBER = 6;

    private final Name name;
    private final Map<Action.Identifier, String> languageMap;
    private final char[] alphabet;

    private String[] customCommandTexts;

    public Language(Name name) {
        this.name = name;
        this.languageMap = new HashMap<>();
        this.customCommandTexts = new String[CUSTOM_COMMANDS_NUMBER];

        switch (name) {
            case ENGLISH:
            default:
                this.alphabet = new char[] {
                    'a',
                    'b',
                    'c',
                    'd',
                    'e',
                    'f',
                    'g',
                    'h',
                    'i',
                    'j',
                    'k',
                    'l',
                    'm',
                    'n',
                    'o',
                    'p',
                    'q',
                    'r',
                    's',
                    't',
                    'u',
                    'v',
                    'w',
                    'x',
                    'y',
                    'z'
                };
                break;
        }

        init();
    }

    private void init() {
        switch (name) {
            case ENGLISH:
            default:
                languageMap.put(Action.Identifier.WRONG, "Wrong");
                languageMap.put(Action.Identifier.YES, "Yes");
                languageMap.put(Action.Identifier.NO, "No");
                languageMap.put(Action.Identifier.OK, "I'm OK");
                languageMap.put(Action.Identifier.NOT_OK, "I'm not OK");
                languageMap.put(Action.Identifier.CALL_GUARDIAN, "Call my guardian");
                languageMap.put(Action.Identifier.CALL_DOCTOR, "Call a doctor");
                languageMap.put(Action.Identifier.WANT_TO_SLEEP, "I want to sleep");
                languageMap.put(Action.Identifier.BREATHLESSNESS, "I can't breathe");
                languageMap.put(Action.Identifier.WATER, "I need water");
                languageMap.put(Action.Identifier.TOILET, "I need to go to toilet");
                languageMap.put(Action.Identifier.HEARTACHE, "I've got a heartache");
                languageMap.put(Action.Identifier.HOW_ARE_YOU, "How are you?");
                languageMap.put(Action.Identifier.EMERGENCY, "Emergency");
                languageMap.put(Action.Identifier.DANGER, "I'm in danger");
                languageMap.put(Action.Identifier.PROBLEM, "I have a problem");
                languageMap.put(Action.Identifier.TRANSFER, "Transfer me");
                languageMap.put(Action.Identifier.I_LOVE_YOU, "I love you");
                languageMap.put(Action.Identifier.SORRY, "Sorry");
                languageMap.put(Action.Identifier.THANK_YOU, "Thank you");
                languageMap.put(Action.Identifier.NEED_A_HUG, "I need a hug");
                languageMap.put(Action.Identifier.LETS_TALK, "Let's talk");
                languageMap.put(Action.Identifier.GO_OUT_IN_THE_OPEN, "Go out in the open");
                languageMap.put(Action.Identifier.WANT_TO_GO_HOME, "I want to go home");
                languageMap.put(Action.Identifier.WANT_TO_MEET_MY_PET, "I want to meet my pet");
                languageMap.put(Action.Identifier.CONGRATULATIONS, "Congratulations!");
                languageMap.put(Action.Identifier.PROUD_OF_YOU, "I'm proud of you");
                languageMap.put(Action.Identifier.IN_PAIN, "I'm in pain");
                languageMap.put(Action.Identifier.CHANGE_POSITION, "I need to change my position");
                languageMap.put(Action.Identifier.FEEL_LIKE_EATING, "I feel like eating");
                languageMap.put(Action.Identifier.ENTERTAINMENT, "I want entertainment");
                languageMap.put(Action.Identifier.ELECTRICAL_APPLIANCE, "I want you to do something with an electrical appliance");
                languageMap.put(Action.Identifier.WIPE, "Wipe");
                languageMap.put(Action.Identifier.MOVE, "Move");
                languageMap.put(Action.Identifier.MASSAGE, "I need a massage");
                languageMap.put(Action.Identifier.HOLD, "Hold");
                languageMap.put(Action.Identifier.LIFT, "Lift");
                languageMap.put(Action.Identifier.WASH, "Wash");
                languageMap.put(Action.Identifier.SCRATCH, "Scratch");
                languageMap.put(Action.Identifier.CHANGE, "Change");
                languageMap.put(Action.Identifier.ADJUST, "Adjust");
                languageMap.put(Action.Identifier.HAPPY_HOLIDAY, "Happy holiday!");
                break;
        }
    }

    public Name getName() {
        return name;
    }

    public String getText(Action.Identifier id) {
        return languageMap.get(id);
    }

    public String getCustomCommandText(int customIndex) {
        return customCommandTexts[customIndex];
    }

    public void setCustomCommandText(int customIndex, String text) {
        customCommandTexts[customIndex] = text;
    }

    public Locale toLocale() {
        switch (name) {
            case ENGLISH:
            default:
                return Locale.ENGLISH;
        }
    }

    public char[] getAlphabet() {
        return alphabet;
    }
}
