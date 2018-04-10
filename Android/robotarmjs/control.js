
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
    alert('PUT robotarm/motor', errorCode, errorMessage);
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
    alert('PUT robotarm/motor', errorCode, errorMessage);
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
    alert('DELETE robotarm/motor', errorCode, errorMessage);
  });

}




function doHand(hz, value, duration) {
  var builder = new dConnect.URIBuilder();
  builder.setProfile('robotarm');
  builder.setAttribute('hand');
  builder.setServiceId(armId);
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
    alert('PUT robotarm/motor', errorCode, errorMessage);
  });

}


function doHandStop() {
  var builder = new dConnect.URIBuilder();
  builder.setHost(ip)
  builder.setProfile('robotarm');
  builder.setAttribute('hand');
  builder.setServiceId(armId);
  var uri = builder.build();

  if (DEBUG) {
    console.log('Uri:' + uri);
  }

  dConnect.delete(uri, null, null, function(json) {
    if (DEBUG) {
      console.log('Response: ', json);
    }
  }, function(errorCode, errorMessage) {
    alert('DELETE robotarm/motor', errorCode, errorMessage);
  });

}
