from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pandas as pd

app = Flask(__name__)


# Enable CORS for all domains on all routes
CORS(app)


# Load data initially to avoid reloading it on each request
df = pd.read_json('./PulpAndPaperJSON.json')


@app.route('/raw_data', methods=['GET'])
def get_raw_data():
    return jsonify(df.to_dict(orient='records'))

@app.route('/industries', methods=['GET'])
def get_industries():
    industries = df['Industry'].unique().tolist()
    return jsonify(industries)

@app.route('/equipment', methods=['GET'])
def get_equipment():
    industry = request.args.get('industry')
    if not industry:
        return jsonify({"error": "Missing 'industry' query parameter"}), 400

    df_filtered = df[df['Industry'] == industry]
    EquipmentData = []
    for _, row in df_filtered.iterrows():
        for item in row['Equipment']:
            if item not in EquipmentData:
                EquipmentData.append(item)
    return jsonify(EquipmentData)

@app.route('/component_parts', methods=['GET'])
def get_component_parts():
    industry = request.args.get('industry')
    equipment = request.args.get('equipment')
    if not industry or not equipment:
        return jsonify({"error": "Missing 'industry' or 'equipment' query parameter"}), 400

    df_filtered = df[df['Industry'] == industry]
    component_parts = df_filtered[df_filtered['Equipment'].apply(lambda x: equipment in x)]['Component Part'].unique().tolist()
    return jsonify(component_parts)

@app.route('/lube_details', methods=['GET'])
def get_lube_details():
    industry = request.args.get('industry')
    equipment = request.args.get('equipment')
    component_part = request.args.get('component_part')
    if not all([industry, equipment, component_part]):
        return jsonify({"error": "Missing query parameter(s)"}), 400

    df_filtered = df[(df['Industry'] == industry) & (df['Equipment'].apply(lambda x: equipment in x))]
    lube_spec = df_filtered[df_filtered['Component Part'] == component_part]['Lube Spec'].unique()[0].replace('\n', '  \n')
    lube_requirements = df_filtered[df_filtered['Component Part'] == component_part]['Lube Requirements'].unique()[0].replace('\n', '  \n')
    
    return jsonify({"Lube Specification": lube_spec, "Lube Requirements": lube_requirements})

@app.route('/products', methods=['GET'])
def get_products():
    industry = request.args.get('industry')
    equipment = request.args.get('equipment')
    component_part = request.args.get('component_part')
    if not all([industry, equipment, component_part]):
        return jsonify({"error": "Missing query parameter(s)"}), 400

    df_filtered = df[(df['Industry'] == industry) & (df['Equipment'].apply(lambda x: equipment in x))]
    product_info = df_filtered[df_filtered['Component Part'] == component_part][['Standard', 'Premium', 'Supreme']].drop_duplicates().to_dict(orient='records')
    return jsonify(product_info)

if __name__ == '__main__':
    app.run(debug=True)
