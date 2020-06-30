from flask import Flask, request, redirect, url_for, render_template
from flask_mail import Mail, Message
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MAIL_DEFAULT_SENDER"] = "flask@mineworldmc.net"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'VO+!iPkjL.RqG0P_46E&'
app.config['MYSQL_DB'] = 'web'

mail = Mail(app)
mysql = MySQL(app)

def build_form_msg_body(formdata):
	bodytext = "A form has been received, containing the following data:\n\n"
	for fieldname, value in formdata.items():
		bodytext+=fieldname + ": " + value + "\n"

	bodytext += "\n\nIf this message har reached you in error, please send a message to postmaster@mineworldmc.net"

	return bodytext

@app.route("/")
def test():
	return render_template("demo.html")

@app.route("/other")
def other_page():
	return "WTF!"
#	return render_template("demo2.html")

@app.route("/store_form_data", methods=['POST'])
def store_form_data():
	form_data = request.form.to_dict(flat=True)
	origin = request.referrer
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO formData(origin, submitTime, formData) VALUES (%s, NOW(), %s)", (origin, form_data))
	mysql.connection.commit()
	cur.close()

	return redirect(url_for("form_received"))


@app.route("/send_adminmail", methods=['POST'])
def send_webform_mail():
	msg = Message(f'Mail from webform at {request.referrer}')
	msg.recipients = ['support@mineworldmc.net']
	msg.body = build_form_msg_body(request.form)
	mail.send(msg)
	return redirect(url_for("form_received"))

@app.route("/form_received")
def form_received():
	return "We have recieved your request and will look at it when we feel like it"

if __name__ == "__main__":
	app.run()
