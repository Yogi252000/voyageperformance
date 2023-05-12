
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread

st.set_page_config(page_title='VOYAGE PERFORMANCE REPORT', layout="wide", page_icon='🚢')

st.write("<h1 style='text-align: left;'>VOYAGE PERFORMANCE REPORT</h1>", unsafe_allow_html=True)



hide_st_style = """
         <style>
         footer {visibility : hidden;}
         </style>
         """

# Set up authentication

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
client = gspread.authorize(creds)

# Select the worksheet by name
worksheet = client.open("Vessel Performance").worksheet("Sheet42")

# User input
vessel_name = st.selectbox('Vessel Name', ('GCL Yamuna', 'GCL Mahanadi','GCL Ganga','GCL Sabarmati','GCL Narmada','GCL Tapi','AM Tarang','AM Kirti',
                                           'AM Umang','Vinayak','True Cartier','Bunun Wisdom','Amis Wisdom I','Amis Wisdom II','Amis Wisdom III',
                                           'Amis Kalon','Daiwan Kalon','Daiwan Infinity','Daiwan Hero','Bunun Queen','Amis Brave','Amis Leader',
                                           'Frontier Bonanza','Coreocean OL','Bunun xcel','Blue Horizon','Amis Ace','Eternity SW','Sakizaya Respect',
                                           'Amis Nature', 'Amis Integrity','Amis Justice','Naluhu','Bunun Kalon','Amis Fortune','Amis Elegance'))

laden_ballast = st.selectbox('Laden/Ballast', ('Laden', 'Ballast'))
voyage = st.text_input("Voyage Number")

st.subheader('Report Type')
report_type = st.selectbox('Select Report Type',('Commencement of Sea Passage to Noon', 'Noon to Noon','Noon to End of Sea Passage'))

