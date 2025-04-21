# Step 1 - Build
FROM node:22 AS build

# Set the working directory
WORKDIR /app

# Copy package files for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the source code
COPY . .

# Build the application for production
RUN npm run build --prod

# Step 2 - Run
FROM nginx:alpine

# Copy the built application to the nginx directory
COPY --from=build /app/dist/front/browser /usr/share/nginx/html

# Copy the Nginx configuration template
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Set the internal port environment variable
ENV INTERNAL_PORT=80

# Expose the internal port
EXPOSE ${INTERNAL_PORT}

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]