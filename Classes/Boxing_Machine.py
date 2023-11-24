import math
import sys
import time


class BoxingMachine:

    def __init__(self, controller):
        self.hx711_controller = controller
        self.session_high_score = 0

        def convert_kg(data):
            return data / 1000

        def calculate_score(elapsed_time):
            # bags mass, calculated by taking the dimensions of my speed bag to get its volume,
            # and the density of its material. genuine leather sits between,
            # .9 to 1.2 g/cm2, so we used 1.0 g/cm2 as an average density, converted it to cubic meters,
            # we multiply the volume and density together to get our mass in grams and finally convert it to kgs.
            BAG_MASS_KG = 0.023328

            # calculate angular velocity, the bag will travel 90 degrees before it hits the bag
            ANGULAR_DISPLACEMENT = 90

            # convert displacement degrees to radians
            angular_displacement_rad = ANGULAR_DISPLACEMENT * (math.pi / 180)

            # calculate angular velocity
            angular_velocity = angular_displacement_rad / elapsed_time

            # calculate acceleration as a = angular_velocity / elapsed_time
            acceleration = angular_velocity / elapsed_time

            # calculate force as f = m * a
            punch_force = (BAG_MASS_KG * acceleration)
            print("Score: ", punch_force)

        def prompt_user(this):
            choice = input("Press E to exit or any other key to punch again")

            if choice.lower() == 'e':
                print("Exiting...")
                sys.exit()

        def run(this):
            # idle limit is the max value a reading can be before we register it as a valid hit
            IDLE_LIMIT = 3000
            # amount of readings since last valid reading
            reading_count = 0

            # prompt the user to interact.
            print("PUNCH TO GET A HIGH SCORE!")

            # main program loop
            while True:
                # zero the load cell
                this.hx711_controller.zero()
                # check for a reading, start our timer, used to calculate acceleration
                start_time = time.time()
                reading = this.hx711_controller.get_data_mean()

                # if the reading is greater than the idle limit in either direction, the bag has been punched.
                if reading > IDLE_LIMIT or reading < -IDLE_LIMIT:
                    # calculate the elapsed time since the bag has been punched
                    elapsed_time = time.time() - start_time
                    # calculate our score
                    this.calculate_score(elapsed_time)
                    # prompt the user if they want to hit the bag again
                    this.prompt_user()
                    # reset idle reading count
                    reading_count = 0
                else:
                    # if no reading found, up the idle reading count and prompt the user
                    reading_count += 1
                    print("Waiting for punch: ", reading_count)

                # if enough readings pass without the bag being hit, exit the program.
                if reading_count > 3:
                    print("Too slow! Exiting..")
                    break
