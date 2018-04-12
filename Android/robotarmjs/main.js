var rightInterval;
var leftInterval;
var strength = 300;
/** 共通 **/
function stopAllArmMove() {
  doArmStop(0);
  doArmStop(1);
  doArmStop(2);
  doArmStop(3);
  doArmStop(4);
}
function handleGrabEvent (event) {
    if (strength < 400) {
      strength += 10;
      doHand(10,strength);
    }
}
function handleReleaseEvent (event) {
  if (strength > 200) {
    strength -= 10;
    doHand(10,strength);
  }
}
function initGrabEvent (event) {
  doHand(10, 300);
}
function moveArmForLeftController(type) {
  if (type === "dir:up") {
    doArmForward(3,50,100, 60000);
  } else if (type === "dir:down") {
    doArmReverse(3,50,100,60000);
  } else if (type === "dir:left") {
    doArmForward(4,50,100,60000);
  } else if (type === "dir:right") {
    doArmReverse(4,50,100,60000);
  }
}
function moveArmForRightController(type) {
  if (type === "dir:up") {
    doArmForward(2,50,100,60000);
  } else if (type === "dir:down") {
    doArmReverse(2,50,100,60000);
  } else if (type === "dir:left") {
    doArmForward(0,50,100,60000);
  } else if (type === "dir:right") {
    doArmReverse(0,50,100,60000);
  }
}
/** タッチパッド **/
// const left = nipplejs.create({
//       zone: document.getElementById('left_joystick'),
//       mode: 'static',
//       position: {left: '30%', top: '40%'},
//       color: 'black'
// });
// left.on('start', function (evt, data) {
//       console.log("left:" + evt.type);
// }).on('dir:up dir:left dir:down dir:right',
//       function (evt, data) {
//           if (leftInterval !== null) {
//             clearInterval(leftInterval);
//           }
//           moveArmForLeftController(evt.type);
//           leftInterval = setInterval(function(){
//             console.log("left:" + evt.type);
//             moveArmForLeftController(evt.type);
//           }, 10000);
// }).on('end', function (evt, data) {
//       console.log("left:" + evt.type);
//       clearInterval(leftInterval);
//       stopAllArmMove();
// });
//
// const right = nipplejs.create({
//       zone: document.getElementById('right_joystick'),
//       mode: 'static',
//       position: {left: '70%', top: '40%'},
//       color: 'black'
// });
// right.on('start', function (evt, data) {
//       console.log("right:" + evt.type);
// }).on('dir:up dir:left dir:down dir:right',
//       function (evt, data) {
//         if (rightInterval !== null) {
//           clearInterval(rightInterval);
//         }
//         moveArmForRightController(evt.type);
//         rightInterval = setInterval(function(){
//           console.log("right:" + evt.type);
//           moveArmForRightController(evt.type);
//         }, 10000);
//      }
// ).on('end', function (evt, data) {
//       console.log("right:" + evt.type);
//       clearInterval(rightInterval);
//       stopAllArmMove();
// });


/** ゲームパッド **/
const gamepad = new Gamepad();

// oボタン:掴む
gamepad.on('press', 'button_2', e => {
    console.log(`${e.button} was pressed!`);
    handleGrabEvent();
});
// xボタン:離す
gamepad.on('press', 'button_1', e => {
    console.log(`${e.button} was hold!`);
    handleReleaseEvent();
});
// □ボタン:初期値
gamepad.on('press', 'button_3', e => {
    console.log(`${e.button} was hold!`);
    initGrabEvent();
});

gamepad.on('press', 'stick_axis_left', e => {
    console.log(`${e.value[0]} : ${e.value[1]}`)
    if (e.value[0] <= -0.3 && (e.value[1] >= -0.3 && e.value[1] <= 0.3)) {
      console.log("左");
      moveArmForLeftController("dir:left");
    } else if ((e.value[0] >= -0.3 && e.value[0] <= 0.3) && e.value[1] <= 0) {
      console.log("上");
      moveArmForLeftController("dir:up");
    } else if (e.value[0] >= 0 && (e.value[1] >= -0.3 && e.value[1] <= 0.3)) {
      console.log("右");
      moveArmForLeftController("dir:right");
    } else if ((e.value[0] >= -0.3 && e.value[0] <= 0.3) && e.value[1] >= 0) {
      console.log("下");
      moveArmForLeftController("dir:down");
    }

});

gamepad.on('release', 'stick_axis_left', e => {
  stopAllArmMove();
});

gamepad.on('press', 'stick_axis_right', e => {
  console.log(`${e.value[0]} : ${e.value[1]}`)
  if (e.value[0] <= -0.3 && (e.value[1] >= -0.3 && e.value[1] <= 0.3)) {
    console.log("左");
    moveArmForRightController("dir:left");
  } else if ((e.value[0] >= -0.3 && e.value[0] <= 0.3) && e.value[1] <= 0) {
    console.log("上");
    moveArmForRightController("dir:up");
  } else if (e.value[0] >= 0 && (e.value[1] >= -0.3 && e.value[1] <= 0.3)) {
    console.log("右");
    moveArmForRightController("dir:right");
  } else if ((e.value[0] >= -0.3 && e.value[0] <= 0.3) && e.value[1] >= 0) {
    console.log("下");
    moveArmForRightController("dir:down");
  }
});
gamepad.on('release', 'stick_axis_right', e => {
  stopAllArmMove();
});

gamepad.on('press', 'd_pad_left', e => {
  console.log(`${e.button}`)
  doArmForward(1,50,100,500);
});

gamepad.on('release', 'd_pad_left', e => {
  console.log(`${e.button}`)
  stopAllArmMove();
});
gamepad.on('press', 'd_pad_right', e => {
  console.log(`${e.button}`)
  doArmReverse(1,50,100,500);
});
gamepad.on('press', 'd_pad_right', e => {
  console.log(`${e.button}`)
  stopAllArmMove();
});
