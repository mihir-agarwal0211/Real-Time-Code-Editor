# Use a lightweight Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json first (ensures proper caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy frontend files AFTER installing dependencies
COPY . .

# Build the project
RUN npm run build

# Expose frontend port
EXPOSE 5173

# Serve frontend in production mode, with logging
CMD ["npx", "serve", "-s", "-l", "5173", "dist"]