if report_type == "Commencement of Sea Passage to Noon":
    date = st.date_input("UTC Date (COSP)")
    date_str = date.strftime("%Y-%m-%d")
    time = st.time_input("UTC Time (COSP)")
    time_str = time.strftime('%H:%M:%S')

    nd = st.date_input("Noon Date (UTC)")
    nd_str = nd.strftime("%Y-%m-%d")
    tg = st.time_input("Noon Time (UTC)")
    tg_str = time.strftime('%H:%M:%S')

    port = st.text_input("Departure Port Name")
    draft = st.text_input("Draft(Forward) (m)")
    aft = st.text_input("Draft(Aftward) (m)")
    dis = st.text_input("Displacement (Ton)")
    cargo = st.text_input("Total cargo loaded onboard (MT)")
    time_elapsed = st.text_input("Time Elapsed from Last Report")
    wind_force = st.selectbox("Wind Force", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    actual_wind_direction = st.selectbox('Actual Wind Direction', ('E', 'N', 'S', 'W', 'NE', 'SE', 'SW', 'NW'))
    relative_wind_direction = st.selectbox('Relative Wind Direction', (
    'Starboard Tail', 'Port Quarter', 'Head', 'Port Beam', 'Port Tail', 'Tail', 'Starboard Beam', 'Starboard Quarter'))
    state_of_sea = st.selectbox("State of Sea", (0, 1, 2, 3, 4, 5))
    current_speed = st.text_input("Current Speed (Knots)")
    current_direction = st.selectbox('Current Direction', (
    'Starboard Tail', 'Port Quarter', 'Head', 'Port Beam', 'Port Tail', 'Tail', 'Starboard Beam', 'Starboard Quarter'))
    main_engine_rpm = st.text_input("Main Engine RPM")
    average_slip = st.text_input("Slip(%)")
    average_main_engine_power = st.text_input(" Main Engine Power(KW)")
    total_generator_power = st.text_input("Total Generator Power (KW)")
    total_generator_running_hour = st.text_input("Total Generator Running Hour (Hrs)")
    distance = st.text_input("Distance Travelled (NM)")
    fresh_water_production = st.text_input("Fresh water Production (MT)")
    ballast_exchange = st.selectbox('Any AE Running Attributed To Ballast Exchange / Deck Wash/Maneuvering etc', (
    'NA', 'Ballast Exchange', 'Manoeuvring', 'Deck Wash', 'Maintenance', 'Other Reasons'))
    vessel_remarks = st.text_area("Vessel Remarks")

    st.subheader("SPEED & FO CONSUMPTION ")
    should = st.selectbox('Instructed speed by Charter party',
                          ('Vessel Instructed to go in ECO Speed', 'Vessel Instructed to go in FULL Speed'))

    speed_input = st.number_input("Enter the Charter Party Speed (Particular Voyage)")
    actual_speed = st.number_input("Actual Vessel Speed  ")

    if actual_speed >= speed_input:
        st.success("Vessel Speed meets CP Requirement")
    else:
        st.error("Vessel Speed not meeting  CP Requirement")
        reason = st.text_area("Reason for not meeting the CP Requirement")

    # Sheet name based on user input
    sheet_name = f"{vessel_name}"

    data = None
    try:
        # Open the specific sheet based on user input
        gc = gspread.authorize(creds)
        spreadsheet = gc.open('Vessel Performance')
        sheet = spreadsheet.worksheet(sheet_name)
        data = sheet.get_all_records()
    except gspread.exceptions.WorksheetNotFound:
        st.warning(f"No data found for {vessel_name} - {laden_ballast}.")

    # Find the corresponding row based on user input (assuming 'speed' is a column in the sheet)
    matching_row = None
    if data:
        for row in data:
            if laden_ballast == 'Laden' and row['LADEN SPEED'] == speed_input:
                matching_row = row
                break
            elif laden_ballast == 'Ballast' and row['BALLAST SPEED'] == speed_input:
                matching_row = row
                break

    # Pre-fill the input fields with the retrieved data

    total_VLSFO = 0
    if matching_row:
        if laden_ballast == 'Laden':
            full_laden = st.number_input("CHARTER PARTY SPEED ", value=matching_row['LADEN SPEED'], key='charter_speed',
                                         disabled=True)
            me_full = st.number_input("CHARTER PARTY ME FO CONS", value=matching_row['LADEN ME FO CONS'], key='me_cons',
                                      disabled=True)
            aux_full = st.number_input("CHARTER PARTY AE FO CONS", value=matching_row['LADEN AE FO CONS'],
                                       key='ae_cons', disabled=True)
            total_VLSFO = st.number_input(" CHARTER PARTY VLSFO CONS", value=matching_row['LADEN VLSFO CONS'],
                                          key='vlsfo_cons', disabled=True)
        elif laden_ballast == 'Ballast':
            full_laden = st.number_input("CHARTER PARTY SPEED ", value=matching_row['BALLAST SPEED'],
                                         key='charter_speed', disabled=True)
            me_full = st.number_input("CHARTER PARTY ME FO CONS ", value=matching_row['BALLAST ME FO CONS'],
                                      key='me_cons', disabled=True)
            aux_full = st.number_input("CHARTER PARTY AE FO CONS ", value=matching_row['BALLAST AE FO CONS'],
                                       key='ae_cons', disabled=True)
            total_VLSFO = st.number_input(" CHARTER PARTY VLSFO CONS", value=matching_row['BALLAST VLSFO CONS'],
                                          key='vlsfo_cons', disabled=True)

    else:
        st.warning("No data found for the provided speed.")

    vessel_con = st.number_input("Actual Total FO Consumption (ME+AE): ")

    if vessel_con <= total_VLSFO:

        st.success("FO Consumption meets CP Requirement")

    else:
        st.error("FO Consumption exceeds CP Requirement")
        reason2 = st.text_area("Reason for over consuming :")
        extra = vessel_con - total_VLSFO
        rounded_number = round(extra, 2)
        st.write(rounded_number, " MT FO Consumed Extra")

elif report_type == "Noon to Noon":
    last = st.date_input("Last noon Date (UTC)")
    last_str = last.strftime("%Y-%m-%d")
    t = st.time_input("Last noon Time (UTC)")
    t_str = t.strftime('%H:%M:%S')
    current = st.date_input("Current Noon Date (UTC)")
    current = current.strftime("%Y-%m-%d")
    time2 = st.time_input("Current Noon Time (UTC)")
    time2_str = time2.strftime('%H:%M:%S')
    time_elapsed = st.text_input("Time Elapsed from Last Report")
    wind_force = st.selectbox("Wind Force", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    actual_wind_direction = st.selectbox('Actual Wind Direction', ('E', 'N', 'S', 'W', 'NE', 'SE', 'SW', 'NW'))
    relative_wind_direction = st.selectbox('Relative Wind Direction', (
        'Starboard Tail', 'Port Quarter', 'Head', 'Port Beam', 'Port Tail', 'Tail', 'Starboard Beam',
        'Starboard Quarter'))
    state_of_sea = st.selectbox("State of Sea", (0, 1, 2, 3, 4, 5))
    current_speed = st.text_input("Current Speed (Knots)")
    current_direction = st.selectbox('Current Direction', (
        'Starboard Tail', 'Port Quarter', 'Head', 'Port Beam', 'Port Tail', 'Tail', 'Starboard Beam',
        'Starboard Quarter'))
    main_engine_rpm = st.text_input("Main Engine RPM")
    average_slip = st.text_input("Slip(%)")
    average_main_engine_power = st.text_input(" Main Engine Power(KW)")
    total_generator_power = st.text_input("Total Generator Power (KW)")
    total_generator_running_hour = st.text_input("Total Generator Running Hour (Hrs)")
    distance = st.text_input("Distance Travelled (NM)")
    fresh_water_production = st.text_input("Fresh water Production (MT)")
    ballast_exchange = st.selectbox('Any AE Running Attributed To Ballast Exchange / Deck Wash/Maneuvering etc', (
        'NA', 'Ballast Exchange', 'Manoeuvring', 'Deck Wash', 'Maintenance', 'Other Reasons'))
    vessel_remarks = st.text_area("Vessel Remarks")

    st.subheader("SPEED & FO CONSUMPTION ")
    should = st.selectbox('Instructed speed by Charter party',
                          ('Vessel Instructed to go in ECO Speed', 'Vessel Instructed to go in FULL Speed'))

    speed_input = st.number_input("Enter the Charter Party Speed (Particular Voyage)")
    actual_speed = st.number_input("Actual Vessel Speed  ")

    if actual_speed >= speed_input:
        st.success("Vessel Speed meets CP Requirement")
    else:
        st.error("Vessel Speed not meeting  CP Requirement")
        reason = st.text_area("Reason for not meeting the CP Requirement")

    # Sheet name based on user input
    sheet_name = f"{vessel_name}"

    data = None
    try:
        # Open the specific sheet based on user input
        gc = gspread.authorize(creds)
        spreadsheet = gc.open('Vessel Performance')
        sheet = spreadsheet.worksheet(sheet_name)
        data = sheet.get_all_records()
    except gspread.exceptions.WorksheetNotFound:
        st.warning(f"No data found for {vessel_name} - {laden_ballast}.")

    # Find the corresponding row based on user input (assuming 'speed' is a column in the sheet)
    matching_row = None
    if data:
        for row in data:
            if laden_ballast == 'Laden' and row['LADEN SPEED'] == speed_input:
                matching_row = row
                break
            elif laden_ballast == 'Ballast' and row['BALLAST SPEED'] == speed_input:
                matching_row = row
                break

    # Pre-fill the input fields with the retrieved data

    total_VLSFO = 0
    if matching_row:
        if laden_ballast == 'Laden':
            full_laden = st.number_input("CHARTER PARTY SPEED ", value=matching_row['LADEN SPEED'], key='charter_speed',
                                         disabled=True)
            me_full = st.number_input("CHARTER PARTY ME FO CONS", value=matching_row['LADEN ME FO CONS'], key='me_cons',
                                      disabled=True)
            aux_full = st.number_input("CHARTER PARTY AE FO CONS", value=matching_row['LADEN AE FO CONS'],
                                       key='ae_cons', disabled=True)
            total_VLSFO = st.number_input(" CHARTER PARTY VLSFO CONS", value=matching_row['LADEN VLSFO CONS'],
                                          key='vlsfo_cons', disabled=True)
        elif laden_ballast == 'Ballast':
            full_laden = st.number_input("CHARTER PARTY SPEED ", value=matching_row['BALLAST SPEED'],
                                         key='charter_speed', disabled=True)
            me_full = st.number_input("CHARTER PARTY ME FO CONS ", value=matching_row['BALLAST ME FO CONS'],
                                      key='me_cons', disabled=True)
            aux_full = st.number_input("CHARTER PARTY AE FO CONS ", value=matching_row['BALLAST AE FO CONS'],
                                       key='ae_cons', disabled=True)
            total_VLSFO = st.number_input(" CHARTER PARTY VLSFO CONS", value=matching_row['BALLAST VLSFO CONS'],
                                          key='vlsfo_cons', disabled=True)

    else:
        st.warning("No data found for the provided speed.")

    vessel_con = st.number_input("Actual Total FO Consumption (ME+AE): ")

    if vessel_con <= total_VLSFO:

        st.success("FO Consumption meets CP Requirement")

    else:
        st.error("FO Consumption exceeds CP Requirement")
        reason2 = st.text_area("Reason for over consuming :")
        extra = vessel_con - total_VLSFO
        rounded_number = round(extra, 2)
        st.write(rounded_number, " MT FO Consumed Extra")



elif report_type == "Noon to End of Sea Passage":
    noon = st.date_input("Last Noon Date(EOSP) ")
    noon_str = noon.strftime("%Y-%m-%d")
    g = st.time_input("Last Noon Time(EOSP)")
    g_str = g.strftime('%H:%M:%S')
    date1 = st.date_input("UTC Date (Arrival)")
    date1_str = date1.strftime("%Y-%m-%d")
    time1 = st.time_input("UTC Time (Arrival)")
    time1_str = time1.strftime('%H:%M:%S')
    port1 = st.text_input("Arrival Port Name")
    time_elapsed = st.text_input("Time Elapsed from Last Report")
    wind_force = st.selectbox("Wind Force", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    actual_wind_direction = st.selectbox('Actual Wind Direction', ('E', 'N', 'S', 'W', 'NE', 'SE', 'SW', 'NW'))
    relative_wind_direction = st.selectbox('Relative Wind Direction', (
        'Starboard Tail', 'Port Quarter', 'Head', 'Port Beam', 'Port Tail', 'Tail', 'Starboard Beam',
        'Starboard Quarter'))
    state_of_sea = st.selectbox("State of Sea", (0, 1, 2, 3, 4, 5))
    current_speed = st.text_input("Current Speed (Knots)")
    current_direction = st.selectbox('Current Direction', (
        'Starboard Tail', 'Port Quarter', 'Head', 'Port Beam', 'Port Tail', 'Tail', 'Starboard Beam',
        'Starboard Quarter'))
    main_engine_rpm = st.text_input("Main Engine RPM")
    average_slip = st.text_input("Slip(%)")
    average_main_engine_power = st.text_input(" Main Engine Power(KW)")
    total_generator_power = st.text_input("Total Generator Power (KW)")
    total_generator_running_hour = st.text_input("Total Generator Running Hour (Hrs)")
    distance = st.text_input("Distance Travelled (NM)")
    fresh_water_production = st.text_input("Fresh water Production (MT)")
    ballast_exchange = st.selectbox('Any AE Running Attributed To Ballast Exchange / Deck Wash/Maneuvering etc', (
        'NA', 'Ballast Exchange', 'Manoeuvring', 'Deck Wash', 'Maintenance', 'Other Reasons'))
    vessel_remarks = st.text_area("Vessel Remarks")

    st.subheader("SPEED & FO CONSUMPTION ")
    should = st.selectbox('Instructed speed by Charter party',
                          ('Vessel Instructed to go in ECO Speed', 'Vessel Instructed to go in FULL Speed'))

    speed_input = st.number_input("Enter the Charter Party Speed (Particular Voyage)")
    actual_speed = st.number_input("Actual Vessel Speed  ")

    if actual_speed >= speed_input:
        st.success("Vessel Speed meets CP Requirement")
    else:
        st.error("Vessel Speed not meeting  CP Requirement")
        reason = st.text_area("Reason for not meeting the CP Requirement")

    # Sheet name based on user input
    sheet_name = f"{vessel_name}"

    data = None
    try:
        # Open the specific sheet based on user input
        gc = gspread.authorize(creds)
        spreadsheet = gc.open('Vessel Performance')
        sheet = spreadsheet.worksheet(sheet_name)
        data = sheet.get_all_records()
    except gspread.exceptions.WorksheetNotFound:
        st.warning(f"No data found for {vessel_name} - {laden_ballast}.")

    # Find the corresponding row based on user input (assuming 'speed' is a column in the sheet)
    matching_row = None
    if data:
        for row in data:
            if laden_ballast == 'Laden' and row['LADEN SPEED'] == speed_input:
                matching_row = row
                break
            elif laden_ballast == 'Ballast' and row['BALLAST SPEED'] == speed_input:
                matching_row = row
                break

    # Pre-fill the input fields with the retrieved data

    total_VLSFO = 0
    if matching_row:
        if laden_ballast == 'Laden':
            full_laden = st.number_input("CHARTER PARTY SPEED ", value=matching_row['LADEN SPEED'], key='charter_speed',
                                         disabled=True)
            me_full = st.number_input("CHARTER PARTY ME FO CONS", value=matching_row['LADEN ME FO CONS'], key='me_cons',
                                      disabled=True)
            aux_full = st.number_input("CHARTER PARTY AE FO CONS", value=matching_row['LADEN AE FO CONS'],
                                       key='ae_cons', disabled=True)
            total_VLSFO = st.number_input(" CHARTER PARTY VLSFO CONS", value=matching_row['LADEN VLSFO CONS'],
                                          key='vlsfo_cons', disabled=True)
        elif laden_ballast == 'Ballast':
            full_laden = st.number_input("CHARTER PARTY SPEED ", value=matching_row['BALLAST SPEED'],
                                         key='charter_speed', disabled=True)
            me_full = st.number_input("CHARTER PARTY ME FO CONS ", value=matching_row['BALLAST ME FO CONS'],
                                      key='me_cons', disabled=True)
            aux_full = st.number_input("CHARTER PARTY AE FO CONS ", value=matching_row['BALLAST AE FO CONS'],
                                       key='ae_cons', disabled=True)
            total_VLSFO = st.number_input(" CHARTER PARTY VLSFO CONS", value=matching_row['BALLAST VLSFO CONS'],
                                          key='vlsfo_cons', disabled=True)

    else:
        st.warning("No data found for the provided speed.")

    vessel_con = st.number_input("Actual Total FO Consumption (ME+AE): ")

    if vessel_con <= total_VLSFO:

        st.success("FO Consumption meets CP Requirement")

    else:
        st.error("FO Consumption exceeds CP Requirement")
        reason2 = st.text_area("Reason for over consuming :")
        extra = vessel_con - total_VLSFO
        rounded_number = round(extra, 2)
        st.write(rounded_number, " MT FO Consumed Extra")





