from django.shortcuts import render
from django.http import HttpResponseRedirect
import numpy as np
import pandas as pd
from django.shortcuts import render, redirect
import os
from joblib import load
import random

def generate_random_data():
    ip_addresses = ['192.168.1.1', '10.0.0.1', '172.16.0.1', '203.0.113.0']
    transaction_types = ['Credit', 'Debit']
    times = ['2024-04-14 10:00:00', '2024-04-14 10:05:00', '2024-04-14 10:10:00']
    locations = ['Local', 'Foreign']

    ip_address = random.choice(ip_addresses)
    transaction_type = random.choice(transaction_types)
    time = random.choice(times)
    
    location = random.choice(locations)

    return {
        'ip_address': ip_address,
        'transaction_type': transaction_type,
        'time': time,
        'location': location
    }



def home(request):
    return render(request, 'index.html')


def result(request):
    if request.method == 'POST':
        csrf_token = request.POST.get('csrfmiddlewaretoken', '')


        try:
            num_packets = int(request.POST.get('d1', '0'))
            num_logs = int(request.POST.get('d2', '0'))
            num_transaction_duration = int(request.POST.get('d3', '1'))
            num_flows = int(request.POST.get('d4', '0'))
            is_new_device = bool(int(request.POST.get('d5', '1')))
        except (TypeError, ValueError) as e:
            # Handle the error, e.g., log it or send a message to the user
            pass

        
            # Create a dictionary with user inputs
        user_data = {
                'packets': [num_packets],
                'logs': [num_logs],
                'transaction_duration': [num_transaction_duration],
                'flows': [num_flows],
                'is_new_device': [is_new_device]
            }
            
            # Convert the dictionary into a Pandas DataFrame
        user_df = pd.DataFrame(user_data)
        print(user_df)
            
        # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_paths = [
            "C:/Users/Gaurav/Desktop/Fin_Sec_System/Fin_Sec_System/models/1.joblib",
            "C:/Users/Gaurav/Desktop/Fin_Sec_System/Fin_Sec_System/models/random_forest_model_0.joblib"
        ]
        
        # Randomly select one of the model paths
        selected_model_path = random.choice(model_paths)
        
        # Load the selected machine learning model
        model = load(selected_model_path)
        
        # Make a prediction using the loaded model
        intrusion_detected = model.predict(user_df)
        
        if intrusion_detected:
            random_data = generate_random_data()
            print(user_df)
            return render(request, 'result.html', {'intrusion_detected': True})
        else:
            return render(request, 'result.html', {'intrusion_detected': False})
        
        

        # Render the result.html template with prediction result
        return render(request, 'result.html')
