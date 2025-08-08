# Этап сборки
#FROM node:16 AS build-stage

#WORKDIR /app

# Сначала копируем только package.json
#COPY package*.json ./
#COPY package*.json .
#COPY quasar.config.js .
# Устанавливаем зависимости
#RUN npm install

# Затем копируем все остальные файлы
#COPY . .

# Собираем приложение
#RUN npm run build

# Этап production
#FROM nginx:alpine

# Копируем собранное приложение
#COPY --from=build-stage /app/dist/spa /usr/share/nginx/html

# Копируем конфиг Nginx (временно скопируем файл в папку frontend)
#COPY frontend.conf /etc/nginx/conf.d/default.conf

#EXPOSE 80
#FROM node:16 AS build-stage

#WORKDIR /app

# 1. Сначала копируем только package.json
#COPY package.json .
#COPY package-lock.json* .

# 2. Устанавливаем ВСЕ зависимости (включая devDependencies)
#RUN npm install --include=dev

# 3. Копируем остальные файлы проекта
#COPY . .

# 4. Собираем приложение
#RUN npm run build

#FROM nginx:alpine

#COPY --from=build-stage /app/dist/spa /usr/share/nginx/html
#COPY ../nginx/frontend.conf /etc/nginx/conf.d/default.conf

#EXPOSE 80
FROM node:16 AS build-stage

WORKDIR /app

# 1. Копируем package.json
COPY package.json .
COPY package-lock.json .

# 2. Устанавливаем зависимости
RUN npm install --include=dev

# 3. Копируем остальные файлы
COPY . .

# 4. Собираем приложение
RUN npm run build

FROM nginx:alpine

# 5. Копируем собранное приложение
COPY --from=build-stage /app/dist/spa /usr/share/nginx/html

# 6. Копируем конфиг Nginx (теперь он в той же папке)
COPY frontend.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
