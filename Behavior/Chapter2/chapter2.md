# Robot Arm制御2 <動作制御編>

## 動作環境
マイコン
* Raspberry Pi 3(RASPBIAN STRETCH)
* Raspberry pi 3 shield #605

RTミドルウェア
* OpenRTM-aist

使用言語
* python 3.6

IDE
* Eclipse

環境設定などは以下のURL参照
http://docs.fabo.io/openrtm/

## RTCコンポーネント作成
#### PS4コントローラコンポーネント
PS4コントローラーからRobotArmの制御を行う
PS4コントローラーのRTコンポーネントは以下のURL参照
http://docs.fabo.io/openrtm/robotcontroller.html

#### ロボットアームコンポーネント

###### 操作概要
x ボタン : 土台部分回転モーター指定
o ボタン : 第一軸回転モーター指定
□ ボタン : 第二軸回転モーター指定
△ ボタン : 手首軸モーター指定
R1 ボタン :　指先モーター指定
L1 ボタン : 第三軸回転モーター指定
左joy stick : 縦、横回転動作制御


###### プログラム
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

# Import Arm module
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import math

MT0 = 0
MT1 = 1
MT2 = 2
MT3 = 3
MT4 = 4
MT5 = 5
MTNO  = 99

MTs = [0,1,2,3,4,5,99]

GIAs = [90,90,90,90]

arm_spec = ["implementation_id", "Arm",
		 "type_name",         "Arm",
		 "description",       "ModuleDescription",
		 "version",           "1.0.0",
		 "vendor",            "GClue, Inc.",
		 "category",          "Category",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 ""]

#Arm class
class Arm(OpenRTM_aist.DataFlowComponentBase):

  #each stepper opt freq
	freq = [2000,800,4000,1000,500,60]

	#CW/CCW GPIO number
	cw = [4,5,21,6,12]
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		#Joystick
		self._d_Analog = RTC.TimedDoubleSeq(RTC.Time(0,0),0)
		self._AnalogIn = OpenRTM_aist.InPort("Analog", self._d_Analog)

		#Button
		self._d_Button = RTC.TimedLongSeq(RTC.Time(0,0),0)
		self._ButtonIn = OpenRTM_aist.InPort("Button", self._d_Button)

		# GPIO setup
		GPIO.setmode( GPIO.BCM )

		#initialize arm
		self.mt = MTNO
		self.open = 300
		self.pwm = Adafruit_PCA9685.PCA9685()
		for i in self.cw: GPIO.setup(i,GPIO.OUT)

		#variable controller
		self.joys_button = MTNO
		self.joys_x = 0
		self.joys_y = 0s

	#Once startup this component
	def onInitialize(self):

		# Set InPort buffers
		self.addInPort("Analog",self._AnalogIn)
		self.addInPort("Button",self._ButtonIn)

		return RTC.RTC_OK

	#Once finish this component
	def onFinalize(self):
		GPIO.cleanup()
		return RTC.RTC_OK

	#Getting start component
	def onActivated(self, ec_id):
		print "Activate"
		return RTC.RTC_OK

	#Getting end component
	def onDeactivated(self, ec_id):
		print "Deactivate"
		return RTC.RTC_OK

	#loop while executing
	def onExecute(self, ec_id):

		#Get Analog Data
		if self._AnalogIn.isNew():
			analog_data = self._AnalogIn.read()
			self.joys_x = int(round(analog_data.data[3],0))
			self.joys_y = int(round(analog_data.data[2],0))

		#Get Button Data
		if self._ButtonIn.isNew():
			button_data = self._ButtonIn.read()
			if button_data.data[0] == 1: self.joys_button = MTs[2]
			if button_data.data[1] == 1: self.joys_button = MTs[0]
			if button_data.data[2] == 1: self.joys_button = MTs[1]
			if button_data.data[3] == 1: self.joys_button = MTs[3]
			if button_data.data[4] == 1: self.joys_button = MTs[4]
			if button_data.data[5] == 1: self.joys_button = MTs[5]

		#Print data
		print "self.joys_x = {}".format(self.joys_x)
		print "self.joys_y = {}".format(self.joys_y)
		print "self.joys_button = {}".format(self.joys_button)

		self.ctrl_mt()

		return RTC.RTC_OK

	#Select motor
	def ctrl_mt(self):
		if self.joys_button == MTs[0]:	self.ctrl_stepper(self.joys_x)
		elif self.joys_button == MTs[1]: self.ctrl_stepper(-1 * self.joys_y)
		elif self.joys_button == NTs[2]: self.ctrl_stepper(self.joys_y)
		elif self.joys_button == MTs[3]: self.ctrl_stepper(-1 * self.joys_x)
		elif self.joys_button == MTs[4]: self.ctrl_stepper(self.joys_y)
		elif self.joys_button == MTs[5]: self.ctrl_servo(self.joys_y)

	#Control Stepping motor
	def ctrl_stepper(self,data):
		if data == 0:
			self.pwm.set_pwm(self.joys_button,0,0)
			if self.mt != MTNO : self.pwm.set_pwm(self.mt,0,0)
			self.mt = MTNO
		else :
			print("else")
			GPIO.output(self.cw[self.joys_button],1 & (data < 0))
			if self.mt != self.joys_button:
				print("create")
				self.mt = self.joys_button
				self.pwm.set_pwm_freq(self.freq[self.mt])
				self.pwm.set_pwm(self.mt,0,50)

	#Control Servo motor
	def ctrl_servo(self,data):
		if data == 0:
			return
		else :
			if (self.mt != MTs[5]):
				self.mt = MTs[5]
				self.pwm.set_pwm_freq(60)
			self.open = self.open + 50 * (-1 + 2 * (data > 0))
			if self.open > 600:self.open = 600
			if self.open < 300:self.open = 300
			self.pwm.set_pwm(MTs[5],0,self.open)
			time.sleep(1/60)
		return

	#error
	def onError(self, ec_id):
		print "Error"
		return RTC.RTC_OK


def ArmInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=arm_spec)
    manager.registerFactory(profile,
                            Arm,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ArmInit(manager)

    # Create a component
    comp = manager.createComponent("Arm")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

```
