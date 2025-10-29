/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            boxShadow: {
                '2x1l': '0 10px 25px -5px rgba(0, 0, 0, 0.3)',
            }
        },
    },
    plugins: [],
}



