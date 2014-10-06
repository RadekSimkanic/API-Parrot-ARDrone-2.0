#! /usr/bin/env python
# coding:utf-8


class Config:
	"""
	ARDrone_Developer_Guide 2.0 page 63-65
	"""
	# GENERAL
	GENERAL_NAVDATA_DEMO	= "general:navdata_demo"
	GENERAL_NUM_VERSION_CONFIG = "general:num_version_config"
	GENERAL_NUM_VERSION_MB	= "general:num_version_mb"
	GENERAL_NUM_VERSION_SOFT	= "general:num_version_soft"
	GENERAL_DRONE_SERIAL	= "general:drone_serial"
	GENERAL_SOFT_BUILD_DATE	= "general:soft_build_date"
	GENERAL_MOTOR1_SOFT	= "general:motor1_soft"
	GENERAL_MOTOR1_HARD	= "general:motor1_hard"
	GENERAL_MOTOR1_SUPPLIER	= "general:motor1_supplier"
	GENERAL_MOTOR2_SOFT	= "general:motor2_soft"
	GENERAL_MOTOR2_HARD	= "general:motor2_hard"
	GENERAL_MOTOR2_SUPPLIER	= "general:motor2_supplier"
	GENERAL_MOTOR3_SOFT	= "general:motor3_soft"
	GENERAL_MOTOR3_HARD	= "general:motor3_hard"
	GENERAL_MOTOR3_SUPPLIER	= "general:motor3_supplier"
	GENERAL_MOTOR4_SOFT	= "general:motor4_soft"
	GENERAL_MOTOR4_HARD	= "general:motor4_hard"
	GENERAL_MOTOR4_SUPPLIER	= "general:motor4_supplier"
	GENERAL_ARDRONE_NAME	= "general:ardrone_name"
	GENERAL_FLYING_TIME	= "general:flying_time"
	GENERAL_NAVDATA_OPTIONS	= "general:navdata_options"
	GENERAL_COM_WATCHDOG	= "general:com_watchdog"
	GENERAL_VIDEO_ENABLE	= "general:video_enable"
	GENERAL_VISION_ENABLE	= "general:vision_enable"
	GENERAL_VBAT_MIN	= "general:vbat_min"

	
	# CONTROL
	CONTROL_ACCS_OFFSET	= "control:accs_offset"
	CONTROL_ACCS_GAINS	= "control:accs_gains"
	CONTROL_GYROS_OFFSET	= "control:gyros_offset"
	CONTROL_GYROS_GAINS	= "control:gyros_gains"
	CONTROL_GYROS110_OFFSET	= "control:gyros110_offset"
	CONTROL_GYROS110_GAINS	= "control:gyros110_gains"
	CONTROL_MAGNETO_OFFSET	= "control:magneto_offset"
	CONTROL_MAGNETO_RADIUS	= "control:magneto_radius"
	CONTROL_GYRO_OFFSET_THR_X	= "control:gyro_offset_thr_x"
	CONTROL_GYRO_OFFSET_THR_Y	= "control:gyro_offset_thr_y"
	CONTROL_GYRO_OFFSET_THR_Z	= "control:gyro_offset_thr_z"
	CONTROL_PWM_REF_GYROS	= "control:pwm_ref_gyros"
	CONTROL_OSCTUN_VALUE	= "control:osctun_value"
	CONTROL_OSCTUN_TEST	= "control:osctun_test"
	CONTROL_ALTITUDE_MAX	= "control:altitude_max"
	CONTROL_ALTITUDE_MIN	= "control:altitude_min"
	CONTROL_CONTROL_LEVEL	= "control:control_level"
	CONTROL_EULER_ANGLE_MAX	= "control:euler_angle_max"
	CONTROL_CONTROL_IPHONE_TILT	= "control:control_iphone_tilt"
	CONTROL_CONTROL_VZ_MAX	= "control:control_vz_max"
	CONTROL_CONTROL_YAW	= "control:control_yaw"
	CONTROL_OUTDOOR	= "control:outdoor"
	CONTROL_FLIGHT_WITHOUT_SHELL	= "control:flight_without_shell"
	CONTROL_AUTONOMOUS_FLIGHT	= "control:autonomous_flight"
	CONTROL_MANUAL_TRIM	= "control:manual_trim"
	CONTROL_INDOOR_EULER_ANGLE_MAX	= "control:indoor_euler_angle_max"
	CONTROL_INDOOR_CONTROL_VZ_MAX	= "control:indoor_control_vz_max"
	CONTROL_INDOOR_CONTROL_YAW	= "control:indoor_control_yaw"
	CONTROL_OUTDOOR_EULER_ANGLE_MAX	= "control:outdoor_euler_angle_max"
	CONTROL_OUTDOOR_CONTROL_VZ_MAX	= "control:outdoor_control_vz_max"
	CONTROL_OUTDOOR_CONTROL_YAW	= "control:outdoor_control_yaw"
	CONTROL_FLYING_MODE	= "control:flying_mode"
	CONTROL_HOVERING_RANGE	= "control:hovering_range"
	CONTROL_FLIGHT_ANIM	= "control:flight_anim"

	
	# NETWORK
	NETWORK_SSID_SINGLE_PLAYER	= "network:ssid_single_player"
	NETWORK_SSID_MULTI_PLAYER	= "network:ssid_multi_player"
	NETWORK_WIFI_MODE	= "network:wifi_mode"
	NETWORK_WIFI_RATE	= "network:wifi_rate"
	NETWORK_OWNER_MAC	= "network:owner_mac"
	
	
	# PIC
	PIC_ULTRASOUND_FREQ	= "pic:ultrasound_freq"
	PIC_ULTRASOUND_WATCHDOG	= "pic:ultrasound_watchdog"
	PIC_PIC_VERSION	= "pic:pic_version"
	
	
	# VIDEO
	VIDEO_CAMIF_FPS	= "video:camif_fps"
	VIDEO_CODEC_FPS	= "video:codec_fps"
	VIDEO_CAMIF_BUFFERS	= "video:camif_buffers"
	VIDEO_NUM_TRACKERS	= "video:num_trackers"
	VIDEO_VIDEO_CODEC	= "video:video_codec"
	VIDEO_VIDEO_SLICES	= "video:video_slices"
	VIDEO_VIDEO_LIVE_SOCKET	= "video:video_live_socket"
	VIDEO_VIDEO_STORAGE_SPACE	= "video:video_storage_space"
	VIDEO_BITRATE	= "video:bitrate"
	VIDEO_MAX_BITRATE	= "video:max_bitrate"
	VIDEO_BITRATE_CTRL_MODE	= "video:bitrate_ctrl_mode"
	VIDEO_BITRATE_STORAGE	= "video:bitrate_storage"
	VIDEO_VIDEO_CHANNEL	= "video:video_channel"
	VIDEO_VIDEO_ON_USB	= "video:video_on_usb"
	VIDEO_VIDEO_FILE_INDEX	= "video:video_file_index"

	
	# LEDS
	LEDS_LEDS_ANIM	= "leds:leds_anim"
	
	
	# DETECT
	DETECT_ENEMY_COLORS	= "detect:enemy_colors
	DETECT_GROUNDSTRIPE_COLORS	= "detect:groundstripe_colors
	DETECT_ENEMY_WITHOUT_SHELL	= "detect:enemy_without_shell
	DETECT_DETECT_TYPE	= "detect:detect_type
	DETECT_DETECTIONS_SELECT_H	= "detect:detections_select_h
	DETECT_DETECTIONS_SELECT_V_HSYNC	= "detect:detections_select_v_hsync
	DETECT_DETECTIONS_SELECT_V	= "detect:detections_select_v
	
	
	# SYSLOG
	SYSLOG_OUTPUT	= "syslog:output
	SYSLOG_MAX_SIZE	= "syslog:max_size
	SYSLOG_NB_FILES	= "syslog:nb_files
	
	
	# USERBOX
	USERBOX_USERBOX_CMD	= "userbox:userbox_cmd
	
	
	# GPS
	GPS_LATITUDE	= "gps:latitude
	GPS_LONGITUDE	= "gps:longitude
	GPS_ALTITUDE	= "gps:altitude
	
	
	#CUSTOM
	CUSTOM_APPLICATION_ID	= "custom:application_id
	CUSTOM_APPLICATION_DESC	= "custom:application_desc
	CUSTOM_PROFILE_ID	= "custom:profile_id
	CUSTOM_PROFILE_DESC	= "custom:profile_desc
	CUSTOM_SESSION_ID	= "custom:session_id
	CUSTOM_SESSION_DESC	= "custom:session_desc

