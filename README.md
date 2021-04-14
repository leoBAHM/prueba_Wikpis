Regular tirando a sobresaliente

# prueba_Wikpis

Deben tener MySQL instalado y crear una base de datos llamada "api"

Pasos para ejecutar la aplicación.

1. Instalar las librerías especificadas en el archivo requirements.txt

2. ejecurar en una consola (cmd) lo siguiente:

  Para Windows:
  
  2.1. SET FLASK_APP=application.py
  
  2.2. SET FLASK_ENV=development
  
  2.3.- SET APP_SETTINGS_MODULE=config.config
  
  2.4.- flask db init
 
  2.5.- flask db migrate
  
  2.6.- flask bd upgrade

  2.7. flask run
  
  Para Ubuntu:
  
  2.1. export FLASK_APP=application.py
 
  2.2. export FLASK_ENV=development
  
  2.3. export APP_SETTINGS_MODULE=config.config
  
  2.4. flask db init
  
  2.5. flask db migrate
  
  2.6. flask bd upgrade

  2.7. flask run
