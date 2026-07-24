export const environment = {
  production: import.meta.env.IS_PRODUCTION === 'true',
  serverIp: import.meta.env.BACKEND_URL || "http://localhost:8000/",
  webserver: import.meta.env.WEBSERVER_URL || "http://localhost:4200/",
  ws: import.meta.env.WS_URL || "ws://localhost:8000/",
};