from fhwise import FhwisePlayer
import time
import logging  # 引入logging模块
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做

player = FhwisePlayer('192.168.1.173')
player.connect()

while True:
    ret = player.send_heartbeat()
    print('Send heart beat. model %s' % (ret))
    time.sleep(1)
    ret = player.send_play_pause()
    print('Send play/pause')
    time.sleep(1)
    ret = player.get_play_status()
    print('get play status %s' %(ret))
    time.sleep(1)
    ret = player.send_play_pause()
    print('Send play/pause')
    time.sleep(1)
    ret = player.get_play_status()
    print('get play status %s' %(ret))
    time.sleep(1)
    ret = player.set_toggle_play_mode()
    print('toggle play mode')
    time.sleep(1)
    ret = player.get_play_mode()
    print('get play mode %s' %(ret))
    time.sleep(1)
    ret = player.set_toggle_play_mode()
    print('toggle play mode')
    time.sleep(1)
    ret = player.get_play_mode()
    print('get play mode %s' %(ret))
    time.sleep(1)
    ret = player.send_previous_song()
    print('send previoud song')
    time.sleep(1)
    ret = player.get_current_file_name()
    print('current file name %s' % (ret))
    time.sleep(1)
    ret = player.get_current_file_length()
    print('current file length %s' % (ret))
    time.sleep(1)
    ret = player.get_current_file_position()
    print('current file pos %s' % (ret))
    time.sleep(1)
    ret = player.send_next_song()
    print('send next song')
    time.sleep(1)
    ret = player.get_current_file_name()
    print('current file name %s' % (ret))
    time.sleep(1)
    ret = player.get_current_room_info()
    print('current room info %s' % (ret))
    time.sleep(1)
    ret = player.set_current_file_position(1000)
    print('set file pos to 1000')
    time.sleep(1)
    ret = player.get_current_file_position()
    print('current file pos %s' % (ret))
    time.sleep(1)
    ret = player.get_current_list_file_account()
    print('current list count number %s' % (ret))
    time.sleep(1)
    ret = player.get_current_list_file_info(1)
    print('current list file 1 info %s' % (ret))
    time.sleep(1)
    ret = player.set_current_list_play_file(2)
    print('set play file to 2')
    time.sleep(1)
    ret = player.get_current_list_file_info(2)
    print('current list file 2 info %s' % (ret))
    time.sleep(1)
    ret = player.get_current_file_artist()
    print('current artist %s' % (ret))
    time.sleep(1)
    ret = player.set_volume_level(1)
    print('set volume to 1')
    time.sleep(1)
    ret = player.get_volume_level()
    print('get volume %s' % (ret))
    time.sleep(1)
    ret = player.set_volume_up()
    print('set volume up')
    time.sleep(1)
    ret = player.get_volume_level()
    print('get volume %s' % (ret))
    time.sleep(1)
    ret = player.set_volume_down()
    print('set volume down')
    time.sleep(1)
    ret = player.get_volume_level()
    print('get volume %s' % (ret))
    time.sleep(1)
    ret = player.set_volume_toggle_mute()
    print('toggle mute')
    time.sleep(1)
    ret = player.get_volume_level()
    print('get volume %s' % (ret))
    time.sleep(1)
    ret = player.set_volume_toggle_mute()
    print('toggle mute')
    time.sleep(1)
    ret = player.get_volume_level()
    print('get volume %s' % (ret))
    time.sleep(1)
    ret = player.set_room_number('2')
    print('get room number to %s' % ('2'))
    time.sleep(1)
    ret = player.set_room_name('测试')
    print('get room name to %s' % ('测试'))
    time.sleep(1)
    ret = player.get_current_room_info()
    print('current room info %s' % (ret))
    time.sleep(1)
    ret = player.get_volume_source()
    print('current volume source %s' % (ret))
    time.sleep(1)
    ret = player.set_volume_source(3)
    print('set volume source 3')
    time.sleep(1)
    ret = player.get_volume_source()
    print('current volume source %s' % (ret))
    time.sleep(1)
    ret = player.set_sub_area_control(1,10,False)
    print('get current area control %s' % (ret))
    time.sleep(1)
    ret = player.get_sub_area_control(1)
    print('get area 1 control %s' % (ret))
    time.sleep(1)
    ret = player.set_eq_switch(False)
    print('Set eq off' % (ret))
    time.sleep(1)
    ret = player.get_eq_switch()
    print('Current eq status is %s' % (ret))
    time.sleep(1)
    ret = player.set_eq_switch(True)
    print('Set eq on' % (ret))
    time.sleep(1)
    ret = player.get_eq_switch()
    print('Current eq status is %s' % (ret))
    time.sleep(1)
    ret = player.set_eq_type(6)
    print('set eq type to 6')
    time.sleep(1)
    ret = player.get_eq_type()
    print('current eq type %s' % (ret))
    time.sleep(1)