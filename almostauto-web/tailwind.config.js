import daisyui from "daisyui";

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/almostauto/web/components/**/*.jinja"],
  theme: {
    extend: {},
  },
  plugins: [daisyui]
};
