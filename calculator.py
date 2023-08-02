def heatloss_estimate (gasuse_total, dhw_monthly, balance_point, furnace_eff, hl_derate, location): #, heatpumpsize, heatpumpcap_17_c1, heatpumpcap_47_c1, heatpumpcap_17_c2, heatpumpcap_47_c2, heatpumpcap_17_c3, heatpumpcap_47_c3, hp_derate, derate_c1, derate_c2, derate_c3):
    import pandas as pd
    import numpy as np
    import math
    from datetime import datetime
    import datetime

    estimate_2021=[]
    start_2021 = '2021-01-01 00:00:00'
    end_2021 = '2021-12-31 23:00:00'
    # import weather data and specify design temperature based on location (GTHA locations)
    if location == 'toronto':
        weatherdata = pd.read_csv("static/5yr_toronto_weather.csv",parse_dates=['date_time_local'])
        weatherdata = weatherdata.set_index('date_time_local')
        estimate_2021 = weatherdata.loc[start_2021 : end_2021]
        location_name = 'Toronto'
        dtemp = -18
    elif location == 'caledon':
        weatherdata = pd.read_csv("static/5yr_caledon_weather.csv",parse_dates=['date_time_local'])
        weatherdata = weatherdata.set_index('date_time_local')
        estimate_2021 = weatherdata.loc[start_2021 : end_2021]
        location_name = 'Caledon'
        dtemp = -21
    #elif location == 'markham':
    #    weatherdata = pd.read_csv("static/5yr_markham_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Markham'
    #    dtemp = -21
    elif location == 'brampton':
        weatherdata = pd.read_csv("static/5yr_brampton_weather.csv",parse_dates=['date_time_local'])
        weatherdata = weatherdata.set_index('date_time_local')
        estimate_2021 = weatherdata.loc[start_2021 : end_2021]
        location_name = 'Brampton'
        dtemp = -19
    elif location == 'mississauga':
        weatherdata = pd.read_csv("static/5yr_mississauga_weather.csv",parse_dates=['date_time_local'])
        weatherdata = weatherdata.set_index('date_time_local')
        estimate_2021 = weatherdata.loc[start_2021 : end_2021]
        location_name = 'Mississauga'
        dtemp = -18
    #elif location == 'burlington':
    #    weatherdata = pd.read_csv("static/5yr_burlington_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Burlington'
    #    dtemp = -17
    #elif location == 'hamilton':
    #    weatherdata = pd.read_csv("static/5yr_hamilton_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Hamilton'
    #    dtemp = -17
    #elif location == 'oakville':
    #    weatherdata = pd.read_csv("static/5yr_oakville_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Oakville'
    #    dtemp = -18
    #elif location == 'richmondhill':
    #    weatherdata = pd.read_csv("static/5yr_richmondhill_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Richmond Hill'
    #    dtemp = -21
    #elif location == 'vaughan':
    #    weatherdata = pd.read_csv("static/5yr_vaughan_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Vaughan'
    #    dtemp = -20
    #elif location == 'oshawa':
    #    weatherdata = pd.read_csv("static/5yr_oshawa_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Oshawa'
    #    dtemp = -19
    #elif location == 'pickering':
    #    weatherdata = pd.read_csv("static/5yr_pickering_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Pickering'
    #    dtemp = -19
    #elif location == 'newmarket':
    #    weatherdata = pd.read_csv("static/5yr_newmarket_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Newmarket'
    #    dtemp = -22
    #elif location == 'milton':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Milton'
    #    dtemp = -18
    #elif location == 'haltonhills':
    #    weatherdata = pd.read_csv("static/5yr_haltonhills_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Halton Hills'
    #    dtemp = -19
    #elif location == 'caledon':
    #    weatherdata = pd.read_csv("static/5yr_caledon_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Caledon'
    #    dtemp = 
    #elif location == 'king':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'King'
    #    dtemp = 
    #elif location == 'aurora':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Aurora'
    #    dtemp = -21
    #elif location == 'whitchurchstouffville':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Whitchurch-Stouffville'
    #    dtemp = 
    #elif location == 'eastgwillimbury':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'East Gwillimbury'
    #    dtemp = 
    #elif location == 'georgina':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Georgina'
    #    dtemp = 
    #elif location == 'brock':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Brock'
    #    dtemp = 
    #elif location == 'uxbridge':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Uxbridge'
    #    dtemp = -22
    #elif location == 'ajax':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Ajax'
    #    dtemp = -20
    #elif location == 'whitby':
    #    weatherdata = pd.read_csv("static/5yr_whitby_weather.csv",parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Whitby'
    #    dtemp = -20
    #elif location == 'scugog':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Scugog'
    #    dtemp = 
    #elif location == 'clarington':
    #    weatherdata = pd.read_csv(,parse_dates=['date_time_local'])
    #    weatherdata = weatherdata.set_index('date_time_local')
    #    estimate_2021 = weatherdata.loc[start_2021 : end_2021]
    #    location_name = 'Clarington'
    #    dtemp = 

    # calculate annual gas use from furnace
    dhw_annual = dhw_monthly*12
    gasuse_annual = gasuse_total - dhw_annual
    
    # define variables and state first heat loss guess
    heatloss_guess = 10 # kBtu/hr - first guess of heat loss at -15C (not a reasonable guess, but a relatively low value to reduce runtime)
    gas_estimate_total = 0
    
    # loop through different heat loss estimates until annual usage estimate is close to the user input
    while int(gas_estimate_total) < gasuse_annual*(1+(hl_derate/100)):
        heatloss_guess += 1
        # estimate heat loss slope and intercept with each guess
        m = (heatloss_guess - 0)/(-15 - balance_point)
        b = 0 - (m * balance_point)
    
    # estimate hourly heat loss based on weather data
        heatloss = []
        for x in estimate_2021.temperature:
            if x > balance_point:
                heatloss.append(0)
            else:
                heatloss.append(m * x + b)
        estimate_2021['heatloss'] = heatloss
        estimate_2021['gas_m3'] = estimate_2021.heatloss * (1/3.41) * (1/10.5) * (1/(furnace_eff/100))
    
    # calculate total annual estimated gas use
        gas_estimate_total = estimate_2021.gas_m3.sum()

        if int(gas_estimate_total) == gasuse_annual*(1+(hl_derate/100)):
            break

    # calculate total annual heat loss (needed for histogram plot)
    heatloss_annual = estimate_2021.heatloss.sum()

    # calculate design heat loss 
    heatloss_design = (m * dtemp) + b

    # create output variables for plotting
    #x_plots = []
    #for min in mintemp:
    #    x_plots.append(np.linspace(min,balance_point,20))

    # calculate heatloss for 5-year period (2017-2021)
    weatherdata['heatloss'] = m * weatherdata.temperature + b

    # create dataframe for plotting heat load distribution
    temp_points = np.arange(-30,balance_point,5)
    hours1 = []
    load1 = []
    for point in temp_points:
        hour_count = 0
        load_sum = 0
        for temp,hl in zip(weatherdata['temperature'],weatherdata['heatloss']):
            if (temp >= (point - 0.5)) & (temp < point + 0.5):
                hour_count = hour_count + 1
                load_sum = load_sum + hl
        hour_count = hour_count/5 # average over 5 years
        load_sum = load_sum/5
        hours1.append(hour_count)
        load1.append(load_sum)
    hours_dict1 = {
        'temp':temp_points,
        'hours': hours1,
        'load':load1}
    heatload_dist_temp = pd.DataFrame(hours_dict1)

    # create dataframe for plotting heat load distribution histogram
    bin_midpoints = np.arange(-29.5,balance_point,1)
    hours = []
    load = []
    for mid_point in bin_midpoints:
        hour_count = 0
        load_sum = 0
        for temp,hl in zip(weatherdata['temperature'],weatherdata['heatloss']):
            if (temp >= (mid_point - 0.5)) & (temp < mid_point + 0.5):
                hour_count = hour_count + 1
                load_sum = load_sum + hl
        hour_count = hour_count/5 # average over 5 years
        load_sum = load_sum/5
        hours.append(hour_count)
        load.append(load_sum)
    hours_dict = {
        'temp':bin_midpoints,
        'hours': hours,
        'load':load}
    heatload_dist = pd.DataFrame(hours_dict)
    # calculate heat load required in GJ
    # convert load from kBTU to GJ using a factor of 0.001055
    heatload_dist['GJ'] = heatload_dist.load*0.001055

    return [m, b, dtemp, heatloss_design, heatloss_annual, estimate_2021, heatload_dist, gasuse_annual, location_name, heatload_dist_temp]