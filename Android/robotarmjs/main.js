var rightInterval;
var leftInterval;
var handGrabInterval;
var handReleaseInterva;
function stopAllArmMove() {
  doArmStop(0);
  doArmStop(1);
  doArmStop(2);
  doArmStop(3);
  doArmStop(4);
}
function handleGrabEvent (event) {
    if (handReleaseInterval !== null) {
      clearInterval(handReleaseInterval);
    }
    if (handGrabInterval !== null) {
      clearInterval(handGrabInterval);
    }
   handGrabInterval = setInterval(function(){
     console.log("Grab");
     // TODO 方向に合わせたリクエストを送り続ける
   }, 3000);
}
function handleReleaseEvent (event) {
    if (handReleaseInterval !== null) {
      clearInterval(handReleaseInterval);
    }
    if (handGrabInterval !== null) {
      clearInterval(handGrabInterval);
    }
    handReleaseInterval = setInterval(function(){
      console.log("Release");
      // TODO 方向に合わせたリクエストを送り続ける
    }, 3000);
}
function handleStopEvent (event) {
     console.log("Stop");
     if (handReleaseInterval !== null) {
       clearInterval(handReleaseInterval);
     }
     if (handGrabInterval !== null) {
       clearInterval(handGrabInterval);
     }
}

document.getElementById("grab").addEventListener("mousedown", handleGrabEvent, false);
document.getElementById("release").addEventListener("mousedown", handleReleaseEvent, false);
document.getElementById("stop").addEventListener("mousedown", handleStopEvent, false);

var left = nipplejs.create({
      zone: document.getElementById('left_joystick'),
      mode: 'static',
      position: {left: '30%', top: '30%'},
      color: 'black'
});
left.on('start', function (evt, data) {
      console.log("left:" + evt.type);
}).on('dir:up dir:left dir:down dir:right',
      function (evt, data) {
          if (leftInterval !== null) {
            clearInterval(leftInterval);
          }
          leftInterval = setInterval(function(){
            console.log("left:" + evt.type);
            if (evt.type === "dir:up") {
              doArmForward(4,10,100,1000);
            } else if (evt.type === "dir:down") {
              doArmReverse(4,10,100,1000);
            } else if (evt.type === "dir:left") {
              doArmForward(4,10,100,1000);
            } else if (evt.type === "dir:right") {
              doArmReverse(4,10,100,1000);
            }
          }, 3000);
}).on('end', function (evt, data) {
      console.log("left:" + evt.type);
      clearInterval(leftInterval);
      stopAllArmMove();
});

var right = nipplejs.create({
      zone: document.getElementById('right_joystick'),
      mode: 'static',
      position: {left: '70%', top: '30%'},
      color: 'black'
});
right.on('start', function (evt, data) {
      console.log("right:" + evt.type);
}).on('dir:up dir:left dir:down dir:right',
      function (evt, data) {
        if (rightInterval !== null) {
          clearInterval(rightInterval);
        }
        rightInterval = setInterval(function(){
          console.log("right:" + evt.type);
          if (evt.type === "dir:up") {
            doArmForward(1,5,100,1000);
          } else if (evt.type === "dir:down") {
            doArmReverse(1,5,100,1000);
          } else if (evt.type === "dir:left") {
            doArmForward(0,5,100,1000);
          } else if (evt.type === "dir:right") {
            doArmReverse(0,5,100,1000);
          }
        }, 3000);
     }
).on('end', function (evt, data) {
      console.log("right:" + evt.type);
      clearInterval(rightInterval);
      stopAllArmMove();
});
