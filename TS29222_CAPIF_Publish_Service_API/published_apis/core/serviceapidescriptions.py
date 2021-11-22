import pymongo
import secrets
from flask import current_app, Flask, Response
import json
from ..encoder import JSONEncoder
from ..models.problem_details import ProblemDetails



## Variables that will be used for all the methods


##  Method 1:
def add_serviceapidescription(apf_id, body):
    
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']

    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)
    mydb = myclient[db]
    mycol = mydb[col]
    user_registry = mydb[jwt]

    apf_res = user_registry.find({'_id': apf_id})

    if apf_res.count() == 0:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="APF not existing",
                              cause="APF id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')
    else:
        res = mycol.find({'api_name': body.api_name})
        if res.count() != 0:
            myclient.close()
            prob = ProblemDetails(title="Forbidden", status=403, detail="Service already published",
                                  cause="Identical API name")
            return Response(json.dumps(prob, cls=JSONEncoder), status=403, mimetype='application/json')
        else:
            api_id = secrets.token_hex(15)
            body.api_id = api_id
            rec = dict()
            rec['apf_id'] = apf_id
            rec.update(body.to_dict())
            mycol.insert_one(rec)
            myclient.close()
            res = Response(json.dumps(body, cls=JSONEncoder), status=201, mimetype='application/json')
            res.headers['Location'] = "http://localhost:8080/published-apis/v1/" + str(apf_id) + "/service-apis/" + str(api_id)
            return res



##  Method 1: GET all Service ID from an APF id -- WIP
def get_serviceapidescription(apf_id):
    
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']   


    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)

    mydb = myclient[db]
    mycol = mydb[col]
    user_registry = mydb[jwt]


    apf_res = user_registry.find({'_id': apf_id})

    

    print(apf_res)

    if apf_res.count() == 0:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="APF not existing",
                              cause="APF id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')
    
    else:


        ##TODO: Here, I have to deal with any exception that can happen

        ## now return the response with al the services ID

        myQuery = {'apf_id': apf_id}
        serviceapidescription = mycol.find(myQuery, {'_id': False})

        result= []

        ## loop in order to get thorugh all  services
        for post in serviceapidescription:
            result.append(post)

        ## Def = str in order to convert to string all those object that are not serializable by JSON
        res = Response(json.dumps(result, indent=2, default=str), status=201, mimetype='application/json')
        
        return res



##  Method 2: GET Specific Service ID
def getServiceId_serviceapidescription(service_api_id,apf_id):

    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']   


    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)

    mydb = myclient[db]
    mycol = mydb[col]
    user_registry = mydb[jwt]


    apf_res = user_registry.find({'_id': apf_id})



    if apf_res.count() == 0:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="APF not existing",
                              cause="APF id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')
    
    else:

        ##TODO: Here, I have to deal with any exception that can happen
        ## now return the response with al the services ID


        myQuery = {'apf_id': apf_id, 'api_id': service_api_id}
        serviceapidescription = mycol.find_one(myQuery, {'_id': False})


        if (serviceapidescription == None):
            myclient.close()
            return "Please provide an existing Netapp ID", 404

        else:
            myclient.close()
            res = Response(json.dumps(serviceapidescription, default=str,cls=JSONEncoder), status=201, mimetype='application/json')
            return res




def update_serviceapidescription(service_api_id,apf_id, service_api_description):

    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']   


    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)

    mydb = myclient[db]
    mycol = mydb[col]
    user_registry = mydb[jwt]


    apf_res = user_registry.find({'_id': apf_id})



    if apf_res.count() == 0:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="APF not existing",
                                cause="APF id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    else:

        ##TODO: Here, I have to deal with any exception that can happen
        ## now return the response with al the services ID


        myQuery = {'apf_id': apf_id, 'api_id': service_api_id}
        serviceapidescription = mycol.find_one(myQuery)


        if (serviceapidescription == None):
            myclient.close()
            return "Please provide an existing service api ID", 404

        else:
            print(serviceapidescription)
            print("ahora con la nueva")
            print(service_api_description)
            mycol.replace_one(serviceapidescription, service_api_description.to_dict())
            myclient.close()
            res = Response(json.dumps(serviceapidescription, default=str,cls=JSONEncoder), status=201, mimetype='application/json')
            return res


def delete_serviceapidescription(service_api_id,apf_id):
    
    user = current_app.config['MONGODB_SETTINGS']['user']
    password = current_app.config['MONGODB_SETTINGS']['password']
    db = current_app.config['MONGODB_SETTINGS']['db']
    col = current_app.config['MONGODB_SETTINGS']['col']
    jwt = current_app.config['MONGODB_SETTINGS']['jwt']
    host = current_app.config['MONGODB_SETTINGS']['host']
    port = current_app.config['MONGODB_SETTINGS']['port']   


    uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)

    myclient = pymongo.MongoClient(uri)

    mydb = myclient[db]
    mycol = mydb[col]
    user_registry = mydb[jwt]

    apf_res = user_registry.find({'_id': apf_id})


    if apf_res.count() == 0:
        myclient.close()
        prob = ProblemDetails(title="Unauthorized", status=401, detail="APF not existing",
                                cause="APF id not found")
        return Response(json.dumps(prob, cls=JSONEncoder), status=401, mimetype='application/json')

    else:

        ##TODO: Here, I have to deal with any exception that can happen
        ## now return the response with al the services ID


        myQuery = {'apf_id': apf_id, 'api_id': service_api_id}
        serviceapidescription = mycol.find_one(myQuery)

        if (serviceapidescription == None):
            return "Please provide an existing service api ID", 404
        else:
            mycol.delete_one(myQuery)
            return Response(json.dumps(serviceapidescription, default=str, cls=JSONEncoder), status=204, mimetype='application/json')
                    


