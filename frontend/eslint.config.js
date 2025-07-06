// @ts-check
const eslint = require("@eslint/js");
const tseslint = require("typescript-eslint");
const angular = require("angular-eslint");
const eslintConfigPrettier = require("eslint-config-prettier/flat");
const prettierPlugin = require("eslint-plugin-prettier");
const sonarjs = require("eslint-plugin-sonarjs");
const importPlugin = require("eslint-plugin-import");


module.exports = tseslint.config(
  {
    files: ["**/*.ts"],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        project: ["./tsconfig.json"],
        tsconfigRootDir: __dirname,
      },
    },
    extends: [
      eslint.configs.recommended,
      ...tseslint.configs.recommended,
      ...tseslint.configs.stylistic,
      ...angular.configs.tsRecommended,
      eslintConfigPrettier,
    ],
    plugins: {
      prettier: prettierPlugin,
      sonarjs: sonarjs,
      import: importPlugin,
    },
    processor: angular.processInlineTemplates,
    rules: {
      "prettier/prettier": "error",
      "@angular-eslint/directive-selector": [
        "error",
        {
          type: "attribute",
          prefix: "app",
          style: "camelCase",
        },
      ],
      "@angular-eslint/component-selector": [
        "error",
        {
          type: "element",
          prefix: "app",
          style: "kebab-case",
        },
      ],
      // Força uso de `readonly` em membros não reassinados
      "@typescript-eslint/prefer-readonly": "warn",
      // Garante que await só seja usado em promises
      "@typescript-eslint/await-thenable": "error",
      // Impede type assertions desnecessárias: `as X` quando não muda o tipo
      "@typescript-eslint/no-unnecessary-type-assertion": "warn",
      // Reforça comentários relevantes (se quiser manter isso)
      "sonarjs/no-commented-code": "warn",
      ...sonarjs.configs.recommended.rules,

      "import/order": [
        "error",
        {
          groups: [
            "builtin",
            "external",
            "internal",
            ["parent", "sibling", "index"]
          ],
          pathGroups: [
            {
              pattern: "{@angular{,/**},@angular/material{,/**}}",
              group: "external",
              position: "before"
            },
            {
              pattern: "rxjs{,/**}",
              group: "external",
              position: "after"
            }
          ],
          pathGroupsExcludedImportTypes: ["builtin"],
          alphabetize: {
            order: "asc",
            caseInsensitive: true
          },
          "newlines-between": "always"
        }
      ]

    },
    settings: {
      'import/resolver': {
        typescript: {
          project: "./tsconfig.json",
        },
      },
    }
  },

  {
    files: ["**/*.html"],
    extends: [
      ...angular.configs.templateRecommended,
      ...angular.configs.templateAccessibility,
    ],
    rules: {},
  }
);
