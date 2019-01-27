package com.eye2action.util;

import com.eye2action.util.Action.Identifier;

import java.util.HashMap;
import java.util.Map;

public class Parser {

    private final String[] alphabetCommands =
            {
                    "B",
                    "BW",
                    "BU",
                    "BO",
                    "BL",
                    "BR",
                    "BB",
                    "W",
                    "WU",
                    "WO",
                    "WL",
                    "WR",
                    "WW",
                    "WWW",
                    "O",
                    "OO",
                    "U",
                    "UD",
                    "UL",
                    "UR",
                    "UU",
                    "R",
                    "RL",
                    "RR",
                    "L",
                    "WlWr"
            };

    private Map<String, Action> parserMap;
    private Map<String, Character> alphabetMap;

    public Parser(Language language) {
        parserMap = new HashMap<>();
        parserMap.put("S*", Action.newAction(Identifier.START_STOP));
        parserMap.put("B#", Action.newAction(Identifier.WRONG));
        parserMap.put("B", Action.newAction(Identifier.YES));
        parserMap.put("BB", Action.newAction(Identifier.NO));
        parserMap.put("BBB", Action.newAction(Identifier.OK));
        parserMap.put("LRB", Action.newAction(Identifier.NOT_OK));
        parserMap.put("BL", Action.newAction(Identifier.CALL_GUARDIAN));
        parserMap.put("BR", Action.newAction(Identifier.CALL_DOCTOR));
        parserMap.put("BBBB", Action.newAction(Identifier.WANT_TO_SLEEP));
        parserMap.put("L^", Action.newAction(Identifier.BREATHLESSNESS));
        parserMap.put("LR", Action.newAction(Identifier.WATER));
        parserMap.put("U", Action.newAction(Identifier.TOILET));
        parserMap.put("BU", Action.newAction(Identifier.HEARTACHE));
        parserMap.put("BBLBB", Action.newAction(Identifier.HOW_ARE_YOU));
        parserMap.put("W#", Action.newAction(Identifier.EMERGENCY));
        parserMap.put("S*B#", Action.newAction(Identifier.DANGER));
        parserMap.put("WW", Action.newAction(Identifier.PROBLEM));
        parserMap.put("WWO", Action.newAction(Identifier.TRANSFER));
        parserMap.put("WWW", Action.newAction(Identifier.I_LOVE_YOU));
        parserMap.put("UW", Action.newAction(Identifier.SORRY));
        parserMap.put("WrWlBB", Action.newAction(Identifier.THANK_YOU));
        parserMap.put("UDBB", Action.newAction(Identifier.NEED_A_HUG));
        parserMap.put("W", Action.newAction(Identifier.LETS_TALK));
        parserMap.put("BUW", Action.newAction(Identifier.GO_OUT_IN_THE_OPEN));
        parserMap.put("LRW", Action.newAction(Identifier.WANT_TO_GO_HOME));
        parserMap.put("LO", Action.newAction(Identifier.WANT_TO_MEET_MY_PET));
        parserMap.put("BBOBB", Action.newAction(Identifier.CONGRATULATIONS));
        parserMap.put("BBS*", Action.newAction(Identifier.PROUD_OF_YOU));
        parserMap.put("WB", Action.newAction(Identifier.IN_PAIN));
        parserMap.put("OW", Action.newAction(Identifier.CHANGE_POSITION));
        parserMap.put("UD", Action.newAction(Identifier.FEEL_LIKE_EATING));
        parserMap.put("O", Action.newAction(Identifier.ENTERTAINMENT));
        parserMap.put("OB", Action.newAction(Identifier.ELECTRICAL_APPLIANCE));
        parserMap.put("WlWlWrWr", Action.newAction(Identifier.WIPE));
        parserMap.put("WrWrWlWl", Action.newAction(Identifier.SCRATCH));
        parserMap.put("WWB", Action.newAction(Identifier.CHANGE));
        parserMap.put("WWBB", Action.newAction(Identifier.ADJUST));
        parserMap.put("UDW", Action.newAction(Identifier.HAPPY_HOLIDAY));
        parserMap.put("BOB", Action.newAction(Identifier.START_TYPING));
        parserMap.put("UDWW", Action.newAction(Identifier.CUSTOM1));
        parserMap.put("OBOW", Action.newAction(Identifier.CUSTOM2));
        parserMap.put("LBBR", Action.newAction(Identifier.CUSTOM3));
        parserMap.put("RLBBB", Action.newAction(Identifier.CUSTOM4));
        parserMap.put("WlWrWr", Action.newAction(Identifier.CUSTOM5));
        parserMap.put("WlWlBWrWr", Action.newAction(Identifier.CUSTOM6));

        this.alphabetMap = new HashMap<>();

        setLanguage(language);
    }

    public void setLanguage(Language language) {
        alphabetMap.clear();

        for (int i = 0; i < alphabetCommands.length && i < language.getAlphabet().length; i++) {
            this.alphabetMap.put(alphabetCommands[i], language.getAlphabet()[i]);
        }
    }

    public Action parseSequence(String sequence) {
        return parserMap.containsKey(sequence) ? parserMap.get(sequence) : null;
    }

    public Character parseSequenceAlphabetMode(String sequence) {
        return alphabetMap.containsKey(sequence) ? alphabetMap.get(sequence) : null;
    }

}