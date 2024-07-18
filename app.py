from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Define your SQLAlchemy models
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)

    def __init__(self, role_name):
        self.role_name = role_name
        
    def __repr__(self):
        return f'<Role {self.id}: {self.role_name}>'
    
class BaseDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver = db.Column(db.String(100), nullable=False)
    fuel_mode = db.Column(db.String(50))
    vehicle = db.Column(db.String(100))
    new_fuel_mode = db.Column(db.String(50))
    new_vehicle_no = db.Column(db.String(50))

    def __init__(self, driver, fuel_mode, vehicle, new_fuel_mode, new_vehicle_no):
        self.driver = driver
        self.fuel_mode = fuel_mode
        self.vehicle = vehicle
        self.new_fuel_mode = new_fuel_mode
        self.new_vehicle_no = new_vehicle_no

    def __repr__(self):
        return f'<BaseDetails {self.id}: Driver={self.driver}, Fuel Mode={self.fuel_mode}, Vehicle={self.vehicle}, New Fuel Mode={self.new_fuel_mode}, New Vehicle No={self.new_vehicle_no}>'

class RunningDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)   
    shift = db.Column(db.Integer)
    loading = db.Column(db.String(10))
    route = db.Column(db.String(50))
    start_time = db.Column(db.String(10))
    start_odo = db.Column(db.Integer)
    start_soc = db.Column(db.Integer)
    end_time = db.Column(db.String(10))
    end_odo = db.Column(db.Integer)
    end_soc = db.Column(db.Integer)
    total_km = db.Column(db.Integer)
    energy_consumption = db.Column(db.Float)
    range = db.Column(db.Float)

    def __init__(self, date, shift, loading, route, start_time, start_odo, start_soc,
                 end_time, end_odo, end_soc, total_km, energy_consumption, range):
        self.date = date
        self.shift = shift
        self.loading = loading
        self.route = route
        self.start_time = start_time
        self.start_odo = start_odo
        self.start_soc = start_soc
        self.end_time = end_time
        self.end_odo = end_odo
        self.end_soc = end_soc
        self.total_km = total_km
        self.energy_consumption = energy_consumption
        self.range = range

    def __repr__(self):
        return f'Date={self.date}, Shift={self.shift}, Loading={self.loading}, Route={self.route}, ' \
               f'Start Time={self.start_time}, Start Odo={self.start_odo}, Start SOC={self.start_soc}, ' \
               f'End Time={self.end_time}, End Odo={self.end_odo}, End SOC={self.end_soc}, ' \
               f'Total km={self.total_km}, Energy Consumption={self.energy_consumption}, Range={self.range}>'

# Routes and functions
@app.route('/', methods=['GET', 'POST'])
def role_selection():
    if request.method == 'POST':
        date = request.form.get('date')
        if date is not None:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        # Now date_obj is a Python date object
        else:
            # Handle the case where date is None (optional)
            date_obj = None  # Or any other default value you want to assign
        shift = request.form.get('shift')
        loading = request.form.get('loading')
        route = request.form.get('route')
        start_time = request.form.get('start_time')
        start_odo = request.form.get('start_odo')
        start_soc = request.form.get('start_soc')
        end_time = request.form.get('end_time')
        end_odo = request.form.get('end_odo')
        end_soc = request.form.get('end_soc')
        total_km = request.form.get('field_11')
        energy_consumption = request.form.get('field_12')
        range = request.form.get('field_13')

        running_details = RunningDetails(date=date_obj, shift=shift, loading=loading, route=route,
                                start_time=start_time, start_odo=start_odo, start_soc=start_soc,
                                end_time=end_time, end_odo=end_odo, end_soc=end_soc,
                                total_km=total_km, energy_consumption=energy_consumption, range=range)
        db.session.add(running_details)
        db.session.commit()
        return render_template('role_selection.html')
    return render_template('role_selection.html')

@app.route('/base-details', methods=['POST'])
def base_details():
    role_name = request.form.get('role')
    role = Role(role_name=role_name)
    db.session.add(role)
    db.session.commit()
    return render_template('base_details.html', role=role)

@app.route('/vehicle-running-details', methods=['POST'])
def vehicle_running_details():
    vehicle = request.form.get('vehicle')
    
    driver = request.form.get('driver')
    fuel_mode = request.form.get('fuel_mode')
    vehicle = request.form.get('vehicle')
    new_fuel_mode = request.form.get('new_fuel_mode')
    new_vehicle_no = request.form.get('new_vehicle_no')

    base_details = BaseDetails(driver=driver, fuel_mode=fuel_mode, vehicle=vehicle, new_fuel_mode=new_fuel_mode, new_vehicle_no=new_vehicle_no)
    db.session.add(base_details)
    
    return render_template('vehicle_running_details.html', vehicle=vehicle)

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
