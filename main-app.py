from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
# need to install PIP for python to use 'requests' and other api calls

# US Census api url: sample
#url = 'http://api.census.gov/data/2021/pep/population?get=DENSITY_2021,POP_2021'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

# map each state name to its corresponding number in the table to access it
state_num_dict = {'Alabama': '01', 'Alaska': '02', 'Arizona': '04', 'Arkansas': '05', 'California': '06', 'Colorado': '08', 
                    'Connecticut': '09', 'Delaware': '10', 'Florida': '12', 'Georgia': '13', 'Hawaii': '15', 'Idaho': '16', 
                    'Illinois': '17', 'Indiana': '18', 'Iowa': '19', 'Kansas': '20', 'Kentucky': '21', 'Lousiana': '22', 
                    'Maine': '23', 'Maryland': '24', 'Massachusetts': '25', 'Michigan': '26', 'Minnesota': '27', 
                    'Mississippi': '28', 'Missouri': '29', 'Montana': '30', 'Nebraska': '31', 'Nevada': '32',
                    'New Hampshire': '33', 'New Jersey': '34', 'New Mexico': '35', 'New York': '36', 'North Carolina': '37',
                    'North Dakota': '38', 'Ohio': '39', 'Oklahoma': '40', 'Oregon': '41', 'Pennsylvania': '42', 'Rhode Island': '44',
                    'South Carolina': '45', 'South Dakota': '46', 'Tennessee': '47', 'Texas': '48', 'Utah': '49', 'Vermont': '50', 
                    'Virginia': '51', 'Washington': '53', 'West Virginia': '54',
                    'Wisconsin': '55', 'Wyoming': '56'  }


# get population of a state
def get_population(state) :
    print(state)
    #print(state_num_dict[state])
    number = state_num_dict[state]
    #number = '05'
    newurl = 'http://api.census.gov/data/2021/pep/population?get=NAME,POP_2021,DENSITY_2021&for=state:{}'
    result = requests.get(newurl.format(number, api_key))
    if result:
        print('good request')
        # print(result.content) <-- raw data
        # clean up data received from API call
        # make it easier to access by reformatting as json object
        json = result.json()
        print(json)
        return json
    else:
        print('bad request')
        return None

#get_population('Illinois') # test case

# python populations application app: python app with tkinter, calls api to display data

# set up display window
app = Tk();
app.title("City Populations App")
app.geometry('700x350')

# define search button function to find and display population data for a state
def searchCities() :
    pass
    state = stateinput_text.get()
    if state in state_num_dict:
        #population is a 2D list (json object) holding information returned about the state
        population = get_population(state)
        # output data
        state_label['text'] = population[1][0]
        population_label['text'] = population[1][1]
        density_label['text'] = population[1][2]

    else:
        messagebox.showerror('Error', 'cannot find state {}'.format(state))


# variables to take input for state name from user
stateinput_text = StringVar()
stateinput_entry = Entry(app, textvariable=stateinput_text)
stateinput_entry.pack()

# display search button 
search_button = Button(app, text='Search population', width=20, command=searchCities)
search_button.pack()

# display label before the state name
state_label = Label(app, text='State: ', font=('bold',20))
state_label.pack()

# display label before population of city
population_label = Label(app, text='Population: ', font=('bold', 20))
population_label.pack()

# display label before population density of city
density_label = Label(app, text='Population Density: ', font=('bold', 20))
density_label.pack()

app.mainloop()

