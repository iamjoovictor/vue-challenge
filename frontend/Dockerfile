FROM node:20-alpine

WORKDIR /app

# Install dependencies before copying source (better layer caching)
COPY package*.json ./
RUN npm install

# Copy remaining source files
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
