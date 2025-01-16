import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
    base: mode === "development"
        ? "http://localhost:5173/"
        : "/static/api/spa/",
    
    build: {
        emptyOutDir: true,
        outDir: "../api/static/api/spa",  // Output folder for Django to serve
        assetsDir: "assets",              // Place assets in a subfolder
    },

    server: {
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',  // Proxy API requests to Django
                changeOrigin: true,
                secure: false,
            },
            '/static': {
                target: 'http://127.0.0.1:8000',  // Proxy static files during development
                changeOrigin: true,
            }
        },
        port: 5173,
        strictPort: true,  // Ensures Vite uses this port or fails
    },

    plugins: [vue()],

    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),  // Allow imports with '@' as alias for src
        },
    },

}));
