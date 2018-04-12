
function doArmForward(arm, hz, value, duration) {
  var builder = new dConnect.URIBuilder();
  builder.setProfile('robotarm');
  builder.setAttribute('motor');
  builder.setServiceId(armId);
  builder.addParameter('channel', arm);
  builder.addParameter('direction', true);
  builder.addParameter('frequency', hz);
  builder.addParameter('speed', value);
  builder.addParameter('duration', duration);
  builder.setHost(ip)
  var uri = builder.build();

  if (DEBUG) {
    console.log('Uri:' + uri);
  }

  dConnect.put(uri, null, null, function(json) {
    if (DEBUG) {
      console.log('Response: ', json);
    }
  }, function(errorCode, errorMessage) {
    console.log('PUT robotarm/motor'+errorCode+errorMessage);
  });

}


function doArmReverse(arm, hz, value, duration) {
  var builder = new dConnect.URIBuilder();
  builder.setHost(ip)
  builder.setProfile('robotarm');
  builder.setAttribute('motor');
  builder.setServiceId(armId);
  builder.addParameter('channel', arm);
  builder.addParameter('direction', false);
  builder.addParameter('frequency', hz);
  builder.addParameter('speed', value);
  builder.addParameter('duration', duration);
  var uri = builder.build();

  if (DEBUG) {
    console.log('Uri:' + uri);
  }

  dConnect.put(uri, null, null, function(json) {
    if (DEBUG) {
      console.log('Response: ', json);
    }
  }, function(errorCode, errorMessage) {
    console.log('PUT robotarm/motor'+errorCode+errorMessage);
  });

}

function doArmStop(arm) {
  var builder = new dConnect.URIBuilder();
  builder.setHost(ip)
  builder.setProfile('robotarm');
  builder.setAttribute('motor');
  builder.setServiceId(armId);
  builder.addParameter('channel', arm);
  var uri = builder.build();

  if (DEBUG) {
    console.log('Uri:' + uri);
  }

  dConnect.delete(uri, null, null, function(json) {
    if (DEBUG) {
      console.log('Response: ', json);
    }
  }, function(errorCode, errorMessage) {
    console.log('DELETE robotarm/motor'+errorCode+":"+errorMessage);
  });

}

function doHand(hz, value) {
  var builder = new dConnect.URIBuilder();
  builder.setProfile('robotarm');
  builder.setAttribute('hand');
  builder.setServiceId(armId);
  builder.addParameter('frequency', hz);
  builder.addParameter('speed', value);
  builder.setHost(ip)
  var uri = builder.build();

  if (DEBUG) {
    console.log('Uri:' + uri);
  }

  dConnect.put(uri, null, null, function(json) {
    if (DEBUG) {
      console.log('Response: ', json);
    }
  }, function(errorCode, errorMessage) {
    console.log('PUT robotarm/hand'+errorCode +":" +errorMessage);
  });

}


function preview_start() {
    var imageElement = document.getElementById("image");
    var uri = "http://" + ip + ":" + port + "/gotapi/mediastreamRecording/preview?serviceId=" + uvcId;

    var header = null;
    var data = null;
    dConnect.put(uri, header, data, function(json) {
        if (json.result == 0) {
            var uri = json.uri;
            console.log(uri);
            uri = uri.replace(/localhost/g,ip);
            imageElement.src = uri;
            console.log(uri);
        } else {
            console.log(json.result);
        }
    }, function(errorCode, errorMessage) {
        console.log(errorMessage);
    });
}

function preview_stop() {
    var imageElement = document.getElementById("image");
    var uri = "http://" + ip + ":" + port + "/gotapi/mediastreamRecording/preview?serviceId=" + uvcId;

    var header = null;
    var data = null;
    dConnect.delete(uri, header, data, function(json) {
        console.log(json.result);
    }, function(errorCode, errorMessage) {
        console.log(errorMessage);
    });
}
