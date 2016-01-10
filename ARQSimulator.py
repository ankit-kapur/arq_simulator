import pygame
import Utils
import Components
import Config

# No. of packets
num_of_packets = (Config.window_width - Config.wall_padding)/(Config.packet_width + Config.packet_padding)

# Is the simulation over?
is_simulation_over = False
start_new_simulation = False

# Mouse coordinates
mouse_x = 0
mouse_y = 0
mouse_pressed = False


class Main:
    def __init__(self):
        global is_simulation_over
        global start_new_simulation
        global mouse_x
        global mouse_y

        # Initialize the pygame library
        pygame.init()

        # This clock will control the FPS
        clock = pygame.time.Clock()

        # Setup the game-screen
        screensize = (Config.window_width, Config.window_height)
        self.surface = pygame.display.set_mode(screensize)
        pygame.display.set_caption("ARQ protocol simulator")

        # Make the simulator
        simulator = Simulator(self.surface)

        # The main loop begins
        while not simulator.quit_simulation:

            # Store mouse-pointer position
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0]
            mouse_y = mouse_pos[1]

            # If user requested for a new simulation, make a new one
            if start_new_simulation:
                start_new_simulation = False
                is_simulation_over = False

                # Make the simulator
                simulator = Simulator(self.surface)

            # Unless the simulation is over, keep updating all sprites
            if not is_simulation_over:
                # Update all the sprites
                simulator.packet_list.update()
                simulator.ack_list.update()

            # Fill the background surface
            simulator.surface.fill(Config.background_color)

            # Make background image
            # simulator.blit_background_img_surface()

            # Draw all the sprites (the ordering is important)
            simulator.border_sprite_list.draw(simulator.surface)
            simulator.transmitter_list.draw(simulator.surface)
            simulator.receiver_list.draw(simulator.surface)
            simulator.ack_list.draw(simulator.surface)
            simulator.packet_list.draw(simulator.surface)

            # Show text banners
            # simulator.show_text_banners()

            # Check if the current transmitter got an ACK.
            # If yes, move on to the next transmitter.
            simulator.is_transmission_complete()

            # FPS
            clock.tick(120)

            # Update the screen with everything we've drawn.
            pygame.display.flip()

            # Handle events
            simulator.handle_events()



class Simulator:

    def __init__(self, surface):
        print 'Starting new simulation.'
        global num_of_packets

        # Current transmitter position
        self.current_position = 0

        # Initialize stuff
        self.surface = surface
        self.quit_simulation = False

        # These maps all have a numeric key corresponding to the i-th transmitter/receiver/whatever.
        # We use them so we can look up the i-th component immediately
        self.transmitter_map = {}
        self.receiver_map = {}
        self.packet_map = {}
        self.ack_map = {}

        # Sprite groups - useful for updating & drawing all the shapes all-at-once as a group
        # List of transmitters (x_pos, y_pos, width, height)
        self.transmitter_list = pygame.sprite.Group()
        # List of receivers (x_pos, y_pos, width, height)
        self.receiver_list = pygame.sprite.Group()
        # Packets
        self.packet_list = pygame.sprite.Group()
        # ACK Packets
        self.ack_list = pygame.sprite.Group()
        # Border boxes around the packets
        self.border_sprite_list = pygame.sprite.Group()

        # Make transmitters and receivers
        self.make_transmitter_boxes()
        self.make_receiver_boxes()

        # Start simulation
        self.start_simulation()

    def start_simulation(self):

        # Begin transmission for the 1st packet
        self.begin_transmission(i=0)

    # Send the packet at the i-th position
    def begin_transmission(self, i):

        # Does a transmitter exist at position i?
        if not self.transmitter_map.has_key(i):
            return

        # Find the i-th transmitter (by looking it up from the map)
        current_transmitter = self.transmitter_map[i]

        # ======================== Handshakes ========================
        # [Let everyone know who their corresponding components are (at this i-th position)]

        # Tell the transmitter box which packet it needs to send
        self.transmitter_map[i].set_packet(self.packet_map[i])

        # Tell the packet which receiver box it has to travel to
        self.packet_map[i].set_receiver(self.receiver_map[i])

        # Tell the receiver box know which ack packet corresponds to it.
        self.receiver_map[i].set_ack_packet(self.ack_map[i])

        # Tell the ack packet which transmitter box it's supposed to return to.
        self.ack_map[i].set_transmission_box(self.transmitter_map[i])

        # ============ Start transmission for this packet =============
        current_transmitter.start_transmission()

    # Checks if the current transmitter is done sending it's packet (and has received an ACK for it).
    # If it's got an ACK, we move on to the next transmitter.
    def is_transmission_complete(self):
        if (self.transmitter_map[self.current_position].has_ack_been_received()):
            # This transmitter got an ACK for it had sent. Move on.
            self.current_position += 1
            self.begin_transmission(self.current_position)


    # Make the transmitter packet boxes (and their borders)
    def make_transmitter_boxes(self):
        y_coord = 0 + Config.wall_padding
        x_start = 0 + Config.wall_padding

        i = 0
        for x_coord in Utils.frange(x_start, Config.wall_padding + (num_of_packets*Config.packet_width) + (num_of_packets*Config.packet_padding), Config.packet_padding + Config.packet_width):

            # First make the border for the packet
            border = Components.Box(x_coord-Config.border_width, y_coord-Config.border_width, Config.packet_width+2*Config.border_width, Config.packet_height+2*Config.border_width, Config.border_color)
            self.border_sprite_list.add(border)

            # Make the transmitter box
            new_transbox = Components.TransmitterBox(x_coord, y_coord)
            self.transmitter_list.add(new_transbox)
            self.transmitter_map[i] = new_transbox

            # Make the packet (with it's coordinates the same as the transmitter box)
            new_packet = Components.Packet(x_coord, y_coord)
            self.packet_list.add(new_packet)
            self.packet_map[i] = new_packet
            i += 1

    # Make the receiver packet boxes (and their borders)
    def make_receiver_boxes(self):
        y_coord = Config.window_height - Config.wall_padding - Config.packet_height
        x_start = 0 + Config.wall_padding

        i = 0
        for x_coord in Utils.frange(x_start, Config.wall_padding + (num_of_packets*Config.packet_width) + (num_of_packets*Config.packet_padding), Config.packet_padding + Config.packet_width):

            # First make the border for the packet
            border = Components.Box(x_coord-Config.border_width, y_coord-Config.border_width, Config.packet_width+2*Config.border_width, Config.packet_height+2*Config.border_width, Config.border_color)
            self.border_sprite_list.add(border)

            # Make the new receiver box
            new_recbox = Components.ReceiverBox(x_coord, y_coord)
            self.receiver_list.add(new_recbox)
            self.receiver_map[i] = new_recbox

            # Make the ACK packet (with it's coordinates the same as the receiver box)
            ack_packet = Components.AckPacket(x_coord, y_coord)
            self.ack_list.add(ack_packet)
            self.ack_map[i] = ack_packet
            i += 1


    # Handle mouse click and key-press events
    def handle_events(self):
        global mousepressed
        global start_new_simulation

        # ----------- Event handlers ------------- #
        events = pygame.event.get()
        for e in events:
            if e.type is pygame.MOUSEBUTTONDOWN:
                mousepressed = True
            elif e.type is pygame.MOUSEBUTTONUP:
                mousepressed = False

            if e.type is pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.quit_simulation = True
                if e.key == pygame.K_SPACE:
                    start_new_simulation = True

            if e.type is pygame.QUIT:
                # To quit when the close button is clicked
                self.quit_simulation = True


Main()