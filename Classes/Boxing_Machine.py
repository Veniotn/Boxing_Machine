class BoxingMachine:

    def __init__(self, controller):
        self.hx711_controller = controller
        self.session_high_score = 0

    def calculate_score(self, reading, last_reading):
        # bags mass, calculated by taking the dimensions of my speed bag to get its volume,
        # and the density of its material. genuine leather sits between,
        # .9 to 1.2 g/cm2, so we used 1.0 g/cm2 as an average density, converted it to cubic meters,
        # we multiply the volume and density together to get our mass in grams and finally convert it to kgs.
        BAG_MASS_KG = 0.023328

        # if either readings are negative, negate them
        if reading < 0:
            reading = -reading
        if last_reading < 0:
            last_reading = -last_reading

        # calculate the raw punch value by finding the difference between the idle reading and punch reading
        print("Reading: ", reading)
        print("raw punch value: ", (reading - last_reading))

        # our reading is in grams so we convert it to kgs to stay consistent
        reading_kg = reading / 1000

        # for now we will use the current reading as acceleration (to be tweaked) and calulate the force as f = m * a
        punch_force = BAG_MASS_KG * reading_kg
        print("Score: ", punch_force)


    def run(self):
        # idle limit is the max value a reading can be before we register it as a valid hit
        IDLE_LIMIT = 1000
        # amount of readings since last valid reading
        reading_count = 0
        # value of the last idle reading used to find the value of our hit.
        last_idle_reading = 0

        # prompt the user to interact.
        print("PUNCH TO GET A HIGH SCORE!")

        while True:
            # zero the load cell
            self.hx711_controller.zero()
            # check for a reading
            reading = self.hx711_controller.get_data_mean()

            # if the reading is greater than the idle limit in either direction, the bag has been punched.
            if reading > IDLE_LIMIT or reading < -IDLE_LIMIT:
                self.calculate_score(reading, last_idle_reading)
            else:
                # if no reading found, up the idle reading count and prompt the user
                reading_count += 1
                # save the current idle reading
                last_idle_reading = reading
                print("Waiting for punch: ", reading_count)

            # if enough readings pass without the bag being hit, exit the program.
            if reading_count > 3:
                break
