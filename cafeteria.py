import random
import numpy as np
import pandas as pd
import simpy
import statistics
import calendar
import time


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

        # timestamp lists
        self.full_wait_times = []
        self.kiosk_wait_times = []
        self.chef_wait_times = []
        self.utensil_wait_times = []
        self.pop_wait_times = []

    # processes/events. time unit is seconds
    def order_food(self, customer):
        yield self.env.timeout(random.randint(60, 181))

    def make_food(self, customer):
        yield self.env.timeout(random.randint(180, 421))

    def get_utensils(self, customers):
        # print(f"get utensils before: {env.now}")
        yield self.env.timeout(random.randint(0, 31))

    def get_drink(self, customers):
        # print(f"get drink before: {env.now}")
        yield self.env.timeout(random.randint(30, 91))


# flow of processes
def get_lunch(env, customer, cafeteria, is_quiet=True):
    # customer/employee arrives at cafeteria
    arrival_time = env.now

    # customer goes up to a kiosk to order
    with cafeteria.kiosk.request() as request:
        yield request

        kiosk_start_ts = env.now
        if not is_quiet:
            print(f"Customer {customer} starts order at kiosk at {kiosk_start_ts}s")

        yield env.process(cafeteria.order_food(customer))

        kiosk_end_ts = env.now
        if not is_quiet:
            print(f"Customer {customer} completes order at kiosk at {kiosk_end_ts}s")

    with cafeteria.chef.request() as request:
        yield request

        chef_start_ts = env.now
        if not is_quiet:
            print(f"Chef starts making food ordered by customer {customer} at {chef_start_ts}s")

        yield env.process(cafeteria.make_food(customer))

        chef_end_ts = env.now
        if not is_quiet:
            print(f"Chef completes making food ordered by customer {customer} at {chef_end_ts}s")

    # if customer orders food that require utensils, request utensil dispenser resource
    utensil_start_ts = 0
    utensil_end_ts = 0
    if random.choice([True, False]):
        with cafeteria.utensil_dispenser.request() as request:
            yield request

            utensil_start_ts = env.now
            if not is_quiet:
                print(f"Customer {customer} goes to utensil dispenser at {utensil_start_ts}s")

            yield env.process(cafeteria.get_utensils(customer))

            utensil_end_ts = env.now
            if not is_quiet:
                print(f"Customer {customer} leaves utensil dispenser at {utensil_end_ts}s")
    elif not is_quiet:
        print(f"Customer {customer} does not require utensils for the food ordered")

    # if customer orders a drink in addition to the food
    pop_start_ts = 0
    pop_end_ts = 0
    if random.choice([True, False]):
        with cafeteria.pop_machine.request() as request:
            yield request

            pop_start_ts = env.now
            if not is_quiet:
                print(f"Customer {customer} goes to pop machine at {pop_start_ts}s")

            yield env.process(cafeteria.get_drink(customer))

            pop_end_ts = env.now
            if not is_quiet:
                print(f"Customer {customer} leaves pop machine at {pop_end_ts}s")
    elif not is_quiet:
        print(f"Customer {customer} did not order a drink")


    cafeteria.full_wait_times.append(env.now - arrival_time)
    cafeteria.kiosk_wait_times.append(pop_end_ts - pop_start_ts)
    cafeteria.chef_wait_times.append(chef_end_ts - chef_start_ts)
    cafeteria.utensil_wait_times.append(utensil_end_ts - utensil_start_ts)
    cafeteria.pop_wait_times.append(utensil_end_ts - utensil_start_ts)

# method to run the simulation
def run_cafeteria(env, cafeteria, is_quiet):

    customer = 0

    while True:
        # wait 1-3 minutes before generating a new person
        yield env.timeout(random.randint(60, 181))

        customer += 1
        env.process(get_lunch(env, customer, cafeteria, is_quiet))

# method to get average wait time in hours
def get_average_wait_time_hr(wait_time):
    avg_wait_time =  statistics.mean(wait_time)
    average_wait_hr = int(avg_wait_time / (60 * 60))

    return average_wait_hr

# method to get average wait time in minutes
def get_average_wait_time_min(wait_time):
    avg_wait_time =  statistics.mean(wait_time)
    average_wait_sec = int(avg_wait_time / 60)

    return average_wait_sec

# method to get average wait time in seconds
def get_average_wait_time_sec(wait_time):
    avg_wait_time =  statistics.mean(wait_time)
    average_wait_sec = int(avg_wait_time % 60)

    return average_wait_sec

def get_average_wait_time(wait_times):
    average_wait_hr = get_average_wait_time_hr(wait_times)
    average_wait_time_min = get_average_wait_time_min(wait_times)
    average_wait_time_sec = get_average_wait_time_sec(wait_times)

    return [average_wait_hr, average_wait_time_min, average_wait_time_sec]

def wait_times_to_df(full_wait_list, kiosk_list, chef_list, utensil_list, pop_list):
    d = {'Total_wait_time': full_wait_list, 'Kiosk_wait_times': kiosk_list, 'Chef_wait_times':
        chef_list, 'Utensil_dispenser_wait_times': utensil_list, 'Pop_machine_wait_times':
        pop_list}

    df = pd.DataFrame(data=d)

    return df

