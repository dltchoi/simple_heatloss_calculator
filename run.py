from traceback import format_list
from flask import Flask, request, render_template, make_response
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from random import randint
import os, glob
from calculator import heatloss_estimate as hl_estimate

app = Flask(__name__)
port = int(os.environ.get('PORT',5000))

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/methodology")
def methodology():
    return render_template('methodology.html')

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/calculator")
def calculator():
    return render_template('calculator.html')

@app.route("/calculator_output", methods=["GET","POST"])
def calculator_output():
    for filename in glob.glob("static/heatloss*"): #removes any files in the directory beginning with example
        os.remove(filename)
    for filename in glob.glob("static/heatenergy*"):
        os.remove(filename)
    for filename in glob.glob("static/customheatenergy*"): 
        os.remove(filename)
    for filename in glob.glob("static/heatdist*"): 
        os.remove(filename)

    #Colour
    step_blue = "#00a3af"
    step_gold = "#f8a81d"
    
    # get user inputs
    if request.method=='POST':
        gasuse_total = float(request.form.get('gasuse_total'))
        dhw_monthly = float(request.form.get('dhw_monthly'))
        balance_point = float(request.form.get('balance_point'))
        furnace_eff = float(request.form.get('furnace_eff'))
        derate = float(request.form.get('derate'))
        location = request.form.get('location')

    # calculate heat loss with defined function
        result = hl_estimate(gasuse_total, dhw_monthly, balance_point, furnace_eff, derate, location) #, heatpumpsize, heatpumpcap_17_c1, heatpumpcap_47_c1, heatpumpcap_17_c2, heatpumpcap_47_c2, heatpumpcap_17_c3, heatpumpcap_47_c3, hp_derate, derate_c1, derate_c2, derate_c3)
                    
        m = result[0]
        b = result[1]
        dtemp = result[2]
        heatloss_design = result[3]
        heatloss_annual = result[4]
        estimate_2021 = result[5]
        heatload_dist = result[6]
        gasuse_annual = result[7]
        location_name = result[8]
        heatload_dist_temp = result[9]


        # create plots of results
        x = np.linspace(-30,balance_point,20)
        y = m*x+b

        # building load plot
        fig,ax = plt.subplots(figsize=(10,7))
        ax.plot(x,y,color='red', linewidth=2.5, label='Heat loss')

        # calculate total annual heating load for 2021
        GJ_total = heatload_dist.GJ.sum()
        kbtu_total = heatload_dist.load.sum()

        # zip together heat pump parameters to display on output page
        #ziplist = zip(switchtemp_list,hp_size,hp_frac_list,ehp_frac_list,hybrid_costs,elec_costs,size_name)

        ax.set_ylim(0)
        ax.set_title('Estimated Heat Loss', fontsize=20)
        ax.set_xlabel('Outdoor Temperature [\N{DEGREE SIGN}C]', fontsize=17)
        ax.set_ylabel('Heat Loss [kBTU/hr]', fontsize=20)
        #ax.legend(framealpha=0.2, fontsize=18,loc='lower center', bbox_to_anchor=(0.5,-0.48))
        fig.tight_layout()
        ax.grid(which='major')
        ax.grid(which='minor',linestyle=':', linewidth=0.5)
        ax.minorticks_on()
        value = str(randint(0, 100000))
        heatloss_url=f'static/heatloss{value}.png'
        plt.savefig(heatloss_url,transparent=True)
        plt.close()

        # create histogram plot of outdoor temperature and annual heating required
        fig4,ax4 = plt.subplots(figsize=(10,7))
        ax4.bar(heatload_dist.loc[heatload_dist.temp < balance_point].temp,(heatload_dist.loc[heatload_dist.temp < balance_point].load/kbtu_total)*100, color = step_blue)
        ax4.grid()
        ax4.set_title('Average Annual Heating Load Distribution (2017 - 2023)', fontsize=19)
        ax4.set_ylabel('Fraction of Annual Heating Required (%)', fontsize=17)
        ax4.set_xlabel('Outdoor Temperature [\N{DEGREE SIGN}C]', fontsize=17)
        fig4.tight_layout()
        value = str(randint(0, 100000))
        heatdist_url=f'static/heatdist{value}.png'
        plt.savefig(heatdist_url,transparent=True)
        plt.close()

        # create plot of fraction of total annual heating above outdoor temperatures
        fig5,ax5 = plt.subplots(figsize=(10,7))
        ax5.plot(heatload_dist_temp.loc[heatload_dist_temp.temp < balance_point].temp,(100-(heatload_dist_temp.loc[heatload_dist_temp.temp < balance_point].hours/heatload_dist_temp.hours.sum())*100))
        ax5.grid()
        ax5.set_title('Fraction of Total Annual Heating Above an Outdoor Temperature', fontsize=19)
        ax5.set_ylabel('Percentage of Total Annual Heating', fontsize=17)
        ax5.set_xlabel('Outdoor Temperature [\N{DEGREE SIGN}C]', fontsize=17)
        fig5.tight_layout()
        value = str(randint(0, 100000))
        heatdist_temp_url=f'static/heatdist_temp{value}.png'
        plt.savefig(heatdist_temp_url,transparent=True)
        plt.close()

    return render_template('calculator_output.html', heatloss_url=heatloss_url, heatdist_url=heatdist_url, heatdist_temp_url=heatdist_temp_url, dtemp=dtemp, heatloss_design=round(heatloss_design), gasuse_total=int(gasuse_total), dhw_annual=int(dhw_monthly*12), balance_point=int(balance_point), furnace_eff=furnace_eff, gasuse_annual=round(gasuse_annual), location_name=location_name, derate=round(derate))#, size_name=size_name, derate_c1=derate_c1, derate_c2=derate_c2, derate_c3=derate_c3) #,  hp_derate=round(hp_derate),heatpumpsize=heatpumpsize #, switchlist=switchtemp_list, curve1=curve1, curve2=curve2, curve3=curve3, curve1_result=curve1_result, curve2_result=curve2_result, curve3_result=curve3_result, scop=scop, base_cost=round(base_cost), hybrid_costs=hybrid_costs, elec_costs=elec_costs, ziplist=ziplist,)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)