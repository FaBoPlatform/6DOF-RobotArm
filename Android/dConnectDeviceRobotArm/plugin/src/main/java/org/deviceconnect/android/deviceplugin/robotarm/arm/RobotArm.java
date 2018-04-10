package org.deviceconnect.android.deviceplugin.robotarm.arm;

import android.os.Handler;
import android.util.Log;

import com.google.android.things.pio.Gpio;
import com.google.android.things.pio.I2cDevice;
import com.google.android.things.pio.PeripheralManager;
import com.google.android.things.pio.Pwm;

import org.deviceconnect.android.deviceplugin.robotarm.BuildConfig;

import java.io.IOException;

public class RobotArm implements IRobtArm {

    private final static String TAG = "ROBOTARM";
    private Gpio[] mArmGpio = new Gpio[5];
    private String[] PIN_NAME =  {"BCM4", "BCM5", "BCM6", "BCM12","BCM21"};
    private I2cDevice mDevice;


    // I2C Device Name
    private static final String I2C_DEVICE_NAME = "I2C1";
    // I2C Slave Address
    private static final double OSC_CLOCK = 25000000.0;
    private static final int I2C_ADDRESS = 0x40;
    private static final int MODE1 = 0x00; // Mode register 1
    private static final int MODE2 = 0x01; // Mode register 2
    private static final int ALL_LED_ON_L = 0xFA; // load all the LEDn_ON registers, byte 0
    private static final int ALL_LED_ON_H = 0xFB; // load all the LEDn_ON registers, byte 1
    private static final int ALL_LED_OFF_L = 0xFC; // load all the LEDn_OFF registers, byte 0
    private static final int ALL_LED_OFF_H = 0xFD; // load all the LEDn_OFF registers, byte 1
    private static final int ALLCALL = 0x01;
    private static final int OUTDRV = 0x04; // 2bit
    private static final int SLEEP = 0x10;
    private static final int PRE_SCALE = 0xFE; // prescaler for PWM output frequency
    private static final int RESTART = 0x80;
    private static final int LED0_ON_L = 0x06;
    private static final int LED0_ON_H = 0x07;
    private static final int LED0_OFF_L = 0x08;
    private static final int LED0_OFF_H = 0x09;


    public RobotArm() {
        init();
    }
    @Override
    public void init() {
        try {

            for(int i = 0; i < mArmGpio.length; i++) {
                mArmGpio[i] = PeripheralManager.getInstance().openGpio(PIN_NAME[i]);
                mArmGpio[i].setDirection(Gpio.DIRECTION_OUT_INITIALLY_LOW);
            }
            mDevice = PeripheralManager.getInstance().openI2cDevice(I2C_DEVICE_NAME, I2C_ADDRESS);
            initPCA9685();
        } catch (IOException e) {
            Log.e(TAG, "Error on PeripheralIO API", e);
        }
    }

    @Override
    public void destroy() {
        for(int i = 0; i < mArmGpio.length; i++) {
            if (mArmGpio[i] != null) {
                try {
                    mArmGpio[i].close();
                    mArmGpio[i] = null;
                } catch (IOException e) {
                    Log.e(TAG, "Unable to close  arms", e);
                }
            }
        }
    }

    @Override
    public boolean isRobotArm() {
        // Armの初期化が行われているかどうか
        boolean isGPIOs = false;
        for (int i = 0; i < mArmGpio.length; i++) {
            if (mArmGpio[i] != null) {
                isGPIOs = true;
                break;
            }
        }
        return isGPIOs;
    }

