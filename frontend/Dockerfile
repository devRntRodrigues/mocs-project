# Use Node.js 18 Alpine image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies (including dev dependencies for development)
RUN npm ci

# Copy project files
COPY . .

# Expose port
EXPOSE 3000

# Set environment variable for API URL
ENV NEXT_PUBLIC_API_URL=http://backend:8000

# Run the application in development mode
CMD ["npm", "run", "dev"]


