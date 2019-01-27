package com.eye2action.util;

public class Action {

  public enum Identifier {
    START_STOP,
    WRONG,
    YES,
    NO,
    OK,
    NOT_OK,
    CALL_GUARDIAN,
    CALL_DOCTOR,
    WANT_TO_SLEEP,
    BREATHLESSNESS,
    WATER,
    TOILET,
    HEARTACHE,
    HOW_ARE_YOU,
    EMERGENCY,
    DANGER,
    PROBLEM,
    TRANSFER,
    I_LOVE_YOU,
    SORRY,
    THANK_YOU,
    NEED_A_HUG,
    LETS_TALK,
    GO_OUT_IN_THE_OPEN,
    WANT_TO_GO_HOME,
    WANT_TO_MEET_MY_PET,
    CONGRATULATIONS,
    PROUD_OF_YOU,
    IN_PAIN,
    CHANGE_POSITION,
    FEEL_LIKE_EATING,
    ENTERTAINMENT,
    ELECTRICAL_APPLIANCE,
    WIPE,
    MOVE,
    MASSAGE,
    HOLD,
    LIFT,
    WASH,
    SCRATCH,
    CHANGE,
    ADJUST,
    HAPPY_HOLIDAY,
    START_TYPING,
    CUSTOM1(0),
    CUSTOM2(1),
    CUSTOM3(2),
    CUSTOM4(3),
    CUSTOM5(4),
    CUSTOM6(5);

    int customIndex;

    Identifier() {

    }

    Identifier(int customIndex) {
      this.customIndex = customIndex;
    }

    public int getCustomIndex() {
      return customIndex;
    }
  }

  public enum Type {
    CALL,
    SPEAK,
    START_STOP,
    CUSTOM_SPEAK,
    START_TYPING
  }

  private final Identifier id;
  private final Type type;

  private Action(Identifier id, Type type) {
    this.id = id;
    this.type = type;
  }

  public Identifier getID() {
    return id;
  }

  public Type getType() {
    return type;
  }

  public String getText(Language language) {
    switch (type) {
      case CUSTOM_SPEAK:
        return language.getCustomCommandText(id.getCustomIndex());

      default:
        return language.getText(id);
    }
  }

  public static Action newAction(Identifier id) {
    Type type;

    switch (id) {
      case START_STOP:
        type = Type.START_STOP;
        break;

      case START_TYPING:
        type = Type.START_TYPING;
        break;

      case CUSTOM1:
      case CUSTOM2:
      case CUSTOM3:
      case CUSTOM4:
      case CUSTOM5:
      case CUSTOM6:
        type = Type.CUSTOM_SPEAK;
        break;

      case CALL_DOCTOR:
      case CALL_GUARDIAN:
        type = Type.CALL;
        break;

      default:
        type = Type.SPEAK;
        break;
    }

    return new Action(id, type);
  }

}
