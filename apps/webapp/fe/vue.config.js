const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        timeout: 6000,
        secure: false,
        changeOrigin: true,
      },
    },
  },
});
