import csv

def load_data(filepath='plurpgh.csv'):
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        return []

def calculate_scores(data, user_zip, user_budget, user_types, user_prefs):
    price_rank = {'$': 1, '$$': 2, '$$$': 3}
    user_rank = price_rank.get(user_budget, 1)

    scored_results = []

    for row in data:
        score = 0

        # 1. Preferences (+50 points each - HIGHEST PRIORITY)
        for pref in user_prefs:
            val = row.get(pref, '').strip()
            if val and val != '0':
                score += 50

        # 2. Type Match (+30 points - SECOND PRIORITY)
        if row.get('type', '').strip() in user_types:
            score += 30

        # 3. Zip Code Match (+20 points - THIRD PRIORITY)
        if row.get('Zip Code', '').strip() == user_zip:
            score += 20

        # 4. Budget Weighting (LOWER PRIORITY)
        v_price = row.get('price', '').strip()

        if v_price in price_rank:
            v_rank = price_rank[v_price]
            diff = user_rank - v_rank

            if diff < 0:
                # Venue is more expensive than budget -> Huge Penalty
                score -= 1000
            else:
                # 15 pts for exact match, -5 for every step cheaper
                weight_score = 15 - (diff * 5)
                score += max(0, weight_score)

        # Store result if it's not totally excluded
        if score > -100:
            row['match_score'] = score
            scored_results.append(row)

    # Sort by score descending (highest first)
    scored_results.sort(key=lambda x: x['match_score'], reverse=True)

    return scored_results[:3]

# Test the scoring function
data = load_data()
if data:
    results = calculate_scores(data, '15201', '$', ['Bar / Pub'], ['LGBT +'])
    print('Test results: ' + str(len(results)) + ' venues found')
    for i, venue in enumerate(results, 1):
        title = venue.get('title', 'Unknown')
        score = venue.get('match_score', 0)
        print(str(i) + '. ' + title + ' - Score: ' + str(score))
else:
    print('No data loaded')