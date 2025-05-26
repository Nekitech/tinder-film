import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'
import react from 'eslint-plugin-react'

export default tseslint.config(
    {
        ignores: ['dist',
            'node_modules',
            'src/routeTree.gen.ts',
            'src/shared/components/ui/*.tsx',
            'src/shared/api/generated'
        ],
    },
    {
        extends: [js.configs.recommended, ...tseslint.configs.recommended],
        files: ['**/*.{ts,tsx}'],
        languageOptions: {
            ecmaVersion: 2020,
            globals: globals.browser,
        },
        plugins: {
            'react': react,
            'react-hooks': reactHooks,
            'react-refresh': reactRefresh,
        },
        rules: {
            ...reactHooks.configs.recommended.rules,
            '@typescript-eslint/no-explicit-any': 0,
            'react-refresh/only-export-components': [
                'warn',
                {allowConstantExport: true},
            ],
            'indent': ['error', 'tab'],
            'no-mixed-spaces-and-tabs': 'error',
            'no-tabs': 'off',

            'react/jsx-indent': ['error', 'tab'],
            'react/jsx-indent-props': ['error', 'tab'],
            'react/jsx-closing-bracket-location': ['error', 'line-aligned'],
            'react/jsx-tag-spacing': [
                'error',
                {
                    beforeSelfClosing: 'always',
                    afterOpening: 'never',
                    closingSlash: 'never',
                },
            ],
            'react/jsx-first-prop-new-line': ['error', 'multiline'],
            'react/jsx-max-props-per-line': ['error', {maximum: 1, when: 'multiline'}],
            'react/self-closing-comp': ['error', {
                component: true,
                html: true,
            }],
            'react/jsx-curly-spacing': ['error', {
                when: 'never',
                children: {when: 'always'},
            }],
            'react/jsx-equals-spacing': ['error', 'never'],
            'react/jsx-wrap-multilines': ['error', {
                declaration: 'parens-new-line',
                assignment: 'parens-new-line',
                return: 'parens-new-line',
                arrow: 'parens-new-line',
                condition: 'parens-new-line',
                logical: 'parens-new-line',
                prop: 'parens-new-line',
            }],
        },
    },
)
