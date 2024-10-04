# Machine Temperature Data

This class will represent the data.
it will abstract away what used underneath (how to store the data, etc) and provide methods to interact with the data.

# data generation

each datum represent a temperature reading from a sensor at a single point in time.
the generation of the next datum is **determined by the state of the machine**.

**how much** the temperature will go up or down is determined by how long the machine has been working or not working,
it follows **Newton's law of cooling**, to simulate real life temperature change.

## behavior

- **normally**, as the machine is not working, the temperature will go down.
- **if the machine is currently running**, the temperature will go up.
- **once in a while**, there will be noise.

# noise

noise will be generated randomly with certain probability.
this is to **simulate** the real-world condition where the **sensor might be broken**. 
Noise is implemented as additional deviation from the normal temperature reading (the implementation shouldn't matter, as long as it's able to produce a different value than the normal one).
