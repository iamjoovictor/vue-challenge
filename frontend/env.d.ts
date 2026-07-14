/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly BACKEND_URL: string
  readonly WS_URL: string
  readonly WEBSERVER_URL: string
  readonly IS_PRODUCTION: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
