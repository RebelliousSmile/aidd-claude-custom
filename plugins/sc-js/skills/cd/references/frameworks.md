# JavaScript delivery strategies

Reuse `sc-js:sniff` classification and confirm it against project configuration.

| Signals | Local | Server artifact/runtime |
| --- | --- | --- |
| Vite or Vue SPA | existing dev script | configured static output, commonly `dist/` |
| Astro static | existing dev script | configured static output |
| Nuxt, SvelteKit, Astro SSR | framework dev script | adapter output and its documented Node/runtime entrypoint |
| Node service | existing start/dev script | built server or source runtime already chosen by the project |

Never assume an output directory from the framework name alone. Read its configured adapter and output. Unknown or custom adapters are a gap: explain it and make no deployment target.
