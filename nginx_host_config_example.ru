server {
    listen 443 ssl;
    server_name {yourdomain.ru} www.{yourdomain.ru};
    #ssl_certificate /etc/letsencrypt/live/www.{yourdomain.ru}/fullchain.pem; # managed by Certbot
    #ssl_certificate_key /etc/letsencrypt/live/www.{yourdomain.ru}/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    ssl_certificate /etc/ssl/certs/{yourdomain.ru}.pem; # Cloudflare SSL certificate
    ssl_certificate_key /etc/ssl/private/{yourdomain.ru}.key; # Cloudflare SSL certificate

    location / {
        proxy_pass http://127.0.0.1:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }


}