def summarize_df(df):
    total_min = min(df.loc[:, 'Total_wait_time'])
    total_max = max(df.loc[:, 'Total_wait_time'])
    total_avg = statistics.mean(df.loc[:, 'Total_wait_time'])
    total_05 = df['Total_wait_time'].quantile(.05)
    total_95 = df['Total_wait_time'].quantile(.95)
    total_sd = statistics.stdev(df.loc[:, 'Total_wait_time'])

    kiosk_min = min(df.loc[:, 'Kiosk_wait_times'])
    kiosk_max = max(df.loc[:, 'Kiosk_wait_times'])
    kiosk_avg = statistics.mean(df.loc[:, 'Kiosk_wait_times'])
    kiosk_05 = df['Kiosk_wait_times'].quantile(.05)
    kiosk_95 = df['Kiosk_wait_times'].quantile(.95)
    kiosk_sd = statistics.stdev(df.loc[:, 'Kiosk_wait_times'])

    chef_min = min(df.loc[:, 'Chef_wait_times'])
    chef_max = max(df.loc[:, 'Chef_wait_times'])
    chef_avg = statistics.mean(df.loc[:, 'Chef_wait_times'])
    chef_05 = df['Chef_wait_times'].quantile(.05)
    chef_95 = df['Chef_wait_times'].quantile(.95)
    chef_sd = statistics.stdev(df.loc[:, 'Chef_wait_times'])

    utensil_min = min(df.loc[:, 'Utensil_dispenser_wait_times'])
    utensil_max = max(df.loc[:, 'Utensil_dispenser_wait_times'])
    utensil_avg = statistics.mean(df.loc[:, 'Utensil_dispenser_wait_times'])
    utensil_05 = df['Utensil_dispenser_wait_times'].quantile(.05)
    utensil_95 = df['Utensil_dispenser_wait_times'].quantile(.95)
    utensil_sd = statistics.stdev(df.loc[:, 'Utensil_dispenser_wait_times'])

    pop_min = min(df.loc[:, 'Pop_machine_wait_times'])
    pop_max = max(df.loc[:, 'Pop_machine_wait_times'])
    pop_avg = statistics.mean(df.loc[:, 'Pop_machine_wait_times'])
    pop_05 = df['Pop_machine_wait_times'].quantile(.05)
    pop_95 = df['Pop_machine_wait_times'].quantile(.95)
    pop_sd = statistics.stdev(df.loc[:, 'Pop_machine_wait_times'])

    min_list = [total_min, kiosk_min, chef_min, utensil_min, pop_min]
    max_list = [total_max, kiosk_max, chef_max, utensil_max, pop_max]
    avg_list = [total_avg, kiosk_avg, chef_avg, utensil_avg, pop_avg]
    pct05_list = [total_05, kiosk_05, chef_05, utensil_05, pop_05]
    pct95_list = [total_95, kiosk_95, chef_95, utensil_95, pop_95]
    sd_list = [total_sd, kiosk_sd, chef_sd, utensil_sd, pop_sd]

    summary_dict = {'min': min_list, 'max': max_list, 'avg': avg_list,
                    '5th_pctile': pct05_list, '95th_pctile': pct95_list, 'sd': sd_list}

    summary_df = pd.DataFrame(data=summary_dict, index=['Total', 'Kiosk', 'Chef', 'Utensil', 'Pop'])

    return summary_df

def main():
    # resource numbers / changes can be made to these settings
    num_kiosks = 3
    num_chefs = 2
    num_utensil_dispensers = 4
    num_pop_machines = 2

    # whether to supress event timestamps or print them / up to user
    is_quiet = True

    # how long to run in seconds / up to user to change
    duration = 7200

    # time stamp / not recommended to change
    curr_time_stamp = calendar.timegm(time.gmtime())

    # path of output file / nothing recommended to change below this
    data_path = './output/' + 'd' + str(duration) + '_k' + str(num_kiosks) + '_c' + str(num_chefs)\
              + '_u' + str(num_utensil_dispensers) + '_p' + str(num_pop_machines) + '_ts' + \
           str(curr_time_stamp) + '.csv'

    summary_path = './output/' + 'd' + str(duration) + '_k' + str(num_kiosks) + '_c' + str(
        num_chefs) + '_u' + str(num_utensil_dispensers) + '_p' + str(num_pop_machines) + '_ts' + \
           str(curr_time_stamp) + '_summary.csv'

    env = simpy.Environment()

    cafeteria = Cafeteria(env=env, num_kiosks=num_kiosks, num_chefs=num_chefs,
                          num_utensil_dispensers=num_utensil_dispensers,
                          num_pop_machines=num_pop_machines)

    env.process(run_cafeteria(env, cafeteria, is_quiet))

    env.run(until=duration)

    df = wait_times_to_df(cafeteria.full_wait_times, cafeteria.kiosk_wait_times,
                          cafeteria.chef_wait_times, cafeteria.utensil_wait_times,
                          cafeteria.pop_wait_times)

    df.to_csv(data_path)

    df_ = summarize_df(df)
    df_.to_csv(summary_path)

    print(df_)

    avg = get_average_wait_time(cafeteria.full_wait_times)
    print(f"\nAverage wait time per customer: {avg[0]} hours, {avg[1]} minutes, {avg[2]} seconds")

if __name__ == '__main__':
    main()