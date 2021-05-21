from email import message
from logging import exception
from pstats import Stats
from shutil import register_unpack_format

from flask import Flask,jsonify,request
import pymongo
import json
from werkzeug import Response
from bson.objectid import ObjectId
app=Flask(__name__)

try:
       
        mongo=pymongo.MongoClient(host="localhost",port=27017)        
        db=mongo.Customer      
        
except:
        
        print("error- can not connect with db")

@app.route("/users",methods=["POST"])
def create_users():
        
        try:
            data={
                "FirstName":request.form["Fname"],
                "LastName":request.form["Lname"]
                }
            #data={"Fname":"Python","Lname":"Flask"}
            db_inset=db.user.insert_one(data)
           
            return Response(
                response=json.dumps({"message":"User created","id":f"{db_inset.inserted_id}"}),
                status=200,
                mimetype="application/json"
            )
        except: 
            return Response(
                response=json.dumps({"message":"User not created"}),
                status=500,
                mimetype="application/json"
            )
      

@app.route("/getUser",methods=["GET"])
def get_users():
        
    try:    
            data=list(db.user.find())
            for u in data:
                u["_id"]=str(u["_id"])
            return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex: 
                return Response(
                response=json.dumps({"message":"User not found"}),
                status=500,
                mimetype="application/json"
            )


@app.route("/updateUser/<id>",methods=["PATCH"])
def update_User(id):
    print(id)
    try:    
            update=db.user.update_one(
                {"_id":ObjectId(id)},
                {"$set":{"FirstName":request.form["FirstName"]}
            })
            return Response(
            response=json.dumps({"message":"user update"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex: 
                return Response(
                response=json.dumps({"message":"User can not update"}),
                status=500,
                mimetype="application/json"
            )    

@app.route("/deleteUser/<id>",methods=["DELETE"])
def delete_User(id):
    
    try:    
            val=db.user.delete_one({"_id":ObjectId(id)})
            return Response(
            response=json.dumps({"message":"user deleted","id":f"{id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex: 
                return Response(
                response=json.dumps({"message":"User can not delete"}),
                status=500,
                mimetype="application/json"
            )  

app.run(debug=True)

