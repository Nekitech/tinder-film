import {StrictMode} from 'react'
import './index.css'
import {getFilms} from "@/shared/api/films.api.ts";
import ReactDOM from 'react-dom/client';
import {createRouter, RouterProvider} from "@tanstack/react-router";
import {routeTree} from "@/routeTree.gen.ts";
import FilmsProvider from "@/shared/providers/films.provider.tsx";
import {AuthProvider} from "@/shared/providers/auth.provider.tsx";
import {QueryClient, QueryClientProvider} from '@tanstack/react-query';

const router = createRouter({
	routeTree,
	defaultPreload: 'intent',
	scrollRestoration: true,

})

// const loginRootRoute = createRootRoute({
//     component: LoginForm,
// })

// const loginRouter = createRoute({
//     getParentRoute: () => <></>,
//     path: "/login",
//     component: function Login (){
//         return <LoginForm/>
//     }
// })


declare module '@tanstack/react-router' {
    interface Register {
        router: typeof router
    }
}
const queryClient = new QueryClient()

const rootElement = document.getElementById('root')!

if (!rootElement?.innerHTML) {
	const root = ReactDOM.createRoot(rootElement)
	root.render(
		<StrictMode>
			<QueryClientProvider client={queryClient}>
				<AuthProvider>
					<FilmsProvider initialFilms={getFilms()}>
						<RouterProvider router={router} />
					</FilmsProvider>
				</AuthProvider>
			</QueryClientProvider>
		</StrictMode>
	)
}