    @Override
    public void rotate(final int channel, final boolean turn, final int hz, final int value, final int time) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    mArmGpio[channel].setValue(turn);
                    try {
                        Thread.sleep((long) 50);
                    } catch (InterruptedException e) {
                        Log.e(TAG, "Interrupted1", e);
                    }
                    setHz(hz);
                    setChannelValue(channel,  0, value);
                    try {
                        Thread.sleep((long) time);
                    } catch (InterruptedException e) {
                        Log.e(TAG, "Interrupted1", e);
                    }
                    setChannelValue(channel,  0, 0);

                } catch (IOException e) {
                    Log.e(TAG, "Error on PeripheralIO API", e);
                }

            }
        }).start();
    }

    @Override
    public void stopArmRotation(final int channel) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                setChannelValue(channel, 0, 0);
            }
        }).start();
    }
    @Override
    public void grabHand(final int hz, final int value, final int time) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                setHz(10);
                setChannelValue(5,  0, value);
                try {
                    Thread.sleep((long) 50);
                } catch (InterruptedException e) {
                    Log.e(TAG, "PWM error", e);
                }
            }
        }).start();
    }

    @Override
    public void releaseHand() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                // TODO 離す処理
            }
        }).start();
    }

    @Override
    public void stopHand() {
        new Thread(new Runnable() {
            @Override
            public void run() {
            }
        }).start();
    }
    //*********************
    // ステッピングモーター
    //*********************
    private void initPCA9685() {
        // 通電時、PCA9685の全channleの値は、サーボ稼働範囲外の4096になっているのでこれを適切な範囲に設定しておく
        try {
            setAllPWM(0,0);
            mDevice.writeRegByte(MODE2,(byte)(OUTDRV));
            mDevice.writeRegByte(MODE1,(byte)(ALLCALL));
            try {
                Thread.sleep((long) 50);
            } catch (InterruptedException e) {
                Log.e(TAG, "PWM error", e);
            }

            // スリープ状態なら解除する
            byte mode = mDevice.readRegByte(MODE1);
            mode = (byte) (mode & ~SLEEP); // SLEEPビットを除去する

            mDevice.writeRegByte(MODE1, mode);
            try {
                Thread.sleep((long) 50);
            } catch (InterruptedException e) {
                Log.e(TAG, "PWM error", e);
            }
        } catch (IOException e) {
            Log.e(TAG, "PWM error", e);
        }
    }
    private void getRegisterByHz(int i) {
        try {
            // スリープ状態なら解除する
            byte mode = mDevice.readRegByte(PRE_SCALE);
            Log.d(TAG, i +"HZ:" + mode);
        } catch (IOException e) {
            Log.e(TAG, "PWM error", e);
        }
    }
    private void setHz(int hz) {
        getRegisterByHz(0);
        double prescaleval = 25000000.0;    // # 25MHz
        prescaleval /= 4096.0;       // # 12-bit
        prescaleval /= (float)hz;
        prescaleval -= 1.0;
        int prescale = (int)(Math.floor(prescaleval + 0.5));

        byte oldmode = 0;
        try {
            oldmode = mDevice.readRegByte(MODE1);
            byte newmode = (byte) (oldmode | SLEEP); // sleep
            mDevice.writeRegByte(MODE1,(byte)newmode);
            mDevice.writeRegByte(PRE_SCALE, (byte) prescale);
            mDevice.writeRegByte(MODE1,(byte)oldmode);
            if (BuildConfig.DEBUG) {
                Log.i(TAG, "oldmode:" + oldmode);
                Log.i(TAG, "newmode:" + newmode);
                Log.i(TAG, "prescale:" + prescale);
                Log.i(TAG, "oldmode:" + oldmode);
            }
            try {
                Thread.sleep((long) 50);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            mDevice.writeRegByte(MODE1, (byte) (oldmode | RESTART));
            Log.i(TAG, "restart:" + (oldmode | RESTART));
        } catch (IOException e) {
            Log.e(TAG, "set hz error", e);
        }

    }

    private void setAllPWM(int on, int off) {
        try {
            mDevice.writeRegByte(ALL_LED_ON_L, (byte) (on & 0xFF));
            mDevice.writeRegByte(ALL_LED_ON_H, (byte) (on >> 8));
            mDevice.writeRegByte(ALL_LED_OFF_L, (byte) (off & 0xFF));
            mDevice.writeRegByte(ALL_LED_OFF_H, (byte) (off >> 8));
        } catch (IOException e) {
            Log.e(TAG, "set All PWM error", e);

        }
    }

    private void setChannelValue(int channel, int on, int off) {
        try {
            mDevice.writeRegByte(LED0_ON_L+channel*4, (byte) (on & 0xFF));
            mDevice.writeRegByte(LED0_ON_H+channel*4, (byte) (on >> 8));

            mDevice.writeRegByte(LED0_OFF_L+channel*4, (byte) (off & 0xFF));
            mDevice.writeRegByte(LED0_OFF_H+channel*4, (byte) (off >> 8));
        } catch (IOException e) {
            Log.e(TAG, "Set channel value", e);
        }
    }
    //*********************
    // サーボモーター
    //*********************


}
