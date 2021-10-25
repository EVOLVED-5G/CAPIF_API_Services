import requests
import re
import pandas as pd

def get_spirent_tests_ids_from_response(response):
    ids=[]
    for item in response["runningTests"]:
        ids.append(item.get('id'))
    return ids


def retrieve_remote_file(url):
    if url.find('/'):
        filename=url.rsplit('/', 1)[1]
    output='/opt/robot-tests/results/' + filename
    print(output)

    r = requests.get(url, allow_redirects=True)
    open(output, 'wb').write(r.content)
    return output

def retrieve_all_remote_files(test_info):
    output_filenames=[]
    urls=test_info.get('resultFilesList')
    for url in urls:
        output_filenames.append(retrieve_remote_file(url))
    return output_filenames

def get_xml_filename(filenames):

    for filename in filenames:
        if '.xls' in filename:
            return filename

    raise Exception("No xml file found")


def get_parameter_value_from_excel(filename, table, parameter):
    df = pd.read_excel(filename, sheet_name=table, header=0)
    
    last_parameter_value=df.tail(1)[parameter].to_numpy()[0]
    return last_parameter_value

def get_rate_between_parameters_from_excel(filename, table, parameter1, parameter2):
    parameter1_value=get_parameter_value_from_excel(filename, table, parameter1)
    parameter2_value=get_parameter_value_from_excel(filename, table, parameter2)
    if parameter2_value == 0:
        raise Exception("Is not possible to calculate rate, because parameter (" + parameter2 + ") is 0")

    return parameter1_value/parameter2_value

def check_rate_between_parameters_from_excel(filename, table, parameter1, parameter2, threshold):
    rate=get_rate_between_parameters_from_excel(filename, table, parameter1, parameter2)

    if float(rate) > float(threshold):
        print("\"" + parameter1 + "\"/\"" + parameter2 + "\" Rate (" + str(rate) + ") is over threshold (" + threshold + ")")
        return rate
    else:
        raise Exception("\"" + parameter1 + "\"/\"" + parameter2 + "\" Rate (" + str(rate) + ") is under threshold (" + threshold + ")")

def check_value_between_parameters_from_excel(filename, table, parameter1, parameter2=None, value=None):
    parameter1_value=get_parameter_value_from_excel(filename, table, parameter1)
    parameter2_value=None
    if parameter2 != None:
        parameter2_value=get_parameter_value_from_excel(filename, table, parameter2)
    elif value != None:
        parameter2_value=float(value)
    else:
        raise Exception("ERROR: There is not a value to compare with")
    
    if parameter1_value == parameter2_value:
        print(parameter1 + " is equal to " + str(parameter2_value))
        return True
    else:
        raise Exception("\"" + parameter1 + "\" with value " + str(parameter1_value) + " not match with value " + (parameter2_value))

def get_ts_from_response(response, tsname):
    tservers = response.json().get('testServers')
    for ts in tservers:
        if ts.get('name') == tsname:
            return ts
    raise Exception("TS with name " + tsname + " is not present at TAS server")


def merge_configurations(test_session, new_test_session_conf, name=None, delay=None, overrides=None):
    parameters_allowed=list(test_session.get('tsGroups')[0].get('testCases')[0].get('parameters').keys())
    print("Parameters allowed")
    print(parameters_allowed)
    parameters=new_test_session_conf.get('tsGroups')[0].get('testCases')[0].get('parameters')
    present_parameters=list(parameters.keys())
    for present_parameter in present_parameters:
        if present_parameter not in parameters_allowed:
            print("Deleting " + present_parameter + " from environment because is not needed")
            del parameters[present_parameter]

    if name != None:
        print("Name of session overrided to: " + name)
        new_test_session_conf["name"]=name

    if delay != None:
        print("Duration of session overrided to " + delay)
        steps = new_test_session_conf.get('steps')
        for step in steps:
            if step.get('tcActivity') == "Stop":
                step["delaySec"]=delay
                break
    
    if overrides != None:
        print('Under development')

    return new_test_session_conf
