package org.deviceconnect.android.deviceplugin.robotarm;

import org.deviceconnect.android.deviceplugin.robotarm.arm.IRobtArm;
import org.deviceconnect.android.deviceplugin.robotarm.arm.RobotArm;
import org.deviceconnect.android.deviceplugin.robotarm.profiles.MyDeviceProfile;
import org.deviceconnect.android.message.DConnectMessageService;
import org.deviceconnect.android.profile.SystemProfile;
import org.deviceconnect.android.service.DConnectService;

import org.deviceconnect.android.deviceplugin.robotarm.profiles.MyRobotarmProfile;
import org.deviceconnect.android.deviceplugin.robotarm.profiles.MySystemProfile;
import org.deviceconnect.profile.ServiceDiscoveryProfileConstants.NetworkType;


public class MyMessageService extends DConnectMessageService {

    private static final String SERVICE_ID = "robot_arm_0";
    private IRobtArm mArm;
    @Override
    public void onCreate() {
        super.onCreate();
        // TODO 複数のarmを制御できるようにする必要がある
        mArm = new RobotArm();

        // 決め打ち
        DConnectService service = new DConnectService(SERVICE_ID);
        service.setName("RobotArm");
        service.setOnline(true);
        service.setNetworkType(NetworkType.UNKNOWN);
        service.addProfile(new MyRobotarmProfile());
        service.addProfile(new MyDeviceProfile());
        getServiceProvider().addService(service);

        // AndroidThingsなのでプラグイン認証用OAuthはOFF
        setUseLocalOAuth(false);
    }

    @Override
    public void onDestroy() {
        // Armの後始末
        if (mArm != null) {
            mArm.destroy();
        }
        super.onDestroy();
    }
    @Override
    protected SystemProfile getSystemProfile() {
        return new MySystemProfile();
    }

    @Override
    protected void onManagerUninstalled() {
        // TODO Device Connect Managerアンインストール時に実行したい処理. 実装は任意.
    }

    @Override
    protected void onManagerTerminated() {
        // TODO Device Connect Manager停止時に実行したい処理. 実装は任意.
    }

    @Override
    protected void onManagerEventTransmitDisconnected(final String origin) {
        // TODO アプリとのWebSocket接続が切断された時に実行したい処理. 実装は任意.
    }

    @Override
    protected void onDevicePluginReset() {
        // TODO Device Connect Managerの設定画面上で「プラグイン再起動」を要求された場合の処理. 実装は任意.
    }

    public IRobtArm getRobotArm() {
        return mArm;
    }

    public void setServiceOnline(String serviceId, boolean online) {
        DConnectService service = getServiceProvider().getService(serviceId);
        if (service != null) {
            service.setOnline(online);
        }
    }
}