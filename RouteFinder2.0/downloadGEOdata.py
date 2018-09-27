import requests, zipfile, io, os


def Download_Unzip_GEOs(state):
    '''
    INPUT:  (1) state FIPS code
            
    OUTPUT: String; path to block level GEO data 
    
    ** This function downloads and extracts data to the './data' directory
    '''
    
    # download zip file and extract to a local 'data' folder
    url = 'https://www2.census.gov/geo/tiger/TIGER2017/TABBLOCK/' + 'tl_2017_{}_tabblock10.zip'.format(state)
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    new_path = 'LOCAL/blockGEOs_{}'.format(state)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    z.extractall(new_path)
    
    return new_path
    
if __name__ == "__main__":
    state = str(input('enter state FIPS code: '))
    Download_Unzip_GEOs(state) 
