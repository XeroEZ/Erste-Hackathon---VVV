FROM node:20

WORKDIR /app

# Copy package.json and package-lock.json first
COPY package*.json ./

# Install Expo CLI globally + project dependencies
RUN npm install @expo/ngrok@^4.1.0 && npm install

# Copy the rest of your project files
COPY . .

# Expose Expo dev ports
EXPOSE 19000 19001 19002 19006

# Start Expo in web mode for browser access
CMD ["npx", "expo", "start", "--tunnel", "--non-interactive", "--host", "lan"]


