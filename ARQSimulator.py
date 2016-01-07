import pygame
import Utils


# ========= Configurations ========== #

# Dimensions of packet
packet_height = 40
packet_width = 20

# Window dimensions
window_width = 870
window_height = 400

# Border width
border_width = 2

# Padding
wall_padding = 40
packet_padding = 25

# No. of packets
num_of_packets = (window_width - wall_padding)/(packet_width + packet_padding)

# ------- Colors ------- #
# Background color
background_color = pygame.Color('black')
transmitter_color = (0,0,135)
# (135,0,0) # RED
receiver_color = (0,0,0)
border_color = (255,255,255)

# Is the simulation over?
is_simulation_over = False
new_game = False

# Mouse coordinates
mouse_x = 0
mouse_y = 0
mouse_pressed = False
# ========== End of config ========== #


class Interactable(object):
    def __init__(self, x_pos=None, y_pos=None, height=None, width=None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.height = height
        self.width = width


class Packet(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color_of_packet):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a surface for the packet
        self.image = pygame.Surface([w,h])
        self.image.fill(color_of_packet)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


class Main:
    def __init__(self):
        global is_simulation_over
        global new_game
        global mouse_x
        global mouse_y

        # Initialize the pygame library
        pygame.init()

        # This clock will control the FPS
        clock = pygame.time.Clock()

        # Setup the game-screen
        screensize = (window_width, window_height)
        self.surface = pygame.display.set_mode(screensize)
        pygame.display.set_caption("ARQ protocol simulator")

        # Make the simulator
        simulator = Simulator(self.surface)
        # The main loop begins
        while not simulator.quit_game:

            # Store mouse-pointer position
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0]
            mouse_y = mouse_pos[1]

            # If it's time for a new game, make a new game
            if new_game:
                new_game = False
                is_simulation_over = False
                # game = Game(self.surface)

            # Unless the simulation is over, keep updating all sprites
            if not is_simulation_over:
                # Update all the sprites
                simulator.transmitter_list.update()
                simulator.receiver_list.update()

            # Fill the background surface
            simulator.surface.fill(background_color)

            # Make background image
            # simulator.blit_background_img_surface()

            # Check for collisions
            # simulator.check_for_collisions()

            # Draw all the sprites
            simulator.border_sprite_list.draw(simulator.surface)
            simulator.transmitter_list.draw(simulator.surface)
            simulator.receiver_list.draw(simulator.surface)

            # Show text banners
            # simulator.show_text_banners()
            #
            # if is_simulation_over:
            #     simulator.make_gameover_surface()

            # FPS
            clock.tick(120)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # Handle events
            simulator.handle_events()



class Simulator:

    def __init__(self, surface):
        global interactables
        global num_of_packets

        # Initialize stuff
        self.surface = surface
        interactables = []
        self.quit_game = False

        # List of transmitters (x_pos, y_pos, width, height)
        self.transmitter_list = pygame.sprite.Group()
        # List of receivers (x_pos, y_pos, width, height)
        self.receiver_list = pygame.sprite.Group()
        # Borders around packets
        self.border_sprite_list = pygame.sprite.Group()

        # Make transmitters and receivers
        self.transmitter_list.add(self.make_packet_wall(0 + wall_padding, transmitter_color))
        self.receiver_list.add(self.make_packet_wall(window_height - wall_padding - packet_height, receiver_color))

    # Make the transmitter & receiver packets
    def make_packet_wall(self, y_coord, color_of_packet):
        x_start = 0 + wall_padding
        packet_list_temp = []

        for x_coord in Utils.frange(x_start, wall_padding + (num_of_packets*packet_width) + (num_of_packets*packet_padding), packet_padding + packet_width):

            # First make the border for the packet
            border = Packet(x_coord-border_width, y_coord-border_width, packet_width+2*border_width, packet_height+2*border_width, border_color)
            self.border_sprite_list.add(border)

            # Make the packet
            new_packet = Packet(x_coord, y_coord, packet_width, packet_height, color_of_packet)
            packet_list_temp.append(new_packet)

        return packet_list_temp

    # Handle mouse click and key-press events
    def handle_events(self):
        global mousepressed

        # ----------- Event handlers ------------- #
        events = pygame.event.get()
        for e in events:
            if e.type is pygame.MOUSEBUTTONDOWN:
                mousepressed = True
            elif e.type is pygame.MOUSEBUTTONUP:
                mousepressed = False

            if e.type is pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.quit_game = True

            if e.type is pygame.QUIT:
                # To quit when the close button is clicked
                self.quit_game = True


Main()