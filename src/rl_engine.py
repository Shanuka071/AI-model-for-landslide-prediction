from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class DisasterPredictor:
    def __init__(self):
        self.flood_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.landslide_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.flood_accuracy = 0.0
        self.landslide_accuracy = 0.0

    def train(self, df):
        # Features
        X = df[['Rainfall_mm', 'Rainfall_3day_avg', 'Rainfall_7day_avg']]
        
        # Targets
        y_flood = df['Flood_Risk']
        y_landslide = df['Landslide_Risk']
        
        # 1. Train Flood Model
        X_train, X_test, y_train, y_test = train_test_split(X, y_flood, test_size=0.2, random_state=42)
        self.flood_model.fit(X_train, y_train)
        self.flood_accuracy = accuracy_score(y_test, self.flood_model.predict(X_test))
        
        # 2. Train Landslide Model
        X_train, X_test, y_train, y_test = train_test_split(X, y_landslide, test_size=0.2, random_state=42)
        self.landslide_model.fit(X_train, y_train)
        self.landslide_accuracy = accuracy_score(y_test, self.landslide_model.predict(X_test))
        
        self.is_trained = True
        
        # ⚠️ IMPORTANT: Return TWO values, not one!
        return self.flood_accuracy, self.landslide_accuracy

    def predict(self, rainfall, rain_3day, rain_7day):
        if not self.is_trained:
            return "Model not trained", "Model not trained"
            
        features = [[rainfall, rain_3day, rain_7day]]
        
        flood_pred = self.flood_model.predict(features)[0]
        landslide_pred = self.landslide_model.predict(features)[0]
        
        flood_status = "RESTRICTED (High Risk)" if flood_pred == 1 else "NOT RESTRICTED (Safe)"
        landslide_status = "RESTRICTED (High Risk)" if landslide_pred == 1 else "NOT RESTRICTED (Safe)"
        
        return flood_status, landslide_status