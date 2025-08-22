from flask import Flask, render_template, request, send_file
from pathlib import Path
from datetime import date, datetime
import tempfile, zipfile, io
from generator import list_templates, generate_docs

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')

def get_policies_meta():
    mapping = {
        'access_control.j2': ('Access Control', 'Least privilege, joiners/movers/leavers, access reviews.'),
        'incident_response.j2': ('Incident Response', 'Triage, containment, comms, RCA and lessons learned.'),
        'change_management.j2': ('Change Management', 'Peer review, approvals, rollback plans, logging.'),
        'vendor_management.j2': ('Vendor Management', 'Due diligence, DPAs/SCCs, annual reviews.'),
        'data_retention_disposal.j2': ('Data Retention & Disposal', 'Retention durations and secure disposal.'),
        'encryption.j2': ('Encryption', 'At rest and in transit requirements, KMS usage.'),
        'backup_recovery.j2': ('Backup & Recovery', 'Backup cadence and disaster recovery objectives.'),
        'bcp_dr.j2': ('BCP / DR', 'Business continuity planning and disaster recovery.'),
        'logging_monitoring.j2': ('Logging & Monitoring', 'Events, centralization, alerting, runbooks.'),
        'acceptable_use.j2': ('Acceptable Use', 'User responsibilities and prohibited activities.'),
    }
    result = []
    for p in list_templates():
        title, desc = mapping.get(p.name, (p.stem.replace('_',' ').title(), ''))
        result.append({'file': p.name, 'title': title, 'description': desc})
    return sorted(result, key=lambda x: x['title'])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', policies=get_policies_meta(), year=date.today().year)

@app.route('/generate', methods=['POST'])
def generate():
    company = {
        'name': request.form.get('company_name','Your Company'),
        'industry': request.form.get('industry','SaaS'),
        'hosting_model': request.form.get('hosting_model','cloud'),
        'remote_policy': request.form.get('remote_policy','remote-first'),
        'timezone': request.form.get('timezone','UTC')
    }
    retention = {'years': int(request.form.get('retention_years', '7'))}
    controls = {
        'access_review_frequency': request.form.get('access_review_frequency','quarterly'),
        'backup_frequency': request.form.get('backup_frequency','daily'),
        'vendor_review_cadence': request.form.get('vendor_review_cadence','annually'),
        'encryption_at_rest': request.form.get('encryption_at_rest','AES-256'),
        'encryption_in_transit': request.form.get('encryption_in_transit','TLS 1.2+')
    }

    context = {
        'company': company,
        'retention': retention,
        'controls': controls,
        'today': date.today().isoformat()
    }

    selected = request.form.getlist('selected')

    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    export_dir = Path('exports') / ts
    output_dir = Path(__file__).parent / export_dir
    generate_docs(output_dir, selected, context)

    # Zip the folder into memory
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for p in output_dir.glob('*.docx'):
            zf.write(p, arcname=p.name)
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name=f"policies-{ts}.zip", mimetype='application/zip')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)