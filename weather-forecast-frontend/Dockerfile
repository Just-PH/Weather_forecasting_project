# Utiliser l'image officielle Node.js version 16
FROM node:16

# Créer et définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier package.json et package-lock.json pour installer les dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste des fichiers de l'application
COPY . .

# Construire l'application pour le déploiement
RUN npm run build

# Spécifier la commande de lancement
CMD ["npm", "start"]

# Exposer le port utilisé par l'application
EXPOSE 3000
