# Usa una imagen base oficial de Node.js
FROM node:18

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos package.json y package-lock.json
COPY package*.json ./

# Instala las dependencias del proyecto
RUN npm config set cache /app/.npm-cache --global
RUN npm install

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto de la aplicación
EXPOSE 3000

# Comando para correr la aplicación
CMD ["npm", "run", "dev"]
