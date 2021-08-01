# CryptoPunks Script; Scrap, Clean & Upload Data to SQL
# ==============================================================================

# Dependencies 
# ==============================================================================

from numpy.matrixlib import defmatrix
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
from getpass import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# Contants
# ==============================================================================

url = "https://defypunk.com/punks"
npunks = 1 #10000

user =  getpass("Enter username: ")
password = getpass("Enter password: ")
DB ='criptopunks'

# Upload Database PUNKS
# ==============================================================================
def upload_SQL(df, table):
    try:
        conn = msql.connect(host='localhost', 
                           database=DB, user=user, 
                           password=password)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
        
            for i,row in df.iterrows():
                sql = 'INSERT INTO {DB}.{table} VALUES (%s,%s,%s,%s,%s)'
                cursor.execute(sql, tuple(row))
                print("Record inserted")
                # the connection is not autocommitted by default, so we 
                # must commit to save our changes
                conn.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)

# Upload Database TRANSACTIONS   *****Refactor & add to Upload PUNK
# ==============================================================================
def upload_SQL(df, table):
    try:
        conn = msql.connect(host='localhost', 
                           database=DB, user=user, 
                           password=password)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
        
            for i,row in df.iterrows():
                sql = 'INSERT INTO {DB}.{table} VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, tuple(row))
                print("Record inserted")
                # the connection is not autocommitted by default, so we 
                # must commit to save our changes
                conn.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
        
        
# Extract Punks
# ==============================================================================
def extract_Punks():

    df = pd.DataFrame(columns=['Number', 'Type', 'Skin', 'Traits', 'Rarity', 'Owner', 'Url'])
    table = 'PUNK'

    for i in range(npunks):

        url_scrap = url + '/' + str(i)
        driver.implicitly_wait(15)
        driver.get(url_scrap)

        # Extract Number, Type, Skin, Traits, Number Traits
        # ==============================================================================
        response = driver.find_elements_by_class_name('font-semibold')
        data = [i.text for i in response]    
        hidden = [i for i in data if 'Hidden' in i]
        data = [i for i in data if i not in hidden]
    
        # Extract Rarity
        # ==============================================================================
        response = driver.find_elements_by_class_name('font-bold')
        rarity = response[0].text.split()[0][:-2].replace(',','')

        # Extract Number Punk
        # ==============================================================================
        data[0] = data[0].split('#')[1]

        # Number Traits
        # ==============================================================================
        data[3] = data[3].split('(')[1].rstrip(')')

        # Traits
        # ==============================================================================
        data[4] = data[4:4+int(data[3])]
        data = data[:5]

        # Get owner
        # ==============================================================================
        response = driver.find_elements_by_class_name('mt-4')
        owner = [i.text for i in response]
        owner = '' if 'ERC721' in owner[1] else owner[1].split('(')[0].split()[-1]

        # Get HiddenTraits
        # ==============================================================================
        hidden = '' if len(hidden) == 0 else hidden

        # url
        # ==============================================================================
        url = url_scrap
    
        # Recopile Data to DataFrame
        # ==============================================================================
        data.append(rarity)
        data.append(hidden)
        data.append(owner)
        data.append(url)
    
        df.loc[len(df)] = data

        df_SQL = df[['Number','Type','Skin','Url','Rarity']]

        upload_SQL(df_SQL, table )
         
    return df


# Extract Transactions
# ==============================================================================
def extrac_Transactions():

    df = pd.DataFrame(columns=['Type','From', 'To','Amount','Transaction','Number', 'FromURL','ToURL','TxURL'])
    table = 'TRANSACTION'

    for i in range(npunks):
        
        df_transaction = pd.DataFrame(columns=['Type', 'From', 'To', 'Amount', 'Transaction'])
        
        url_scrap = url+'/'+str(i)
        driver.implicitly_wait(15)
        driver.get(url_scrap)  

        # Extract table
        # ==============================================================================
        response = driver.find_elements_by_tag_name('table')

        # Extract td's
        # ==============================================================================
        transaction = [i.text for i in response[0].find_elements_by_tag_name('td')]

        # Extract URL's
        # ==============================================================================
        
        urls =  [i.get_attribute("href") for i in response[0].find_elements_by_tag_name('a')]
        fromUrl = []
        toUrl = []
        txUrl = []
        fromlink = 'https://etherscan.io/address/'
        tolink='https://defypunk.com/punks/owners/'
        txlink ='https://etherscan.io/tx/'
        counter = 0

        for a in urls:
            counter +=1
            if counter  == 1 and fromlink in a:
                fromUrl.append(a)

            elif counter == 1 and tolink in a:
                fromUrl.append('')
                toUrl.append(a)

            elif counter == 1 and txlink in a:
                fromUrl.append('')
                toUrl.append('')
                txUrl.append(a)
                counter = 0

            elif counter == 2 and tolink in a:
                toUrl.append(a)

            elif counter == 2 and txlink in a:
                toUrl.append('')
                txUrl.append(a)
                counter = 0

            elif  counter == 3 and txlink in a:
                txUrl.append(a)        
                counter = 0 

              
        # Extract columns
        # ==============================================================================   
        length = len(transaction) // len(df_transaction.columns)
        
        for i in range(length):

            df_transaction.loc[len(df_transaction)] = transaction[0:5]
            
            transaction = transaction[5:]
        
        # Extract Punk Number
        # ==============================================================================
        response = driver.find_elements_by_class_name('font-semibold')

        data = [i.text for i in response]
        data = data[0].split('#')[1]
            

        # Recopile data to Dataframe
        # ==============================================================================
        dif = len(toUrl)-len(fromUrl) # Bug 1 or 2 more
        if dif != 0:
            toUrl = toUrl[:-dif]


        df['FromURL'] = fromUrl
        df['ToURL'] = toUrl
        df['TxURL'] = txUrl
        df['Number'] = data
        
        
        df = pd.concat([df, df_transaction], axis=0)

        # Clean Data *****refactor*****
        # ==============================================================================
        """df['transaction_id'] = df['Transaction'].str.split().apply(lambda x: x[-1])
        df['date'] = df['Transaction'].str.split().apply(lambda x: x[:-1])
        df['date'] = df['date'].apply(lambda x: str(x))
        df['date'] = df['date'].apply(lambda x: re.sub(r'[^\w\s]','',x))
        df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%b %d %Y'))
        df['Amount_ether'] = df['Amount_ether'].astype(str).str.replace('Ξ', '')
        df['Number'] = df['Number'].fillna(0)
        df['Amount_ether'] = df['Amount_ether'].fillna(0)
        df['Number'] = df['Number'].apply(lambda x:int(x))
        df = df.drop(['Transaction'], axis=1)
        index = []
        for n in range(1, len(df)+1):
            index.append(n)
        df['id']= index
        df = df.drop(['Transaction'], axis = 1, inplace = True)
        df['amount_usd'] =  df['Amount_ether'] """
        # Upload Database 
        # ==============================================================================
        
        df_SQL = df[['Number','Type','From','FromURL','To','ToURL','Amount_ether','Amount_usd','date','TransactNumber','TxURL']]

        upload_SQL(df_SQL, table )
     

    return df