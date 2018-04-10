package org.deviceconnect.android.deviceplugin.robotarm.profiles;

import android.content.Intent;

import org.deviceconnect.android.deviceplugin.robotarm.MyMessageService;
import org.deviceconnect.android.deviceplugin.robotarm.arm.IRobtArm;
import org.deviceconnect.android.message.MessageUtils;
import org.deviceconnect.android.profile.DConnectProfile;
import org.deviceconnect.android.profile.api.DeleteApi;
import org.deviceconnect.android.profile.api.PostApi;
import org.deviceconnect.message.DConnectMessage;

public class MyDeviceProfile extends DConnectProfile {

    public MyDeviceProfile() {
        addApi(new PostApi() {
            @Override
            public String getAttribute() {
                return "pairing";
            }
            @Override
            public boolean onRequest(Intent request, Intent response) {
                IRobtArm arm = ((MyMessageService) getContext()).getRobotArm();
                if (arm == null) {
                    MessageUtils.setIllegalDeviceStateError(response);
                    return true;
                }
                if (!arm.isRobotArm()) {
                    arm.init();
                    String serviceId = getServiceID(request);
                    ((MyMessageService) getContext()).setServiceOnline(serviceId, true);
                }
                setResult(response, DConnectMessage.RESULT_OK);
                return true;
            }
        });
        addApi(new DeleteApi() {
            @Override
            public String getAttribute() {
                return "pairing";
            }
            @Override
            public boolean onRequest(Intent request, Intent response) {
                IRobtArm arm = ((MyMessageService) getContext()).getRobotArm();
                if (arm == null) {
                    MessageUtils.setIllegalDeviceStateError(response);
                    return true;
                }
                if (arm.isRobotArm()) {
                    arm.destroy();
                    String serviceId = getServiceID(request);
                    ((MyMessageService) getContext()).setServiceOnline(serviceId, false);
                }
                setResult(response, DConnectMessage.RESULT_OK);
                return true;
            }
        });
    }
    @Override
    public String getProfileName() {
        return "device";
    }
}
