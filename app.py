import geopy
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from geopy.geocoders import Nominatim
import pandas
import datetime
import uuid
app=Flask(__name__)
geolocator = Nominatim(user_agent="Shesek")
db = SQLAlchemy(app)

geopy.geocoders.options.default_user_agent = "Yossi"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/success-table', methods=['POST'])
def success_table():
    global filename
    if request.method=="POST":
        file=request.files['file']
        try:
            df=pandas.read_csv(file)
            gc=Nominatim(scheme='http')
            df["coordinates"]=df["Address"].apply(gc.geocode)
            df['Latitude'] = df['coordinates'].apply(lambda x: x.latitude if x != None else None)
            df['Longitude'] = df['coordinates'].apply(lambda x: x.longitude if x != None else None)

            p=Point(id=uuid.uuid1,lon=df['Latitude'],lat=df['Longitude'])
            print(p)
            print(p.lat)
            print(p.lon)
            # print(geolocator.reverse(str(p.lat),str(p.lon)))


            print(df)

            filename=datetime.datetime.now().strftime("sample_files/%Y-%m-%d-%H-%M-%S-%f"+".csv")
            df.to_csv(filename,index=None)
            return render_template("index.html", text=df.to_html(), btn='download.html')
        except Exception as e:
            return render_template("index.html", text=str(e))

@app.route("/download-file/")
def download():
    return send_file(filename, attachment_filename='yourfile.csv', as_attachment=True)

class Point(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    lon = db.Column(db.String(80), unique=True, nullable=False)
    lat = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


if __name__=="__main__":
    app.run(debug=True,port=5002)
