import random
import simpy
import statistics

full_wait_times = []


class Cafeteria(object):
    def __init__(self, env, num_kiosks=2, num_chefs=2,
                 num_utensil_dispensers=4, num_pop_machines=2):
        # environment
        self.env = env

        # resources
        self.kiosk = simpy.Resource(env, num_kiosks)
        self.chef = simpy.Resource(env, num_chefs)
        self.utensil_dispenser = simpy.Resource(env, num_utensil_dispensers)
        self.pop_machine = simpy.Resource(env, num_pop_machines)

    # processes/events. time unit is seconds
    def order_food(self, customer):
        # print(f"order food before: {env.now}")
        yield self.env.timeout(random.randint(60, 181))

    def make_food(self, customer):
        yield self.env.timeout(random.randint(180, 361))

    def get_utensils(self, customers):
        # print(f"get utensils before: {env.now}")
        yield self.env.timeout(random.randint(0, 31))

    def get_drink(self, customers):
        # print(f"get drink before: {env.now}")
        yield self.env.timeout(random.randint(30, 91))


def get_lunch(env, customer, cafeteria):
    # customer/employee arrives at cafeteria
    arrival_time = env.now

    with cafeteria.kiosk.request() as request:
        yield request
        yield env.process(cafeteria.order_food(customer))

    with cafeteria.chef.request() as request:
        yield request
        yield env.process(cafeteria.make_food(customer))

    if random.choice([True, False]):
        with cafeteria.utensil_dispenser.request() as request:
            yield request
            yield env.process(cafeteria.get_utensils(customer))

    if random.choice([True, False]):
        with cafeteria.pop_machine.request() as request:
            yield request
            yield env.process(cafeteria.get_drink(customer))

    full_wait_times.append(env.now - arrival_time)

def run_cafeteria(env, num_kiosks, num_chefs, num_utensil_dispensers,
                  num_pop_machines):
    cafeteria = Cafeteria(env, num_kiosks, num_chefs, num_utensil_dispensers,
                          num_pop_machines)
    customer = 0

    while True:
        # wait 1-5 minutes before generating a new person
        yield env.timeout(random.randint(60, 361))

        customer += 1
        env.process(get_lunch(env, customer, cafeteria))

def get_average_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)

    return average_wait

def main():
    print("hi from main")
    num_kiosks = 2
    num_chefs = 2
    num_utensil_dispensers = 4
    num_pop_machines = 2

    env = simpy.Environment()

    env.process(run_cafeteria(env, num_kiosks, num_chefs,
                              num_utensil_dispensers, num_pop_machines))

    env.run(until=3600)

    print(f"Average wait time in minutes: "
          f"{get_average_wait_time(full_wait_times)/60:,.2f}")

if __name__ == '__main__':
    main()