package org.deviceconnect.android.deviceplugin.robotarm.arm;

public interface IRobtArm {
    void init();
    void destroy();
    boolean isRobotArm();
    void rotate(int channel, boolean turn, int hz, int value, int time);
    void stopArmRotation(int channel);
    void grabHand(final int hz, final int value);
    void releaseHand();
    void stopHand();

}
