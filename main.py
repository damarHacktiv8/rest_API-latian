# import packages
from fastapi import FastAPI, HTTPException,Header
from pydantic import BaseModel
import pandas as pd

# create FastAPI object
app = FastAPI() 
# create api key
password = "kopiluwak"

class Profile(BaseModel):
    '''
    Profile class - used for making request body
    '''
    name: str
    location: str

# endopoint> mengatur aplikasi untuk mendapatkan data dari server

@app.get('/')
def getHome():
    '''
    endpoint 1 - home page
    '''

    return {
        "msg": "Hello world"
    }


@app.get('/profiles')
def getProfiles():
    '''
    endpoint 2 - get all profiles
    '''

    # membaca isi datasource
    df = pd.read_csv('dataset.csv')

    return{
        "data": df.to_dict(orient=  'records')
    }


@app.get('/profiles/{id}')
def getProfile(id: int):
    '''
    endpoint 3 - get profile by id
    '''

    # membaca isi datasource
    df = pd.read_csv('dataset.csv')

    # filter data sesuai id 
    result = df.query(f"id == {id}")
    # ketika result kosong -> pesan error 
     
    if len(result) ==0:
        # tampilkan error 
        raise HTTPException(status_code=404, detail="data not found!")
    
    # ketika result tidak kosong -> Data
    return{
        "data": result.to_dict(orient=  'records')
    }


@app.delete('/profiles/{id}')
def deleteProfile(id: int, api_key:str = Header()):
    '''
    endpoint 4 - delete profile by id
    '''
    # cek password
    if (api_key== None)or (api_key != password):
        # raise error
        raise HTTPException(status_code=401, detail= "unauthorize data!")
    
    # membaca isi datasource
    df = pd.read_csv('dataset.csv')

    # filter - exclude id yang bersangkutan
    result = df[df.id != id]

    # replace dataset dangan yang Bersangkutan
    result.to_csv('dataset.csv', index=False)
    return{
        "data": result.to_dict(orient=  'records')
    }



@app.put('/profiles/{id}')
def updateProfile(id: int, profile: Profile):
    '''
    endpoint 5 - update profile by id
    '''

    # complete this endpoint
    pass


@app.post('/profiles/')
def createProfile(profile: Profile):
    '''
    endpoint 6 - create new profile
    
    '''

    # membaca isi datasource
    df = pd.read_csv('dataset.csv')
    # buat databaru
    NewDf = pd.DataFrame({
        "id": [len(df) + 1],
        "name": [profile.name],
        "location": [profile.location]
    })
    # concat- gabung 2 dataframe yang berbeda menjadi 1
    df= pd.concat([df,NewDf])

    df.to_csv('dataset.csv', index=False)

    return{
        "msg": "data has created succesfully"
    }
