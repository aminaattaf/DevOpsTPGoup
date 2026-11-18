#le serveur Nginx
FROM nginx:latest

# on copie le fichier index.html dans le dossier du serveur web
COPY index.html /usr/share/nginx/html/index.html


# les commande qu'on a utilliser :
# docker build -t aminachakira/devopstp:latest .
# docker login
# docker push aminachakira/devopstp:latest