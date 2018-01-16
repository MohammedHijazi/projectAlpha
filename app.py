from flask import Flask,request,render_template, redirect
import dataset


app = Flask(__name__)

db=dataset.connect("sqlite:///ordersData")


accounts=db["accounts"]
ordersDB=db["orders"]
Login = False
Ema = ""

@app.route("/",methods=["GET","POST"])
def login():
	global Ema
	global Login
	Ema = ""

	if(request.method=="POST"):
		email=request.form["email"]
		password=request.form["password"]
		e=accounts.find(email=email,password=password)
		check=len(list(e))
		if check != 0:
			Login= True
			Ema = email
			return redirect ('/orders') 
		else:
			Login= False
			return render_template("login.html", login=Login)
	else:
		Login= False
		return render_template("login.html", login=Login)



@app.route("/signup",methods=["POST","GET"])
def signup():
	global Login
	if(request.method=="POST"):
		name=request.form["name"]
		email=request.form["email"]
		password=request.form["password"]
		pconfirm=request.form["password-confirm"]
		echeck=accounts.find(email=email)
		echeck2=len(list(echeck))
		if password==pconfirm and echeck2==0:
			accounts.insert(dict(name=name,email=email,password=password))
			return redirect('/')
		else:
			return redirect('/signup')
	else:
		return render_template("signup.html", login=Login)


@app.route("/out",methods=["post","get"])
def signout():
	global Login
	global Ema
	Login=False
	Ema=""
	return redirect('/')


@app.route("/addOrder",methods=["post","get"])
def addOrder():
	global Login

	if(request.method=="POST"):
		email=request.form["email"]
		address=request.form["address"]
		#phone=request.form["phone"]
		order=request.form["order"]
		ordersDB.insert(dict(email=str(email),address=address,order=order))
		return redirect('/orders')
	else:
		if (Login == True):
			return render_template("addOrder.html", login=Login)
		else:
			return redirect('/')



@app.route("/orders", methods=["post","get"])
def orders():
	global Login
	if(request.method=="GET"):
		if (Login == True):
			return render_template("Orders.html", ordersList=getOrders(Ema), user=accounts.find_one(email=Ema), login=Login)
		else:
			return redirect('/')

def getOrders(OrderEmail):
	return list(ordersDB.find(email=OrderEmail))


if __name__ == "__main__":
	app.run()
