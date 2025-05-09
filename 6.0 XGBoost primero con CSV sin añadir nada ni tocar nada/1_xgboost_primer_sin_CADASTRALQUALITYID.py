import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
import joblib

print("Modelo guardado correctamente.")

# 1. Cargar los datos
data = pd.read_csv(r"6.0 XGBoost primero con CSV sin añadir nada ni tocar nada\Madrid_Sale.csv")  # Cambia "datos.csv" por la ruta real

data = data.drop(columns=['ASSETID', 'PERIOD', 'UNITPRICE', 'CONSTRUCTIONYEAR', 'CADASTRALQUALITYID' ,'geometry'])


# 2. Preprocesamiento
# Rellenar valores nulos con 0
data.fillna(0, inplace=True)



# Convertir variables categóricas en dummies
data = pd.get_dummies(data, drop_first=True)

# 3. Definir variables predictoras y objetivo
X = data.drop(columns=["PRICE"])  # Todas menos PRICE
y = data["PRICE"]


# 4. Dividir en entrenamiento y validación (80%-20%)
X_sample, _, y_sample, _ = train_test_split(X, y, test_size=0.4, random_state=35)  # Quedarse con el 50% de los datos por sencillez
X_train, X_valid, y_train, y_valid = train_test_split(X_sample, y_sample, test_size=0.2, random_state=42)


"""
print(X_train.isna().sum())
print(y_train.isna().sum())


"""

# 5. Entrenar XGBoost con valores por defecto
model = xgb.XGBRegressor(objective="reg:squarederror", random_state=42)
model.fit(X_train, y_train)

# 6. Predicción y evaluación
y_pred = model.predict(X_valid)
mae = mean_absolute_error(y_valid, y_pred)
print(f"Error absoluto medio (MAE): {mae}")

error_porcentual = np.zeros(len(y_pred))

y_valid = y_valid.to_numpy()  

for i in range(1, len(y_pred)):

    dif = y_pred[i] / y_valid[i]
    if dif <= 1:
        error_porcentual[i] = (1 - dif) 
    else:
        error_porcentual[i] = (dif - 1)

mean_porcentual_error = np.mean(error_porcentual)

print(f"Error porcentual medio: {mean_porcentual_error}")


# 7. Guardar resultados en un archivo CSV

# Crear un DataFrame con los valores reales y predichos
df_resultados = pd.DataFrame({'y_valid': y_valid, 'y_pred': y_pred})

print(f"La media de precio de los pisos es de {y_pred.mean()}")

# Guardar en un archivo CSV
df_resultados.to_csv(r'6.0 XGBoost primero con CSV sin añadir nada ni tocar nada\Mresultados_xgboost_60per_NO_CATASQUAL.csv', index=False)

print("Archivo 'resultados_xgboost.csv' generado correctamente.")


# 8. Guardar el modelo en un archivo
# Guardar el modelo en un archivo
joblib.dump(model, r"6.0 XGBoost primero con CSV sin añadir nada ni tocar nada\Mmodelo_xgboost_60per_NO_CATASQUAL.pkl")

