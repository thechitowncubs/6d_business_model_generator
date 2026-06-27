import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# NEW: Imported the modernized, unified Google GenAI SDK
from google import genai

app = Flask(__name__)

# ==========================================
# SECURE CONFIGURATION
# ==========================================
# Injects your specific MariaDB/MySQL URI. 
# It checks the .env file first for security, and falls back to your hardcoded string if not found.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URI', 
    'mysql+pymysql://develop:utopia_management@localhost:3306/cube_management_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# NEW: Initialize the unified Gemini Client
# The client automatically detects the GEMINI_API_KEY from your .env file
client = genai.Client()

# ==========================================
# DATABASE MODELS (THE 6 SIDES OF THE CUBE)
# ==========================================

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    employee_id_str = db.Column(db.String(50), unique=True, nullable=False)
    
    compensation = db.relationship('CompensationMatrix', backref='employee', lazy=True)
    operations = db.relationship('OperationsInfrastructure', backref='employee', lazy=True)
    products = db.relationship('ProductRouting', backref='employee', lazy=True)
    risks = db.relationship('RiskCompliance', backref='employee', lazy=True)
    kpis = db.relationship('ExecutiveKPI', backref='employee', lazy=True)

class CompensationMatrix(db.Model):
    __tablename__ = 'compensation_matrix'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    contract_year = db.Column(db.Integer, nullable=False)
    btc_amount = db.Column(db.Float, default=0.0)
    gold_ounces = db.Column(db.Float, default=0.0)
    silver_ounces = db.Column(db.Float, default=0.0)
    fiat_amount = db.Column(db.Float, default=0.0)
    fiat_ticker = db.Column(db.String(10), default='USD')
    job_description = db.Column(db.Text, nullable=True)

class TreasuryAllocation(db.Model):
    __tablename__ = 'treasury_allocation'
    id = db.Column(db.Integer, primary_key=True)
    contract_year = db.Column(db.Integer, nullable=False)
    target_currency = db.Column(db.String(20), nullable=False)
    liquidity_source = db.Column(db.String(100), nullable=True)
    hedging_strategy = db.Column(db.Text, nullable=True)

class OperationsInfrastructure(db.Model):
    __tablename__ = 'operations_infrastructure'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    hardware_tier = db.Column(db.String(50))
    os_environment = db.Column(db.String(50))
    infrastructure_access = db.Column(db.String(100))
    annual_ops_budget = db.Column(db.Float, default=0.0)

class ProductRouting(db.Model):
    __tablename__ = 'product_routing'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    contract_year = db.Column(db.Integer, nullable=False)
    primary_project = db.Column(db.String(100))
    core_deliverable = db.Column(db.Text)
    phase = db.Column(db.String(50))

class RiskCompliance(db.Model):
    __tablename__ = 'risk_compliance'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    risk_category = db.Column(db.String(100))
    threat_level = db.Column(db.String(20))
    mitigation_protocol = db.Column(db.Text)

class ExecutiveKPI(db.Model):
    __tablename__ = 'executive_kpis'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    contract_year = db.Column(db.Integer, nullable=False)
    q1_metric = db.Column(db.String(200))
    q2_metric = db.Column(db.String(200))
    q3_metric = db.Column(db.String(200))
    q4_metric = db.Column(db.String(200))

# ==========================================
# CORE ROUTING & LOGIC
# ==========================================

def get_or_create_employee(emp_id_val):
    """Ensures relational integrity. Creates an employee ID root if it doesn't exist yet."""
    emp_id_str = str(emp_id_val).strip()
    employee = Employee.query.filter_by(employee_id_str=emp_id_str).first()
    if not employee:
        employee = Employee(employee_id_str=emp_id_str)
        db.session.add(employee)
        db.session.commit()
    return employee

@app.route('/')
def dashboard():
    """Loads the dashboard and fetches all 6 sides of the database for the top UI viewer."""
    employees = Employee.query.all()
    treasuries = TreasuryAllocation.query.all()
    operations = OperationsInfrastructure.query.all()
    products = ProductRouting.query.all()
    risks = RiskCompliance.query.all()
    kpis = ExecutiveKPI.query.all()
    
    return render_template('dashboard.html', 
                           employees=employees, 
                           treasuries=treasuries,
                           operations=operations,
                           products=products,
                           risks=risks,
                           kpis=kpis)

# --- FORM SUBMISSION ROUTES (THE 6 SIDES) ---

