import sys
import time
import smbus2
sys.modules['smbus'] = smbus2
from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True) # init lcd

# 顯示inStr1在lcd第一列、inStr2在lcd第二列
# cursor 0=hide 1=line 2=blink
def lcd_print(inStr1 : str, inStr2 = "", clear = True, cursor = 0):
    if cursor:
        lcd.cursor_mode = 'line'
    else:
        lcd.cursor_mode = 'hide'
        
    if clear:
        lcd.clear()
    if (len(inStr1) != 0):
        lcd.cursor_pos = (0, 0)
        lcd.write_string(inStr1)
        if (len(inStr2) != 0):
            lcd.cursor_pos = (1, 0)
            lcd.write_string(inStr2)
    time.sleep(0.1)

def lcd_clear(cursor = 1):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    if cursor:
        lcd.cursor_mode = 'line'
    else:
        lcd.cursor_mode = 'hide'