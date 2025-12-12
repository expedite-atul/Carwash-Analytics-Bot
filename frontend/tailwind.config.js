/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{html,js,svelte,ts}'],
    theme: {
        extend: {
            colors: {
                primary: '#6366f1', // Indigo-500
                secondary: '#a5b4fc',
                surface: '#ffffff',
                background: '#f3f4f6',
                sidebar: '#f8fafc',
                text: '#1e293b',
                muted: '#64748b',
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
