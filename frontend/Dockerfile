# ******************
# Step 1 - Base
# ******************
FROM node:22 AS base

# Set the working directory
WORKDIR /app

# Copy package files for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the source code
COPY . .

# ******************
# Step 2 - Development
# ******************
FROM base AS dev

# Set the internal port environment variable
ENV NG_CLI_ANALYTICS=false

# Set the default command for development
CMD ["npm run start -- --port=${INTERNAL_PORT} --host=0.0.0.0"]

# ******************
# Step 3 - Build
# ******************
FROM base AS build

# Build the application for production
RUN npm run build --prod

# ******************
# Step 4 - Run
# ******************
FROM nginx:alpine AS prod

# Copy the built application to the nginx directory
COPY --from=build /app/dist/front/browser /usr/share/nginx/html

# Copy the Nginx configuration template
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Set the internal port environment variable
ENV INTERNAL_PORT=80

# Expose the internal port
EXPOSE ${INTERNAL_PORT}

# Replace environment variables in the Nginx configuration (if needed)
RUN envsubst '${INTERNAL_PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Use the default Nginx command to start the server
CMD ["nginx", "-g", "daemon off;"]
