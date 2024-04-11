import streamlit as st
import pandas as pd

# Read data from the CSV file
df = pd.read_csv('./combined.csv')

# Display the main header
st.write('# Petronas Lubricant Application')

# Display raw data
with st.expander('Raw Data'):
    st.write(df)

# Select Industry from dropdown
Industry = st.selectbox('Select Industry', df['Industry'].unique())

# filter by industry
df_filtered = df[df['Industry'] == Industry]

# Create a list to store unique equipment data
EquipmentData = []
for i in range(len(df_filtered)):
    if EquipmentData.count(df_filtered.iloc[i]['Equipment']) == 0:
        import ast        
        # convert to list
        items = ast.literal_eval(df_filtered.iloc[i]['Equipment'])        
        for item in items:
            if EquipmentData.count(item) == 0:
                EquipmentData.append(item)
                
        
        
              
          
        

 
# Select Equipment from dropdown
Equipment = st.selectbox('Select Equipment', EquipmentData)

# Filter DataFrame based on selected Industry
df_filtered = df[df['Industry'] == Industry]

# Select Component Part from dropdown
ComponentPart = st.selectbox('Select Component Part', df_filtered[df_filtered['Equipment'].apply(lambda x: Equipment in x)]['Component Part'].unique())

st.write('## Lube Specification')
st.write(df_filtered[df_filtered['Component Part'] == ComponentPart]['Lube Spec'].unique()[0].replace('\n', '  \n'))

st.write('## Lube Requirements')
st.markdown(df_filtered[df_filtered['Component Part'] == ComponentPart]['Lube Requirements'].unique()[0].replace('\n', '  \n'))


# Display Products section
st.write('# Products')

# Show Standard
st.write('## Standard')
st.write((df_filtered[df_filtered['Component Part'] == ComponentPart]['Standard']).unique()[0])

st.write('## Premium')
st.write(df_filtered[df_filtered['Component Part'] == ComponentPart]['Premium'].unique()[0])

st.write('## Supreme')
st.write(df_filtered[df_filtered['Component Part'] == ComponentPart]['Supreme'].unique()[0])


# Hide the Streamlit default footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
