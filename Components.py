import pygame
import Config

class Box(pygame.sprite.Sprite):
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
        self.w = w
        self.h = h


# The Packet and Ack classes will both inherit from this GenericPacket class
class GenericPacket(Box):
    def __init__(self, x, y, packet_color):
        # Is moving?
        self.is_moving = False

        # Keep record of these initial coordinates. We'll need to them to reset the packet when it's destroyed.
        self.init_x = x
        self.init_y = y
        self.init_color = packet_color

        # Call super constructor
        Box.__init__(self, x, y, Config.packet_width, Config.packet_height, packet_color)

    def reset_packet(self):
        self.rect.x = self.init_x
        self.rect.y = self.init_y
        self.image.fill(self.init_color)

    def erase_packet(self):
        # Camouflage it into a corner
        self.image.fill(Config.background_color)
        self.rect.x = Config.window_width
        self.rect.y = Config.window_height


# The packet
class Packet(GenericPacket):

    def __init__(self, x, y):
        GenericPacket.__init__(self, x, y, Config.transmitter_init_color)
        self.receiver_box = None

    def update(self):
        if self.is_moving:
            # Move
            self.rect.y += Config.rate_of_movement

            # Collision detection
            if self.rect.y >= Config.window_height - Config.wall_padding - Config.packet_height:
                # Packet has reached the receiver
                self.is_moving = False
                self.receiver_box.send_ack()

                # Erase the packet (it's job is done)
                self.erase_packet()

    def set_receiver(self, receiver_box):
        self.receiver_box = receiver_box

    def start_packet_transmission(self):
        # Restore the packets defaults before starting it's movement
        self.reset_packet()
        self.image.fill(Config.packet_color)
        # Start moving
        self.is_moving = True


# The packet
class AckPacket(GenericPacket):

    def __init__(self, x, y):
        GenericPacket.__init__(self, x, y, Config.receiver_init_color)
        self.transmitter_box = None

    def set_transmission_box(self, transmission_box):
        self.transmitter_box = transmission_box

    def start_ack_tranmission(self):
        # Restore the packets defaults before starting it's movement
        self.reset_packet()
        # Start moving
        self.is_moving = True
        self.image.fill(Config.ack_packet_color)

    def update(self):
        if self.is_moving:
            # Move
            self.rect.y -= Config.rate_of_movement

            # Collision detection
            if self.rect.y <= 0 + Config.wall_padding:
                self.is_moving = False
                self.transmitter_box.changestate('ack_received')

                # Erase the packet (it's job is done)
                self.erase_packet()


# The transmitter box
class TransmitterBox(Box):

    def __init__(self, x, y):
        # Set default state to 'init'
        self.state = "init"
        self.packet_in_this_box = None

        # Call super constructor
        boxfill_color = self.get_color_by_state()
        Box.__init__(self, x, y, Config.packet_width, Config.packet_height, boxfill_color)

    def set_packet(self, packet):
        self.packet_in_this_box = packet

    def get_color_by_state(self):
        if self.state == "init":
            return Config.transmitter_init_color
        if self.state == "transmitted":
            return Config.transmitter_transmitted_color
        if self.state == "ack_received":
            return Config.transmitter_ackreceived_color
        else:
            return None

    def update(self):
        boxfill_color = self.get_color_by_state()
        self.image.fill(boxfill_color)

    def changestate(self, new_state):
        self.state = new_state
        self.update()

    def start_transmission(self):
        self.changestate("transmitted")
        self.packet_in_this_box.start_packet_transmission()

    def has_ack_been_received(self):
        return self.state == "ack_received"


# The receiver box
class ReceiverBox(Box):

    def __init__(self, x, y):
        # Set default state to 'init'
        self.state = "init"
        self.ack_packet = None

        # Call super constructor
        boxfill_color = self.get_color_by_state()
        Box.__init__(self, x, y, Config.packet_width, Config.packet_height, boxfill_color)

    def send_ack(self):
        self.changestate('sending_ack')
        self.ack_packet.start_ack_tranmission()

    def set_ack_packet(self, ack_packet):
        self.ack_packet = ack_packet

    def get_color_by_state(self):
        # TODO: Change later
        if self.state == "init":
            return Config.receiver_init_color
        if self.state == "sending_ack":
            return Config.receiver_received_color
        else:
            return None

    def update(self):
        boxfill_color = self.get_color_by_state()
        self.image.fill(boxfill_color)

    def changestate(self, new_state):
        self.state = new_state
        self.update()