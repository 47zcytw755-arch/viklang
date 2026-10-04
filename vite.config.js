import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

function openRouterDevProxy(apiKey) {
  return {
    name: 'openrouter-dev-proxy',
    configureServer(server) {
      server.middlewares.use(async (req, res, next) => {
        if (!req.url?.startsWith('/openrouter/')) {
          next();
          return;
        }

        if (!apiKey) {
          res.statusCode = 500;
          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify({ error: 'VITE_OPENROUTER_API_KEY is not configured.' }));
          return;
        }

        try {
          const chunks = [];

          for await (const chunk of req) {
            chunks.push(chunk);
          }

          const targetPath = req.url.replace(/^\/openrouter/, '');
          const response = await fetch(`https://openrouter.ai${targetPath}`, {
            method: req.method,
            headers: {
              'Content-Type': req.headers['content-type'] || 'application/json',
              'Authorization': `Bearer ${apiKey}`,
              'HTTP-Referer': 'https://verba.app',
              'X-Title': 'Verba ASL'
            },
            body: chunks.length ? Buffer.concat(chunks) : undefined
          });

          res.statusCode = response.status;
          res.setHeader('Content-Type', response.headers.get('content-type') || 'application/json');
          res.end(Buffer.from(await response.arrayBuffer()));
        } catch (error) {
          server.config.logger.error(error);
          res.statusCode = 502;
          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify({ error: 'OpenRouter request failed.' }));
        }
      });
    }
  };
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [react(), openRouterDevProxy(env.VITE_OPENROUTER_API_KEY)]
  };
});
