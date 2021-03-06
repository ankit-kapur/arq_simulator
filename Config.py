import pygame

# ========= Configurations ========== #

# Rate of packet movement
rate_of_movement = 1

# Timer config
timer_increment = 1
timeout = 800
timer_radius = 18
clock_thickness = 3

# Dimensions of packet
packet_height = 40
packet_width = 20

# Window dimensions
window_width = 870
window_height = 500

# Border width
border_width = 2

# Padding
wall_padding = 70
packet_padding = 25

# ------- Colors ------- #
# Background color
clock_color = (255,255,255)  # WHITE
background_color = pygame.Color('black')
transmitter_init_color = (0,135,135)  # AQUA
transmitter_transmitted_color = (0,0,135)  # BLUE
transmitter_ackreceived_color = (105,0,0)  # RED
receiver_init_color = (0,0,0)  # BLACK
receiver_received_color = (0,135,0)  # GREEN
packet_color = (255, 102, 0)  # ORANGE
ack_packet_color = (225,225,0)  # GREEN
border_color = (255,255,255)  # WHITE

# ========== End of config ========== #