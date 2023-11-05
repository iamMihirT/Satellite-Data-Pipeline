#TODO: look into pycountries for country code matching
import lmql
import torch
import pandas as pd
torch.cuda.empty_cache()    
# lmql serve-model llama.cpp:/local/llama-2-70b.Q5_K_M.gguf --cuda --n_ctx 4096 --temperature 0
@lmql.query(model="llama.cpp:/local/llama-2-70b.Q5_K_S.gguf") #use served model
def extract_date(question):
    '''lmql
    "You are given this context: {question}" 
    "The month that the context took place in is: [MONTH]" where MONTH in ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    "The day the context took place in is: [DAY]" where DAY in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    return MONTH,DAY
    '''
    
    
@lmql.query(model="llama.cpp:/local/llama-2-70b.Q5_K_S.gguf") #use served model
def extract_location(question):
    '''lmql
    "You are given this context: {question} \n" 
    "The location information in this context, structured as city,country is: [LOCATION]"\
    where REGEX(LOCATION, r"[A-Za-z]+,\s[A-Za-z]+") and len(LOCATION) < 30 
    return LOCATION
    '''


df = pd.read_json('telegram_data_n1000.json')
data = []
sample = 1
for index, row in df.iterrows():
   
    
    if sample == 250: 
        break
    text = row['message.text']
    date = row['message.date']
    media = row['file.location']
    
    location_info = ""
    date_info = ""
    event_info = ""
    if text != None:
        if len(text) > 15:
        
            location_info = extract_location(text)
            # location_info = "not extracted"
            date_info = extract_date(text)
            event_info = "not extracted"
            
        print(location_info,date_info,event_info)
        
        data.append([text, date, location_info, date_info, event_info, media])
        print(data)
        df = pd.DataFrame(data, columns=["message.text", "message.date", "extracted.location", "extracted.date", "extracted.event", "message.media"])
        df.to_json('telegram_data_n1000_augmented.json')
    sample += 1
    print(sample)
print(data)
df = pd.DataFrame(data, columns=["message.text", "message.date", "extracted.location", "extracted.date", "extracted.event", "message.media"])
df.to_json('telegram_data_n1000_augmented.json')
