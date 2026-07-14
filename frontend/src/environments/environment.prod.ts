export const environment = {
  production: import.meta.env.IS_PRODUCTION === 'true',
  serverIp: import.meta.env.BACKEND_URL,
  webserver: import.meta.env.WEBSERVER_URL,
  ws: import.meta.env.WS_URL,
};