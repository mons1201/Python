from flask import Flask,make_response,render_template,jsonify,request,session
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from datetime import datetime


app=Flask(__name__)

#database configuration
app.config['MONGODB_HOST']="mongodb+srv://mohan:mohan@cluster0.traigro.mongodb.net/Placement?retryWrites=true&w=majority"

# object document mapping config


mydb=MongoEngine()
mydb.init_app(app)
CORS(app)


class Jobs(mydb.Document):
    CompanyName=mydb.StringField()
    JobRole=mydb.StringField()
    Availablevacancy=mydb.IntField()
    SelectedCandidates=mydb.IntField()
    Qualification=mydb.StringField()
    ConductingDate=mydb.DateField()
    Salery=mydb.IntField()


@app.route("/Create",methods=['POST'])
def addNew():
    yes=request.json
    jobs=Jobs()
    jobs.CompanyName=yes['CompanyName']
    jobs.JobRole=yes['JobRole']
    jobs.Availablevacancy=yes['Availablevacancy']
    jobs.SelectedCandidates=yes['SelectedCandidates']
    jobs.Qualification=yes['Qualification']
    jobs.ConductingDate=yes['ConductingDate']
    jobs.Salery=yes['Salery']

    jobs.save()
    return jsonify(jobs)


#ERASE 
@app.route("/erase/<ComName>",methods=['DELETE'])
def deleting(ComName):
    check=Jobs.objects(CompanyName=ComName).first()
    check.delete()
    return jsonify(ComName+"Company has deleted")

@app.route("/",methods=['GET'])
def showall():
    return jsonify(Jobs.objects.all())

#Filter

@app.route("/Job/<jr>")
def getByJobRole(jr):
    return jsonify(Jobs.objects(JobRole=jr))

@app.route("/Sale/<rup>")
def getBySalery(rup):
    return jsonify(Jobs.objects(Salery=rup))


@app.route("/qual/<quali>")
def getByQualification(quali):
    return jsonify(Jobs.objects(Qualification=quali))

#update method
@app.route("/<ComName>",methods=['GET','PUT'])
def getByCompanyName(ComName):
    if request.method=="GET":
        one=Jobs.objects(CompanyName=ComName).first()
        return jsonify(one)
    else:
        yes=request.json
        Jobs.objects(CompanyName=ComName).update_one(set__JobRole=yes['JobRole'],set__Qualification=yes['Qualification'],set__SelectedCandidates=yes['SelectedCandidates'],set__ConductingDate=yes['ConductingDate'],set__Availablevacancy=yes['Availablevacancy'])
        return jsonify(Jobs.objects(CompanyName=ComName))

# @app.route("/fresh")
# def adding():
#     jobs=Jobs()
#     jobs.CompanyName="TCS"
#     jobs.JobRole="Senior Software Engg"
#     jobs.Availablevacancy=15
#     jobs.SelectedCandidates=2
#     jobs.Qualification="B.E-CSE"
#     jobs.ConductingDate=2022-10-10
#     jobs.Slaery=20000
    

#     jobs.save()
#     return jsonify(jobs)
    
    
if __name__=="__main__":
    app.run(debug=True,port=1122)

