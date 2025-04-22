// tailwind.config.js
module.exports = {
    content: [
      "./pages/**/*.{js,ts,jsx,tsx}",
      "./components/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          lightShades: '#faf8f7',
          lightAccent: '#eeaf48',
          mainBrand: '#75b0d9',
          darkAccent: '#2aafda',
          darkShades: '#363962',
        },
      },
    },
    plugins: [],
  };
  