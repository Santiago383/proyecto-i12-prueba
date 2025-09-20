#clonar el repo
#en la carpeta postgres crear una carpeta vacía llamada data en el mismo nivel donde esta la carpeta init-scripts
#hacer docker compose up --build -d desde la carpeta del proyecto
#navegar a http://localhost:5000/ o http://localhost para ver si se conecta con flask/proxy



Credenciales DB:
    host: aws-1-us-east-2.pooler.supabase.com
    port: 6543
    database: postgres
    user: postgres.aibvvfplsvhmrkavxyth
    pool_mode: transaction
    pass: i12pass
