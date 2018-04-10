package org.deviceconnect.android.deviceplugin.robotarm.profiles;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import org.deviceconnect.android.deviceplugin.robotarm.MyMessageService;
import org.deviceconnect.android.deviceplugin.robotarm.arm.IRobtArm;
import org.deviceconnect.android.message.MessageUtils;
import org.deviceconnect.android.profile.DConnectProfile;
import org.deviceconnect.android.profile.api.PutApi;
import org.deviceconnect.android.profile.api.DeleteApi;
import org.deviceconnect.message.DConnectMessage;

public class MyRobotarmProfile extends DConnectProfile {

    public MyRobotarmProfile() {

        // PUT /gotapi/robotarm/motor
        addApi(new PutApi() {
            @Override
            public String getAttribute() {
                return "motor";
            }

            @Override
            public boolean onRequest(final Intent request, final Intent response) {
                Integer channel = parseInteger(request, "channel");
                Boolean direction = parseBoolean(request, "direction");
                Integer frequency = parseInteger(request, "frequency");
                Integer speed = parseInteger(request, "speed");
                Integer duration = parseInteger(request, "duration");
                IRobtArm arm = ((MyMessageService) getContext()).getRobotArm();
                if (arm == null) {
                    MessageUtils.setIllegalDeviceStateError(response);
                    return true;
                }
                arm.rotate(channel, direction, frequency, speed, duration);
                setResult(response, DConnectMessage.RESULT_OK);
                return true;
            }
        });

        // DELETE /gotapi/robotarm/motor
        addApi(new DeleteApi() {
            @Override
            public String getAttribute() {
                return "motor";
            }

            @Override
            public boolean onRequest(final Intent request, final Intent response) {
                Integer channel = parseInteger(request, "channel");

                IRobtArm arm = ((MyMessageService) getContext()).getRobotArm();
                if (arm == null) {
                    MessageUtils.setIllegalDeviceStateError(response);
                    return true;
                }
                arm.stopArmRotation(channel);
                setResult(response, DConnectMessage.RESULT_OK);
                return true;
            }
        });
        // PUT /gotapi/robotarm/hand
        addApi(new PutApi() {
            @Override
            public String getAttribute() {
                return "hand";
            }

            @Override
            public boolean onRequest(final Intent request, final Intent response) {
                Integer frequency = parseInteger(request, "frequency");
                Integer speed = parseInteger(request, "speed");
                Integer duration = parseInteger(request, "duration");
                IRobtArm arm = ((MyMessageService) getContext()).getRobotArm();
                if (arm == null) {
                    MessageUtils.setIllegalDeviceStateError(response);
                    return true;
                }
                Log.d("ABC", frequency + ":" + speed +  ":" + duration);
                arm.grabHand(frequency, speed, duration);
                setResult(response, DConnectMessage.RESULT_OK);
                return true;
            }
        });

        // DELETE /gotapi/robotarm/hand
        addApi(new DeleteApi() {
            @Override
            public String getAttribute() {
                return "hand";
            }

            @Override
            public boolean onRequest(final Intent request, final Intent response) {
                String serviceId = (String) request.getExtras().get("serviceId");

                IRobtArm arm = ((MyMessageService) getContext()).getRobotArm();
                if (arm == null) {
                    MessageUtils.setIllegalDeviceStateError(response);
                    return true;
                }
//                arm.grabHand(120, 25, false);
                setResult(response, DConnectMessage.RESULT_OK);
                return true;
            }
        });
    }

    @Override
    public String getProfileName() {
        return "robotarm";
    }
}