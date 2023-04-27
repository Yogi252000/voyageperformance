
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials


st.set_page_config(page_title='VESSEL PERFORMANCE REPORT', layout="wide", page_icon='🚢')

st.write("<h1 style='text-align: left;'>VESSEL PERFORMANCE REPORT</h1>", unsafe_allow_html=True)



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
worksheet = client.open("Vessel Performance").worksheet("Sheet1")


name = st.selectbox('Vessel Name' ,('GCL YAMUNA','GCL NARMADA','GCL GANGA','GCL MAHANADI','GCL TAPI','GCL SABARMATI','BUNUN KALON','VINAYAK','AM TARANG'
    'DAIWAN KALON','AMIS WISDOM II','AMIS ELEGANCE','NALUHU','AMIS FORTUNE','AMIS WISDOM III','BUNUN QUEEN','AM KIRTI','TRUE CARTIER','AMIS WISDOM I','DAIWAN INFINITY'
      ,'DAIWAN HERO','AMIS KALON','BUNUN WISDOM','AM UMANG','AMIS BRAVE','AMIS LEADER','FRONTIER BONANZA','CORECOEAN OL','BUNUN XCEL',
           'BLUE HORIZON','AMIS ACE','ETERNITY SW','SAKIZAYA RESPECT','AMIS NATURE','AMIS INTEGRITY','AMIS JUSTICE' ))
laden = st.selectbox('Laden/Ballast', ('Laden', 'Ballast'))
voyage = st.text_input("Voyage Number")
date = st.date_input("UTC Date (Departure)")
date_str = date.strftime("%Y-%m-%d")
time = st.time_input("UTC Time (Departure)")
time_str = time.strftime('%H:%M:%S')
port = st.text_input("Departure Port Name")
date1 = st.date_input("UTC Date (Arrival)")
date1_str = date1.strftime("%Y-%m-%d")
time1 = st.time_input("UTC Time (Arrival)")
time1_str = time1.strftime('%H:%M:%S')
port1 = st.text_input("Arrival Port Name")
draft = st.text_input("Draft(Forward)")
aft = st.text_input("Draft(Aftward)")
dis = st.text_input("Displacement")
cargo = st.text_input("Total cargo loaded onboard")
time_elapsed = st.text_input("Time Elapsed from Last Report")
instructed_speed = st.text_input("Instructed Speed ")
wind_force = st.selectbox("Wind Force",(0,1,2,3,4,5,6,7,8,9,10))
actual_wind_direction = st.selectbox('Actual Wind Direction', ('E', 'N', 'S', 'W', 'NE', 'SE', 'SW', 'NW'))
relative_wind_direction = st.selectbox('Relative Wind Direction', ('Starboard Tail', 'Port Quarter', 'Head', 'Port Beam', 'Port Tail', 'Tail', 'Starboard Beam', 'Starboard Quarter'))
state_of_sea = st.selectbox("State of Sea",(0,1,2,3,4,5))
current_speed = st.text_input("Current Speed (Knots)")
current_direction = st.selectbox('Current Direction', ('Starboard Tail', 'Port Quarter', 'Head', 'Port Beam', 'Port Tail', 'Tail', 'Starboard Beam', 'Starboard Quarter'))
main_engine_rpm = st.text_input("Main Engine RPM")
average_slip = st.text_input("Slip(%)")
average_main_engine_power = st.text_input(" Main Engine Power in KW")
additional = st.text_input("Additional AE Running Hour")
total_generator_power = st.text_input("Total Generator Power (KW)")
total_generator_running_hour = st.text_input("Total Generator Running Hour")
distance = st.text_input("Distance Travelled (NM)")
fresh_water_production = st.text_input("Fresh water Production in MT")
ballast_exchange = st.selectbox('Any AE Running Attributed To Ballast Exchange / Deck Wash/Maneuvering etc', ('NA', 'Ballast Exchange', 'Manoeuvring', 'Deck Wash', 'Maintenance', 'Other Reasons'))
vessel_remarks = st.text_area("Vessel Remarks")


if st.button('Save Data'):
        worksheet.append_row([name,laden,voyage,date_str,time_str,port,date1_str,time1_str,port1,draft,aft,dis,cargo,
                               time_elapsed, instructed_speed, wind_force, actual_wind_direction, relative_wind_direction,
                              state_of_sea, current_speed, current_direction,main_engine_rpm, average_slip, average_main_engine_power,
                              total_generator_power, total_generator_running_hour,distance, fresh_water_production,
                              ballast_exchange, vessel_remarks])

        # Notify the user that the data has been stored
        st.success("Data saved")


