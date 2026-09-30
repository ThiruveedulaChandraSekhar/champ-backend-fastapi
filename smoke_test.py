from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

health = client.get('/api/v1/health')
print('HEALTH', health.status_code, health.json())

safety_payload = {
    'medicineName': 'Amoxicillin',
    'activeIngredient': 'amoxicillin',
    'patientDrugAllergies': ['Penicillin'],
}
safety = client.post('/api/v1/safety/check', json=safety_payload)
print('SAFETY', safety.status_code, safety.json())

history_payload = {
    'patient': {'age': 35, 'gender': 'MALE'},
    'diagnoses': [{'name': 'Respiratory Infection', 'code': 'J06.9'}],
    'medicines': [{'name': 'Medicine A', 'active_ingredient': 'Ingredient A', 'duration': 5, 'outcome': 'EFFECTIVE'}],
    'allergies': [{'title': 'Penicillin Allergy', 'severity': 'HIGH'}],
    'visits': [{'diagnosis': 'Respiratory Infection', 'medicine': 'Medicine A', 'recovery_days': 5, 'outcome': 'RECOVERED'}],
}
history = client.post('/api/v1/history/summary', json=history_payload)
print('HISTORY', history.status_code, history.json())

train_medicine = {
    'records': [{
        'age': 35,
        'gender': 'MALE',
        'diagnosis': 'Respiratory Infection',
        'diagnosis_code': 'J06.9',
        'medicine': 'Medicine A',
        'active_ingredient': 'Ingredient A',
        'dosage': '500 mg',
        'duration': 5,
        'previous_recovery_days': 4,
        'previous_treatment_success': 1,
        'medicine_success': 1,
    }]
}
train_medicine_resp = client.post('/api/v1/admin/train/medicine-success', json=train_medicine)
print('TRAIN_MEDICINE', train_medicine_resp.status_code, train_medicine_resp.json())

train_recovery = {
    'records': [{
        'age': 35,
        'gender': 'MALE',
        'diagnosis': 'Respiratory Infection',
        'diagnosis_code': 'J06.9',
        'medicine': 'Medicine A',
        'active_ingredient': 'Ingredient A',
        'dosage': '500 mg',
        'duration': 5,
        'previous_recovery_days': 4,
        'previous_visit_count': 3,
        'previous_treatment_success': 1,
        'recovery_days': 5,
    }]
}
train_recovery_resp = client.post('/api/v1/admin/train/recovery', json=train_recovery)
print('TRAIN_RECOVERY', train_recovery_resp.status_code, train_recovery_resp.json())

print('DOCS', client.get('/docs').status_code)
