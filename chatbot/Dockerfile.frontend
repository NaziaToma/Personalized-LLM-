FROM node:22.11

COPY ./frontend /frontend
RUN rm -rf /frontend/node_modules

WORKDIR /frontend
RUN npm ci

CMD ["npm", "run", "dev"]
