from pathlib import Path
from src import generator

def test_templates_exist():
    tpls = generator.list_templates()
    assert len(tpls) >= 5

def test_generate(tmp_path):
    context = {
        'company': {'name':'TestCo','industry':'SaaS','hosting_model':'cloud','remote_policy':'remote-first','timezone':'UTC'},
        'retention': {'years': 7},
        'controls': {'access_review_frequency':'quarterly','backup_frequency':'daily','vendor_review_cadence':'annually','encryption_at_rest':'AES-256','encryption_in_transit':'TLS 1.2+'},
        'today': '2025-08-21'
    }
    out = generator.generate_docs(tmp_path, [], context)
    outputs = list(Path(out).glob('*.docx'))
    assert outputs and all(p.suffix=='.docx' for p in outputs)