@app.route('/add_side1_data', methods=['POST'])
def add_side1_data():
    emp = get_or_create_employee(request.form.get('employee_id'))
    row = CompensationMatrix(
        employee_id=emp.id,
        contract_year=int(request.form.get('contract_year') or 2026),
        btc_amount=float(request.form.get('btc_amount') or 0.0),
        gold_ounces=float(request.form.get('gold_ounces') or 0.0),
        silver_ounces=float(request.form.get('silver_ounces') or 0.0),
        fiat_amount=float(request.form.get('fiat_amount') or 0.0),
        fiat_ticker=request.form.get('fiat_ticker', 'USD'),
        job_description=request.form.get('job_description', '')
    )
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_side2_data', methods=['POST'])
def add_side2_data():
    row = TreasuryAllocation(
        contract_year=int(request.form.get('contract_year') or 2026),
        target_currency=request.form.get('target_currency', ''),
        liquidity_source=request.form.get('liquidity_source', ''),
        hedging_strategy=request.form.get('hedging_strategy', '')
    )
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_side3_data', methods=['POST'])
def add_side3_data():
    emp = get_or_create_employee(request.form.get('employee_id'))
    row = OperationsInfrastructure(
        employee_id=emp.id,
        hardware_tier=request.form.get('hardware_tier', ''),
        os_environment=request.form.get('os_environment', ''),
        infrastructure_access=request.form.get('infrastructure_access', ''),
        annual_ops_budget=float(request.form.get('annual_ops_budget') or 0.0)
    )
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_side4_data', methods=['POST'])
def add_side4_data():
    emp = get_or_create_employee(request.form.get('employee_id'))
    row = ProductRouting(
        employee_id=emp.id,
        contract_year=int(request.form.get('contract_year') or 2026),
        primary_project=request.form.get('primary_project', ''),
        core_deliverable=request.form.get('core_deliverable', ''),
        phase=request.form.get('phase', '')
    )
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_side5_data', methods=['POST'])
def add_side5_data():
    emp = get_or_create_employee(request.form.get('employee_id'))
    row = RiskCompliance(
        employee_id=emp.id,
        risk_category=request.form.get('risk_category', ''),
        threat_level=request.form.get('threat_level', ''),
        mitigation_protocol=request.form.get('mitigation_protocol', '')
    )
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_side6_data', methods=['POST'])
def add_side6_data():
    emp = get_or_create_employee(request.form.get('employee_id'))
    row = ExecutiveKPI(
        employee_id=emp.id,
        contract_year=int(request.form.get('contract_year') or 2026),
        q1_metric=request.form.get('q1_metric', ''),
        q2_metric=request.form.get('q2_metric', ''),
        q3_metric=request.form.get('q3_metric', ''),
        q4_metric=request.form.get('q4_metric', '')
    )
    db.session.add(row)
    db.session.commit()
    return redirect(url_for('dashboard'))

# --- AI SYNTHESIS ENGINE ---
#

@app.route('/generate_plan', methods=['GET'])
def generate_plan():
    """Queries relational tables, logs user telemetry, and passes metadata to the header."""

    # Calculate row counts across your data dimensions
    side1_count = CompensationMatrix.query.count()
    side2_count = TreasuryAllocation.query.count()
    side3_count = OperationsInfrastructure.query.count()
    side4_count = ProductRouting.query.count()
    side5_count = RiskCompliance.query.count()
    side6_count = ExecutiveKPI.query.count()

    total_records = side1_count + side2_count + side3_count + side4_count + side5_count + side6_count

    # Telemetry Tracking: Log who is executing your code securely on the server side
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    log_entry = ApplicationAuditLog(
        user_ip=user_ip,
        action_performed="Executed AI Strategic Synthesis",
        records_synthesized=total_records
    )
    db.session.add(log_entry)
    db.session.commit()

    def format_table(model, headers):
        records = model.query.all()
        if not records:
            return "[No data entered for this dimension yet.]\n"
        output = "\t".join(headers) + "\n"
        for r in records:
            row = [str(getattr(r, h.lower(), '') or '') for h in headers]
            output += "\t".join(row) + "\n"
        return output

    # Build prompt string contexts
    side1_txt = format_table(CompensationMatrix, ['Contract_Year', 'BTC_Amount', 'Fiat_Amount', 'Job_Description'])
    # (Keep your remaining side_txt formatting blocks here...)

    prompt = f"Synthesize a complete corporate business plan using these metrics:\n{side1_txt}" # (truncated for brevity)

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        plan_content = response.text
    except Exception as e:
        plan_content = f"Error generating plan: {str(e)}"

    # Package metadata payload for the header template
    meta_header = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_records": total_records,
        "environment": "Production (Secure API Gateway)",
        "build_version": "2.1.0"
    }


    ### SIDE 1: COMPENSATION MATRIX
    {side1_txt}

    ### SIDE 2: TREASURY ECONOMIC FUNDING
    {side2_txt}

    ### SIDE 3: OPERATIONS & PROVISIONING
    {side3_txt}

    ### SIDE 4: PRODUCT ROUTING ROADMAP
    {side4_txt}

    ### SIDE 5: RISK MANAGEMENT PROFILES
    {side5_txt}

    ### SIDE 6: STRATEGIC PERFORMANCE KPIS
    {side6_txt}

    Generate a detailed, highly structured narrative breaking down executive strategies, resource burn models across hard assets vs fiat currency setups, operational logistics allocations, and project execution phases.
    """

    try:
        # NEW: Using the updated client.models SDK syntax
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        plan_content = response.text
    except Exception as e:
        plan_content = f"Error generating plan: {str(e)}"
    
    return render_template('result.html', plan_content=plan_content, meta=meta_header)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
