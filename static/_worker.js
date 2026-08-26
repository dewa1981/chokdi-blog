// CF Pages Worker — override robots.txt (bypass Cloudflare Content Signals)
const ROBOTS = `# Chokdi Blog — robots.txt (SEO fix 26-Agu-2026)
# Izin selective AI crawler untuk GEO/AEO (GPTBot, PerplexityBot, Google-Extended)
# Blok crawler yang tidak diinginkan

Sitemap: https://chokdi.ano99.com/sitemap.xml

User-agent: *
Allow: /

# AI / GEO crawlers — DIIZINKAN (strategi visibilitas AI search)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: CCBot
Allow: /

User-agent: Applebot
Allow: /

# Crawler yang diblokir
User-agent: Bytespider
Disallow: /

User-agent: Amazonbot
Disallow: /

User-agent: meta-externalagent
Disallow: /
`;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/robots.txt") {
      return new Response(ROBOTS, {
        headers: { "Content-Type": "text/plain; charset=utf-8" },
      });
    }
    return env.ASSETS.fetch(request);
  },
};