should = st.selectbox('Instructed speed by Charter party',('Vessel Instructed to go in ECO Speed', 'Vessel Instructed to go in FULL Speed'))

if should == 'Vessel Instructed to go in ECO Speed':
    should1 = st.selectbox('Laden/Ballast', ('LADEN', 'BALLAST'))


    if should1 == 'LADEN':
        st.write("CHARTER PARTY ECO SPEED- LADEN ")
        eco_laden = st.number_input("Charter Party Eco Speed - Laden : ")
        me_laden = st.number_input("Charter Party Main Engine Consumption - ECO Speed (Laden)")
        aux_laden = st.number_input("Charter Party Auxiliary Engine Consumption - ECO Speed (Laden) ")
        total = me_laden + aux_laden
        st.write("Charter Party Total Con (ME + AE) :")
        st.write(total)

        st.write("ACTUAL SPEED & FO CONSUMPTION")

        actual_speed = st.number_input("Actual Vessel Speed : ")
        vessel_con = st.number_input("Actual Total FO Consumption (ME+AE): ")

        if actual_speed <= eco_laden:

            st.success("Vessel Speed meets CP Requirement")
        else:
            st.error("Vessel Speed exceeds CP Requirement")

        if vessel_con <= total:

            st.success("FO Consumption meets CP Requirement")

        else:
            st.error("FO Consumption exceeds CP Requirement")

        if actual_speed <= eco_laden and vessel_con <= total:
            st.success("Speed and FO Con meets the Charter Party requirements.")
            submit = st.button("Submit data")
            if submit:
                worksheet.append_row([total, actual_speed, vessel_con])
                st.success("Data submitted \U0001F44D")
            else:
                st.warning("Data not submitted.")
        else:
            st.error("The vessel does not meet the Charter Party requirements.")
            reason2 = st.text_input("Reason for not meeting the CP Requirement:")
            if reason2:
                confirmed = st.checkbox("Are you sure you want to submit the data? click ")
                if confirmed:
                    with st.spinner(f"Data Saving...."):
                        worksheet.append_row([total, actual_speed, vessel_con, reason2])

                else:
                    st.warning("Data not submitted.")
            else:
                st.warning("Please provide a reason for not meeting the CP Requirement.")



    elif should1 == 'BALLAST':

        st.write("CHARTER PARTY ECO SPEED - BALLAST")
        eco_ballast = st.number_input("Charter Party Eco Speed - ballast : ")
        me_eco = st.number_input("Charter Party Main Engine Consumption - ECO Speed (Ballast) ")
        aux_eco = st.number_input("Charter Party Auxiliary Engine Consumption - ECO Speed (Ballast) ")
        total1 = me_eco + aux_eco
        st.write("Charter Party Total Con (ME + AE) :")
        st.write(total1)

        st.write("ACTUAL SPEED & FO CONSUMPTION")

        actual_speed1 = st.number_input("Actual Vessel Speed : ")
        vessel_con1 = st.number_input("Actual Total FO Consumption (ME+AE): ")

        if actual_speed1 <= eco_ballast:

            st.success("Vessel Speed meets CP Requirement")
        else:
            st.error("Vessel Speed exceeds CP Requirement")

        if vessel_con1 <= total1:

            st.success("FO Consumption meets CP Requirement")

        else:
            st.error("FO Consumption exceeds CP Requirement")

        if actual_speed1 <= eco_ballast and vessel_con1 <= total1:
            st.success("Speed and FO Con meets the Charter Party requirements.")
            submit = st.button("Submit data")
            if submit:
                worksheet.append_row([total1, actual_speed1, vessel_con1])
                st.success("Data submitted \U0001F44D")
            else:
                st.warning("Data not submitted.")
        else:
            st.error("The vessel does not meet the Charter Party requirements.")
            reason2 = st.text_input("Reason for not meeting the CP Requirement:")
            if reason2:
                confirmed = st.checkbox("Are you sure you want to submit the data? click ")
                if confirmed:
                    with st.spinner(f"Data Saving...."):
                        worksheet.append_row([total1, actual_speed1, vessel_con1, reason2])

                else:
                    st.warning("Data not submitted.")
            else:
                st.warning("Please provide a reason for not meeting the CP Requirement.")


