# Dockerfile for Vite development server
FROM node:24-alpine

# Set environment variables
ENV NODE_ENV=development
ENV PORT=5173

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5173

# Start the Vite development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]