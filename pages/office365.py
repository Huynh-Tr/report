# Useful libraries
import pandas as pd
import streamlit as st
from office365.sharepoint.files.file import File
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
import io
import time

# Page setup
st.set_page_config(layout = 'wide')

# SharePoint and Folder urls
sharepoint_url = r'https://pnjcomvn.sharepoint.com/sites/HuynhTN'
folder_in_sharepoint = r"/sites/HuynhTN/Shared Documents/Project/streamlit/Dthu/parquet_files"

# First section: e-mail and password as input
placeholder = st.empty()
with placeholder.container():
  col1, col2, col3 = st.columns(3)
  with col2:
    st.markdown("## **SharePoint connection with Streamlit**")
    st.markdown("--------------")
    email_user = st.text_input("Your e-mail")
    password_user = st.text_input("Your password", type="password")

    # Save the button status
    Button = st.button("Connect")
    if st.session_state.get('button') != True:
      st.session_state['button'] = Button

# starttime
start = time.time()

# email_user = r"huynh.th@pnj.com.vn"
# password_user = r"Android!123"
# Authentication and connection to SharePoint
def authentication(email_user, password_user, sharepoint_url) :
  auth = AuthenticationContext(sharepoint_url) 
  auth.acquire_token_for_user(email_user, password_user)
  ctx = ClientContext(sharepoint_url, auth)
  web = ctx.web
  ctx.load(web)
  ctx.execute_query()
  return ctx

# Second section: display results
# Check if the button "Connect" has been clicked
if st.session_state['button'] :  
  try :                            
    placeholder.empty()
    if "ctx" not in st.session_state :
      st.session_state["ctx"] = authentication(email_user, 
                                                password_user,
                                                sharepoint_url)
    
    st.write("Authentication: successfull!")
    st.write("Connected to SharePoint: **{}**".format( st.session_state["ctx"].web.properties['Title']))
  
# Connection to the SharePoint folder
target_folder = st.session_state["ctx"].web.get_folder_by_server_relative_url(folder_in_sharepoint)
    
# Read and load items
items = target_folder.files
st.session_state["ctx"].load(items)
st.session_state["ctx"].execute_query()    

# Save some information for each file using item.properties
info = {}
for item in items:
    info[item.properties["Name"]] = item.properties["ServerRelativeUrl"]

    abs_url = [sharepoint_url + url for url in relative_url]
    abs_url = [url.replace(" ", "%20") for url in abs_url]
    
    df = pd.read_csv(abs_url[0], encoding = "utf-8", sep = ",")

    # Create and display the final data frame
    Index = ["File name", "Last modified", "Relative url"]
    dataframe = pd.DataFrame([names, last_mod, relative_url], index = Index).T
    st.write("")
    st.write("")
    st.write("These are the files in the folder:")
    st.table(dataframe)
  
  # Handle the error in the authentication section
  except :
    col1, col2, col3 = st.columns(3)
    with col2:
      st.write("**Authentication error: reload the page**")

# # select the file to display
# st.write("Select the file to display:")
# file_name = st.multiselect("File name", info.keys())
# file_name = [info[k] for k in file_name]

# data = []
# for file in file_name:
#   # read the file content and concatenate the data
#   response_reports = File.open_binary(st.session_state["ctx"], file)
#   bytes_file_obj_reports = io.BytesIO()                    # Save data to BytesIO stream
#   bytes_file_obj_reports.write(response_reports.content)
#   bytes_file_obj_reports.seek(0)                           # Set file object to start
#   File_content = data.append(pd.read_parquet(bytes_file_obj_reports))     # Save content in a pandas dataframe

# df = pd.concat(data)
# # df = df.sum()

# st.write(df)
# # endtime
# end = time.time()
# # convert run time from end - start to minutes and seconds
# run_time = time.gmtime(end - start)
# st.write("Run time: ", time.strftime("%M:%S", run_time))

# # Read the file content
# response_reports = File.open_binary(st.session_state["ctx"], path_to_the_file)
# bytes_file_obj_reports = io.BytesIO()                    # Save data to BytesIO stream                            
# bytes_file_obj_reports.write(response_reports.content)
# bytes_file_obj_reports.seek(0)                           # Set file object to start
# File_content = pd.read_csv(bytes_file_obj_reports)     # Save content in a pandas dataframe

# # Display the dataframe
# st.write("This is your file:")
# st.table(File_content)