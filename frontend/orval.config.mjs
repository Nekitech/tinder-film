export default {
    tinder_films: {
        output: {
            mode: 'tags-split',
            target: 'src/shared/api/generated',
            client: 'react-query',
            override: {
                mutator: {
                    path: './src/shared/api/custom-instance.ts',
                    name: 'customInstance',
                },
            },
        },
        input: {
            target: 'http://127.0.0.1:8000/openapi.json',
        },
    },
};