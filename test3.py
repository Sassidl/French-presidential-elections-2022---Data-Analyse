import streamlit as st
import pandas as pd
import numpy as np
 
st.title('My app title is : Wonderful app')
st.write('Hello, *World!* :sunglasses:')
 
st.write('st.write accepts text, but also other data formats, such as numbers, data frames, styled data frames, and assorted objects, ...')
st.write(1234)
st.write(pd.DataFrame({
     'first column': [1, 2, 3, 4],
     'second column': [10, 20, 30, 40],
}))
 
data_frame = pd.DataFrame(np.random.randn(200, 3), columns=['a', 'b', 'c'])
st.write('st.write accepts also multiple arguments like ')
st.write('1 + 1 = ', 2)
st.write('Below is a DataFrame:', data_frame, 'Above is a dataframe.')
 
st.title('Displaying data elements with code snippets :')
#st.dataframe
code_1 = '''
    df = pd.DataFrame(
                np.random.randn(10, 20),
                columns=('col %d' % i for i in range(20)))
    st.dataframe(df.style.highlight_max(axis=0))
    '''
st.code(code_1, language='python')
df = pd.DataFrame(
            np.random.randn(10, 20),
            columns=('col %d' % i for i in range(20)))
 
st.dataframe(df.style.highlight_max(axis=0))
#st.metric
code_2 = '''
        st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
        '''
st.code(code_2, language='python')
st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
code_2 = '''
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", "70 °F", "1.2 °F")
        col2.metric("Wind", "9 mph", "-8%")
        col3.metric("Humidity", "86%", "4%")
        '''
st.code(code_2, language='python')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")
#st.json
code_3 = '''
        st.json({'foo': 'bar','baz': 'boz','stuff': [
            'stuff 1',
            'stuff 2',
            'stuff 3',
            'stuff 5',
            ],
        })
        '''
st.code(code_3, language='python')
st.json({
     'foo': 'bar',
     'baz': 'boz',
     'stuff': [
         'stuff 1',
         'stuff 2',
         'stuff 3',
         'stuff 5',
     ],
})