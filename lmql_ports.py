import lmql
import pandas as pd

@lmql.query(model=lmql.model("llama.cpp:/local/llama-2-70b.Q5_K_M.gguf", endpoint="172.17.0.1:8080")) #use served model
def extract_date(question):
    '''lmql
    "You are given this context: {question}" 
    "The month that the context took place in is: [MONTH]" where MONTH in ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    "The day the context took place in is: [DAY]" where DAY in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    return MONTH,DAY
    '''

text = "#Guatemala #eruption  #climate #destruction #anomaly #Fuego\n🇬🇹 Fuego one of the most active volcanoes in Central America, is one of the three major stratovolcanoes towering above the former Guatemalan capital, Antigua. Typically, Strombolian activity is observed here, and sometimes phases of intense lava flow, creating high ash plumes and dangerous pyroclastic flows. As of today, October 10, 2023, explosive activity continues. The Volcanic Ash Advisory Center (VAAC) in Washington has warned of a volcanic ash plume that has risen to an altitude of approximately 16,000 feet (4,900 meters) at 13:51 UTC.\n\nFollow us on social media:\nInstagram - shorturl.at/fkpZ9\nFacebook - shorturl.at/guBH2\nCreative Society - www.creativesociety.com"

print(extract_date(text))