#FULL SPEED


elif should == 'Vessel Instructed to go in FULL Speed':
    should1 = st.selectbox('Laden/Ballast', ('LADEN', 'BALLAST'))

    if should1 == 'LADEN':

        st.write("CHARTER PARTY FULL SPEED - LADEN")
        full_laden = st.number_input("Charter Party Full Speed - Laden : ")
        me_full = st.number_input("Charter Party Main Engine Consumption - Full Speed (Laden)")
        aux_full = st.number_input("Charter Party Auxiliary Engine Consumption - Full Speed (Laden)")
        total2 = me_full + aux_full
        st.write("Charter Party Total Con (ME + AE) :")
        st.write(total2)

        st.write("ACTUAL SPEED & FO CONSUMPTION")

        actual_speed2 = st.number_input("Actual Vessel Speed : ")
        vessel_con2 = st.number_input("Actual Total FO Consumption (ME+AE): ")

        if actual_speed2 <= full_laden:

            st.success("Vessel Speed meets CP Requirement")
        else:
            st.error("Vessel Speed exceeds CP Requirement")


        if vessel_con2 <= total2:

            st.success("FO Consumption meets CP Requirement")

        else:
            st.error("FO Consumption exceeds CP Requirement")

        if actual_speed2 <= full_laden and vessel_con2<= total2:
            st.success("Speed and FO Con meets the Charter Party requirements.")
            submit = st.button("Submit data")
            if submit:
                worksheet.append_row([total2, actual_speed2, vessel_con2])
                st.success("Data submitted \U0001F44D")
            else:
                st.warning("Data not submitted.")
        else:
            st.error("The vessel does not meet the Charter Party requirements.")
            reason2 = st.text_input("Reason for not meeting the CP Requirement:")
            if reason2:
                confirmed = st.checkbox("Are you sure you want to submit the data? click ")
                if confirmed:
                    with st.spinner(f"Data Saving...."):
                        worksheet.append_row([total2, actual_speed2, vessel_con2, reason2])

                else:
                    st.warning("Data not submitted.")
            else:
                st.warning("Please provide a reason for not meeting the CP Requirement.")



    elif should1 == 'BALLAST':

        st.write("CHARTER PARTY FULL SPEED - BALLAST")
        full_ballast = st.number_input("Charter Party Full Speed - Ballast : ")
        me_ballast = st.number_input("Charter Party Main Engine Consumption - Full Speed (Ballast) ")
        aux_ballast = st.number_input("Charter Party Auxiliary Engine Consumption - Full Speed (Ballast) ")
        total3 = me_ballast + aux_ballast
        st.write("Charter Party Total Con (ME + AE) :")
        st.write(total3)

        st.write("ACTUAL SPEED & FO CONSUMPTION")

        actual_speed3 = st.number_input("Actual Vessel Speed : ")
        vessel_con3 = st.number_input("Actual Total FO Consumption (ME+AE): ")


        if actual_speed3 <= full_ballast:

            st.success("Vessel Speed meets CP Requirement")
        else:
            st.error("Vessel Speed exceeds CP Requirement")


        if vessel_con3 <= total3:

            st.success("FO Consumption meets CP Requirement")

        else:
            st.error("FO Consumption exceeds CP Requirement")

        if actual_speed3 <= full_ballast and vessel_con3 <= total3:
            st.success("Speed and FO Con meets the Charter Party requirements.")
            submit = st.button("Submit data")
            if submit:
                worksheet.append_row([total3, actual_speed3, vessel_con3])
                st.success("Data submitted \U0001F44D")
            else:
                st.warning("Data not submitted.")
        else:
            st.error("The vessel does not meet the Charter Party requirements.")
            reason3 = st.text_input("Reason for not meeting the CP Requirement:")
            if reason3:
                confirmed = st.checkbox("Are you sure you want to submit the data? click ")
                if confirmed:
                    with st.spinner(f"Data Saving...."):
                        worksheet.append_row([total3, actual_speed3, vessel_con3, reason3])

                else:
                    st.warning("Data not submitted.")
            else:
                st.warning("Please provide a reason for not meeting the CP Requirement.")





