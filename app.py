from flask import Flask, request, jsonify, render_template
import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator, DataStructs
import openpyxl

# Load and prepare the dataset
file_path = 'cross_reactivity_analysis.xlsx'
data = pd.read_excel(file_path, 'Sheet1')
cross_reactivity_data = data[['Drug1', 'Drug2', 'Cross_Reactivity_Label', 'SMILES_Drug1_x', 'SMILES_Drug2_x']]

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # The HTML page you provided

@app.route('/check_cross_reactivity', methods=['POST'])
def check_cross_reactivity():
    # Get data from the POST request
    drug1 = request.json.get('drug1')
    drug2 = request.json.get('drug2')

    # Find the relevant data entry
    filtered_data = cross_reactivity_data[(cross_reactivity_data['Drug1'] == drug1) & (cross_reactivity_data['Drug2'] == drug2)]

    if filtered_data.empty:
        return jsonify({'message': 'No data available for the selected drugs.', 'label': 'warning'})

    cross_reactivity_label = filtered_data.iloc[0]['Cross_Reactivity_Label']
    response = {}

    # Determine response message based on cross-reactivity label
    if cross_reactivity_label == 0:
        response['message'] = '<2% chance of cross-reactivity expected.'
        response['label'] = 'success'
    elif cross_reactivity_label == 1:
        response['message'] = '⚠️ 20-40% chance of cross-reactivity. Consider another agent or utilizing a test dose.'
        response['label'] = 'danger'
    elif cross_reactivity_label == 2:
        response['message'] = 'Possible cross-reactivity. Use with caution.'
        response['label'] = 'warning'
    else:
        response['message'] = 'Unknown cross-reactivity label. Please verify the data.'
        response['label'] = 'danger'

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
