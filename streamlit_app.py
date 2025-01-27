import streamlit as st

st.title('💸 Data Scientists Salaries 💸')

st.write('This is an app for data scientists salaries with analysis and a currency converter for USD to SEK')

st.sidebar.header('Input Options')

## Sidebar - Currency price unit
currency_list = ['SEK', 'USD']
base_price_unit = st.sidebar.selectbox('Select base currency for conversion', currency_list)
symbols_price_unit = st.sidebar.selectbox('Select target currency to convert to', currency_list)

 #Retrieving currency data from ratesapi.io
# https://api.ratesapi.io/api/latest?base=AUD&symbols=AUD
#@st.cache
#def load_data():
    #url = ''.join(['https://api.ratesapi.io/api/latest?base=', base_price_unit, '&symbols=', symbols_price_unit])
    #response = requests.get(url)
    #data = response.json()
    #base_currency = pd.Series( data['base'], name='base_currency')
    #rates_df = pd.DataFrame.from_dict( data['rates'].items() )
    #rates_df.columns = ['converted_currency', 'price']
    #conversion_date = pd.Series( data['date'], name='date' )
    #df = pd.concat( [base_currency, rates_df, conversion_date], axis=1 )
    #return df

#df = load_data()

#st.header('Currency conversion')

#st.write(df)

