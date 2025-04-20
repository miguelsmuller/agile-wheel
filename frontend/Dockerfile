# Etapa 1: Construção do aplicativo Angular
FROM node:22 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build --prod


# Etapa 2: Configuração do servidor Nginx
FROM nginx:alpine

# Copia os arquivos compilados do Angular
COPY --from=build /app/dist/front/browser /usr/share/nginx/html

# Copia o arquivo de configuração do Nginx
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Define uma variável de ambiente para a porta
ENV PORT=80

# Substitui a porta no arquivo de configuração do Nginx
RUN sh -c "envsubst '\$PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf"

# Expõe a porta configurada
EXPOSE ${PORT}

# Comando padrão para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]