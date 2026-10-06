
### Starten
```bash
docker run -d -p 80:80 -p 5001:5001 \ 
-e CADDY_HOST=localhost \ 
-e CADDY_PORT=80 
-v "$(pwd)/output:/srv/www/static" 
-v "$(pwd)/logs:/var/log/app" 
--name htmlhoster 
<docker_image_name>
```

### Webseite definieren
http://localhost:5001

### Webseite aufrufen
http://localhost:80