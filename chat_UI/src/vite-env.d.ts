/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_BASE?: string;
  }
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
  
  declare global {
    interface Window {
      __API_BASE__?: string; 
    }
  }
  export {};

