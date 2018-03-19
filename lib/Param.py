FORWARD = 1
BACKWARD = 0

Waiting = 0
Running = 1

'''
initilize value
'''
INI_ABS_POS    = 0          
INI_EL_POS     = 0    
INI_MARK       = 0    
INI_SPEED      = 0    
INI_ACC        = 10000  
INI_DEC        = 10000
INI_MAX_SPEED  = 400
INI_MIN_SPEED  = 0    
INI_KVAL_HOLD  = 0xFF    
INI_KVAL_RUN   = 0xFF    
INI_KVAL_ACC   = 0xFF   
INI_KVAL_DEC   = 0x40   
INI_INT_SPD    = 246
INI_ST_SLP     = 0x19    
INI_FN_SLP_ACC = 0x29    
INI_FN_SLP_DEC = 0x29    
INI_K_THERA    = 0x0    
INI_OCD_TH     = 0xF      
INI_STALL_TH   = 0x7F
INI_FS_SPD     = 1000
INI_STEP_MODE  = 0x7
INI_ARARM_FN   = 0xFF
INI_CONFIG     = 0x2E88    

'''
address of register
'''
REG_NO = 0x0
REG_ABS_POS = 0x01
REG_EL_POS = 0x02
REG_MARK = 0x03
REG_SPEED = 0x04
REG_ACC = 0x05
REG_DEC = 0x06
REG_MAX_SPEED = 0x07
REG_MIN_SPEED = 0x08
REG_KVAL_HOLD = 0x9
REG_KVAL_RUN = 0x0A
REG_KVAL_ACC = 0x0B
REG_KVAL_DEC = 0x0C
REG_INT_SPEED = 0x0D
REG_ST_SLP = 0x0E
REG_FN_SLP_ACC = 0x0F
REG_FN_SLP_DEC = 0x10
REG_K_THERM = 0x11
REG_ADC_OUT = 0x12
REG_OCD_TH = 0x13
REG_STALL_TH = 0x14
REG_FS_SPD = 0x15
REG_STEP_MODE = 0x16
REG_ALARM_EN = 0x17
REG_CONFIG = 0x18
REG_STATUS = 0x19

'''
length of register
'''
LEN_ABS_POS = 22       
LEN_EL_POS = 9
LEN_MARK = 22
LEN_SPEED = 20
LEN_ACC = 12
LEN_DEC = 12
LEN_MAX_SPEED = 10
LEN_MIN_SPEED = 13
LEN_KVAL_HOLD = 8
LEN_KVAL_RUN = 8
LEN_KVAL_ACC = 8
LEN_KVAL_DEC = 8
LEN_INT_SPD = 14
LEN_ST_SLP = 8
LEN_FN_SLP_ACC = 8
LEN_FN_SLP_DEC = 8 
LEN_K_THERA = 4
LEN_ADC_OUT = 5
LEN_OCR_TH = 4
LEN_STALL_TH = 7
LEN_FS_SPD = 10
LEN_STEP_MODE = 8
LEN_ARARM_FN = 8
LEN_CONFIG  = 16
LEN_STATUS = 16

'''
command value
'''
CMD_NOP = 0x00
CMD_SETPARAM = 0x00
CMD_GETPARAM = 0x20
CMD_RUN_PLUS = 0x51
CMD_RUN_MINUS = 0x50
CMD_STEPCLOCK_PLUS = 0x59
CMD_STEPCLOCK_MINUS = 0x58
CMD_MOVE_PLUS = 0x41
CMD_MOVE_MINUS = 0x40
CMD_GOTO = 0x60
CMD_GOTO_DIR_PLUS = 0x69
CMD_GOTO_DIR_MINUS = 0x68
CMD_GOUNTIL_PLUS = 0x83
CMD_GOUNTIL_MINUS = 0x82
CMD_RELEASESW_PLUS = 0x93
CMD_RELEASESW_MINUS = 0x92
CMD_GOHOME = 0x70
CMD_GOMARK = 0x78
CMD_RESETPOS = 0xD8
CMD_RESETDEVICE = 0xC0
CMD_SOFTSTOP = 0xB0
CMD_HARDSTOP = 0xB8
CMD_SOFTHIZ = 0xA0
CMD_HARDHIZ = 0xA8
CMD_GETSTATUS = 0xD0
