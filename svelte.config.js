import adapter from '@sveltejs/adapter-auto';

const config = {
	kit: {
		adapter: adapter()
	},
	vitePlugin: {
		configFile: 'vite.config.js'
	}
};

export default config;
