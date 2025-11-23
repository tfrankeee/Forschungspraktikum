FROM node:20-alpine

# Arbeitsverzeichnis im Container
WORKDIR /app

# Nur package-Dateien kopieren und installieren (für Cache)
COPY package*.json ./
RUN npm install

# Restlichen Code kopieren
COPY . .

# Vue CLI verwendet standardmäßig Port 8080
EXPOSE 8080

# Dev-Server starten, von außen erreichbar
CMD ["npm", "run", "serve", "--", "--host", "0.0.0.0", "--port", "8080"]
