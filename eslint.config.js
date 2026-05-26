const lwcRecommended = require("@salesforce/eslint-config-lwc/recommended");
const auraPlugin = require("@salesforce/eslint-plugin-aura");

module.exports = [
  {
    ignores: [".sf/**", ".sfdx/**", "coverage/**", "docs/generated-docs/**", "node_modules/**"]
  },
  ...lwcRecommended,
  ...auraPlugin.configs.recommended
];
