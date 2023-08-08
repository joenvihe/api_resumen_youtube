En este repositorio estoy creando un api que internamente llama a un api de youtube para obtener las transcripciones de los videos, estas transcripciones estaran en español

Para esto tengo un droplet de digitalocean, el mas economico (5 dolares mensuales)

- En el droplet instale nginx (ya esta instalado), y cree un archivo de configuracion enrique.conf, contiene la configuracion de mi web:

```
nano /etc/nginx/sites-enabled/enrique.conf 
```
- La configuracion del archivo tiene la configuracion de mi web personal y de una aplicacion a facebook para uso del whatsapp y tambien se agregara el api:

```
server {
    listen 80;
    server_name enrique.vicenteh.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name enrique.vicenteh.com;

    ssl_certificate /etc/letsencrypt/live/enrique.vicenteh.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/enrique.vicenteh.com/privkey.pem;

    # Additional SSL configuration settings if needed
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';

    root /var/www/enrique;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
    # Location for the Facebook app
    location /facebook/ {
        proxy_pass http://127.0.0.1:5000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
