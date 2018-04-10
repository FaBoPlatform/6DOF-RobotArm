package org.deviceconnect.android.deviceplugin.robotarm;

import android.app.Service;

import org.deviceconnect.android.message.DConnectMessageServiceProvider;

public class MyMessageServiceProvider<T extends Service> extends DConnectMessageServiceProvider<Service> {
    @SuppressWarnings("unchecked")
    @Override
    protected Class<Service> getServiceClass() {
        Class<? extends Service> clazz = (Class<? extends Service>) MyMessageService.class;
        return (Class<Service>) clazz;
    }
}