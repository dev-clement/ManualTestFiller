# Stage 1: Build the angular app
FROM node:25-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package files first (for caching pueposes)
COPY package.json package-lock.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the Angular source code
COPY . .

# Build angular in production mode
RUN npm run build --prod

# Stage 2 : Serve the app using nginx
FROM nginx:alpine

# Copy the compiled Angular app from stage 1
COPY --from=build /app/dist/ManualTestFiller /usr/share/nginx/html

# Remove the default NGINX config and add our own if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf # optional if custom config

# Expose port 80
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]


