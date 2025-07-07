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
      // Enforces Prettier formatting rules
      "prettier/prettier": "error",
      // Requires Angular directive selectors to be attributes with the "app" prefix in camelCase
      "@angular-eslint/directive-selector": [
        "error",
        {
          type: "attribute",
          prefix: "app",
          style: "camelCase",
        },
      ],
      // Requires Angular component selectors to be elements with the "app" prefix in kebab-case
      "@angular-eslint/component-selector": [
        "error",
        {
          type: "element",
          prefix: "app",
          style: "kebab-case",
        },
      ],
      // Warns to use readonly for properties that are never reassigned
      "@typescript-eslint/prefer-readonly": "warn",
      // Ensures await is only used on thenable objects (promises)
      "@typescript-eslint/await-thenable": "error",
      // Warns against unnecessary type assertions (using `as X` with no type change)
      "@typescript-eslint/no-unnecessary-type-assertion": "warn",
      // Warns about commented-out code that should be cleaned up
      "sonarjs/no-commented-code": "warn",
      // Blocks imports that cannot be resolved
      "import/no-unresolved": "error",
      // Verifies that imported names actually exist in their modules
      "import/named": "error",
      // Forbids dependencies not declared in package.json
      "import/no-extraneous-dependencies": "error",
      // Includes SonarJS recommended rules for cognitive complexity and code duplication
      ...sonarjs.configs.recommended.rules,
      // Controls import ordering and grouping
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
  },

  {
    files: ["**/*.spec.ts"],
    rules: {
      // Allow 'any' in test files to simplify mocks and stubs
      "@typescript-eslint/no-explicit-any": "off",
    },
  }
);
