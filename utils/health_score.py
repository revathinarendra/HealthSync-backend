def calculate_health_score(body_params):
    # Initialize score components
    score_components = {
        'bmi': 0,
        'body_fat': 0,
        'muscle': 0,
        'visceral_fat': 0,
        'sleep': 0,
        'stress': 0,
        'body_age': 0,
        'hydration': 0
    }
    
    try:
        height = float(body_params['height']) if isinstance(body_params['height'], str) else body_params['height']
        weight = body_params['weight']
        bmi = body_params['BMI']
        
        # BMI Score (20% weight)
        if bmi < 18.5:
            score_components['bmi'] = 60 * 0.20
        elif 18.5 <= bmi < 25:
            score_components['bmi'] = 100 * 0.20
        elif 25 <= bmi < 30:
            score_components['bmi'] = 70 * 0.20
        else:
            score_components['bmi'] = 40 * 0.20
        
        # Body Fat Score (20% weight)
        body_fat = body_params['body_fat']
        if body_fat < 10:
            score_components['body_fat'] = 80 * 0.20
        elif 10 <= body_fat < 15:
            score_components['body_fat'] = 100 * 0.20
        elif 15 <= body_fat < 20:
            score_components['body_fat'] = 90 * 0.20
        elif 20 <= body_fat < 25:
            score_components['body_fat'] = 80 * 0.20
        elif 25 <= body_fat < 30:
            score_components['body_fat'] = 60 * 0.20
        else:
            score_components['body_fat'] = 40 * 0.20
        
        # Muscle Mass Score (15% weight)
        muscle = body_params['muscle']
        muscle_percent = (muscle / weight) * 100
        if muscle_percent > 40:
            score_components['muscle'] = 100 * 0.15
        elif 35 < muscle_percent <= 40:
            score_components['muscle'] = 85 * 0.15
        elif 30 < muscle_percent <= 35:
            score_components['muscle'] = 70 * 0.15
        elif 25 < muscle_percent <= 30:
            score_components['muscle'] = 60 * 0.15
        else:
            score_components['muscle'] = 40 * 0.15
        
        # Visceral Fat Score (10% weight)
        visceral_fat = int(body_params['viseral_fats'])
        if visceral_fat <= 5:
            score_components['visceral_fat'] = 100 * 0.10
        elif 6 <= visceral_fat <= 9:
            score_components['visceral_fat'] = 70 * 0.10
        elif 10 <= visceral_fat <= 12:
            score_components['visceral_fat'] = 50 * 0.10
        else:
            score_components['visceral_fat'] = 30 * 0.10
        
        # Sleep Score (15% weight)
        if isinstance(body_params['sleep_time'], str):
            sleep_hours = float(body_params['sleep_time'].split(':')[0])
        else:
            sleep_hours = body_params['sleep_time']
        
        sleep_quality = body_params['sleep_quality'].upper()
        
        if sleep_hours >= 7.5:
            sleep_duration_score = 100
        elif 7 <= sleep_hours < 7.5:
            sleep_duration_score = 90
        elif 6 <= sleep_hours < 7:
            sleep_duration_score = 70
        elif 5 <= sleep_hours < 6:
            sleep_duration_score = 50
        else:
            sleep_duration_score = 30
        
        if sleep_quality == 'A':
            sleep_quality_score = 100
        elif sleep_quality == 'B':
            sleep_quality_score = 80
        elif sleep_quality == 'C':
            sleep_quality_score = 60
        else:  # 'D'
            sleep_quality_score = 40
        
        score_components['sleep'] = ((sleep_duration_score * 0.5) + (sleep_quality_score * 0.5)) * 0.15
        
        # Stress Level Score (10% weight)
        stress = body_params['stress_level']
        if stress <= 3:
            score_components['stress'] = 100 * 0.10
        elif 3 < stress <= 5:
            score_components['stress'] = 80 * 0.10
        elif 5 < stress <= 7:
            score_components['stress'] = 60 * 0.10
        else:
            score_components['stress'] = 40 * 0.10
        
        # Body Age (5% weight)
        body_age = body_params['body_age']
        if body_age <= 30:
            score_components['body_age'] = 100 * 0.05
        elif 30 < body_age <= 40:
            score_components['body_age'] = 80 * 0.05
        elif 40 < body_age <= 50:
            score_components['body_age'] = 60 * 0.05
        else:
            score_components['body_age'] = 40 * 0.05
        
        # Hydration (5% weight)
        waste_water = body_params['waste_water'].upper()
        if waste_water in ['A', '1']:
            score_components['hydration'] = 100 * 0.05
        elif waste_water in ['B', '2']:
            score_components['hydration'] = 80 * 0.05
        elif waste_water in ['C', '3']:
            score_components['hydration'] = 60 * 0.05
        else:
            score_components['hydration'] = 40 * 0.05
        
        # Calculate total score
        total_score = sum(score_components.values())
        
        # Classify the score
        if total_score >= 85:
            status = "Above Average"
        elif 70 <= total_score < 85:
            status = "Good"
        elif 50 <= total_score < 70:
            status = "Average"
        else:
            status = "Poor"
        
        return {
            'score': round(total_score, 2),
            'status': status,
            'components': score_components  # Optional: include component breakdown
        }
    
    except Exception as e:
        return {
            'error': str(e),
            'score': 0,
            'status': 'Error'
        }